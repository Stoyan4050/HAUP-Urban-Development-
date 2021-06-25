var map
var mapView
var classifiedAsLayer
var classifiedByLayer
var currentlySelectedTile = null
var currentTileFrame = null

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

        var headerDiv = $('<div class="page-title" id="header-div"></div>')
        $('.title-container').append(headerDiv)

        var titlediv = $('<div class="title-text"></div>')
        headerDiv.append(titlediv)

        titlediv.append('<h2>How to use HAUP<br>Urban Development</h2>')
        titlediv.append('<h3>To view parks on historic maps</h3>')

        var imageDiv = $('<div></div>')
        headerDiv.append(imageDiv)

        imageDiv.append('<img src="../../../static/urban_development/images/tree.png" class="tree">')
        imageDiv.append('<img src="../../../static/urban_development/images/bench.png" class="bench">')

        var infoDiv = $('<div class="steps" id="info-div"></div>')
        $('.page-container').append(infoDiv)

        infoDiv.append('<button type="button" class="collapsible">How to view greenery on historical maps</button>')

        var div1 = $('<div class="content"></div>')
        infoDiv.append(div1)

        var list1 = $('<ol class="steps-list"></ol>')
        div1.append(list1)

        list1.append('<li class="steps-items">From the menu bar at the top of the page, select "Map view".</li>')
        list1.append('<li class="steps-items">In the map view, from the menu bar at the top of the page, select the year, which you want to view the map of.</li>')
        list1.append('<li class="steps-items">From the menu bar at the top of the page, select the overlay, which you want to view.\
            The "Classified as" overlay provides information on what different map tiles have been classified as.\
            The "Classified by" overlay provides information on who different map tiles have been classified by.</li>')

        infoDiv.append('<button type="button" class="collapsible">How to view the (statistical) data of greenery on historical maps</button>')

        var div2 = $('<div class="content"></div>')
        infoDiv.append(div2)

        var list2 = $('<ol class="steps-list"></ol>')
        div2.append(list2)

        list2.append('<li class="steps-items">From the menu bar at the top of the page, select "Data view".</li>')
        list2.append('<li class="steps-items">In the data view, from the menu bar at the top of the page, select the year, \
            the map of which you want to view (statistical) data for.</li>')
        list2.append('<li class="steps-items">On the data view page, you can see statistics regarding what different map tiles\
            have been classified as and who they have been classified by.</li>')

        infoDiv.append('<button type="button" class="collapsible">How to classify map tiles using the classifier</button>')

        var div3 = $('<div class="content"></div>')
        infoDiv.append(div3)

        var list3 = $('<ol class="steps-list"></ol>')
        div3.append(list3)

        list3.append('<li class="steps-items">Log in with your account (guest users are not allowed to classify map tiles using the classifier).</li>')
        list3.append('<li class="steps-items">From the menu bar at the top of the page, select "Map view".</li>')
        list3.append('<li class="steps-items">In the map view, from the menu bar at the top of the page, select the year, \
            which you want to classify map tiles of, and select the "Classified as" overlay.</li>')
        list3.append('<li class="steps-items">In order to classify a certain map tile, select it by clicking on it on the map.\
            This will open a side bar, containing the current information about the selected map tile \
            (all information will appear as "unknown", if the map tile has not been classified yet").</li>')
        list3.append('<li class="steps-items">To classify the selected map tile using the classifier, you should simply press the "Classify" button. \
            This will display a message, saying that a tile is currently being classified, and will give you the option to cancel the classification, \
            before it has completed, using the "Cancel" button. As soon as the selected map tile has been classified by the classifier, the message \
            will disappear and the changes will be visible in the side bar and on the map.</li>')

        infoDiv.append('<button type="button" class="collapsible">How to manually classify map tiles</button>')

        var div4 = $('<div class="content"></div>')
        infoDiv.append(div4)

        var list4 = $('<ol class="steps-list"></ol>')
        div4.append(list4)

        list4.append('<li class="steps-items">Log in with your account (guest users are not allowed to manually classify map tiles).</li>')
        list4.append('<li class="steps-items">From the menu bar at the top of the page, select "Map view".</li>')
        list4.append('<li class="steps-items">In the map view, from the menu bar at the top of the page, select the year, \
            which you want to classify map tiles of, and select the "Classified as" overlay.</li>')
        list4.append('<li class="steps-items">In order to classify a certain map tile, select it by clicking on it on the map.\
            This will open a side bar, containing the current information about the selected map tile \
            (all information will appear as "unknown", if the map tile has not been classified yet").</li>')
        list4.append('<li class="steps-items">To manually classify the selected map tile, you should choose whether or not the map tile contains greenery \
            and, if it does, you should specify the amount of greenery, which the map tile contains. Then, you should simply press the "Save" / "Update" button \
            and, in a couple of seconds, your changes will be visible in the side bar and on the map.</li>')

        var footerDiv = $('<div class="footer" id="footer-div"></div>')
        $('.page-container').append(footerDiv)

        var date = new Date().getFullYear()
        footerDiv.append('<p>' + date + ' Urban Development</p>')

        var collapsible = document.getElementsByClassName('collapsible')
        for (var i = 0; i < collapsible.length; i++) {
            collapsible[i].addEventListener('click', function () {
                this.classList.toggle('active')
                var content = this.nextElementSibling
                if (content.style.display === 'block') {
                    content.style.display = 'none'
                } else {
                    content.style.display = 'block'
                }
            })
        }
    }

    function setupMapView() {
        clearPage()

        $('.page-container').append('<div id="map"></div>')

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
        coordinatesWidget.className = 'esri-widget esri-component coordinates-widget'
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

        mapView.on('click', function(event) {
            $('#update-button').attr('disabled', true)
            $('#classify-button').attr('disabled', true)
            $('#close-button').attr('disabled', true)
            setupManualClassificationForm(event).then(function (value) {
                $('#update-button').attr('disabled', false)

                if (value) {
                    $('#classify-button').attr('disabled', false)
                }

                $('#close-button').attr('disabled', false)
            })
        })

        addMap()
    }

    async function setupManualClassificationForm(event) {
        if ($('#overlay option:selected').val().trim() === 'Classified as') {
            let abortController = new AbortController()
    
            $('#how-to-view-button').click(function () {
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

            var x_coordinate = event.mapPoint.x
            var y_coordinate = event.mapPoint.y
            var year = $('#year option:selected').val().trim()
            const parameters = {
                x_coordinate: x_coordinate,
                y_coordinate: y_coordinate,
                year: year
            }
            const response = await fetch('/urban_development/transform_coordinates/' + JSON.stringify(parameters), { signal: abortController.signal })

            try {
                var json = await response.json()

                var longitude = document.getElementById('coordinates').innerHTML.trim().split(', ')[0]
                var latitude = document.getElementById('coordinates').innerHTML.trim().split(', ')[1]

                if (String(json.x_coordinate) === longitude && String(json.y_coordinate) === latitude) {
                    if (String(json.year) === year && (String(json.classified_by) === 'training data' || String(json.classified_by) === 'user')) {
                        return false
                    } else {
                        return true
                    }
                }

                edits = {
                    deleteFeatures: [],
                }

                if (currentTileFrame != null) {
                    edits.deleteFeatures.push(currentTileFrame)
                }

                classifiedAsLayer.applyEdits(edits)

                const opts = {
                    include: classifiedAsLayer
                }
                
                await mapView.hitTest(event, opts).then(function(response) {
                    if (response.results.length) {
                        currentlySelectedTile = response.results[0].graphic
                    } else {
                        currentlySelectedTile = null
                    }
                })

                edits = {
                    addFeatures: [],
                }

                var graphic = new Graphic({
                    geometry: Polygon.fromExtent(
                        new Extent(
                            json.xmin, // xmin
                            json.ymin, // ymin
                            json.xmax, // xmax
                            json.ymax, // ymax
                            { wkid: 28992 }, // spatial reference
                        )
                    ),
                })

                edits.addFeatures.push(graphic)
                classifiedAsLayer.applyEdits(edits)
                currentTileFrame = graphic

                var user = document.getElementById('user-name').innerHTML.trim().split(' ').join('').split('\n')[2]

                if (user === 'guest') {
                    $('#update-title').css('display', 'none')
                    $('#text-contains-greenery').css('display', 'none')
                    $('#contains-greenery').css('display', 'none')
                    $('#text-greenery-amount').css('display', 'none')
                    $('#greenery-amount').css('display', 'none')
                    $('#update-button').css('display', 'none')
                    $('#classify-button').css('display', 'none')
                }

                if (json['contains_greenery'] != 'unknown'){
                    $('#update-button').html('Update')
                } else {
                    $('#update-button').html('Save')
                }

                $('#coordinates').html(json['x_coordinate'] + ', ' + json['y_coordinate'])
                $('#classification-year').html(json['year'])
                $('#current-contains-greenery').html(String(json['contains_greenery']))
                $('#current-greenery-amount').html(String(json['greenery_amount']))
                $('#classified-by').html(json['classified_by'])
                $('#contains-greenery').val('True').change()
                $('#greenery-amount').val('low').change()

                $('#form-div').css('display', 'block')

                if (String(json.year) === year && (String(json.classified_by) === 'training data' || String(json.classified_by) === 'user')) {
                    return false
                } else {
                    return true
                }
            } catch (exception) {
                alert('Error.')
                return true
            }
        }
    }

    async function setupDataView() {
        clearPage()

        var dataDiv = $('<div id="data"></div>')
        $('.page-container').append(dataDiv)

        let abortController = new AbortController()

        $('#how-to-view-button').click(function () {
            abortController.abort()
        })

        $('#map-view-button').click(function () {
            abortController.abort()
        })

        $('#year').change(function () {
            abortController.abort()
        })

        $('#logout-hyperlink').click(function () {
            abortController.abort()
        })

        var year = $('#year option:selected').val().trim()
        const parameters = { 
            year: year,
            province: "None"
        }
        const response = await fetch('/urban_development/get_classified_tiles/' + JSON.stringify(parameters), { signal: abortController.signal })

        try {
            var json = await response.json()

            const classifiedTiles = Object.keys(json).length
            var noGreenery = 0, greenery = 0, low = 0, medium = 0, high = 0
            var classifiedByUser = 0, classifiedByClassifier = 0, classifiedByTrainingData = 0

            for (var i = 0; i < classifiedTiles; i++) {
                if (json[i].contains_greenery) {
                    greenery++

                    if (String(json[i].greenery_amount) == 'low') {
                        low++
                    } else if (String(json[i].greenery_amount) == 'medium') {
                        medium++
                    } else if (String(json[i].greenery_amount) == 'high') {
                        high++
                    }
                } else {
                    noGreenery++
                }

                if (json[i].classified_by == 'user') {
                    classifiedByUser++
                } else if (json[i].classified_by == 'classifier') {
                    classifiedByClassifier++
                } else if (json[i].classified_by == 'training data') {
                    classifiedByTrainingData++
                }
            }

            $('#data').append('<span class="text-element data-element">Total classified tiles: ' + classifiedTiles + '</span><br><br><br>')
            $('#data').append('<span class="text-element data-element" id="no-greenery">Tiles classified as not containing greenery: ' + noGreenery + '</span><br>')
            $('#data').append('<span class="text-element data-element" id="greenery">Tiles classified as containing greenery: ' + greenery + '</span><br><br><br>')
            $('#data').append('<span class="text-element data-element" id="low">Tiles classified as containing low amount of greenery: ' + low + '</span><br>')
            $('#data').append('<span class="text-element data-element" id="medium">Tiles classified as containing medium amount of greenery: ' + medium + '</span><br>')
            $('#data').append('<span class="text-element data-element" id="high">Tiles classified as containing high amount of greenery: ' + high + '</span><br><br><br>')
            $('#data').append('<span class="text-element data-element" id="user-tiles">Tiles classified by user: ' + classifiedByUser + '</span><br>')
            $('#data').append('<span class="text-element data-element" id="classifier-tiles">Tiles classified by classifier: ' + classifiedByClassifier + '</span><br>')
            $('#data').append('<span class="text-element data-element" id="training-data-tiles">Tiles classified by training data: ' + classifiedByTrainingData + '</span><br>')

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
                setupSpan('low', low)
                setupSpan('medium', medium)
                setupSpan('high', high)
                setupSpan('user-tiles', classifiedByUser)
                setupSpan('classifier-tiles', classifiedByClassifier)
                setupSpan('training-data-tiles', classifiedByTrainingData)
            }
        } catch (exception) {
            alert('Error.')
        }
    }

    function addMap() {
        map.removeAll()

        var overlay = $('#overlay option:selected').val().trim()
        var year = $('#year option:selected').val().trim()
        var province = $('#province option:selected').val().trim()

        var yearLayer = new TileLayer({
            url: 'https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_' + year + '/MapServer',
        })

        map.add(yearLayer)
        addCurrentOverlay(overlay, year, province)
    }

    function addCurrentOverlay(overlay, year, province) {
        if (overlay === 'Classified as') {
            $('#province-cell').removeClass('hidden')
            $('#province-cell').show()

            setupClassifiedAsLayer(FeatureLayer)
            addToClassifiedAsLayer(year, province)
        } else if (overlay === 'Classified by') {
            $('#province-cell').removeClass('hidden')
            $('#province-cell').show()

            setupClassifiedByLayer(FeatureLayer)
            addToClassifiedByLayer(year, province)
        } else {
            $('#province-cell').addClass('hidden')
            $('#province-cell').hide()
            $('#province').val('None').change()
        }
    }

    async function addToClassifiedAsLayer() {
        currentlySelectedTile = null
        currentTileFrame = null

        let abortController = new AbortController()

        $('#how-to-view-button').click(function () {
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

        $('#province').change(function () {
            abortController.abort()
        })

        $('#logout-hyperlink').click(function () {
            abortController.abort()
        })

        var year = $('#year option:selected').val().trim()
        var province = $('#province option:selected').val().trim()
        const parameters = {
            year: year,
            province: province
        }
        const response = await fetch('/urban_development/get_classified_tiles/' + JSON.stringify(parameters), { signal: abortController.signal })

        try {
            var json = await response.json()
            
            edits = {
                addFeatures: [],
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
                graphic.setAttribute('Greenery amount', json[i].greenery_amount)

                edits.addFeatures.push(graphic)
            }

            classifiedAsLayer.applyEdits(edits)
            map.add(classifiedAsLayer)

            var mapDiv = $('#map')

            var formDiv = $('<div id="form-div"></div>')
            mapDiv.append(formDiv)

            var form = $('<form id="form"></form>')
            formDiv.append(form)

            form.append('<br><h1>Tile information</h1><br>')
            form.append('<label class="popup-info"><b>Center coordinates:</b></label><br>')
            form.append('<label class="popup-info" id="coordinates"></label><br>')
            form.append('<label class="popup-info"><b>Latest classification year:</b></label>')
            form.append('<label class="popup-info" id="classification-year"></label><br>')
            form.append('<label class="popup-info"><b>Contains greenery:</b></label>')
            form.append('<label class="popup-info" id="current-contains-greenery"></label><br>')
            form.append('<label class="popup-info" id="text-current-greenery-amount"><b>Greenery amount:</b></label>')
            form.append('<label class="popup-info" id="current-greenery-amount"></label><br>')
            form.append('<label class="popup-info"><b>Classified by:</b></label>')
            form.append('<label class="popup-info" id="classified-by"></label><br>')
            form.append('<br><h2 id="update-title">Update tile</h2><br>')
            form.append('<label class="popup-info" id="text-contains-greenery"><b>Contains greenery:</b></label><br>')

            var select = $('<select class="popup-info" id="contains-greenery"></select><br>')
            form.append(select)

            select.append('<option value="True">True</option>')
            select.append('<option value="False">False</option>')

            $('#contains-greenery').on('change', function () {
                if ($('#contains-greenery').is(':visible')) {
                    if ($('#contains-greenery option:selected').val().trim() === 'True') {
                        $('#text-greenery-amount').css('display', 'inline-block')
                        $('#greenery-amount').css('display', 'inline-block')
                    } else {
                        $('#text-greenery-amount').css('display', 'none')
                        $('#greenery-amount').css('display', 'none')
                        $('#greenery-amount').val('low').change()
                    }
                }
            })
            
            form.append('<label class="popup-info" id="text-greenery-amount"><b>Greenery amount:</b></label><br>')
            var selectContainsGreenery = $('<select class="popup-info" id="greenery-amount"></select><br>')
            form.append(selectContainsGreenery)

            selectContainsGreenery.append('<option value="low">Low</option>')
            selectContainsGreenery.append('<option value="medium">Medium</option>')
            selectContainsGreenery.append('<option value="high">High</option>')

            form.append('<button type="button" id="update-button"></button>')

            $('#update-button').on('click', async function() {
                $('#update-button').attr('disabled', true)
                $('#classify-button').attr('disabled', true)
                $('#close-button').attr('disabled', true)

                await manuallyClassifyTile().then(function() {
                    $('#update-button').attr('disabled', false)
                    $('#classify-button').attr('disabled', true)
                    $('#close-button').attr('disabled', false)
                })
            })

            form.append('<button type="button" id="classify-button">Classify</button>')

            $('#classify-button').on('click', async function() {
                $('#update-button').attr('disabled', true)
                $('#classify-button').attr('disabled', true)
                $('#close-button').attr('disabled', true)

                var lockDiv = $('<div id="lock-div"></div>')
                $('.page-container').append(lockDiv)

                var messageDiv = $('<div id="message-div"></div>')
                lockDiv.append(messageDiv)

                var messageContainer = $('<div id="message-container"></div>')
                messageDiv.append(messageContainer)
                
                var longitude = document.getElementById('coordinates').innerHTML.trim().split(', ')[0]
                var latitude = document.getElementById('coordinates').innerHTML.trim().split(', ')[1]
                var year = $('#year option:selected').val().trim()

                messageContainer.append('<span id="message-span">Map tile with center coordinates ' + longitude + ', ' + latitude + ' is currently being classified for the year ' + year + '.</span>')

                messageDiv.append('<button id="message-button">Cancel</button>')

                $('#message-button').on('click', function() {
                    $('#update-button').attr('disabled', false)
                    $('#classify-button').attr('disabled', false)
                    $('#close-button').attr('disabled', false)

                    $('#lock-div').remove()
                })

                await classifyTile().then(function() {
                    $('#update-button').attr('disabled', false)
                    $('#classify-button').attr('disabled', false)
                    $('#close-button').attr('disabled', false)

                    $('#lock-div').remove()
                })
            })

            form.append('<button type="button" id="close-button">Close</button>')

            $('#close-button').on('click', function() {
                edits = {
                    deleteFeatures:[],
                }

                if (currentTileFrame != null) {
                    edits.deleteFeatures.push(currentTileFrame)
                }

                classifiedAsLayer.applyEdits(edits)

                $('#form-div').css('display', 'none')
            })
        } catch (exception) {
            alert('Error.')
            $('#overlay').val('None').change()
        }
    }

    async function manuallyClassifyTile() {
        let abortController = new AbortController()

        $('#how-to-view-button').click(function () {
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

        $('#province').change(function () {
            abortController.abort()
        })

        $('#logout-hyperlink').click(function () {
            abortController.abort()
        })

        var longitude = document.getElementById('coordinates').innerHTML.trim().split(', ')[0]
        var latitude = document.getElementById('coordinates').innerHTML.trim().split(', ')[1]
        var year = $('#year option:selected').val().trim()
        var classifiedBy = document.getElementById('user-name').innerHTML.trim().split(' ').join('').split('\n')[2]
        var containsGreenery = document.getElementById('contains-greenery').value
        var greeneryAmount = containsGreenery === 'False' ? 'none' : $('#greenery-amount option:selected').val().trim()
        const parameters = {
            longitude: longitude,
            latitude: latitude,
            year: year,
            classified_by: classifiedBy,
            contains_greenery: containsGreenery,
            greenery_amount: greeneryAmount
        }
        const response = await fetch('/urban_development/manual_classification/' + JSON.stringify(parameters), { signal: abortController.signal })

        try {
            var json = await response.json()

            if (json == null) {
                return
            }
            
            edits = {
                addFeatures: [],
                deleteFeatures:[],
            }

            var graphic = new Graphic({
                geometry: Polygon.fromExtent(
                    new Extent(
                        json.xmin, // xmin
                        json.ymin, // ymin
                        json.xmax, // xmax
                        json.ymax, // ymax
                        { wkid: 28992 }
                    )
                ),
            })

            graphic.setAttribute('Longitude', json.x_coordinate)
            graphic.setAttribute('Latitude', json.y_coordinate)
            graphic.setAttribute('Contains greenery', json.contains_greenery)
            graphic.setAttribute('Greenery amount', json.greenery_amount)

            edits.addFeatures.push(graphic)

            if (currentlySelectedTile != null) {
                edits.deleteFeatures.push(currentlySelectedTile)
            }
            
            classifiedAsLayer.applyEdits(edits)

            currentlySelectedTile = graphic

            $('#classification-year').html(year)
            $('#current-contains-greenery').html(json.contains_greenery)

            if (String(json.contains_greenery) === 'true') {
                $('#current-greenery-amount').html(json['greenery_amount'])
            } else if (String(json.contains_greenery) === 'false') {
                $('#current-greenery-amount').html('none')
            }
            
            $('#classified-by').html('user')
        } catch (exception) {
            alert('Error.')
        }
    }

    async function classifyTile() {
        let abortController = new AbortController()

        $('#message-button').click(function () {
            abortController.abort()
        })

        var longitude = document.getElementById('coordinates').innerHTML.trim().split(', ')[0]
        var latitude = document.getElementById('coordinates').innerHTML.trim().split(', ')[1]
        var year = $('#year option:selected').val().trim()
        var user = document.getElementById('user-name').innerHTML.trim().split(' ').join('').split('\n')[2]
        const parameters = {
            longitude: longitude,
            latitude: latitude,
            year: year,
            user: user
        }
        const response = await fetch('/urban_development/classify_tile/' + JSON.stringify(parameters), { signal: abortController.signal })

        try {
            var json = await response.json()

            if (json == null) {
                return
            }

            edits = {
                addFeatures: [],
                deleteFeatures:[],
            }

            var graphic = new Graphic({
                geometry: Polygon.fromExtent(
                    new Extent(
                        json.xmin, // xmin
                        json.ymin, // ymin
                        json.xmax, // xmax
                        json.ymax, // ymax
                        { wkid: 28992 }
                    )
                ),
            })

            graphic.setAttribute('Longitude', json.x_coordinate)
            graphic.setAttribute('Latitude', json.y_coordinate)
            graphic.setAttribute('Contains greenery', json.contains_greenery)
            graphic.setAttribute('Greenery amount', json.greenery_amount)

            edits.addFeatures.push(graphic)

            if (currentlySelectedTile != null) {
                edits.deleteFeatures.push(currentlySelectedTile)
            }
            
            classifiedAsLayer.applyEdits(edits)

            currentlySelectedTile = graphic

            $('#classification-year').html(year)
            $('#current-contains-greenery').html(json.contains_greenery)

            if (String(json.contains_greenery) === 'true') {
                $('#current-greenery-amount').html(json['greenery_amount'])
            } else if (String(json.contains_greenery) === 'false') {
                $('#current-greenery-amount').html('none')
            }
            
            $('#classified-by').html('classifier')
        } catch (exception) {
            alert('Error.')
        }
    }

    async function addToClassifiedByLayer() {
        let abortController = new AbortController()

        $('#how-to-view-button').click(function () {
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

        $('#province').change(function (){
            abortController.abort()
        })

        $('#logout-hyperlink').click(function () {
            abortController.abort()
        })

        var year = $('#year option:selected').val().trim()
        var province = $('#province option:selected').val().trim()
        const parameters = {
            year: year,
            province: province
        }
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
            alert('Error.')
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
                $('#form-div').remove()

                addMap()
            } else {
                setupDataView()
            }
        })

        $('#overlay').change(function (event) {
            if ($('#overlay-cell').is(':visible')) {
                $('#form-div').remove()

                map.remove(classifiedAsLayer)
                map.remove(classifiedByLayer)

                var overlay = $('#overlay option:selected').val().trim()
                var year = $('#year option:selected').val().trim()
                var province = $('#province option:selected').val().trim()

                addCurrentOverlay(overlay, year, province)
            }
        })

        $('#province').change(function (event) {
            if ($('#province-cell').is(':visible')){
                map.remove(classifiedAsLayer)
                map.remove(classifiedByLayer)

                var overlay = $('#overlay option:selected').val().trim()
                var year = $('#year option:selected').val().trim()
                var province = $('#province option:selected').val().trim()

                addCurrentOverlay(overlay, year, province)
             }
    })
        $('#how-to-view-button').click(function (event) {
            if (currentView === VIEWS.info) return

            currentView = VIEWS.info
            clearPage()
            $('#year-cell').hide()
            $('#overlay-cell').hide()
            $('#province-cell').addClass('hidden')
            $('#province-cell').hide()
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
            $('#province-cell').addClass('hidden')
            $('#province-cell').hide()
            setupDataView()
        })
    })
})

function setupClassifiedAsLayer(FeatureLayer) {
    var renderer = {
        type: 'unique-value',
        field: 'Contains greenery',
        field2: 'Greenery amount',
        fieldDelimiter: ':',
        defaultSymbol: { type: 'simple-fill' },
        uniqueValueInfos: [
            {
                value: 'false:none',
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
                value: 'true:low',
                label: 'containing low amount of greenery',
                symbol: {
                    type: 'simple-fill',
                    color: [0, 255, 0, 0.4],
                    style: 'solid',
                    outline: {
                        style: 'none',
                    },
                },
            },
            {
                value: 'true:medium',
                label: 'containing medium amount of greenery',
                symbol: {
                    type: 'simple-fill',
                    color: [0, 255, 0, 0.6],
                    style: 'solid',
                    outline: {
                        style: 'none',
                    },
                },
            },
            {
                value: 'true:high',
                label: 'containing high amount of greenery',
                symbol: {
                    type: 'simple-fill',
                    color: [0, 255, 0, 0.8],
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
                name: 'Greenery amount',
                type: 'string',
            },
        ],
        source: [],
        renderer: renderer,
        geometryType: 'polygon',
        spatialReference: { wkid: 28992 },
        outFields: ['objectid'],
        labelsVisible: 'true',
        title: 'Classified as',
    })
}

function setupClassifiedByLayer(FeatureLayer) {
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
        renderer: renderer,
        geometryType: 'polygon',
        spatialReference: { wkid: 28992 },
        outFields: ['objectid'],
        labelsVisible: 'true',
        title: 'Classified by',
    })
}
