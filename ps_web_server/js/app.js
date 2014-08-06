window.onOffCheckboxChanging = false;
window.deviceConnected = false;

var newCurrentValues = function(reply) {
    var bla = document.location.origin;
    var newIsConnected = (reply !== "");
    var oldIsConnected = window.deviceConnected;
    if (oldIsConnected && !newIsConnected){
        // Connection lost
        blockUI();
    }
    else if (!oldIsConnected && newIsConnected){
        // Connection restored
        unblockUI();
    }
    window.deviceConnected = newIsConnected;
    if (window.deviceConnected){
        var json_object = jQuery.parseJSON(reply)
        updateDisplayValues(json_object)
    }
}

var updateDisplayValues = function(json_reply){
    $("#outputVoltage").text(json_reply["output_voltage_V"]);
    $("#outputCurrent").text(json_reply["output_current_mA"]);
    $("#targetVoltage").text(parseFloat(json_reply["target_voltage_V"]).toFixed(1));
    $("#targetCurrent").text(json_reply["current_limit_mA"]);
    if (!window.onOffCheckboxChanging){
        $("#onOffCheckboxInput").prop('checked', json_reply["output_on"]);
    }
}

var updateValues = function() {
    $.ajax( document.location.origin + "/all_values" )
      .done(function(reply) {
            newCurrentValues(reply);
      })
}

var setTargetVoltageValue = function() {
    $.post(document.location.origin + "/voltage", { target_voltage_V: $("#targetVoltageInput").val()});
}

var setTargetCurrentValue = function() {
    $.post(document.location.origin + "/current", { current_limit_mA: $("#targetCurrentInput").val()});
}

var blockUI = function(){
    $.blockUI({ message: '<h1>Unable to connect to device</h1>' });
}

var unblockUI = function(){
    $.unblockUI();
}

var start = function(){
    $.ajax( document.location.origin + "/device_connected" )
      .done(function(json_connected) {
            if (!jQuery.parseJSON(json_connected)){
                blockUI();
            }
            setInterval("updateValues()",1000);
      })

}

$(document).ready(function() {
    start();

    $('#targetVoltageInput').keydown(function(event) {
        if (event.keyCode == 13) {
            setTargetVoltageValue();
            return false;
         }
    });

    $('#targetCurrentInput').keydown(function(event) {
        if (event.keyCode == 13) {
            setTargetCurrentValue();
            return false;
         }
    });

    $("#setTargetVoltage").click(function() {
        setTargetVoltageValue();
    });

    $("#setTargetCurrent").click(function() {
        setTargetCurrentValue();
    });

    $( "#onOffCheckboxInput").change(function() {
        window.onOffCheckboxChanging = true;
        $.post(document.location.origin + "/output_on", {on: $(this).is(':checked') ? 1 : 0})
    });

     // Runs when the css3 animation is finished on the on/off button
     $('.onoffswitch-switch').on('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
    function(e) {
        window.onOffCheckboxChanging = false;
    });
})