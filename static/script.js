var map = L.map('map').setView([15.814709, 74.488014], 16);
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);
var marker = L.marker([15.81459, 74.488163]).addTo(map);
var circle1 = L.circle([15.81229, 74.488014], {
            color: 'red',
            fillColor: '#f03',
            fillOpacity: 0.5,
            radius: 500
            }).addTo(map);
var circle2 = L.circle([15.847579, 74.532986], {
            color: 'red',
            fillColor: '#00ff0055',
            fillOpacity: 0.5,
            radius: 500
            }).addTo(map);
            
circle1.bindPopup("Safe Zone")
circle2.bindPopup("Safe Zone")
marker.bindPopup("You are here")

var popup = L.popup();

function onMapClick(e) {
    popup
    .setLatLng(e.latlng)
    .setContent("You clicked the map at " + e.latlng.toString())
    .openOn(map);
}
            
map.on('click', onMapClick);