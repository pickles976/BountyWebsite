var L
// const bounds =[[-228,0],[-28,256]]

// MAPINFO
const bounds =[[-256,0],[11.82,288]]

let o={y:-128,x:128}
console.log('hi');

        var map = L.map('map',{    
            crs: L.CRS.Simple,
          maxBounds: [[-278,-50],[22,306]], 
        }).setView([o.y, o.x], 3);

        L.tileLayer('https://raw.githubusercontent.com/Kastow/Foxhole-Map-Tiles/master/Tiles/{z}/{z}_{x}_{y}.png', {
            maxZoom: 5,
            noWrap: true,
            zIndex:100,
            opacity:1,
            continuousWorld: true, /* so it doesn't repeat like a spherical map*/
        }).addTo(map);

  var imageUrl = 'https://cdn.glitch.com/dd3f06b2-b7d4-4ccc-8675-05897efc4bb5%2Fjjjjjj4.jpg?v=1560614235480',
  imageBounds = [[-256, -100], [0, 356]];

var popup = L.popup();
function onMapClick(e) {
    var currentZoom = map.getZoom();
    popup
        .setLatLng(e.latlng)
        .setContent('Zoom is '+currentZoom.toString()+', '+e.latlng.toString())
        .openOn(map);
}

map.on('click', onMapClick);