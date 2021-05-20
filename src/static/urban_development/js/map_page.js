var map;
var view;
var classifiedAsLayer;
var classifiedByLayer;

require(["esri/Map", "esri/views/MapView", "esri/widgets/LayerList", "esri/widgets/Legend", "esri/layers/TileLayer",
        "esri/layers/FeatureLayer", "esri/Graphic", "esri/geometry/Extent", "esri/geometry/Polygon", "esri/widgets/Editor"],
    function (Map, MapView, LayerList, Legend, TileLayer, FeatureLayer, Graphic, Extent, Polygon, Editor) {
        var layer = new TileLayer({
            url: "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_2020/MapServer"
        });
        map = new Map("map");
        map.add(layer);

        view = new MapView({
            container: "map",
            map: map,
        });

        // const editor = new Editor({
        //     layerInfos: [{
        //         enabled: true,
        //         addEnabled: false,
        //         updateEnabled: true,
        //         deleteEnabled: true,
        //     }],
        //     view: view,
        // });
        // view.ui.add(editor, "top-right")

        const legend = new Legend({ view: view, });
        const layerList = new LayerList({
            view: view,
            listItemCreatedFunction: function (event) {
                var item = event.item;
                
                // Don't show the legend twice
                if (item.layer.geometryType === "polygon") {
                    item.title = "Classification legend";
                    item.panel = legend;
                }
            }
        });
        view.ui.add(layerList, "bottom-right");

        var coordsWidget = document.createElement("div");
        coordsWidget.className = "esri-widget esri-component";
        coordsWidget.style.padding = "7px 15px 5px";
        view.ui.add(coordsWidget, "bottom-left");

        function showCoordinates(event) {
            var coords = "Longitude: " + event.x + " | Latitude: " + event.y +
                " | Scale 1:" + Math.round(view.scale * 1) / 1 +
                " | Zoom " + view.zoom +
                " | EPSG: 28992";
            coordsWidget.innerHTML = coords;
        }

        view.watch(["stationary"], function () {
            showCoordinates(view.center);
        });

        view.on(["pointer-down"], function (event) {
            showCoordinates(view.toMap({ x: event.x, y: event.y, }));
        });

        $(document).ready(function () {
            $("#year").change(function (event) {
                map.removeAll();

                overlay = $("#overlay option:selected").val().trim();
                var year = $("#year option:selected").val().trim();
                
                var yearLayer = new TileLayer({
                    url: "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + year + "/MapServer",
                });
                
                map.add(yearLayer);
                addCurrentOverlay(overlay, year)
            });
            $("#overlay").change(async function (event) {
                map.remove(classifiedAsLayer);
                map.remove(classifiedByLayer);

                var overlay = $("#overlay option:selected").val().trim();
                var year = $("#year option:selected").val().trim();
                
                addCurrentOverlay(overlay, year)
            });
        });

        async function addCurrentOverlay(overlay, year) {
            if (overlay === "Classified as") {
                setupClassifiedAsLayer(FeatureLayer);
                map.add(classifiedAsLayer);                
                addToClassifiedAsLayer(year);
            } else if (overlay === "Classified by") {
                setupClassifiedByLayer(FeatureLayer);
                map.add(classifiedByLayer);                
                addToClassifiedByLayer(year);
            }
        }

        async function addToClassifiedAsLayer() {
            let abortController = new AbortController();
            
            $("#year").change(function () {
                abortController.abort();
            });
            
            $("#overlay").change(function () {
                abortController.abort();
            });
            
            var year = $("#year option:selected").val().trim();
            const parameters = { "year": year };
            const response = await fetch("/urban_development/get_classified_as/" + JSON.stringify(parameters), { signal: abortController.signal, });
            
            try {
                var json = await response.json();
                
                edits = {
                    addFeatures: [],
                    updateFeatures: [],
                };
                
                for (let i = 0; i < json.length; i++) {
                    var graphic = new Graphic({
                        geometry: Polygon.fromExtent(new Extent(
                            json[i].xmin, // xmin
                            json[i].ymin, // ymin
                            json[i].xmax, // xmax
                            json[i].ymax, // ymax
                            { wkid: 28992 })), // spatial reference
                    });
                    
                    graphic.setAttribute("Longitude", json[i].x_coordinate);
                    graphic.setAttribute("Latitude", json[i].y_coordinate);
                    graphic.setAttribute("Public space", json[i].public_space);
                    graphic.setAttribute("Not public space", json[i].not_public_space);
                    
                    edits.addFeatures.push(graphic);
                }
                
                classifiedAsLayer.applyEdits(edits);
            } catch (exception) {
                console.error(exception);
                console.error(exception.lineNumber);
                
                alert("No classified tiles for the selected year.")
            }
        }

        async function addToClassifiedByLayer() {
            let abortController = new AbortController();
            
            $("#year").change(function () {
                abortController.abort();
            });
            
            $("#overlay").change(function () {
                abortController.abort();
            });
            
            var year = $("#year option:selected").val().trim();
            const parameters = { "year": year };
            const response = await fetch("/urban_development/get_classified_by/" + JSON.stringify(parameters), { signal: abortController.signal, });
            
            try {
                var json = await response.json();
                
                edits = {
                    addFeatures: [],
                    updateFeatures: [],
                };
                
                for (let i = 0; i < json.length; i++) {
                    var graphic = new Graphic({
                        geometry: Polygon.fromExtent(new Extent(
                            json[i].xmin, // xmin
                            json[i].ymin, // ymin
                            json[i].xmax, // xmax
                            json[i].ymax, // ymax
                            { wkid: 28992 })), // spatial reference
                        });
        
                    graphic.setAttribute("Longitude", json[i].x_coordinate);
                    graphic.setAttribute("Latitude", json[i].y_coordinate);
                    graphic.setAttribute("By user", json[i].user);
                    graphic.setAttribute("By classifier", json[i].classifier);
                    graphic.setAttribute("By training data", json[i].training_data);
                    
                    edits.addFeatures.push(graphic);
                }
                
                classifiedByLayer.applyEdits(edits);
            } catch (exception) {
                console.error(exception);
                console.error(exception.lineNumber);
                
                alert("No classified tiles for the selected year.")
            }
        }
    }
);

