window.onOffCheckboxChanging = false;
window.deviceConnected = false;

var newCurrentValues = function(reply) {
    var bla = document.location.origin;
    var newIsConnected = (reply["connected"]);
    var oldIsConnected = window.deviceConnected;
    if (oldIsConnected && !newIsConnected){
        // Connection lost
        blockUI('Unable to connect to device');
    }
    else if (!oldIsConnected && newIsConnected){
        // Connection restored
        unblockUI();
    }
    else if (window.ui_blocked && newIsConnected){
        // Receiving values after server has been down
        unblockUI();
    }
    window.deviceConnected = newIsConnected;
    if (window.deviceConnected){
        updateDisplayValues(reply)
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
        .done(function(json_reply) {
            newCurrentValues(jQuery.parseJSON(json_reply));
        })
        .fail(function() {
            blockUI('PS201 web server not found. <br /> Start it by running "ps_controller" from terminal');
        })
}

var setTargetVoltageValue = function() {
    $.post(document.location.origin + "/voltage", { target_voltage_V: $("#targetVoltageInput").val()});
}

var setTargetCurrentValue = function() {
    $.post(document.location.origin + "/current", { current_limit_mA: $("#targetCurrentInput").val()});
}

var blockUI = function(blocking_message){
    if (!window.ui_blocked)
    {
        window.ui_blocked = true;
        $.blockUI({ message: '<h1>' + blocking_message + '</h1>' });
    }

}

var unblockUI = function(){
    window.ui_blocked = false;
    $.unblockUI();
}

var start = function(){
    $.ajax( document.location.origin + "/device_connected" )
      .done(function(json_reply) {
            var reply = jQuery.parseJSON(json_reply)
            if (!reply["connected"]){
                if (reply["authentication_error"]){
                    blockUI("Unable to access usb ports. <br />Linux users need to be part of 'dialout' group.");
                }
                else{
                    blockUI("Unable to connect to device");
                }

            }
            setInterval("updateValues()",1000);
      })

}

$(document).ready(function() {
    window.ui_blocked = false;
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