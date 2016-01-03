//getWeek() function ..week+1
Date.prototype.getWeek = function (dowOffset){
dowOffset = typeof(dowOffset) == 'int' ? dowOffset : 0;
var newYear = new Date(this.getFullYear(),0,1);
var day = newYear.getDay() - dowOffset;
day = (day >= 0 ? day : day + 7);
var daynum = Math.floor((this.getTime() - newYear.getTime() - (this.getTimezoneOffset()-newYear.getTimezoneOffset())*60000)/86400000) + 1;
var weeknum;
if(day < 4) {
    weeknum = Math.floor((daynum+day-1)/7) + 1;
    if(weeknum > 52) {
        nYear = new Date(this.getFullYear() + 1,0,1);
        nday = nYear.getDay() - dowOffset;
        nday = nday >= 0 ? nday : nday + 7;
        weeknum = nday < 4 ? 1 : 53;
    }
}
else {
    weeknum = Math.floor((daynum+day-1)/7);
}
return weeknum;
};


//date function
function dateMinus(days){
    var today=new Date();
    today.setDate(today.getDate()-days)
    var yy = today.getFullYear();
    var mm = today.getMonth()+1;
    var dd = today.getDate();
    if(dd<10)
        dd = "0" + dd;
    if(mm<10)
        mm = "0" + mm;
    return yy+ "-" + mm + "-" + dd;
}

function weekMinus(weeks){
    var today=new Date();

    var ww = today.getWeek()+1-weeks;

    return ww;
}

function monthMinus(months){
    var today1=new Date();
    today1.setMonth(today1.getMonth()-months)
    var yy = today1.getFullYear();
    var mm = today1.getMonth()+1;
    if(mm<10)
        mm = "0" + mm;

    return yy+ "-" + mm;
}

var chart_data = eval("(" + $(".chartData").html() + ")");
//Day,Week,Month Datasets {"date": "", "object": "", "value": ""}
var chartDayData = chart_data.day;
var chartWeekData = chart_data.week;
var chartMonthData = chart_data.month;

//Steps
var StepDayData = [];
var StepWeekData = [];
var StepMonthData = [];


for(var i=0; i<chartDayData.length;i++)
{
    for(var j=1;j<=7;j++)
    {
        if(chartDayData[i].date==dateMinus(j)){
            StepDayData[7-j]=chartDayData[i];
        }
    }
}
for(var k=0; k<StepDayData.length;k++)
{
    if(StepDayData[k].step_value>StepDayData[k].step_object)
        StepDayData[k].bulletClass1="achieved";
    StepDayData[k].StepName=StepDayData[k].step_value;
    StepDayData[k].Size=14;
}


for(var i=0; i<chartWeekData.length;i++)
{
    for(j=1;j<=4;j++)
    {
        if(chartWeekData[i].week==weekMinus(j)){
            StepWeekData[4-j]=chartWeekData[i];
        }
    }
}
for(var k=0; k<StepWeekData.length;k++)
{
    if(StepWeekData[k].step_value>StepWeekData[k].step_object)
        StepWeekData[k].bulletClass1="achieved";
    StepWeekData[k].StepName=StepWeekData[k].step_value;
    StepWeekData[k].Size=14;
}


for(var i=0; i<chartMonthData.length;i++)
{
    for(var j=1;j<=6;j++)
    {
        if(chartMonthData[i].date==monthMinus(j)){
            StepMonthData[6-j]=chartMonthData[i];
        }
    }
}

for(var k=0; k<StepMonthData.length;k++)
{
    if(StepMonthData[k].step_value>StepMonthData[k].step_object)
        StepMonthData[k].bulletClass1="achieved";
    StepMonthData[k].StepName=StepMonthData[k].step_value;
    StepMonthData[k].Size=14;
}



