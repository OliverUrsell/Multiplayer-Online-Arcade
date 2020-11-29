
// TODO: setup will to send name + "lost" to "move/server"

$( document ).ready(function() {
    MQTTConnect();

    // First number of votes is 4
    setButtonNumber(4);
});

// Name and host are defined by frogger.php
var port = 8081;

function MQTTConnect(){
	mqtt = new Paho.MQTT.Client(host, port, name);
	var options = {
		useSSL:true,
		timeout:3,
		onSuccess: onConnect
	}

	mqtt.onMessageArrived = messageRecieved;
	mqtt.onConnectionLost = onConnectionLost;
	console.log("Connecting...");
	mqtt.connect(options);
}

function onConnect(){
	console.log("Connection success");
	mqtt.subscribe("move/player");
}

function onConnectionLost(){
	console.log("Connection Lost");
}

function sendMessage(topic, content){
	// Send an mqtt message
	message = new Paho.MQTT.Message(content);
	message.destinationName = topic;
	mqtt.send(message);
}

function messageRecieved(message){
	// Shouldn't be recieving messages other than disconnect
	console.log(message.payloadString);
	if(message.payloadString == "disconnected"){
		// The broker has lost connection
		window.location = "../index.html";
	}else{
		// The broker is setting the number of buttons
		setButtonNumber(message.payloadString);
	}
}

function setButtonNumber(count){
	if(count > 9 || count < 1){
		throw "should not be more than 9 buttons and should be above 0";
	}else{
		html = "";
		for (var i = 1; i <= count; i++) {
			html += '<button style="top:' +
					(100/count)*(i-1) + 'vh;" class="moveButton" action='+i+'>Vote '+i+'</button>';
		}

		$("#buttons").html(html);
		$(".moveButton").css("height", (100/count) + "vh");

		// Update click events
		$(".moveButton").click(function(){
	    	if($(this).attr("action") > 9){
	    		throw "Action value should not be more than a single digit.";
	    	}
	    	sendMessage("move/server", name + $(this).attr("action"));
	    	// console.log($(this).attr("action"));
	    });
	}
}