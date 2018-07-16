accessToken = "pk.eyJ1IjoidGhlZXN0aW1hdG9yIiwiYSI6ImNqaWR2bHpqMzBmeG4za29udTc1ams2MHoifQ.OBMySdK6qhBjC3VAOCBinA"

// Mapbox API
var mapboxLight = `https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token=${accessToken}`;
var mapboxOutdoor = `https://api.mapbox.com/styles/v1/mapbox/outdoors-v9/tiles/256/{z}/{x}/{y}@2x?access_token=${accessToken}`



// Adding tile layer to the map
var lightLayer = L.tileLayer(mapboxLight);
var outdoorLayer = L.tileLayer(mapboxOutdoor)

// Creating map object
var myMap = L.map("map", {
  center: [37.78, -122.42],
  zoom: 13,
  layers: [lightLayer]

});

// read csv
var mapDataURL = ("/map_data")

// Grabbing the data with d3..
d3.json(mapDataURL, function(data) {
  console.log(data)
  

  
  
  // Creating a new marker cluster group
  var markers = L.markerClusterGroup();

  // Loop through our data...
  for (var i = 0; i < data.length; i++) {
    // set the data location property to a variable
    var latitude = data[i].Latitude;
    var longitude = data[i].Longitude;

    // If the data has a location property...
    if (latitude) {

      // Add a new marker to the cluster group and bind a pop-up
      markers.addLayer(L.marker([latitude, longitude])
        .bindPopup(`${data[i].Address}: ${data[i].Care_Taker}`));
    }

  }

  // Add our marker cluster layer to the map
  myMap.addLayer(markers);

});
var baseMaps = {
  Light: lightLayer,
  Outdoors: outdoorLayer
};

L.control.layers(baseMaps).addTo(myMap);