//daily graph1
AmCharts.ready(function () {

    // SERIAL CHART
    chart = new AmCharts.AmSerialChart();
    chart.addClassNames = true;
    chart.dataProvider = StepDayData;
    chart.categoryField = "date";
    chart.dataDateFormat = "YYYY-MM-DD";
    chart.startvalue = 1;
    chart.color = "#747474";
    chart.marginLeft = 0;


    // category
    var categoryAxis = chart.categoryAxis;
    categoryAxis.parseDates = true; // data-based
    categoryAxis.minPeriod = "DD"; // data is daily, set minPeriod to DD
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
    valueGraph.valueField = "step_value";
    valueGraph.id = "g1";
    valueGraph.classNameField = "bulletClass1";
    valueGraph.title = "Stepvalue";
    valueGraph.type = "line";
    valueGraph.valueAxis = valueAxis; 
    valueGraph.lineColor = "#786c56";
    valueGraph.lineThickness = 1;
    valueGraph.legendValueText = "[[step_value]]";
    valueGraph.bullet = "round";
    valueGraph.bulletSizeField = "Size"; //bullet size
    valueGraph.bulletBorderColor = "#786c56";
    valueGraph.bulletBorderAlpha = 1;
    valueGraph.bulletBorderThickness = 2;
    valueGraph.bulletColor = "#000000";
    valueGraph.labelText = "[[StepName]]";
    valueGraph.labelPosition = "right";
    valueGraph.balloonText = "[[step_value]]";
    valueGraph.showBalloon = true;
    valueGraph.animationPlayed = true;
    chart.addGraph(valueGraph);

    // object graph
    var objectGraph = new AmCharts.AmGraph();
    objectGraph.title = "Stepobject";
    objectGraph.valueField = "step_object";
    objectGraph.type = "line"; 
    objectGraph.lineColor = "#FF0000";
    objectGraph.balloonText = "[[step_object]]";
    objectGraph.lineThickness = 1;
    objectGraph.legendValueText = "[[step_object]]";
    objectGraph.bullet = "square";
    objectGraph.bulletBorderColor = "#FF0000";
    objectGraph.bulletBorderThickness = 1;
    objectGraph.dashLengthField = "dashLength";
    objectGraph.animationPlayed = true;
    chart.addGraph(objectGraph);

    // CURSOR
    var chartCursor = new AmCharts.ChartCursor();
    chartCursor.zoomable = false;
    chartCursor.categoryBalloonDateFormat = "DD";
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
    chart.write("DaysChart1");
});


//weekly graph1
AmCharts.ready(function () {
    
    chart = new AmCharts.AmSerialChart();
    chart.addClassNames = true;
    chart.dataProvider = StepWeekData;
    chart.categoryField = "date";
    chart.dataDateFormat = "YYYY-MM-DD";
    chart.startvalue = 1;
    chart.color = "#747474";
    chart.marginLeft = 0;

    // AXES
    // category
    var categoryAxis = chart.categoryAxis;
    categoryAxis.parseDates = true; // data-based
    categoryAxis.minPeriod = "WW"; // data is weekly, set minPeriod to ww
    categoryAxis.autoGridCount = false;
    categoryAxis.gridCount = 50;
    categoryAxis.gridAlpha = 0.1;
    categoryAxis.gridColor = "#FFFFFF";
    categoryAxis.axisColor = "#555555";
        

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
    // GRAPH
    var valuegraph = new AmCharts.AmGraph();
    valuegraph.valueField = "step_value";
    valuegraph.id = "g1";
    valuegraph.classNameField = "bulletClass1";
    valuegraph.title = "Stepvalue";
    valuegraph.type = "line";
    valuegraph.valueAxis = valueAxis;
    valuegraph.lineColor = "#786c56";
    valuegraph.lineThickness = 1;
    valuegraph.legendValueText = "[[step_value]]";
    valuegraph.bullet = "round";
    valuegraph.bulletSizeField = "Size"; //bullet size
    valuegraph.bulletBorderColor = "#786c56";
    valuegraph.bulletBorderAlpha = 1;
    valuegraph.bulletBorderThickness = 2;
    valuegraph.bulletColor = "#000000";
    valuegraph.labelText = "[[StepName]]";
    valuegraph.labelPosition = "right";
    valuegraph.balloonText = "[[step_value]]";
    valuegraph.showBalloon = true;
    valuegraph.animationPlayed = true;

    chart.addGraph(valuegraph);

    var objectGraph = new AmCharts.AmGraph();
    objectGraph.title = "Stepobject";
    objectGraph.valueField = "step_object";
    objectGraph.type = "line"; 
    objectGraph.lineColor = "#FF0000";
    objectGraph.balloonText = "[[step_object]]";
    objectGraph.lineThickness = 1;
    objectGraph.legendValueText = "[[step_object]]";
    objectGraph.bullet = "square";
    objectGraph.bulletBorderColor = "#FF0000";
    objectGraph.bulletBorderThickness = 1;
    objectGraph.dashLengthField = "dashLength";
    objectGraph.animationPlayed = true;
    chart.addGraph(objectGraph);

    // CURSOR
    var chartCursor = new AmCharts.ChartCursor();
    chartCursor.zoomable = false;
    chartCursor.categoryBalloonDateFormat = "W";
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
    chart.write("WeeksChart1");
});


