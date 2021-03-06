window.onOffCheckboxChanging = false;
window.deviceConnected = false;
var disconnectedCounter = 3; // Number of times we receive a disconnected signal until a connection lost string is shown

var newCurrentValues = function(reply) {
    var isConnected = reply["connected"];

    if (window.ui_blocked && isConnected){
        unblockUI();
    } else if(!window.ui_blocked && !isConnected){
        if (disconnectedCounter == 0){
            blockUI('Unable to connect to device. Trying to reconnect ...');
        } else {
            disconnectedCounter--;
        }
    }

    if (isConnected){
        disconnectedCounter = 3;
    }

    window.deviceConnected = isConnected;

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
            setTimeout(updateValues, 500);
        })
        .fail(function() {
            blockUI('PS201 web server not found. <br /> Start it by running "PsController" from terminal');
            setTimeout(updateValues, 500);
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
        $.blockUI({ message: '<h1>' + blocking_message + '</h1>' ,css:{cursor:'default'}});
    }
}

var unblockUI = function(){
    window.ui_blocked = false;
    $.unblockUI();
}

var start = function(){
    $.ajax( document.location.origin + "/all_values" )
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
            updateValues();
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