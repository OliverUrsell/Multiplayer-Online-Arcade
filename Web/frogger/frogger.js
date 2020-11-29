
//TODO: Setup will to send name+"lost" to "move/server"

$( document ).ready(function() {
    console.log( "ready!" );

    MQTTConnect();

    $("#move").click(function(){
		sendMessage("move/server", name+"f");
	});

	$("#moveBack").click(function(){
		sendMessage("move/server", name+"b");
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
	mqtt.subscribe("move/player/"+name);
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
	console.log(message.payloadString);
	if(message.payloadString == "disconnected"){
		window.location = "../index.html";
	}else if(message.destinationName == "move/player/"+name){
		// Message is a color setting for us
		// Only color is changed here so no sub topic is required
		var r = message.payloadString.substring(0, 3);
		var g = message.payloadString.substring(3, 6);
		var b = message.payloadString.substring(6, 9);
		setColor(r, g, b);
	}
}

function setColor(r, g, b){
	// Set the colour of the buttons
	$(".moveButton").css("background-color", "rgb("+r+", "+g+", "+b+")");
}