function Matrix(data, options) {

	var paths = options.paths,
        margin = options.margin,
	    width = options.width,
	    height = options.height,
	    container = options.container,
	    showLabels = options.show_labels,
	    startColor = options.start_color,
	    endColor = options.end_color,
        highlightCellOnActive = options.highlight_cell_on_active,
        highlightCellColor = options.highlight_cell_color;

	var dataValues = data['values'];
	var dataLabels = data['labels'];

	if(!dataValues){
		throw new Error('data is empty');
	}

	if(!Array.isArray(dataValues) || !dataValues.length || !Array.isArray(dataValues[0])){
		throw new Error('2-D array expected');
	}

    var maxValue = d3.max(dataValues, function(layer) { return d3.max(layer, function(d) { return d; }); });
    var minValue = d3.min(dataValues, function(layer) { return d3.min(layer, function(d) { return d; }); });

	var numrows = dataValues.length;
	var numcols = dataValues[0].length;

	var svg = d3.select(container).append("g") //from svg to g
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
		.append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	var background = svg.append("rect")
        .attr("data-ignore",true)
	    .style("stroke", "black")
	    .style("stroke-width", "2px")
	    .attr("width", width)
	    .attr("height", height);

	var x = d3.scale.ordinal()
	    .domain(d3.range(numcols))
	    .rangeBands([0, width]);

	var y = d3.scale.ordinal()
	    .domain(d3.range(numrows))
	    .rangeBands([0, height]);

	var colorMap = d3.scale.linear()
	    .domain([minValue,maxValue])
	    .range([startColor, endColor]);

	var row = svg.selectAll(".row")
	    .data(dataValues)
	  	.enter().append("g")
	    .attr("class", "row")
	    .attr("transform", function(d, i) { return "translate(0," + y(i) + ")"; });

	var cell = row.selectAll(".cell")
	    .data(function(d) { return d; })
		.enter().append("g")
	    .attr("class", "cell")
        .attr("stroke-width", 2)
        .attr("stroke", "#ff6969")
        .attr("fill", "none")
	    .attr("transform", function(d, i) { return "translate(" + x(i) + ", 0)"; });

	cell.append('rect')
        .attr("data-ignore",true)
	    .attr("width", x.rangeBand())
	    .attr("height", y.rangeBand())
	    .style("stroke-width", 0);

    cell.append("text")
	    .attr("dy", ".32em")
        .attr("stroke-width", 0)
	    .attr("x", x.rangeBand() / 2)
	    .attr("y", y.rangeBand() / 2)
	    .attr("text-anchor", "middle")
	    .style("fill", function(d, i) { return d >= maxValue/2 ? 'white' : 'black'; })
	    .text(function(d, i) { return d; });
    
    
    if(paths)
    {
        //console.log(paths[0].matrix.c - numcols + 1);
        for(var y_shift = 0; y_shift < paths[0].matrix.r - numrows + 1; y_shift++)
            for (var x_shift = 0; x_shift < paths[0].matrix.c - numcols + 1; x_shift++)
            {
                var mask = cell.append("g")
                    .attr("class", "f_"+x_shift+"_"+y_shift); /**/
                
                createPath(mask, paths, x, y, margin, x_shift, y_shift);
            }
        
    }
    
	row.selectAll(".cell")
	    .data(function(d, i) { return dataValues[i]; })
	    .style("fill", colorMap);

    if(highlightCellOnActive){
        cell
        .on("mouseover", function(d) {
            d3.select(this).style("fill", highlightCellColor);
        })
        .on("mouseout", function() {
            d3.select(this).style("fill", colorMap);
        });
    }

    if (showLabels){
        var labels = svg.append('g')
            .attr('class', "labels");

        var columnLabels = labels.selectAll(".column-label")
            .data(dataLabels)
            .enter().append("g")
            .attr("class", "column-label")
            .attr("transform", function(d, i) { return "translate(" + x(i) + "," + height + ")"; });

        columnLabels.append("line")
            .style("stroke", "black")
            .style("stroke-width", "1px")
            .attr("x1", x.rangeBand() / 2)
            .attr("x2", x.rangeBand() / 2)
            .attr("y1", 0)
            .attr("y2", 5);

        columnLabels.append("text")
            .attr("x", 0)
            .attr("dx", "-0.82em")
            .attr("y", y.rangeBand() / 2)
            .attr("dy", ".41em")
            .attr("text-anchor", "end")
            .attr("transform", "rotate(-90)")
            .text(function(d, i) { return d; });

        var rowLabels = labels.selectAll(".row-label")
            .data(dataLabels)
            .enter().append("g")
            .attr("class", "row-label")
            .attr("transform", function(d, i) { return "translate(" + 0 + "," + y(i) + ")"; });

        rowLabels.append("line")
            .style("stroke", "black")
            .style("stroke-width", "1px")
            .attr("x1", 0)
            .attr("x2", -5)
            .attr("y1", y.rangeBand() / 2)
            .attr("y2", y.rangeBand() / 2);

        rowLabels.append("text")
            .attr("x", -8)
            .attr("y", y.rangeBand() / 2)
            .attr("dy", ".32em")
            .attr("text-anchor", "end")
            .text(function(d, i) { return d; });
    }
    var exitConds =
    {
        x: x,
        y: y,
        w : width + margin.left + margin.right,
        h : height,
        r : numrows,
        c : numcols,
        svg: svg
    };
    return exitConds;
}

function createPath(cellMask, paths, x, y, margin, x_shift, y_shift)
{
    
    //type: "oneToOne
    cellMask.append("line")
        .attr("x1", x.rangeBand()/2)
        .attr("y1", y.rangeBand()/2)
        .attr("x2", function(d, i) { return ( (i+.5+x_shift)*paths[0].matrix.x.rangeBand() - paths[0].matrix.w - x(i));})
        .attr("y2", function(d, i) { return ( (i+1.5+y_shift)*paths[0].matrix.y.rangeBand() - paths[0].matrix.h - y(i) );});
}

