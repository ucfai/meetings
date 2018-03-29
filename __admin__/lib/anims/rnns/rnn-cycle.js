var bodySel = d3.select("body");

var svgSel = bodySel.append("svg")
    .attr("width", 50)
    .attr("height", 50);

var nn_io = {
    "width": 65,
    "height": 65,
    "stroke-width": 2,
}

function nnIO (label) {
    return 
}

var io = d3.symbolSquare()

var sqSel = svgSel.append("rect")
    .attr("x", 0) // center, on x-axis
    .attr("y", 0) // center, on y-axis
    .attr("width", 50)  // radius
    .attr("height", 50)  // radius
    .attr("rx", 10)
    .style("fill", "purple");