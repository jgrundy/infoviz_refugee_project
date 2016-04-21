var width = 1060,
    height = 650,
    x = 0,
    y = 0;
    
// create a color map
colorMap = d3.scale.category10();

//set the map projection
var projection = d3.geo.kavrayskiy7()
    .scale(170)
    .translate([width / 2, height / 2])
    .precision(.1);

//set the geometric pathway    
var path = d3.geo.path()
    .projection(projection);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json("world-110m.json", function(error, world) {
  if (error) throw error;

  var countries = topojson.feature(world, world.objects.countries).features,
      neighbors = topojson.neighbors(world.objects.countries.geometries);

    //radius for circle size
//    radiusMap = d3.scale.linear()
//        .domain([0,5000])
//        .range([0,70])
    
    //create circles
    dorling = d3.select('svg').selectAll('circle').data(countries).enter()
        .append('circle')
        .each(function(it) {
        it.properties.r = 18;
        it.properties.c = path.centroid(it);
        it.properties.x = x;
        it.properties.y = y;
    })
        .attr('cx', function(it) {return it.properties.x + it.properties.c[0] - x;})
        .attr('cy', function(it) {return it.properties.y + it.properties.c[1] - y;})
        .attr('r', function(it) {return it.properties.r;})
        .attr('fill', function(it) {return colorMap(10);})
    
    // prepare data for force layout
    forceNodes = [];
    for(i = 0; i < countries.features ; i++ ) {
        forceNodes.push(countries.features[i].properties);
    }
    // force layout, makes circles closer.
    // This is useful when circle radius changes.
    force = d3.layout.force().gravity(3.0).size([800,600]).charge(-1).nodes(forceNodes);
    
    // collision detection, prevents circles from overlapping each other
    force.on("tick", function() {
    for(i = 0 ; i < countries.features.length ; i++) {
    for(j = 0 ; j < countries.features.length ; j++) { it = countries.features[i].properties; 
      jt = countries.features[j].properties; if(i==j) continue; // not collide with self r = 
      it.r + jt.r; // it.c is the centroid of each county and initial position of circle 
      itx = it.x + it.c[0]; ity = it.y + it.c[1]; jtx = jt.x + jt.c[0]; jty = jt.y + 
      jt.c[1]; 
      // distance between centroid of two circles d = Math.sqrt( (itx - jtx) * (itx - jtx) 
      + (ity - jty) * (ity - jty) }; if(r > d) { 
         // there's a collision if distance is smaller than radius
            dr = ( r - d ) / ( d * 1 );
            it.x = it.x + ( itx - jtx ) * dr;
            it.y = it.y + ( ity - jty ) * dr;
    }}})
});
