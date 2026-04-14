// Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Based on:
//   https://www.d3-graph-gallery.com/graph/network_basic.html
//   https://bl.ocks.org/steveharoz/8c3e2524079a8c440df60c1ab72b5d03
//   https://www.d3indepth.com/zoom-and-pan/

// Pan & Zoom does not work; to be reviewed
//<button onclick="zoomIn()">Zoom in</button>
//<button onclick="zoomOut()">Zoom out</button>
//<button onclick="resetZoom()">Reset zoom</button>
//<button onclick="panLeft()">Pan left</button>
//<button onclick="panRight()">Pan right</button>
//<button onclick="center()">Center</button>

// set the dimensions and margins of the graph
const margin = {top: 5, right: 5, bottom: 5, left: 5};

const icon_width  = 40;
const icon_height = 40;

width = 1400 - margin.left - margin.right;
height = 800 - margin.top - margin.bottom;

//function handleZoom(e) {
//    console.dir(e);
//    d3.select('svg g').attr('transform', e.transform);
//}
//let zoom = d3.zoom().scaleExtent([0.01, 10]).translateExtent([[0, 0], [width, height]]).on('zoom', handleZoom);

// append the svg object to the body of the page
const svg = d3.select('#topology')
    .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        //.call(zoom)
    .append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`)
        ;

// svg objects
var link, node, optical_link, labels;

// values for all forces
forceProperties = {
    center: {x: 0.5, y: 0.5},
    charge: {enabled: true, strength: -500, distanceMin: 10, distanceMax: 2000},
    collide: {enabled: true, strength: 0.7, iterations: 1, radius: 5},
    forceX: {enabled: false, strength: 0.1, x: 0.5},
    forceY: {enabled: false, strength: 0.1, y: 0.5},
    link: {enabled: true, distance: 100, iterations: 1}
}

/**************** FORCE SIMULATION *****************/

var simulation = d3.forceSimulation();

// load the data
d3.json("{{ url_for('main.topology') }}", function(data) {
    // set the data and properties of link lines and node circles
    link = svg.append("g").attr("class", "links")//.style('stroke', '#aaa')
        .selectAll("line")
        .data(data.links)
        .enter()
        .append("line")
        .attr("opacity", 1)
        .attr("stroke", function(l) {
            return l.name.toLowerCase().includes('mgmt') ? '#AAAAAA' : '#555555';
        })
        .attr("stroke-width", function(l) {
            return l.name.toLowerCase().includes('mgmt') ? 1 : 2;
        })
        .attr("stroke-dasharray", function(l) {
            return l.name.toLowerCase().includes('mgmt') ? "5,5" : "0";
        });

    optical_link = svg.append("g").attr("class", "links")//.style('stroke', '#aaa')
        .selectAll("line")
        .data(data.optical_links)
        .enter()
        .append("line")
        .attr("opacity", 1)
        .attr("stroke", function(l) {
            return l.name.toLowerCase().includes('mgmt') ? '#AAAAAA' : '#555555';
        })
        .attr("stroke-width", function(l) {
            return l.name.toLowerCase().includes('mgmt') ? 1 : 2;
        })
        .attr("stroke-dasharray", function(l) {
            return l.name.toLowerCase().includes('mgmt') ? "5,5" : "0";
        });

    node = svg.append("g").attr("class", "devices").attr('r', 20).style('fill', '#69b3a2')
        .selectAll("circle")
        .data(data.devices)
        .enter()
        .append("image")
        .attr('xlink:href', function(d) {
            return "{{ url_for('static', filename='/topology_icons/') }}" + d.type + ".png";
        })
        .attr('width',  icon_width)
        .attr('height', icon_height)
        .call(d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended));

    // node tooltip
    //node.append("title").text(function(n) { return n.name; });
    // persistent node labels
    labels = svg.append("g").attr("class", "labels")
        .selectAll("text")
        .data(data.devices)
        .enter()
        .append("text")
        .text(function(d) { return d.name; })
        .attr("font-family", "sans-serif")
        .attr("font-size", 12)
        .attr("text-anchor", "middle")
        .attr("pointer-events", "none");
    // link tooltip
    link.append("title").text(function(l) { return l.name; });
    // optical link tooltip
    optical_link.append("title").text(function(l) { return l.name; });

    // link style
    //link
    //    .attr("stroke-width", forceProperties.link.enabled ? 2 : 1)
    //    .attr("opacity", forceProperties.link.enabled ? 1 : 0);
    
    // set up the simulation and event to update locations after each tick
    simulation.nodes(data.devices);

    // add forces, associate each with a name, and set their properties
    // Experimental : Optical link part 
    all_links = data.links.concat(data.optical_links)
    simulation
        .force("link", d3.forceLink()
            .id(function(d) {return d.id;})
            .distance(forceProperties.link.distance)
            .iterations(forceProperties.link.iterations)
            .links(
                forceProperties.link.enabled ? (
                    (all_links.length > 0) ? all_links : []
                ) : []
            )
        )

        .force("charge", d3.forceManyBody()
            .strength(forceProperties.charge.strength * forceProperties.charge.enabled)
            .distanceMin(forceProperties.charge.distanceMin)
            .distanceMax(forceProperties.charge.distanceMax))
        .force("collide", d3.forceCollide()
            .strength(forceProperties.collide.strength * forceProperties.collide.enabled)
            .radius(forceProperties.collide.radius)
            .iterations(forceProperties.collide.iterations))
        .force("center", d3.forceCenter()
            .x(width * forceProperties.center.x)
            .y(height * forceProperties.center.y))
        .force("forceX", d3.forceX()
            .strength(forceProperties.forceX.strength * forceProperties.forceX.enabled)
            .x(width * forceProperties.forceX.x))
        .force("forceY", d3.forceY()
            .strength(forceProperties.forceY.strength * forceProperties.forceY.enabled)
            .y(height * forceProperties.forceY.y));
    
    // after each simulation tick, update the display positions
    simulation.on("tick", ticked);
});

// update the display positions
function ticked() {
    link
        .attr('x1', function(d) { return d.source.x; })
        .attr('y1', function(d) { return d.source.y; })
        .attr('x2', function(d) { return d.target.x; })
        .attr('y2', function(d) { return d.target.y; });

    optical_link
        .attr('x1', function(d) { return d.source.x; })
        .attr('y1', function(d) { return d.source.y; })
        .attr('x2', function(d) { return d.target.x; })
        .attr('y2', function(d) { return d.target.y; });

    node
        .attr('x', function(d) { return d.x-icon_width/2; })
        .attr('y', function(d) { return d.y-icon_height/2; });
    if (labels) {
        labels
            .attr('x', function(d) { return d.x; })
            .attr('y', function(d) { return d.y + icon_height/2 + 12; });
    }
}

/******************** UI EVENTS ********************/

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0.0001);
    d.fx = null;
    d.fy = null;
}

// update size-related forces
d3.select(window).on("resize", function(){
    width = +svg.node().getBoundingClientRect().width;
    height = +svg.node().getBoundingClientRect().height;
    simulation.alpha(1).restart();
});

///******************** UI ACTIONS *******************/
//
//function resetZoom() {
//    d3.select('svg').transition().call(zoom.scaleTo, 1.0);
//}
//function zoomIn()    {
//    d3.select('svg').transition().call(zoom.scaleBy, 2.0);
//}
//function zoomOut()   {
//    d3.select('svg').transition().call(zoom.scaleBy, 0.5);
//}
//
//function center()    {
//    d3.select('svg').transition().call(zoom.translateTo, 0.5 * width, 0.5 * height);
//}
//function panLeft()   {
//    d3.select('svg').transition().call(zoom.translateBy, -50, 0);
//}
//function panRight()  {
//    d3.select('svg').transition().call(zoom.translateBy,  50, 0);
//}
