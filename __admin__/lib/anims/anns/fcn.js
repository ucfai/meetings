// Neural network initialization
var layers = new Map();
layers.set("inp", [3]);
layers.set("hid", [4, 4]);
layers.set("out", [2]);

var nn_attrs = {};
nn_attrs.w = 1366;
nn_attrs.h =  768;

var node_attrs = Object();
node_attrs.w = 64;
node_attrs.h = 64;
node_attrs.offx = node_attrs.w * 3;
node_attrs.offy = node_attrs.h * 2;

var nn = d3.select("body").append("svg")
    .attr("width",  nn_attrs.w)
    .attr("height", nn_attrs.h)
    .attr("id", "nn");

// var len_layers = 2 + layers.get("hid").length;

function layerG(id, size, l_cnt) {
    [...Array(size).keys()].forEach(function (idx) {
        node_r(layer, id.substr(0, 3), idx);
    });
}

function node_r(parent, label, idx) {
    var cls;
    switch (label) {
        case "inp": cls = "node_inp"; break;
        case "hid": cls = "node_hid"; break;
        case "out": cls = "node_out"; break;
    }
    parent.append("rect").attr("class", cls)
        .attr("x", 0).attr("y", node_attrs.offy * idx)
        .attr("width", node_attrs.w).attr("height", node_attrs.h)
        .attr("rx", Math.sqrt(node_attrs.w));
};

function layer_gen(layers) {
    var l = [];
    for (key of layers.keys()) {
        for (val of layers.get(key)) {
            var lyr = Object();
            lyr.name = `${key}${l.length}`;
            lyr.x = node_attrs.offx * (l.length + 1);
            lyr.y = node_attrs.offy * 0;
            lyr.units = [...Array(val).keys()];
            l.push(lyr)
        };
    };
    
    return l;
}

function nodes_gen(layers) {
    var n = [];
    for (key of layers.keys()) {
        n.push(layers[key].units);
    };
    return n;
}

var layers = layer_gen(layers);

var ffwd_net = nn.selectAll("g").data(layers).enter().append("g");
    ffwd_net.attr("class", "nn-layer")
            .attr("id", (d) => d.name)
            .attr("transform", (d) => `translate(${d.x},${d.y})`);

var nodes = nodes_gen(layers);
var nn_layers = ffwd_net.selectAll("rect").data(nodes).enter().append("rect");
// network.each(function (net, idx) {
//     var cls = `node_${net.name.substr(0, 3)}`;
//     d3.select(this).data(net.units).enter().append("rect")
//         .attr("class", cls).attr("x", 0).attr("y", function(d) { return node_attrs.offy * d; })
//         .attr("width", node_attrs.w).attr("height", node_attrs.h)
//         .attr("rx", Math.sqrt(node_attrs.w))
// });

// layers.forEach(function (i) {
//     var cls = `node_${i.name.substr(0, 3)}`;
//     d3.selectAll(`#${i.name}`).datum(i.units)
//         .append("rect").attr("class", cls)
//         .attr("x", 0).attr("y", function(d) { return node_attrs.offy * d })
//         .attr("width", node_attrs.w).attr("height", node_attrs.h)
//         .attr("rx", Math.sqrt(node_attrs.w));
// });

// var l_cnt = 0;
// // Input layer
// node_g("inpt", layers.get("inp"), l_cnt++);

// // Hidden layer
// if (layers.get("hid").length > 0) {
//     layers.get("hid").forEach(function (size) {
//         node_g(`hid${l_cnt}`, size, l_cnt++);
//     });
// } else {
//     var warn = "You must have at least one hidden layer!"
//     alert(warn)
//     throw Error(warn)
// };

// // Output layer
// node_g(`outp`, layers.get("out"), l_cnt++);