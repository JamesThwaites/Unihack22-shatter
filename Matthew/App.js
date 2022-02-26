var data = {"nodes" : [{"id" : 1, "name" : "News"}, {"id" : 3, "name" : "Fantasy"}, {"id" : 4, "name" : "Cool"}],
            "links" : [{"source": 4, "target": 1, "similarity" : 40}, {"source": 3, "target": 1, "similarity" : 40}, {"source": 3, "target": 4, "similarity" : 40}]}

var svg = d3.select("#DataVis")
    .append("svg")
    .attr("width", 500)
    .attr("height", 500)
    .attr("transform", "translate(100, 100)")
    .style("border", "1px solid black")

var simulation = d3
    .forceSimulation(data.nodes)
    .force("link", d3.forceLink(data.links).id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody().strength(-30))
    .force("center", d3.forceCenter(250, 250))
    .on("tick", ticked);

var links = svg
    .append("g")
    .selectAll("line")
    .data(data.links)
    .enter()
    .append("line")
    .attr("stroke-width", 1)
    .style("stroke", "grey")
    .style("stroke-linecap", "round")

var nodes = svg
    .append("g")
    .selectAll("circle")
    .data(data.nodes)
    .enter()
    .append("circle")
    .attr("r", 8)
    .attr("fill", "black")

function ticked() {
    nodes
        .attr("cx", function(d) {
            return d.x;
        })
        .attr("cy", function(d) {
            return d.y;
        })
    
    links
        .attr("x1", function(d) {
            return d.source.x;
        })
        .attr("y1", function(d) {
            return d.source.y;
        })
        .attr("x2", function(d) {
            return d.target.x;
        })
        .attr("y2", function(d) {
            return d.target.y;
        })
    }