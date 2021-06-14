var map
var mapView
var classifiedAsLayer
var classifiedByLayer

require([
    'esri/Map',
    'esri/views/MapView',
    'esri/widgets/LayerList',
    'esri/widgets/Legend',
    'esri/layers/TileLayer',
    'esri/Graphic',
    'esri/layers/FeatureLayer',
    'esri/geometry/Extent',
    'esri/geometry/Polygon',
    'esri/widgets/Editor',
    'dojo/domReady!',
], function (
    Map,
    MapView,
    LayerList,
    Legend,
    TileLayer,
    Graphic,
    FeatureLayer,
    Extent,
    Polygon,
) {
    function clearPage() {
        $('#header-div').remove()
        $('#info-div').remove()
        $('#footer-div').remove()
        $('#map').remove()
        $('#data').remove()
    }

    function setupInfoView() {
        clearPage()

        var headerDiv = $("<div class='page-title' id='header-div'></div>")
        $('.title-container').append(headerDiv)

        var titlediv = $("<div class='title-text'></div>")
        headerDiv.append(titlediv)

        titlediv.append("<h2>How to use HAUP<br>Urban Development</h2>")
        titlediv.append("<h3>To view parks on historic maps</h3>")

        var imageDiv = $('<div></div>')
        headerDiv.append(imageDiv)

        imageDiv.append("<img src='../../../static/urban_development/images/tree.png' class='tree'>")
        imageDiv.append("<img src='../../../static/urban_development/images/bench.png' class='bench'>")

        var infoDiv = $("<div class='steps' id='info-div'></div>")
        $('.page-container').append(infoDiv)

        infoDiv.append("<button type='button' class='collapsible'>How to view greenery on historical maps</button>")

        var div1 = $("<div class='content'></div>")
        infoDiv.append(div1)

        var list1 = $("<ol class='steps-list'></ol>")
        div1.append(list1)

        list1.append("<li class='steps-items'>In the menu bar at the top, select 'Map View'.</li>")
        list1.append("<li class='steps-items'>On the map view page, in the menu bar at the top, select the year of map you want to view.</li>")
        list1.append("<li class='steps-items'>In the menu bar at the top, select the type of classification you want to view.\
            'Classified as' provides a overlay on the map with the different types of classifications.\
            'Classified by' provides an overlay depending on who determined the classification. Default is the\
            classification by the classifier algorithm of the tool.</li>")

        infoDiv.append("<button type='button' class='collapsible'>How to view the (statistical) data of greenery on historical maps</button>")

        var div2 = $("<div class='content'></div>")
        infoDiv.append(div2)

        var list2 = $("<ol class='steps-list'></ol>")
        div2.append(list2)

        list2.append("<li class='steps-items'>In the menu bar at the top, select 'Data View'.</li>")
        list2.append("<li class='steps-items'>On the data view page, in the menu bar at the top, select the year of the\
            (statistical) data you want to view.</li>")
        list2.append("<li class='steps-items'>On the data view page, you can see statistics regarding the percentages of the\
            map classified as a certain label, as well as statistics concerning what or who classified (sections of) the map.</li>")

        infoDiv.append("<button type='button' class='collapsible'>How to manually classify sections on a map</button>")

        var div3 = $("<div class='content'></div>")
        infoDiv.append(div3)

        div3.append("<p class='steps-items'>This functionality is not yet available.</p>")

        var footerDiv = $("<div class='footer' id='footer-div'></div>")
        $('.page-container').append(footerDiv)

        var date = new Date().getFullYear()
        footerDiv.append("<p>" + date + " Urban Development</p>")

        var collapsible = document.getElementsByClassName("collapsible");
        for (var i = 0; i < collapsible.length; i++) {
            collapsible[i].addEventListener("click", function () {
                this.classList.toggle("active");
                var content = this.nextElementSibling;
                if (content.style.display === "block") {
                    content.style.display = "none";
                } else {
                    content.style.display = "block";
                }
            });
        }
    }

    function setupMapView() {
        clearPage()

        $('.page-container').append("<div id='map'></div>")

        map = new Map('map')

        mapView = new MapView({
            container: 'map',
            map: map,
            zoom: 3,
            extent: new Extent(13328.546, 306816.384, 278302.013, 619342.658, { wkid: 28992, }),
        })

        const legend = new Legend({ view: mapView })
        const layerList = new LayerList({
            view: mapView,
            listItemCreatedFunction: function (event) {
                var item = event.item

                // Don't show the legend twice
                if (item.layer.geometryType === 'polygon') {
                    item.title = 'Classification legend'
                    item.panel = legend
                }
            },
        })

        var coordinatesWidget = document.createElement('div')
        coordinatesWidget.className = 'esri-widget esri-component'
        coordinatesWidget.style.padding = '7px 15px 5px'
        coordinatesWidget.style.marginBottom = '11px'

        mapView.ui.add(coordinatesWidget, 'bottom-left')
        mapView.ui.add(layerList, 'bottom-right')

        function showCoordinates(event) {
            coordinatesWidget.innerHTML = 'Longitude: ' + event.x +
                ' | Latitude: ' + event.y +
                ' | Scale 1:' + Math.round(mapView.scale * 1) / 1 +
                ' | Zoom ' + mapView.zoom +
                ' | EPSG: 28992'
        }

        mapView.watch(['stationary'], function () {
            showCoordinates(mapView.center)
        })

        mapView.on(['pointer-down'], function (event) {
            showCoordinates(mapView.toMap({ x: event.x, y: event.y }))
        })

        addMap()
    }

    async function setupDataView() {
        clearPage()

        var dataDiv = $("<div id='data'></div>")
        $('.page-container').append(dataDiv)

        let abortController = new AbortController()

        $('#how-to-view-button').click(function () {
            abortController.abort()
        })

        $('#map-view-button').click(function () {
            abortController.abort()
        })

        $('#data-view-button').click(function () {
            abortController.abort()
        })

        $('#year').change(function () {
            abortController.abort()
        })

        $('#overlay').change(function () {
            abortController.abort()
        })

        $('#logout-hyperlink').click(function () {
            abortController.abort()
        })

        var year = $('#year option:selected').val().trim()
        const parameters = { year: year }
        const response = await fetch('/urban_development/get_classified_tiles/' + JSON.stringify(parameters), { signal: abortController.signal })

        try {
            var json = await response.json()

            const classifiedTiles = Object.keys(json).length
            var noGreenery = 0, greenery = 0, quarter1 = 0, quarter2 = 0, quarter3 = 0, quarter4 = 0
            var classifiedByUser = 0, classifiedByClassifier = 0, classifiedByTrainingData = 0

            for (var i = 0; i < classifiedTiles; i++) {
                if (json[i].contains_greenery) {
                    greenery++;

                    if (json[i].greenery_rounded == 25) {
                        quarter1++
                    } else if (json[i].greenery_rounded == 50) {
                        quarter2++
                    } else if (json[i].greenery_rounded == 75) {
                        quarter3++
                    } else if (json[i].greenery_rounded == 100) {
                        quarter4++
                    }
                } else {
                    noGreenery++
                }

                if (json[i].classified_by == "user") {
                    classifiedByUser++
                } else if (json[i].classified_by == "classifier") {
                    classifiedByClassifier++
                } else if (json[i].classified_by == "training data") {
                    classifiedByTrainingData++
                }
            }

            $('#data').append("<span class='text-element data-element'>Total classified tiles: " + classifiedTiles + "</span><br><br><br>")
            $('#data').append("<span class='text-element data-element' id='no-greenery'>Tiles classified as not containing greenery: " + noGreenery + "</span><br>")
            $('#data').append("<span class='text-element data-element' id='greenery'>Tiles classified as containing greenery: " + greenery + "</span><br><br><br>")
            $('#data').append("<span class='text-element data-element' id='quarter1'>Tiles classified as containing 0% - 25% greenery: " + quarter1 + "</span><br>")
            $('#data').append("<span class='text-element data-element' id='quarter2'>Tiles classified as containing 25% - 50% greenery: " + quarter2 + "</span><br>")
            $('#data').append("<span class='text-element data-element' id='quarter3'>Tiles classified as containing 50% - 75% greenery: " + quarter3 + "</span><br>")
            $('#data').append("<span class='text-element data-element' id='quarter4'>Tiles classified as containing 75% - 100% greenery: " + quarter4 + "</span><br><br><br>")
            $('#data').append("<span class='text-element data-element' id='user-tiles'>Tiles classified by user: " + classifiedByUser + "</span><br>")
            $('#data').append("<span class='text-element data-element' id='classifier-tiles'>Tiles classified by classifier: " + classifiedByClassifier + "</span><br>")
            $('#data').append("<span class='text-element data-element' id='training-data-tiles'>Tiles classified by training data: " + classifiedByTrainingData + "</span><br>")

            if (classifiedTiles > 0) {
                function setupSpan(id, value) {
                    function roundToTwoDecimalPlaces(x) {
                        return +(Math.round(x + 'e+2') + 'e-2')
                    }

                    if (value > 0) {
                        const exact = (100 * value) / classifiedTiles
                        const rounded = roundToTwoDecimalPlaces(exact)
                        $('#' + id).append(' (' + (rounded == exact ? '=' : '≈') + rounded + '%)')
                    }
                }

                setupSpan('no-greenery', noGreenery)
                setupSpan('greenery', greenery)
                setupSpan('quarter1', quarter1)
                setupSpan('quarter2', quarter2)
                setupSpan('quarter3', quarter3)
                setupSpan('quarter4', quarter4)
                setupSpan('user-tiles', classifiedByUser)
                setupSpan('classifier-tiles', classifiedByClassifier)
                setupSpan('training-data-tiles', classifiedByTrainingData)
            }
        } catch (exception) {
            alert('No tiles have been classified for the selected year.')
        }
    }

    function addMap() {
        map.removeAll()

        var overlay = $('#overlay option:selected').val().trim()
        var year = $('#year option:selected').val().trim()

        var yearLayer = new TileLayer({
            url: 'https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_' + year + '/MapServer',
        })

        map.add(yearLayer)
        addCurrentOverlay(overlay, year)
    }

    function addCurrentOverlay(overlay, year) {
        if (overlay === 'Classified as') {
            setupClassifiedAsLayer(FeatureLayer)
            addToClassifiedAsLayer(year)
        } else if (overlay === 'Classified by') {
            setupClassifiedByLayer(FeatureLayer)
            addToClassifiedByLayer(year)
        }
    }

    async function addToClassifiedAsLayer() {
        let abortController = new AbortController()

        $('#how-to-view-button').click(function () {
            abortController.abort()
        })

        $('#map-view-button').click(function () {
            abortController.abort()
        })

        $('#data-view-button').click(function () {
            abortController.abort()
        })

        $('#year').change(function () {
            abortController.abort()
        })

        $('#overlay').change(function () {
            abortController.abort()
        })

        $('#logout-hyperlink').click(function () {
            abortController.abort()
        })

        var year = $('#year option:selected').val().trim()
        const parameters = { year: year }
        const response = await fetch('/urban_development/get_classified_tiles/' + JSON.stringify(parameters), { signal: abortController.signal })

        try {
            var json = await response.json()

            edits = {
                addFeatures: [],
                updateFeatures: [],
            }

            for (let i = 0; i < json.length; i++) {
                var graphic = new Graphic({
                    geometry: Polygon.fromExtent(
                        new Extent(
                            json[i].xmin, // xmin
                            json[i].ymin, // ymin
                            json[i].xmax, // xmax
                            json[i].ymax, // ymax
                            { wkid: 28992 }, // spatial reference
                        )
                    ),
                })

                graphic.setAttribute('Longitude', json[i].x_coordinate)
                graphic.setAttribute('Latitude', json[i].y_coordinate)
                graphic.setAttribute('Contains greenery', json[i].contains_greenery)
                graphic.setAttribute('Greenery percentage', json[i].greenery_percentage)
                graphic.setAttribute('Greenery rounded', json[i].greenery_rounded)

                edits.addFeatures.push(graphic)
            }

            classifiedAsLayer.applyEdits(edits)
            map.add(classifiedAsLayer)
        } catch (exception) {
            alert('No tiles have been classified for the selected year.')
            $('#overlay').val('None').change()
        }
    }

    async function addToClassifiedByLayer() {
        let abortController = new AbortController()

        $('#how-to-view-button').click(function () {
            abortController.abort()
        })

        $('#map-view-button').click(function () {
            abortController.abort()
        })

        $('#data-view-button').click(function () {
            abortController.abort()
        })

        $('#year').change(function () {
            abortController.abort()
        })

        $('#overlay').change(function () {
            abortController.abort()
        })

        $('#logout-hyperlink').click(function () {
            abortController.abort()
        })

        var year = $('#year option:selected').val().trim()
        const parameters = { year: year }
        const response = await fetch('/urban_development/get_classified_tiles/' + JSON.stringify(parameters), { signal: abortController.signal })

        try {
            var json = await response.json()

            edits = {
                addFeatures: [],
                updateFeatures: [],
            }

            for (let i = 0; i < json.length; i++) {
                var graphic = new Graphic({
                    geometry: Polygon.fromExtent(
                        new Extent(
                            json[i].xmin, // xmin
                            json[i].ymin, // ymin
                            json[i].xmax, // xmax
                            json[i].ymax, // ymax
                            { wkid: 28992 }, // spatial reference
                        )
                    ),
                })

                graphic.setAttribute('Longitude', json[i].x_coordinate)
                graphic.setAttribute('Latitude', json[i].y_coordinate)
                graphic.setAttribute('Classified by', json[i].classified_by)

                edits.addFeatures.push(graphic)
            }

            classifiedByLayer.applyEdits(edits)
            map.add(classifiedByLayer)
        } catch (exception) {
            alert('No tiles have been classified for the selected year.')
            $('#overlay').val('None').change()
        }
    }

    $(document).ready(function () {
        const VIEWS = {
          info: 'info',
          map: 'map',
          data: 'data',
        }

        var currentView = VIEWS.map
        setupMapView()

        $('#year').change(function (event) {
            if ($('#overlay-cell').is(':visible')) {
                addMap()
            } else {
                setupDataView()
            }
        })

        $('#overlay').change(function (event) {
            if ($('#overlay-cell').is(':visible')) {
                map.remove(classifiedAsLayer)
                map.remove(classifiedByLayer)

                var overlay = $('#overlay option:selected').val().trim()
                var year = $('#year option:selected').val().trim()

                addCurrentOverlay(overlay, year)
            }
        })

        $('#how-to-view-button').click(function (event) {
            if (currentView === VIEWS.info) return

            currentView = VIEWS.info
            clearPage()
            $('#year-cell').hide()
            $('#overlay-cell').hide()
            setupInfoView()
        })

        $('#map-view-button').click(function (event) {
            if (currentView === VIEWS.map) return

            currentView = VIEWS.map
            clearPage()
            $('#year-cell').show()
            $('#overlay-cell').show()
            setupMapView()
        })

        $('#data-view-button').click(function (event) {
            if (currentView === VIEWS.data) return

            currentView = VIEWS.data
            clearPage()
            $('#year-cell').show()
            $('#overlay-cell').hide()
            setupDataView()
        })
    })
})

