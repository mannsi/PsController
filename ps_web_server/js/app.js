var data = {
	labels : ["","","","","","",""],
	datasets : [
		{
			data : [65,59,90,81,56,55,40]
		}
	]
}

window.voltageChartOptions = {
    scaleOverlay : false,  //Boolean - If we show the scale above the chart data
    scaleOverride : true,  //Boolean - If we want to override with a hard coded scale
    scaleSteps : 20, //Number - The number of steps in a hard coded scale   //** Required if scaleOverride is true **
    scaleStepWidth : 0.5,   //Number - The value jump in the hard coded scale
    scaleStartValue : 0,   //Number - The scale starting value
    scaleLineColor : "rgba(0,0,0,.1)",  //String - Colour of the scale line
    scaleLineWidth : 1,  //Number - Pixel width of the scale line
    scaleShowLabels : true,  //Boolean - Whether to show labels on the scale
    scaleLabel : "<%=value%>", //Interpolated JS string - can access value
    scaleFontFamily : "'Arial'", //String - Scale label font declaration for the scale label
    scaleFontSize : 12,  //Number - Scale label font size in pixels
    scaleFontStyle : "normal",  //String - Scale label font weight style
    scaleFontColor : "#666",  //String - Scale label font colour
    scaleShowGridLines : false,  ///Boolean - Whether grid lines are shown across the chart
    scaleGridLineColor : "rgba(0,0,0,.05)", //String - Colour of the grid lines
    scaleGridLineWidth : 1, //Number - Width of the grid lines
    bezierCurve : true,  //Boolean - Whether the line is curved between points
    pointDot : false, //Boolean - Whether to show a dot for each point
    pointDotRadius : 1, //Number - Radius of each point dot in pixels
    pointDotStrokeWidth : 1, //Number - Pixel width of point dot stroke
    datasetStroke : true, //Boolean - Whether to show a stroke for datasets
    datasetStrokeWidth : 1,//Number - Pixel width of dataset stroke
    datasetFill : false, //Boolean - Whether to fill the dataset with a colour
    animation : false,
    animationSteps : 60,//Number - Number of animation steps
    animationEasing : "easeOutQuart",//String - Animation easing effect
    onAnimationComplete : null //Function - Fires when the animation is complete
}

window.currentChartOptions = {
    scaleOverlay : false,  //Boolean - If we show the scale above the chart data
    scaleOverride : true,  //Boolean - If we want to override with a hard coded scale
    scaleSteps : 20, //Number - The number of steps in a hard coded scale   //** Required if scaleOverride is true **
    scaleStepWidth : 50,   //Number - The value jump in the hard coded scale
    scaleStartValue : 0,   //Number - The scale starting value
    scaleLineColor : "rgba(0,0,0,.1)",  //String - Colour of the scale line
    scaleLineWidth : 1,  //Number - Pixel width of the scale line
    scaleShowLabels : true,  //Boolean - Whether to show labels on the scale
    scaleLabel : "<%=value%>", //Interpolated JS string - can access value
    scaleFontFamily : "'Arial'", //String - Scale label font declaration for the scale label
    scaleFontSize : 12,  //Number - Scale label font size in pixels
    scaleFontStyle : "normal",  //String - Scale label font weight style
    scaleFontColor : "#666",  //String - Scale label font colour
    scaleShowGridLines : false,  ///Boolean - Whether grid lines are shown across the chart
    scaleGridLineColor : "rgba(0,0,0,.05)", //String - Colour of the grid lines
    scaleGridLineWidth : 1, //Number - Width of the grid lines
    bezierCurve : false,  //Boolean - Whether the line is curved between points
    pointDot : false, //Boolean - Whether to show a dot for each point
    pointDotRadius : 1, //Number - Radius of each point dot in pixels
    pointDotStrokeWidth : 1, //Number - Pixel width of point dot stroke
    datasetStroke : true, //Boolean - Whether to show a stroke for datasets
    datasetStrokeWidth : 1,//Number - Pixel width of dataset stroke
    datasetFill : false, //Boolean - Whether to fill the dataset with a colour
    animation : false,
    animationSteps : 60,//Number - Number of animation steps
    animationEasing : "easeOutQuart",//String - Animation easing effect
    onAnimationComplete : null //Function - Fires when the animation is complete
}


var voltage_data = "";
var current_data = "";

var updateChart = function() {
    var containerWidth = jQuery(".graphs").width();
    var containerHeight = jQuery(".graphs").height();
    var graphTitleHeight = jQuery(".graphTitle").height();
    containerHeight = containerHeight - (2 * graphTitleHeight);

    // Draw the voltage chart
    var ctx = $('#voltageChart').get(0).getContext("2d");
    ctx.canvas.width = containerWidth;
    ctx.canvas.height = containerHeight/2;
    new Chart(ctx).Line(voltage_data, window.voltageChartOptions);

    // Draw the current chart
    var ctx = $('#currentChart').get(0).getContext("2d");
    ctx.canvas.width = containerWidth;
    ctx.canvas.height = containerHeight/2;
    new Chart(ctx).Line(current_data, window.currentChartOptions);
}

var updateStatusValues = function(json_reply) {
    $("#outputVoltage").text(json_reply["outputVoltage"]);
    $("#outputCurrent").text(json_reply["outputCurrent"]);
    $("#inputVoltage").text(json_reply["inputVoltage"]);
    $("#preRegVoltage").text(json_reply["preRegVoltage"]);
    $("#targetVoltage").val(parseFloat(json_reply["targetVoltage"]).toFixed(1));
    $("#targetCurrent").val(json_reply["targetCurrent"]);
    $("#outputOn").prop('checked', json_reply["outputOn"]);;
}

var updateValues = function() {

    $.ajax( "http://localhost:8080/get_all_values" )
      .done(function(json) {
            var json_object = jQuery.parseJSON(json)
            voltage_data = json_object["voltage"]
            current_data = json_object["current"]
            updateChart();
      })

    $.ajax( "http://localhost:8080/get_current_values" )
      .done(function(json) {
            var json_object = jQuery.parseJSON(json)
            updateStatusValues(json_object);
      })

}

$(document).ready(function() {
    setInterval("updateValues()",2000);

    $("#setTargetVoltage").click(function() {
        $.post("http://localhost:8080/set_target_voltage", { voltage: $("#targetVoltage").val()});
    });

    $("#setTargetCurrent").click(function() {
      $.post("http://localhost:8080/set_target_current", { current: $("#targetCurrent").val()});
    });

    $( "#outputOn" ).change(function() {
        if ($(this).is(':checked')) {
            $.post("http://localhost:8080/turn_on");
        } else {
            $.post("http://localhost:8080/turn_off");
        }
    });
})


