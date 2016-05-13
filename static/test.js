
var width = 960,
    height = 500;

d3.select("#sex_select").on("input", draw_users);
d3.select("#class_select").on("input", draw_users);

var zoom = d3.behavior.zoom()
             .translate([0, 0])
             .scale(1)
             .scaleExtent([1, 6])
             .on("zoom", zoomed);
// set projection 
var projection = d3.geo.mercator()
                   .scale(800)
                   .center([-94, 37]);
var path = d3.geo.path()
             .projection(projection);
    
// prepare canvas 
var svg = d3.select("body").append("svg")
    .attr({ "width": width,
            "height": height,
            "class": "overlay"})
    .call(zoom);

var g = svg.append("g");

var URL_BASE = '/db?';

function update_url(){
    return URL_BASE + 
        'sex=' + document.getElementById("sex_select").value +
        '&class=' + document.getElementById("class_select").value;
}

var us;    // trick from Scott Murray
d3.json('/static/us-states.json', function(error, data){
    if (error) throw error;
    us = data.features;
    g.append('g')
     .attr('class', 'states')
     .selectAll('path')
     .data(us)
     .enter()
     .append('path')
     .attr("d", path); 

    g.append('g')
     .attr('class', 'states-name')
     .selectAll("text")
     .data(us)
     .enter()
     .append("svg:text")
     .text(function(d){
             return d.properties.name;
             })
     .attr("x", function(d){
             return path.centroid(d)[0];
             })
     .attr("y", function(d){
             return  path.centroid(d)[1];
             })
     .attr("text-anchor","middle")
     .attr('fill', 'black');
     // first update
     draw_users();
});

var key = function(d){ return d.id };

function draw_users(){
    url = update_url();

    d3.csv(url, function(error, users){
      if (error) throw error;
      users.forEach(function(d){
            d.latitude = +d.latitude;
            d.longitude= +d.longitude;
        });
      g.selectAll('circle')
           .data(users, key).exit()
           .remove();
      g.selectAll('circle')
       .data(users, key).enter()
       .append('circle')
       .attr('cx', function(d){
         return projection([d['longitude'],d['latitude']])[0] })
       .attr('cy', function(d){
         return projection([d['longitude'],d['latitude']])[1] })
       .attr('r','3px')
       .on('mouseover',function(d){
            svg.append('text').attr({'id':'tooltip',
                                   'fill':'black'})
                              .attr('x', d3.event.pageX+5)
                              .attr('y', d3.event.pageY-110)
                              .text(d.id+', '+d.city)
          })
       .on('mouseout', function(){
           d3.select('#tooltip').remove();
       });

      d3.select('#count')
        .text(users.length);
      });
}

function zoomed() {
  g.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
  g.select(".state-border").style("stroke-width", 1.5 / d3.event.scale + "px");
}

