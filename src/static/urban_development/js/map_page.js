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
  function setupMapView() {
    mapView = new MapView({
      container: 'map-container',
      map: map,
      zoom: 3,
      extent: new Extent(13328.546, 306816.384, 278302.013, 619342.658, {
        wkid: 28992,
      }),
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
      var coords =
        'Longitude: ' +
        event.x +
        ' | Latitude: ' +
        event.y +
        ' | Scale 1:' +
        Math.round(mapView.scale * 1) / 1 +
        ' | Zoom ' +
        mapView.zoom +
        ' | EPSG: 28992'
      coordinatesWidget.innerHTML = coords
    }

    mapView.watch(['stationary'], function () {
      showCoordinates(mapView.center)
    })

    mapView.on(['pointer-down'], function (event) {
      showCoordinates(mapView.toMap({ x: event.x, y: event.y }))
    })
  }

  function addMap() {
    map.removeAll()

    var overlay = $('#overlay option:selected').val().trim()
    var year = $('#year option:selected').val().trim()

    var yearLayer = new TileLayer({
      url:
        'https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_' +
        year +
        '/MapServer',
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

    var year = $('#year option:selected').val().trim()
    const parameters = { year: year }
    const response = await fetch(
      '/urban_development/get_classified_tiles/' + JSON.stringify(parameters),
      { signal: abortController.signal }
    )

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

    var year = $('#year option:selected').val().trim()
    const parameters = { year: year }
    const response = await fetch(
      '/urban_development/get_classified_tiles/' + JSON.stringify(parameters),
      { signal: abortController.signal }
    )

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

  async function setupDataView() {
    $('#data').remove()
    var dataDiv = $("<div id='data'></div>")
    $('.page-container').append(dataDiv)

    let abortController = new AbortController()

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

    var year = $('#year option:selected').val().trim()
    const parameters = { year: year }
    const response = await fetch(
      '/urban_development/get_classified_tiles/' + JSON.stringify(parameters),
      { signal: abortController.signal }
    )

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
      $('#data').append("<span class='text-element data-element' id='public-space-tiles'>Tiles classified as not containing greenery: " + noGreenery + "</span><br>")
      $('#data').append("<span class='text-element data-element' id='public-space-tiles'>Tiles classified as containing greenery: " + greenery + "</span><br><br><br>")
      $('#data').append("<span class='text-element data-element' id='public-space-tiles'>Tiles classified as containing 0% - 25% greenery: " + quarter1 + "</span><br>")
      $('#data').append("<span class='text-element data-element' id='not-public-space-tiles'>Tiles classified as containing 25% - 50% greenery: " + quarter2 + "</span><br>")
      $('#data').append("<span class='text-element data-element' id='not-public-space-tiles'>Tiles classified as containing 50% - 75% greenery: " + quarter3 + "</span><br>")
      $('#data').append("<span class='text-element data-element' id='not-public-space-tiles'>Tiles classified as containing 75% - 100% greenery: " + quarter4 + "</span><br><br><br>")
      $('#data').append("<span class='text-element data-element id='user-tiles'>Tiles classified by user: " + classifiedByUser + "</span><br>")
      $('#data').append("<span class='text-element data-element' id='classifier-tiles'>Tiles classified by classifier: " + classifiedByClassifier + "</span><br>")
      $('#data').append("<span class='text-element data-element' id='training-data-tiles'>Tiles classified by training data: " + classifiedByTrainingData + "</span><br>")

      if (json['total'] > 0) {
        function setupSpan(id, value) {
          function roundToTwoDecimalPlaces(x) {
            return +(Math.round(x + 'e+2') + 'e-2')
          }

          if (value > 0) {
            const exact = (100 * value) / json['total']
            const rounded = roundToTwoDecimalPlaces(exact)
            $('#' + id).append(
              ' (' + (rounded == exact ? '=' : '≈') + rounded + '%)'
            )
          }
        }

        setupSpan('public-space-tiles', publicSpace)
        setupSpan('not-public-space-tiles', notPublicSpace)
        setupSpan('mixed-tiles', json['mixed'])
        setupSpan('user-tiles', user)
        setupSpan('classifier-tiles', classifier)
        setupSpan('training-data-tiles', trainingData)
        setupSpan('user-classifier-tiles', userClassifier)
        setupSpan('user-training-data-tiles', userTrainingData)
        setupSpan('classifier-training-data-tiles', classifierTrainingData)
        setupSpan(
          'user-classifier-training-data-tiles',
          json['user_classifier_training_data']
        )
      }
    } catch (exception) {
      alert('Error.')
    }
  }

  function updateUrl(nextView) {
    const url = window.location.href.replace(
      window.location.search,
      '?view=' + nextView
    )
    history.pushState({}, null, url)
  }

  map = new Map('map')

  $(document).ready(function () {
    // Grab query parameters, e.g. if a url is like ?view=map then we can get
    // the "view" value by running searchParams.get('view')
    var VIEW_TYPES = {
      map: 'map',
      data: 'data',
    }
    var searchParams = new URLSearchParams(window.location.search)
    // Will be either 'map`or 'data'
    var viewType = searchParams.get('view') || VIEW_TYPES.map
    // Depending on the view type in the url, we either load the map or the data view
    if (viewType === 'map') {
      addMap()
      setupMapView()
    } else {
      setupDataView()
    }

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
    $('#map-view-button').click(function (event) {
      if (viewType === VIEW_TYPES.map) return
      $('#map-view-button').prop('disabled', true)
      $('#data').remove()
      $('#overlay').val('None').change()
      $('#overlay-cell').show()
      $('#data-view-button').prop('disabled', false)
      var mapContainer = $('<div id="map-container"></div>')
      var mapDiv = $("<div id='map'></div>")
      map = new Map(mapDiv)
      mapContainer.append(map)
      $('.page-container').append(mapContainer)
      addMap()
      setupMapView(mapView)
      updateUrl('map')
      viewType = VIEW_TYPES.map
    })
    $('#data-view-button').click(function (event) {
      if (viewType === VIEW_TYPES.data) return
      $('#data-view-button').prop('disabled', true)
      $('#map-container').remove()
      $('#overlay-cell').hide()
      $('#map-view-button').prop('disabled', false)

      setupDataView()
      updateUrl('data')
      viewType = VIEW_TYPES.data
    })
  })
})

function setupClassifiedAsLayer(FeatureLayer) {
  var template = {
    title: 'Tile | EPSG: 4326',
    content:
      '<div>Coordinates: {Longitude}, {Latitude}<br>\
                        Contains greenery: {Contains greenery}<br>\
                        Greenery percentage: {Greenery percentage}%</div>',
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
    content:
      '<div>Coordinates: {Longitude}, {Latitude}<br>\
                        Classified by: {Classified by}',
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
