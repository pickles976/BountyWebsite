var L
const bounds =[[-228,0],[-28,256]]
let o={y:-128,x:128}
console.log('hi');

        var map = L.map('map',{    
            crs: L.CRS.Simple,
          maxBounds: [[-278,-50],[22,306]], 
        }).setView([o.y, o.x], 0);
  //map.createPane('tiles');
//map.getPane('tiles').style.zIndex = 500;
        L.tileLayer('https://raw.githubusercontent.com/Kastow/Foxhole-Map-Tiles/master/Tiles/{z}/{z}_{x}_{y}.png', {
            attribution: 'Clapfoot, Kastow, Blade, Derp',
            //bounds:[[-100,-100],[200,200]],
            maxZoom: 5,
            noWrap: true,
            zIndex:100,
            opacity:1,
            //pane: 'tiles',
            continuousWorld: true, /* so it doesn't repeat like a spherical map*/
            //id: 'mapbox.streets',
           // maxBounds: L.latLngBounds(L.latLng(-100, -100), L.latLng(100,100)) /* for reference */
        }).addTo(map);

  var imageUrl = 'https://cdn.glitch.com/dd3f06b2-b7d4-4ccc-8675-05897efc4bb5%2Fjjjjjj4.jpg?v=1560614235480',
  imageBounds = [[-256, -100], [0, 356]];
//L.imageOverlay(imageUrl, imageBounds,{zIndex:-10}).addTo(map);
var popup = L.popup();
function onMapClick(e) {
    var currentZoom = map.getZoom();
    popup
        .setLatLng(e.latlng)
        .setContent('Zoom is '+currentZoom.toString()+', '+e.latlng.toString())
        .openOn(map);
}

map.on('click', onMapClick);
let height =bounds[1][0]-bounds[0][0];
let width=bounds[1][1]-bounds[0][1];
let w = width/5.5
let k = w*Math.sqrt(3)/2
var marker = L.marker([o.y, o.x]).addTo(map);
let array=[
[o.y-k,o.x], //Umbral Wildwood
[o.y-2*k,o.x], //Great March
[o.y+k,o.x],//Callahan's Passage
[o.y+2*k,o.x],//Reaching Trail
  
[o.y-0.5*k,o.x-0.75*w],//Loch Mor
[o.y-1.5*k,o.x-0.75*w],//The Heartlands
[o.y+0.5*k,o.x-0.75*w],//The Linn of Mercy
[o.y+1.5*k,o.x-0.75*w],//The Moors

[o.y-0.5*k,o.x+0.75*w],//The Drowned Vale
[o.y-1.5*k,o.x+0.75*w],//Shackled Chasm
[o.y+0.5*k,o.x+0.75*w],//Marban Hollow
[o.y+1.5*k,o.x+0.75*w],//Viper Pit

[o.y,o.x-1.5*w],//Farranac Coast
[o.y-k,o.x-1.5*w],//Westgate
[o.y+k,o.x-1.5*w],//Stonecradle

[o.y,o.x+1.5*w],//Endless Shore
[o.y-k,o.x+1.5*w],//Allod's Bight
[o.y+k,o.x+1.5*w],//Weathered Expanse
  
[o.y+0.5*k,o.x-2.25*w],//The Oarbreaker Isles
[o.y-0.5*k,o.x-2.25*w],//Fisherman's Row

[o.y+0.5*k,o.x+2.25*w],//Godcrofts
[o.y-0.5*k,o.x+2.25*w]//Tempest Island
]
console.log(array)
for(var i=0;i<array.length;i++){
  let item = array[i]
  //var marker2 = L.marker(item).addTo(map);
  var polygon = L.polygon([
    [item[0],item[1]-w/2],
    [item[0]+k/2,item[1]-w/4],
    [item[0]+k/2,item[1]+w/4],
    [item[0],item[1]+w/2],
    [item[0]-k/2,item[1]+w/4],
    [item[0]-k/2,item[1]-w/4],
],{
    color: 'blue',
    fillColor: 'blue',
    fillOpacity: 0,
}).addTo(map);
//L.rectangle([[item[0]-k/2,item[1]-w/2],[item[0]+k/2,item[1]+w/2]],{color: "red", fillOpacity:0}).addTo(map);
/*L.circle(item, {
    color: 'yellow',
    fillColor: 'yellow',
    fillOpacity: 0,
    radius: w/2
}).addTo(map);*/
}
///Map IDs
let mapArray=[
  {name:'',center:[]},//0
  {name:'',center:[]},//1
  {name:'',center:[]},//2
  {name:'DeadLandsHex',center:[o.y,o.x]},//3
  {name:'CallahansPassageHex',center:[o.y+k,o.x]},//4
  {name:'MarbanHollow',center:[o.y+0.5*k,o.x+0.75*w]},//5
  {name:'UmbralWildwoodHex',center:[o.y-k,o.x]},//6
  {name:'MooringCountyHex',center:[o.y+1.5*k,o.x-0.75*w]},//7
  {name:'HeartlandsHex',center:[o.y-1.5*k,o.x-0.75*w]},//8
  {name:'LochMorHex',center:[o.y-0.5*k,o.x-0.75*w]},//9
  {name:'LinnMercyHex',center:[o.y+0.5*k,o.x-0.75*w]},//10
  {name:'ReachingTrailHex',center:[o.y+2*k,o.x]},//11
  {name:'StonecradleHex',center:[o.y+k,o.x-1.5*w]},//12
  {name:'FarranacCoastHex',center:[o.y,o.x-1.5*w]},//13
  {name:'WestgateHex',center:[o.y-k,o.x-1.5*w]},//14
  {name:'FishermansRowHex',center:[o.y-0.5*k,o.x-2.25*w]},//15
  {name:'OarbreakerHex',center:[o.y+0.5*k,o.x-2.25*w]},//16
  {name:'GreatMarchHex',center:[o.y-2*k,o.x]},//17
  {name:'TempestIslandHex',center:[o.y-0.5*k,o.x+2.25*w]},//18
  {name:'GodcroftsHex',center:[o.y+0.5*k,o.x+2.25*w]},//19
  {name:'EndlessShoreHex',center:[o.y,o.x+1.5*w]},//20
  {name:'AllodsBightHex',center:[o.y-k,o.x+1.5*w]},//21
  {name:'WeatheredExpanseHex',center:[o.y+k,o.x+1.5*w]},//22
  {name:'DrownedValeHex',center:[o.y-0.5*k,o.x+0.75*w]},//23
  {name:'ShackledChasmHex',center:[o.y-1.5*k,o.x+0.75*w]},//24
  {name:'ViperPitHex',center:[o.y+1.5*k,o.x+0.75*w]},//25
]

