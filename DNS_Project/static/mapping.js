var attribution = new ol.control.Attribution({
    collapsible: false
});

var map = new ol.Map({
    controls: ol.control.defaults({attribution: false}).extend([attribution]),
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM({
                attributions: [ ol.source.OSM.ATTRIBUTION, 'Tiles courtesy of <a href="https://geo6.be/">GEO-6</a>' ],
            })
        })
    ],
    target: 'map',
    view: new ol.View({
        center: ol.proj.fromLonLat([lon,lat]),
        maxZoom: 18,
        zoom: 12
    })
});

var layer = new ol.layer.Vector({
    source: new ol.source.Vector({
        features: [
            new ol.Feature({
                geometry: new ol.geom.Point(ol.proj.fromLonLat([lon,lat]))
            })
        ]
    })
});

map.addLayer(layer);