//monthly graph1
AmCharts.ready(function () {

    // SERIAL CHART
    chart = new AmCharts.AmSerialChart();
    chart.addClassNames = true;
    chart.dataProvider = StepMonthData;
    chart.categoryField = "date";
    chart.dataDateFormat = "YYYY-MM";
    chart.startvalue = 1;
    chart.color = "#747474";
    chart.marginLeft = 0;


    // category
    var categoryAxis = chart.categoryAxis;
    categoryAxis.parseDates = true; // data-based
    categoryAxis.minPeriod = "MM"; // data is montly, set minPeriod to mm
    categoryAxis.autoGridCount = false;
    categoryAxis.gridCount = 50;
    categoryAxis.gridAlpha = 0.1;
    categoryAxis.gridColor = "#FFFFFF";
    categoryAxis.axisColor = "#555555";
   
    // custom date format
    categoryAxis.dateFormats = [
    {
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
    valueGraph.valueField = "step_value";
    valueGraph.id = "g1";
    valueGraph.classNameField = "bulletClass1";
    valueGraph.title = "Stepvalue";
    valueGraph.type = "line";
    valueGraph.valueAxis = valueAxis; 
    valueGraph.lineColor = "#786c56";
    valueGraph.lineThickness = 1;
    valueGraph.legendValueText = "[[step_value]]";
    valueGraph.bullet = "round";
    valueGraph.bulletSizeField = "Size"; //bullet size
    valueGraph.bulletBorderColor = "#786c56";
    valueGraph.bulletBorderAlpha = 1;
    valueGraph.bulletBorderThickness = 2;
    valueGraph.bulletColor = "#000000";
    valueGraph.labelText = "[[StepName]]";
    valueGraph.labelPosition = "right";
    valueGraph.balloonText = "[[step_value]]";
    valueGraph.showBalloon = true;
    valueGraph.animationPlayed = true;
    chart.addGraph(valueGraph);

    // object graph
    var objectGraph = new AmCharts.AmGraph();
    objectGraph.title = "Stepobject";
    objectGraph.valueField = "step_object";
    objectGraph.type = "line"; 
    objectGraph.lineColor = "#FF0000";
    objectGraph.balloonText = "[[step_object]]";
    objectGraph.lineThickness = 1;
    objectGraph.legendValueText = "[[step_object]]";
    objectGraph.bullet = "square";
    objectGraph.bulletBorderColor = "#FF0000";
    objectGraph.bulletBorderThickness = 1;
    objectGraph.dashLengthField = "dashLength";
    objectGraph.animationPlayed = true;
    chart.addGraph(objectGraph);

    // CURSOR
    var chartCursor = new AmCharts.ChartCursor();
    chartCursor.zoomable = false;
    chartCursor.categoryBalloonDateFormat = "MM";
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
    chart.write("MonthsChart1");
});




//Calories
var CalDayData = [];
var CalWeekData = [];
var CalMonthData = [];


for(var i=0; i<chartDayData.length;i++)
{
    for(var j=1;j<=7;j++)
    {
        if(chartDayData[i].date==dateMinus(j)){
            CalDayData[7-j]=chartDayData[i];
        }
    }
}
for(var k=0; k<CalDayData.length;k++)
{
    if(CalDayData[k].cal_value>CalDayData[k].cal_object)
        CalDayData[k].bulletClass2="achieved";
    CalDayData[k].CalorieName=CalDayData[k].cal_value;
}


for(var i=0; i<chartWeekData.length;i++)
{
    for(var j=1;j<=4;j++)
    {
        if(chartWeekData[i].week==weekMinus(j))
            CalWeekData[4-j]=chartWeekData[i];
    }
}
for(var k=0; k<CalWeekData.length;k++)
{
    if(CalWeekData[k].cal_value>CalWeekData[k].cal_object)
        CalWeekData[k].bulletClass2="achieved";
    CalWeekData[k].CalorieName=CalWeekData[k].cal_value;
}


for(var i=0; i<chartMonthData.length;i++)
{
    for(var j=1;j<=6;j++)
    {
        if(chartMonthData[i].date==monthMinus(j)){
            CalMonthData[6-j]=chartMonthData[i];
        }
    }
}
for(var k=0; k<CalMonthData.length;k++)
{
    if(CalMonthData[k].cal_value>StepMonthData[k].cal_object)
        CalMonthData[k].bulletClass2="achieved";
    CalMonthData[k].CalorieName=StepMonthData[k].cal_value;
}





//GRAPH 2, DAILY
AmCharts.ready(function () {

    // SERIAL CHART
    chart = new AmCharts.AmSerialChart();
    chart.addClassNames = true;
    chart.dataProvider = CalDayData;
    chart.categoryField = "date";
    chart.dataDateFormat = "YYYY-MM-DD";
    chart.startvalue = 1;
    chart.color = "#747474";
    chart.marginLeft = 0;


    // category
    var categoryAxis = chart.categoryAxis;
    categoryAxis.parseDates = true; // data-based
    categoryAxis.minPeriod = "DD"; // data is daily, set minPeriod to DD
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
    valueGraph.valueField = "cal_value";
    valueGraph.id = "g1";
    valueGraph.classNameField = "bulletClass2";
    valueGraph.title = "Calorievalue";
    valueGraph.type = "line";
    valueGraph.valueAxis = valueAxis; 
    valueGraph.lineColor = "#786c56";
    valueGraph.lineThickness = 1;
    valueGraph.legendValueText = "[[cal_value]]";
    valueGraph.bullet = "round";
    valueGraph.bulletSizeField = "Size"; //bullet size
    valueGraph.bulletBorderColor = "#786c56";
    valueGraph.bulletBorderAlpha = 1;
    valueGraph.bulletBorderThickness = 2;
    valueGraph.bulletColor = "#000000";
    valueGraph.labelText = "[[CalorieName]]";
    valueGraph.labelPosition = "right";
    valueGraph.balloonText = "[[cal_value]]";
    valueGraph.showBalloon = true;
    valueGraph.animationPlayed = true;
    chart.addGraph(valueGraph);

    // object graph
    var objectGraph = new AmCharts.AmGraph();
    objectGraph.title = "Calorieobject";
    objectGraph.valueField = "cal_object";
    objectGraph.type = "line"; 
    objectGraph.lineColor = "#FF0000";
    objectGraph.balloonText = "[[cal_object]]";
    objectGraph.lineThickness = 1;
    objectGraph.legendValueText = "[[cal_object]]";
    objectGraph.bullet = "square";
    objectGraph.bulletBorderColor = "#FF0000";
    objectGraph.bulletBorderThickness = 1;
    objectGraph.dashLengthField = "dashLength";
    objectGraph.animationPlayed = true;
    chart.addGraph(objectGraph);

    // CURSOR
    var chartCursor = new AmCharts.ChartCursor();
    chartCursor.zoomable = false;
    chartCursor.categoryBalloonDateFormat = "DD";
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
    chart.write("DaysChart2");
});

//GRAPH 2, WEEKLY
AmCharts.ready(function () {
    
    chart = new AmCharts.AmSerialChart();
    chart.addClassNames = true;
    chart.dataProvider = CalWeekData;
    chart.categoryField = "date";
    chart.dataDateFormat = "YYYY-MM-DD";
    chart.startvalue = 1;
    chart.color = "#747474";
    chart.marginLeft = 0;

    // AXES
    // category
    var categoryAxis = chart.categoryAxis;
    categoryAxis.parseDates = true; // data-based
    categoryAxis.minPeriod = "WW"; // data is weekly, set minPeriod to ww
    categoryAxis.autoGridCount = false;
    categoryAxis.gridCount = 50;
    categoryAxis.gridAlpha = 0.1;
    categoryAxis.gridColor = "#FFFFFF";
    categoryAxis.axisColor = "#555555";
           

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
    // GRAPH
    var valuegraph = new AmCharts.AmGraph();
    valuegraph.valueField = "cal_value";
    valuegraph.id = "g1";
    valuegraph.classNameField = "bulletClass2";
    valuegraph.title = "Calorievalue";
    valuegraph.type = "line";
    valuegraph.valueAxis = valueAxis;
    valuegraph.lineColor = "#786c56";
    valuegraph.lineThickness = 1;
    valuegraph.legendValueText = "[[cal_value]]";
    valuegraph.bullet = "round";
    valuegraph.bulletSizeField = "Size"; //bullet size
    valuegraph.bulletBorderColor = "#786c56";
    valuegraph.bulletBorderAlpha = 1;
    valuegraph.bulletBorderThickness = 2;
    valuegraph.bulletColor = "#000000";
    valuegraph.labelText = "[[CalorieName]]";
    valuegraph.labelPosition = "right";
    valuegraph.balloonText = "[[cal_value]]";
    valuegraph.showBalloon = true;
    valuegraph.animationPlayed = true;

    chart.addGraph(valuegraph);

    var objectGraph = new AmCharts.AmGraph();
    objectGraph.title = "Calorieobject";
    objectGraph.valueField = "cal_object";
    objectGraph.type = "line"; 
    objectGraph.lineColor = "#FF0000";
    objectGraph.balloonText = "[[cal_object]]";
    objectGraph.lineThickness = 1;
    objectGraph.legendValueText = "[[cal_object]]";
    objectGraph.bullet = "square";
    objectGraph.bulletBorderColor = "#FF0000";
    objectGraph.bulletBorderThickness = 1;
    objectGraph.dashLengthField = "dashLength";
    objectGraph.animationPlayed = true;
    chart.addGraph(objectGraph);

    // CURSOR
    var chartCursor = new AmCharts.ChartCursor();
    chartCursor.zoomable = false;
    chartCursor.categoryBalloonDateFormat = "W";
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
    chart.write("WeeksChart2");
});


//GRAPH 2, MONTHLY
AmCharts.ready(function () {

    // SERIAL CHART
    chart = new AmCharts.AmSerialChart();
    chart.addClassNames = true;
    chart.dataProvider = CalMonthData;
    chart.categoryField = "date";
    chart.dataDateFormat = "YYYY-MM";
    chart.startvalue = 1;
    chart.color = "#747474";
    chart.marginLeft = 0;


    // category
    var categoryAxis = chart.categoryAxis;
    categoryAxis.parseDates = true; // data-based
    categoryAxis.minPeriod = "MM"; // data is montly, set minPeriod to DD
    categoryAxis.autoGridCount = false;
    categoryAxis.gridCount = 50;
    categoryAxis.gridAlpha = 0.1;
    categoryAxis.gridColor = "#FFFFFF";
    categoryAxis.axisColor = "#555555";
   
    // custom date format
    categoryAxis.dateFormats = [
    {
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
    valueGraph.valueField = "cal_value";
    valueGraph.id = "g1";
    valueGraph.classNameField = "bulletClass2";
    valueGraph.title = "Calorievalue";
    valueGraph.type = "line";
    valueGraph.valueAxis = valueAxis; 
    valueGraph.lineColor = "#786c56";
    valueGraph.lineThickness = 1;
    valueGraph.legendValueText = "[[cal_value]]";
    valueGraph.bullet = "round";
    valueGraph.bulletSizeField = "Size"; //bullet size
    valueGraph.bulletBorderColor = "#786c56";
    valueGraph.bulletBorderAlpha = 1;
    valueGraph.bulletBorderThickness = 2;
    valueGraph.bulletColor = "#000000";
    valueGraph.labelText = "[[CalorieName]]";
    valueGraph.labelPosition = "right";
    valueGraph.balloonText = "[[cal_value]]";
    valueGraph.showBalloon = true;
    valueGraph.animationPlayed = true;
    chart.addGraph(valueGraph);

    // object graph
    var objectGraph = new AmCharts.AmGraph();
    objectGraph.title = "Calorieobject";
    objectGraph.valueField = "cal_object";
    objectGraph.type = "line"; 
    objectGraph.lineColor = "#FF0000";
    objectGraph.balloonText = "[[cal_object]]";
    objectGraph.lineThickness = 1;
    objectGraph.legendValueText = "[[cal_object]]";
    objectGraph.bullet = "square";
    objectGraph.bulletBorderColor = "#FF0000";
    objectGraph.bulletBorderThickness = 1;
    objectGraph.dashLengthField = "dashLength";
    objectGraph.animationPlayed = true;
    chart.addGraph(objectGraph);

    // CURSOR
    var chartCursor = new AmCharts.ChartCursor();
    chartCursor.zoomable = false;
    chartCursor.categoryBalloonDateFormat = "MM";
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
    chart.write("MonthsChart2");
});