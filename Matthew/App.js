var data = {"nodes" : [{"id" : 6, "name" : "Awesome", "size" : 8}, 
{"id" : 4, "name" : "Epic", "size" : 800000}, 
{"id" : 1, "name" : "News", "size" : 80000000}, 
{"id" : 3, "name" : "Fantasy", "size" : 8000}, 
{"id" : 2, "name" : "Cool", "size" : 8000000},
{"id" : 5, "name" : "H", "size" : 7837234},
{"id" : 7, "name" : "Flipping Cool", "size" : 45},
{"id" : 8, "name" : "CoolBeans", "size" : 5643},
{"id" : 9, "name" : "GgGg", "size" : 98888}],
"links" : [{"source": 6, "target": 1, "similarity" : 10}, 
{"source": 3, "target": 1, "similarity" : 100}, 
{"source": 3, "target": 4, "similarity" : 40},
{"source": 9, "target": 2, "similarity" : 35},
{"source": 7, "target": 8, "similarity" : 74},
{"source": 3, "target": 5, "similarity" : 96},
{"source": 5, "target": 6, "similarity" : 56}]}

var svg = d3.select("#DataVis")
    .append("svg")
    .attr("width", 800)
    .attr("height", 800)
    .attr("transform", "translate(100, 100)")
    .style("border", "1px solid black")

// var tooltip = d3.select("#DataVis")
//     .append("div")					
//     .style("opacity", 0)
//     .attr("class", "tooltip");

var simulation = d3
    .forceSimulation(data.nodes)
    .force("link", d3.forceLink(data.links).id(function(d) { return d.id; }).distance(60))
    .force("charge", d3.forceManyBody().strength(-30))
    .force("center", d3.forceCenter(400, 400))
    .force("collide", d3.forceCollide().radius(20))
    .on("tick", ticked);

var showSims = function(d) {
    simValues
        .style("visibility", "visible")
}

var hideSims = function(d) {
    simValues
        .style("visibility", "hidden")
}

var showNodeNames = function(d) {
    d3.select(this)
      .style("stroke", "black")
      .style("opacity", 1)
    nodeNames
        .style("visibility", "visible")
}

var hideNodeNames = function(d) {
    d3.select(this)
      .style("stroke", "none")
      .style("opacity", 1)
    nodeNames
        .style("visibility", "hidden")
}

var nodeNames = svg.append('g')
    .selectAll('text')
    .data(data.nodes)
    .join('text')
      .text(d => d.name)
      .attr('font-size', 8)
      .attr("text-anchor", "middle")

var simValues = svg.append('g')
    .selectAll('line')
    .data(data.links)
    .join('text')
        .text(d => d.similarity/100)
        .attr('font-size', 8)
        .attr("font-weight", "bold")
        .attr("text-anchor", "middle")

var links = svg
    .append("g")
    .selectAll("line")
    .data(data.links)
    .enter()
    .append("line")
    .attr("stroke-width", 1)
    .style("stroke", "black")
    .style("stroke-linecap", "round")
    .style("opacity", function(d) {return d.similarity/100})
    .on("mouseover", showSims)
    .on("mouseleave", hideSims)

var nodes = svg
    .append("g")
    .selectAll("circle")
    .data(data.nodes)
    .enter()
    .append("circle")
    .attr("r", function(d) {return (Math.log(d.size))})
    .attr("fill", "#ADD8E6")
    .on("mouseover", showNodeNames)
    .on("mouseleave", hideNodeNames)
    .call(drag(simulation));

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
    
    nodeNames
        .attr("x", function(d) {
            return d.x
        })
        .attr("y", function(d) {
            return d.y + Math.log(d.size) + 10
        })
        .attr("visibility", "hidden")

    simValues
        .attr("x", function(d) {
            if (Math.abs(d.target.y - d.source.y) > 50) {
                return d.source.x + (d.target.x - d.source.x)/2 + 7;
            } 
            else {
                return d.source.x + (d.target.x - d.source.x)/2;
            }
        })
        .attr("y", function(d) {
            if (Math.abs(d.target.y - d.source.y) < 50) {
                return d.source.y + (d.target.y - d.source.y)/2 + 7;
            } 
            else {
                return d.source.y + (d.target.y - d.source.y)/2;
            }
        })
        .attr("visibility", "hidden")
}

function drag(simulation) {    
    function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
    }
    
    function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
    }
    
    function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
    }
    
    return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
  }