function setupClassifiedAsLayer(FeatureLayer) {
    var template = {
        title: "Tile | EPSG: 4326",
        content: "<div>Coordinates: {Longitude}, {Latitude}<br>\
                        <br>\
                        Classified as:<br>\
                        public space: {Public space}<br>\
                        not public space: {Not public space}</div>"
    };

    var renderer = {
        type: "unique-value",
        field: "Public space",
        field2: "Not public space",
        fieldDelimiter: ":",
        defaultSymbol: { type: "simple-fill" },
        uniqueValueInfos: [{
            value: "true:false",
            label: "public space",
            symbol: {
                type: "simple-fill",
                color: [0, 255, 0, 0.5],
                style: "solid",
                outline: {
                    style: "none"
                }
            }
        }, {
            value: "false:true",
            label: "not public space",
            symbol: {
                type: "simple-fill",
                color: [255, 0, 0, 0.5],
                style: "solid",
                outline: {
                    style: "none"
                }
            }
        }, {
            value: "true:true",
            label: "both",
            symbol: {
                type: "simple-fill",
                color: [0, 0, 255, 0.5],
                style: "solid",
                outline: {
                    style: "none"
                }
            }
        },],
        outFields: ["*"],
    }
    
    classifiedAsLayer = new FeatureLayer({
        objectIdField: "objectid",
        fields: [{
            name: "objectid",
            type: "oid"
        }, {
            name: "Longitude",
            type: "double"
        }, {
            name: "Latitude",
            type: "double"
        }, {
            name: "Public space",
            type: "string"
        }, {
            name: "Not public space",
            type: "string"
        },],
        source: [],
        popupTemplate: template,
        renderer: renderer,
        geometryType: "polygon",
        spatialReference: { wkid: 28992 },
        outFields: ["objectid"],
        labelsVisible: "true",
        title: "Classified as",
    });
}

function setupClassifiedByLayer(FeatureLayer) {
    var template = {
        title: "Tile | EPSG: 4326",
        content: "<div>Coordinates: {Longitude}, {Latitude}<br>\
                        <br>\
                        Classified by:<br>\
                        user: {By user}<br>\
                        classifier: {By classifier}<br>\
                        training data: {By training data}</div>"
    };

    var renderer = {
        type: "unique-value",
        field: "By user",
        field2: "By classifier",
        field3: "By training data",
        fieldDelimiter: ":",
        defaultSymbol: { type: "simple-fill" },
        uniqueValueInfos: [{
            value: "true:false:false",
            label: "user",
            symbol: {
                type: "simple-fill",
                color: [255, 0, 0, 0.5],
                style: "solid",
                outline: {
                    style: "none"
                }
            }
        }, {
            value: "false:true:false",
            label: "classifier",
            symbol: {
                type: "simple-fill",
                color: [0, 255, 0, 0.5],
                style: "solid",
                outline: {
                    style: "none"
                }
            }
        }, {
            value: "false:false:true",
            label: "training data",
            symbol: {
                type: "simple-fill",
                color: [0, 0, 255, 0.5],
                style: "solid",
                outline: {
                    style: "none"
                }
            }
        }, {
            value: "true:true:false",
            label: "user and classifier",
            symbol: {
                type: "simple-fill",
                color: [255, 255, 0, 0.5],
                style: "solid",
                outline: {
                    style: "none"
                }
            }
        }, {
            value: "true:false:true",
            label: "user and training data",
            symbol: {
                type: "simple-fill",
                color: [255, 0, 255, 0.5],
                style: "solid",
                outline: {
                    style: "none"
                }
            }
        }, {
            value: "false:true:true",
            label: "classifier and training data",
            symbol: {
                type: "simple-fill",
                color: [0, 255, 255, 0.5],
                style: "solid",
                outline: {
                    style: "none"
                }
            }
        }, {
            value: "true:true:true",
            label: "user, classifier and training data",
            symbol: {
                type: "simple-fill",
                color: [255, 255, 255, 0.5],
                style: "solid",
                outline: {
                    style: "none"
                }
            }
        },],
        outFields: ["*"],
    }
    
    classifiedByLayer = new FeatureLayer({
        objectIdField: "objectid",
        fields: [{
            name: "objectid",
            type: "oid"
        }, {
            name: "Longitude",
            type: "double"
        }, {
            name: "Latitude",
            type: "double"
        }, {
            name: "By user",
            type: "string"
        }, {
            name: "By classifier",
            type: "string"
        }, {
            name: "By training data",
            type: "string"
        },],
        source: [],
        popupTemplate: template,
        renderer: renderer,
        geometryType: "polygon",
        spatialReference: { wkid: 28992 },
        outFields: ["objectid"],
        labelsVisible: "true",
        title: "Classified by",
    });
}
