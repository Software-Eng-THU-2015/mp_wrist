$("input").blur(function(e){
    var userId = $("#userId").attr("userId");
    var node = $(this);
    var val = parseInt(this.value);
    var max = parseInt(node.attr("max"));
    var min = parseInt(node.attr("min"));
    if(val < min || val > max)
        this.value = node.attr("init");
    else{
        var url = domain + "/basic/profile/data?userId=" + userId + "&type=" + node.attr("item") + "&value=" + val;
        getData(url,function(){});
    }
})

var chart_data = eval("(" + $(".chartData").html() + ")");
//Day,Week,Month Datasets {"date": "", "object": "", "value": ""}
var chartData = [chart_data.day,chart_data.week,chart_data.month]
var valueType = ["step","cal","dis","sleep"];

for(var i = 0;i < chartData.length;i++)
{
    var ld = chartData[i].length;
    for(var j = 0;j < ld;j++){
        chartData[i][j].Size = 14;
        for(var k = 0;k < 2;k++){
            chartData[i][j][valueType[k]] = chartData[i][j][valueType[k] + "_value"];
            if(chartData[i][j][valueType[k]+"_value"] >= chartData[i][j][valueType[k]+"_object"])
                chartData[i][j]["bulletClass" + k] = "achieved";
        }
    }
}

function PaintChart(data, type1, type2){
    var conType1 = [{minPeriod:"DD",id:"Days"},{minPeriod:"W",id:"Weeks"},{minPeriod:"MM",id:"Months"}];
    var conType2 = [{title:"步数"},{title:"热量"},{title:"路程"},{title:"睡眠"}];
    
    // SERIAL CHART
    chart = new AmCharts.AmSerialChart();
    chart.addClassNames = true;
    chart.dataProvider = data[type1];
    chart.categoryField = "date";
    chart.dataDateFormat = "YYYY-MM-DD";
    chart.startvalue = 1;
    chart.color = "#747474";
    chart.marginLeft = 0;


    // category
    var categoryAxis = chart.categoryAxis;
    categoryAxis.parseDates = true; // data-based
    categoryAxis.minPeriod = conType1[type1].minPeriod; // data is daily, set minPeriod to DD
    categoryAxis.autoGridCount = false;
    categoryAxis.gridCount = 50;
    categoryAxis.gridAlpha = 0.1;
    categoryAxis.gridColor = "#FFFFFF";
    categoryAxis.axisColor = "#555555";
   
    // custom date format
    categoryAxis.dateFormats = [{
        period: 'DD',
        format: 'DD'
    }, {
        period: 'WW',
        format: 'MMM DD'
    }, {
        period: 'MM',
        format: 'MMM'
    }, {
        period: 'YYYY',
        format: 'YYYY'
    }];


    // value valueaxis
    var valueAxis = new AmCharts.ValueAxis();
    valueAxis.gridAlpha = 0;
    valueAxis.axisAlpha = 0;
    valueAxis.labelsEnabled = false;
    valueAxis.position = "right";
    chart.addValueAxis(valueAxis);

    // object valueaxis
    var objectAxis = new AmCharts.ValueAxis();
    objectAxis.gridAlpha = 0;
    objectAxis.axisAlpha = 0;
    objectAxis.inside = true;
    objectAxis.position = "right";
    chart.addValueAxis(objectAxis);


    // GRAPHS
    // value graph
    var valueGraph = new AmCharts.AmGraph();
    valueGraph.valueField = valueType[type2] + "_value";
    valueGraph.id = "g1";
    valueGraph.classNameField = "bulletClass" + type2;
    valueGraph.title = conType2[type2].title + "数据";
    valueGraph.type = "line";
    valueGraph.valueAxis = valueAxis; 
    valueGraph.lineColor = "#786c56";
    valueGraph.lineThickness = 1;
    valueGraph.legendValueText = "[[" + valueType[type2] + "_value]]";
    valueGraph.bullet = "round";
    valueGraph.bulletSizeField = "Size"; //bullet size
    valueGraph.bulletBorderColor = "#786c56";
    valueGraph.bulletBorderAlpha = 1;
    valueGraph.bulletBorderThickness = 2;
    valueGraph.bulletColor = "#000000";
    valueGraph.labelText = "[[" + valueType[type2] + "]]";
    valueGraph.labelPosition = "right";
    valueGraph.balloonText = "[[" + valueType[type2] + "_value]]";
    valueGraph.showBalloon = true;
    valueGraph.animationPlayed = true;
    chart.addGraph(valueGraph);

    // object graph
    var objectGraph = new AmCharts.AmGraph();
    objectGraph.title = conType2[type2].title + "目标";
    objectGraph.valueField = valueType[type2] + "_object";
    objectGraph.type = "line"; 
    objectGraph.lineColor = "#FF0000";
    objectGraph.balloonText = "[[" + valueType[type2] + "_object]]";
    objectGraph.lineThickness = 1;
    objectGraph.legendValueText = "[[" + valueType[type2] + "_object]]";
    objectGraph.bullet = "square";
    objectGraph.bulletBorderColor = "#FF0000";
    objectGraph.bulletBorderThickness = 1;
    objectGraph.dashLengthField = "dashLength";
    objectGraph.animationPlayed = true;
    chart.addGraph(objectGraph);

    // CURSOR
    var chartCursor = new AmCharts.ChartCursor();
    chartCursor.zoomable = false;
    chartCursor.categoryBalloonDateFormat = conType1[type1].minPeriod;
    chartCursor.cursorAlpha = 0;
    chartCursor.valueBalloonsEnabled = false;
    chart.addChartCursor(chartCursor);

    // LEGEND
    var legend = new AmCharts.AmLegend();
    legend.bulletType = "round";
    legend.equalWidths = false;
    legend.valueWidth = 120;
    legend.useGraphSettings = true;
    legend.color = "#747474";
    chart.addLegend(legend);

    // WRITE
    chart.write(conType1[type1].id + "Chart" + (type2+1));
}
