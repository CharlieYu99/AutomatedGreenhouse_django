var width = 500;
var height = 300;
var padding = { top: 50, right: 50, bottom: 50, left: 50 };

function appendGraph_24h(type, data){
    var svg = d3.select(type)				
    .append("svg") 
    .attr("width", width)
    .attr("height", height);


    var dataArray = data;
    var min = d3.min(dataArray, function(d) {
        return d[1];
    })
    var max = d3.max(dataArray, function(d) {
        return d[1];
    })

    var xScale = d3.scaleLinear()
                .domain([24, 0])
                .range([0, width - padding.left - padding.right]);
    if (type == "Temperature" || type == "Humidity"){
        var yScale = d3.scaleLinear()
                    .domain([min-5, max+5])
                    .range([height - padding.top - padding.bottom, 0]);
    }else{
        var yScale = d3.scaleLinear()
                    .domain([Math.floor(min*0.75), Math.ceil(max*1.25)])
                    .range([height - padding.top - padding.bottom, 0]);
    }



    // graph frame work
    var xAxis = d3.axisBottom()
                .scale(xScale);
    var yAxis = d3.axisLeft()
                .scale(yScale);

    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(' + padding.left + ',' + (height - padding.bottom) + ')')
        .call(xAxis);
    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
        .call(yAxis);

    //line 
    var linePath = d3.line()
                    .x(function(d){ return xScale(d[0]) })
                    .y(function(d){ return yScale(d[1]) });

    svg.append('g')
        .append('path')
        .attr('class', 'line-path')
        .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
        .attr('d', linePath(dataArray))
        .attr('fill', 'none')
        .attr('stroke-width', 3)
        .attr('stroke', '#5cb3cc');
    svg.append('g')
        .selectAll('circle')
        .data(dataArray)
        .enter()
        .append('circle')
        .attr('r', 3)
        .attr('transform', function(d){
            return 'translate(' + (xScale(d[0]) + padding.left) + ',' + (yScale(d[1]) + padding.top) + ')'
        })
        .attr('fill', '#5cb3cc');

    //axis title
    svg.append("text")
        .attr("transform", "translate(" + (width/2) + "," + (height - padding.bottom / 3) + ")")
        .style("text-anchor", "middle")
        .text("Number of hours ago");
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("x", (-height / 2))
        .attr("y", 0)
        .attr("dy", "1em")
        .style("text-anchor" , "middle")
        .text(type);

    //graph title
    svg.append("text")
        .attr("x", (width/2))
        .attr("y", (padding.left / 2 ))
        .attr("text-anchor", "middle")
        .style("font-size", "20px")
        .text(type + " in the last 24h (record per hour)");
}

function appendGraph_device_24h(type, data){
    var svg = d3.select(type)				
    .append("svg") 
    .attr("width", width)
    .attr("height", height);


    var dataArray = data;
    var min = d3.min(dataArray, function(d) {
        return d[1];
    })
    var max = d3.max(dataArray, function(d) {
        return d[1];
    })

    var xScale = d3.scaleLinear()
                .domain([24, 0])
                .range([0, width - padding.left - padding.right]);

    var yScale = d3.scaleLinear()
                .domain([0, 1])
                .range([height - padding.top - padding.bottom, 0]);




    // graph frame work
    var xAxis = d3.axisBottom()
                .scale(xScale);
    var yAxis = d3.axisLeft()
                .scale(yScale);

    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(' + padding.left + ',' + (height - padding.bottom) + ')')
        .call(xAxis);
    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
        .call(yAxis);

    //line 
    var linePath = d3.line()
                    .x(function(d){ return xScale(d[0]) })
                    .y(function(d){ return yScale(d[1]) });

    svg.append('g')
        .append('path')
        .attr('class', 'line-path')
        .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
        .attr('d', linePath(dataArray))
        .attr('fill', 'none')
        .attr('stroke-width', 3)
        .attr('stroke', '#5cb3cc');
    svg.append('g')
        .selectAll('circle')
        .data(dataArray)
        .enter()
        .append('circle')
        .attr('r', 3)
        .attr('transform', function(d){
            return 'translate(' + (xScale(d[0]) + padding.left) + ',' + (yScale(d[1]) + padding.top) + ')'
        })
        .attr('fill', '#5cb3cc');

    //axis title
    svg.append("text")
        .attr("transform", "translate(" + (width/2) + "," + (height - padding.bottom / 3) + ")")
        .style("text-anchor", "middle")
        .text("Number of hours ago");
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("x", (-height / 2))
        .attr("y", 0)
        .attr("dy", "1em")
        .style("text-anchor" , "middle")
        .text(type);

    //graph title
    svg.append("text")
        .attr("x", (width/2))
        .attr("y", (padding.left / 2 ))
        .attr("text-anchor", "middle")
        .style("font-size", "20px")
        .text(type + " in the last 24h (record per hour)");
}