function setupClassifiedAsLayer(FeatureLayer) {
    var template = {
        title: 'Tile | EPSG: 4326',
        content: '<div>Coordinates: {Longitude}, {Latitude}<br>Contains greenery: {Contains greenery}<br>Greenery percentage: {Greenery percentage}%</div>',
    }

    var renderer = {
        type: 'unique-value',
        field: 'Contains greenery',
        field2: 'Greenery rounded',
        fieldDelimiter: ':',
        defaultSymbol: { type: 'simple-fill' },
        uniqueValueInfos: [
            {
                value: 'false:0',
                label: 'not containinig greenery',
                symbol: {
                    type: 'simple-fill',
                    color: [255, 0, 0, 0.5],
                    style: 'solid',
                    outline: {
                        style: 'none',
                    },
                },
            },
            {
                value: 'true:25',
                label: 'containing 0% - 25% greenery',
                symbol: {
                    type: 'simple-fill',
                    color: [0, 255, 0, 0.25],
                    style: 'solid',
                    outline: {
                        style: 'none',
                    },
                },
            },
            {
                value: 'true:50',
                label: 'containing 25% - 50% greenery',
                symbol: {
                    type: 'simple-fill',
                    color: [0, 255, 0, 0.45],
                    style: 'solid',
                    outline: {
                        style: 'none',
                    },
                },
            },
            {
                value: 'true:75',
                label: 'containing 50% - 75% greenery',
                symbol: {
                    type: 'simple-fill',
                    color: [0, 255, 0, 0.65],
                    style: 'solid',
                    outline: {
                        style: 'none',
                    },
                },
            },
            {
                value: 'true:100',
                label: 'containing 75% - 100% greenery',
                symbol: {
                    type: 'simple-fill',
                    color: [0, 255, 0, 0.85],
                    style: 'solid',
                    outline: {
                        style: 'none',
                    },
                },
            },
        ],
        outFields: ['*'],
    }

    classifiedAsLayer = new FeatureLayer({
        objectIdField: 'objectid',
        fields: [
            {
                name: 'objectid',
                type: 'oid',
            },
            {
                name: 'Longitude',
                type: 'double',
            },
            {
                name: 'Latitude',
                type: 'double',
            },
            {
                name: 'Contains greenery',
                type: 'string',
            },
            {
                name: 'Greenery percentage',
                type: 'double',
            },
            {
                name: 'Greenery rounded',
                type: 'integer',
            },
        ],
        source: [],
        popupTemplate: template,
        renderer: renderer,
        geometryType: 'polygon',
        spatialReference: { wkid: 28992 },
        outFields: ['objectid'],
        labelsVisible: 'true',
        title: 'Classified as',
    })
}

