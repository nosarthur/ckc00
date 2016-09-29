
var width = 960,
    height = 500;

d3.select("#sex_select").on("input", draw_users);
d3.select("#class_select").on("input", draw_users);

function search(e){
    var code = (e.keyCode ? e.keyCode : e.which);
    if(code == 13) { //Enter keycode
        var name = document.getElementById("name").value;
        name = name.toLowerCase()
                   .split(' ')
                   .map(function(word) {
                       return word[0].toUpperCase() + word.substr(1); })
                   .join(' ');
        if (name){
          draw_from_url( '/db?name=' + name);
        }
        else{
          draw_from_url(URL_BASE+'sex=all&class_type=all');
        }
    }
}

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
var svg = d3.select("#map").append("svg")
    .attr({ "width": width,
            "height": height,
            "class": "overlay"})
    .call(zoom);

var g = svg.append("g");

var URL_BASE = '/db?';

function update_url(){
    return URL_BASE + 
        'sex=' + document.getElementById("sex_select").value +
        '&class_type=' + document.getElementById("class_select").value;
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

     // first update
     draw_users();
});

var key = function(d){ return d.id }; // state-id

function draw_users(){
    url = update_url();
    draw_from_url(url);
}

function draw_from_url(url){
    d3.csv(url, function(error, users){
      if (error) throw error;
      var activeState = new Set();
      var state2update = []
      for (var i=0;i<users.length;i++){
          activeState.add(users[i].state);
      }
      for (var i=0;i<us.length;i++){
          if (activeState.has(us[i].properties.name)) {
              state2update.push({'id':us[i].properties.name, 
                        's':us[i]});
          }
      }
      g.selectAll("text")
       .data(state2update, key).exit().remove()
      g.selectAll("text")
       .attr('class', 'states-name')
       .data(state2update, key)
       .enter()
       .append("svg:text")
       .text(function(d){
             return d.s.properties.name;
             })
       .attr("x", function(d){
             return path.centroid(d.s)[0];
             })
       .attr("y", function(d){
             return  path.centroid(d.s)[1];
             })
       .attr("text-anchor","middle")
       .attr("font-size","16px")
       .attr('fill', 'black');

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
                                    'font-size':'16px',
                                   'fill':'black'})
                              .attr('x', d3.event.pageX-80)
                              .attr('y', d3.event.pageY-110)
                              .text(d.display_name+', '+d.city)
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

