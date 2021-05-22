var map;
var mapView;
var classifiedAsLayer;
var classifiedByLayer;

require(["esri/Map", "esri/views/MapView", "esri/widgets/LayerList", "esri/widgets/Legend", "esri/layers/TileLayer", "esri/Graphic", 
        "esri/layers/FeatureLayer", "esri/geometry/Extent", "esri/geometry/Polygon", "esri/widgets/Editor", "dojo/domReady!"],
    function (Map, MapView, LayerList, Legend, TileLayer, Graphic, FeatureLayer, Extent, Polygon, Editor) {
        function setupMapView() {
            mapView = new MapView({
                container: "map",
                map: map,
                zoom: 3,
                extent: new Extent(13328.546, 306816.384, 278302.013, 619342.658, { wkid: 28992 })
            });

            // const editor = new Editor({
            //     layerInfos: [{
            //         enabled: true,
            //         addEnabled: false,
            //         updateEnabled: true,
            //         deleteEnabled: true,
            //     }],
            //     view: mapView,
            // });
    
            const legend = new Legend({ view: mapView, });
            const layerList = new LayerList({
                view: mapView,
                listItemCreatedFunction: function (event) {
                    var item = event.item;
                    
                    // Don't show the legend twice
                    if (item.layer.geometryType === "polygon") {
                        item.title = "Classification legend";
                        item.panel = legend;
                    }
                },
            });

            var coordinatesWidget = document.createElement("div");
            coordinatesWidget.className = "esri-widget esri-component";
            coordinatesWidget.style.padding = "7px 15px 5px";
            
            // mapView.ui.add(editor, "top-right");
            mapView.ui.add(coordinatesWidget, "bottom-left");
            mapView.ui.add(layerList, "bottom-right");
            
            function showCoordinates(event) {
                var coords = "Longitude: " + event.x + " | Latitude: " + event.y +
                    " | Scale 1:" + Math.round(mapView.scale * 1) / 1 +
                    " | Zoom " + mapView.zoom +
                    " | EPSG: 28992";
                coordinatesWidget.innerHTML = coords;
            };

            mapView.watch(["stationary"], function () {
                showCoordinates(mapView.center);
            });

            mapView.on(["pointer-down"], function (event) {
                showCoordinates(mapView.toMap({ x: event.x, y: event.y, }));
            });
        };

        function addMap() {
            map.removeAll();

            var overlay = $("#overlay option:selected").val().trim();
            var year = $("#year option:selected").val().trim();
                
            var yearLayer = new TileLayer({
                url: "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + year + "/MapServer",
            });
                
            map.add(yearLayer);
            addCurrentOverlay(overlay, year);
        };

        function addCurrentOverlay(overlay, year) {
            if (overlay === "Classified as") {
                setupClassifiedAsLayer(FeatureLayer);
                map.add(classifiedAsLayer);                
                addToClassifiedAsLayer(year);
            } else if (overlay === "Classified by") {
                setupClassifiedByLayer(FeatureLayer);
                map.add(classifiedByLayer);                
                addToClassifiedByLayer(year);
            }
        };

        async function addToClassifiedAsLayer() {
            let abortController = new AbortController();
            
            $("#map-view-button").click(function () {
                abortController.abort();
            });
            
            $("#data-view-button").click(function () {
                abortController.abort();
            });
            
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
                
                alert("Error.");
            }
        };

        async function addToClassifiedByLayer() {
            let abortController = new AbortController();
            
            $("#map-view-button").click(function () {
                abortController.abort();
            });
            
            $("#data-view-button").click(function () {
                abortController.abort();
            });
            
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
                
                alert("Error.");
            }
        };

        async function setupDataView() {
            $("#data").remove();
            var dataDiv = $("<div id='data'></div>");
            $(document.body).append(dataDiv);

            let abortController = new AbortController();
            
            $("#map-view-button").click(function () {
                abortController.abort();
            });
            
            $("#data-view-button").click(function () {
                abortController.abort();
            });
                
            $("#year").change(function () {
                abortController.abort();
            });
                
            $("#overlay").change(function () {
                abortController.abort();
            });
                
            var year = $("#year option:selected").val().trim();
            const parameters = { "year": year };
            const response = await fetch("/urban_development/get_data/" + JSON.stringify(parameters), { signal: abortController.signal, });

            try {
                var json = await response.json();

                $("#data").append("<span class='text-element data-element'>Total classified tiles: " + json["total"] + " </span><br>");

                const public_space = json["public_space"] - json["mixed"];
                const not_public_space = json["not_public_space"] - json["mixed"];

                $("#data").append("<br><span class='text-element data-element'>Tiles classified as public space: " + public_space + " (" + (100 * public_space / json["total"]).toFixed(2) + "%)</span><br>");
                $("#data").append("<span class='text-element data-element'>Tiles classified as not public space: " + not_public_space + " (" + (100 * not_public_space / json["total"]).toFixed(2) + "%)</span><br>");
                $("#data").append("<span class='text-element data-element'>Tiles classified as mixed: " + json["mixed"] + " (" + (100 * json["mixed"] / json["total"]).toFixed(2) + "%)</span><br>");

                const user = json["user"] - json["user_classifier"] - json["user_training_data"] + json["user_classifier_training_data"];
                const classifier = json["classifier"] - json["user_classifier"] - json["classifier_training_data"] + json["user_classifier_training_data"];
                const training_data = json["training_data"] - json["user_training_data"] - json["classifier_training_data"] + json["user_classifier_training_data"];

                const user_classifier = json["total"] - user - classifier - json["training_data"];
                const user_training_data = json["total"] - user - training_data - json["classifier"];
                const classifier_training_data = json["total"] - classifier - training_data - json["user"];
                    
                $("#data").append("<br><span class='text-element data-element'>Tiles classified by user: " + user + " (" + (100 * user / json["total"]).toFixed(2) + "%)</span><br>");
                $("#data").append("<span class='text-element data-element'>Tiles classified by classifier: " + classifier + " (" + (100 * classifier / json["total"]).toFixed(2) + "%)</span><br>");
                $("#data").append("<span class='text-element data-element'>Tiles classified by training data: " + training_data + " (" + (100 * training_data / json["total"]).toFixed(2) + "%)</span><br>");
                $("#data").append("<span class='text-element data-element'>Tiles classified by user and classifier: " + user_classifier + " (" + (100 * user_classifier / json["total"]).toFixed(2) + "%)</span><br>");
                $("#data").append("<span class='text-element data-element'>Tiles classified by user and training data: " + user_training_data + " (" + (100 * user_training_data / json["total"]).toFixed(2) + "%)</span><br>");
                $("#data").append("<span class='text-element data-element'>Tiles classified by classifier and training data: " + classifier_training_data + " (" + (100 * classifier_training_data / json["total"]).toFixed(2) + "%)</span><br>");
                $("#data").append("<span class='text-element data-element'>Tiles classified by user, classifier and training data: " + json["user_classifier_training_data"] + " (" + (100 * json["user_classifier_training_data"] / json["total"]).toFixed(2) + "%)</span><br>");
            } catch (exception) {
                console.error(exception);
                console.error(exception.lineNumber);
                    
                alert("Error.");
            }
        }
        
        map = new Map("map");

        addMap();
        setupMapView();

        $(document).ready(function () {
            $("#year").change(function (event) {
                if ($("#overlay-cell").is(":visible")){
                    addMap();
                } else {
                    setupDataView();
                }
            });
            $("#overlay").change(function (event) {
                if ($("#overlay-cell").is(":visible")){
                    map.remove(classifiedAsLayer);
                    map.remove(classifiedByLayer);

                    var overlay = $("#overlay option:selected").val().trim();
                    var year = $("#year option:selected").val().trim();
                    
                    addCurrentOverlay(overlay, year);
                }
            });
            $("#map-view-button").click(function (event) {
                $("#map-view-button").prop("disabled", true);
                $("#data").remove();
                $("#overlay").val("None").change();
                $("#overlay-cell").show();
                $("#data-view-button").prop("disabled", false);
                
                var mapDiv = $("<div id='map'></div>");
                
                map = new Map(mapDiv);
                addMap();
                $(document.body).append(mapDiv);

                setupMapView(mapView);

            });
            $("#data-view-button").click(function (event) {
                $("#data-view-button").prop("disabled", true);
                $("#map").remove();
                $("#overlay-cell").hide();
                $("#map-view-button").prop("disabled", false);

                setupDataView();
            });
        });
    }
);

function setupClassifiedAsLayer(FeatureLayer) {
    var template = {
        title: "Tile | EPSG: 4326",
        content: "<div>Coordinates: {Longitude}, {Latitude}<br>\
                        <br>\
                        Classified as:<br>\
                        public space: {Public space}<br>\
                        not public space: {Not public space}</div>",
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
};

function setupClassifiedByLayer(FeatureLayer) {
    var template = {
        title: "Tile | EPSG: 4326",
        content: "<div>Coordinates: {Longitude}, {Latitude}<br>\
                        <br>\
                        Classified by:<br>\
                        user: {By user}<br>\
                        classifier: {By classifier}<br>\
                        training data: {By training data}</div>",
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
};