function setupClassifiedByLayer(FeatureLayer) {
    var template = {
        title: 'Tile | EPSG: 4326',
        content: '<div>Coordinates: {Longitude}, {Latitude}<br>Classified by: {Classified by}',
    }

    var renderer = {
        type: 'unique-value',
        field: 'Classified by',
        defaultSymbol: { type: 'simple-fill' },
        uniqueValueInfos: [
            {
                value: 'user',
                label: 'a user',
                symbol: {
                    type: 'simple-fill',
                    color: [0, 255, 255, 0.5],
                    style: 'solid',
                    outline: {
                        style: 'none',
                    },
                },
            },
            {
                value: 'classifier',
                label: 'the classifier',
                symbol: {
                    type: 'simple-fill',
                    color: [255, 0, 255, 0.5],
                    style: 'solid',
                    outline: {
                        style: 'none',
                    },
                },
            },
            {
                value: 'training data',
                label: 'the training data',
                symbol: {
                    type: 'simple-fill',
                    color: [255, 255, 0, 0.5],
                    style: 'solid',
                    outline: {
                        style: 'none',
                    },
                },
            },
        ],
        outFields: ['*'],
    }

    classifiedByLayer = new FeatureLayer({
        objectIdField: 'objectid',
        fields: [
            {
                name: 'objectid',
                type: 'oid',
            },
            {
                name: 'Longitude',
                type: 'double',
            },
            {
                name: 'Latitude',
                type: 'double',
            },
            {
                name: 'Classified by',
                type: 'string',
            },
        ],
        source: [],
        popupTemplate: template,
        renderer: renderer,
        geometryType: 'polygon',
        spatialReference: { wkid: 28992 },
        outFields: ['objectid'],
        labelsVisible: 'true',
        title: 'Classified by',
    })
}
