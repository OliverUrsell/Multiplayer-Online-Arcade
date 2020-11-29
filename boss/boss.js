
//TODO: Setup will to send name+"lost" to "move/server"

var highlightedButton;

$( document ).ready(function() {
    console.log( "ready!" );

    MQTTConnect();

    $(".moveButton").click(function(){
		if(highlightedButton != undefined){
			highlightedButton.css("background-color", "red");
		}
		highlightedButton = $(this);
		highlightedButton.css("background-color", "orange");
		console.log(name+$(this).attr("zone"));
	});
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
		window.location = "../index.html";
	}
}