function appendGraph_7d(type, data){
    tag = type + "_7d"
    var svg = d3.select(tag)				
    .append("svg") 
    .attr("width", width)
    .attr("height", height);

    var dataArray = data;
    var min = d3.min(dataArray, function(d) {
        return d[1];
    })
    var max = d3.max(dataArray, function(d) {
        return d[1];
    })

    var xScale = d3.scaleLinear()
                .domain([28, 0])
                .range([0, width - padding.left - padding.right]);
    if (type == "Temperature" || type == "Humidity"){
        var yScale = d3.scaleLinear()
                    .domain([min-5, max+5])
                    .range([height - padding.top - padding.bottom, 0]);
    }else{
        var yScale = d3.scaleLinear()
                    .domain([Math.floor(min*0.75), Math.ceil(max*1.25)])
                    .range([height - padding.top - padding.bottom, 0]);
    }



    // graph frame work
    var xAxis = d3.axisBottom()
                .scale(xScale);
    var yAxis = d3.axisLeft()
                .scale(yScale);

    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(' + padding.left + ',' + (height - padding.bottom) + ')')
        .call(xAxis);
    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
        .call(yAxis);

    //line 
    var linePath = d3.line()
                    .x(function(d){ return xScale(d[0]) })
                    .y(function(d){ return yScale(d[1]) });

    svg.append('g')
        .append('path')
        .attr('class', 'line-path')
        .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
        .attr('d', linePath(dataArray))
        .attr('fill', 'none')
        .attr('stroke-width', 3)
        .attr('stroke', '#5cb3cc');
    svg.append('g')
        .selectAll('circle')
        .data(dataArray)
        .enter()
        .append('circle')
        .attr('r', 3)
        .attr('transform', function(d){
            return 'translate(' + (xScale(d[0]) + padding.left) + ',' + (yScale(d[1]) + padding.top) + ')'
        })
        .attr('fill', '#5cb3cc');

    //axis title
    svg.append("text")
        .attr("transform", "translate(" + (width/2) + "," + (height - padding.bottom / 3) + ")")
        .style("text-anchor", "middle")
        .text("Number of 6 hours ago");
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("x", (-height / 2))
        .attr("y", 0)
        .attr("dy", "1em")
        .style("text-anchor" , "middle")
        .text(type);

    //graph title
    svg.append("text")
        .attr("x", (width/2))
        .attr("y", (padding.left / 2 ))
        .attr("text-anchor", "middle")
        .style("font-size", "20px")
        .text(type + " in the last 7 days (record per 6 hours)");
}

function appendGraph_30d(type, data){
    tag = type + "_30d"
    var svg = d3.select(tag)				
    .append("svg") 
    .attr("width", width)
    .attr("height", height);


    var dataArray = data;
    var min = d3.min(dataArray, function(d) {
        return d[1];
    })
    var max = d3.max(dataArray, function(d) {
        return d[1];
    })

    var xScale = d3.scaleLinear()
                .domain([30, 0])
                .range([0, width - padding.left - padding.right]);
    if (type == "Temperature" || type == "Humidity"){
        var yScale = d3.scaleLinear()
                    .domain([min-5, max+5])
                    .range([height - padding.top - padding.bottom, 0]);
    }else{
        var yScale = d3.scaleLinear()
                    .domain([Math.floor(min*0.75), Math.ceil(max*1.25)])
                    .range([height - padding.top - padding.bottom, 0]);
    }



    // graph frame work
    var xAxis = d3.axisBottom()
                .scale(xScale);
    var yAxis = d3.axisLeft()
                .scale(yScale);

    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(' + padding.left + ',' + (height - padding.bottom) + ')')
        .call(xAxis);
    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
        .call(yAxis);

    //line 
    var linePath = d3.line()
                    .x(function(d){ return xScale(d[0]) })
                    .y(function(d){ return yScale(d[1]) });

    svg.append('g')
        .append('path')
        .attr('class', 'line-path')
        .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
        .attr('d', linePath(dataArray))
        .attr('fill', 'none')
        .attr('stroke-width', 3)
        .attr('stroke', '#5cb3cc');
    svg.append('g')
        .selectAll('circle')
        .data(dataArray)
        .enter()
        .append('circle')
        .attr('r', 3)
        .attr('transform', function(d){
            return 'translate(' + (xScale(d[0]) + padding.left) + ',' + (yScale(d[1]) + padding.top) + ')'
        })
        .attr('fill', '#5cb3cc');

    //axis title
    svg.append("text")
        .attr("transform", "translate(" + (width/2) + "," + (height - padding.bottom / 3) + ")")
        .style("text-anchor", "middle")
        .text("Number of days ago");
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("x", (-height / 2))
        .attr("y", 0)
        .attr("dy", "1em")
        .style("text-anchor" , "middle")
        .text(type);

    //graph title
    svg.append("text")
        .attr("x", (width/2))
        .attr("y", (padding.left / 2 ))
        .attr("text-anchor", "middle")
        .style("font-size", "20px")
        .text(type + " in the last 30 days (record per day)");
}