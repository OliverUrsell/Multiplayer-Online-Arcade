
// var host = "test.mosquitto.org";
var port = 8081;
var serverConnectTime = 2000; // Time to wait for connect in milliseconds
var randID = 100+Math.floor((Math.random() * 899));

$( document ).ready(function() {
    $("#submit").click(function(){
    	// performRequest("frogger");
    	// Connect to the given host IP
    	MQTTConnect($("#host").val());
    });
});

function MQTTConnect(host){
	// Generate a random ID
	
	// Connect with that id
	mqtt = new Paho.MQTT.Client(host, port, $("#name").val() + randID);
	var options = {
		useSSL:true,
		timeout:3,
		onSuccess: onConnect
	}

	mqtt.onMessageArrived = messageRecieved;
	mqtt.onConnectionLost = onConnectionLost;
	console.log("Connecting...");
	mqtt.connect(options);

	// If the server hasn't connected by serverConnectTime throw error
	setTimeout(function(){
		try{
			// Attempt to send a message to see if the connection worked
			sendMessage("a", "b");
		}catch{
			$(".error").hide("fade");
			$("#serverNo").show("fade");
		}
	}, serverConnectTime);
}

function onConnect(){
	// Successfully connected to broker
	console.log("Connection success");
	$(".error").hide("fade");
	mqtt.subscribe("check/player");
	mqtt.subscribe("check/player/" + $("#name").val() + randID) // Subscribe to ID
	sendMessage("check/server", $("#name").val() + randID); // check name
	//serverCheck(); // Check name
}

function serverCheck(){
	// Check the name is not already in use
	sendMessage("check/server", name);
}

function onConnectionLost(){
	console.log("Connection Lost");
	$("#serverNo").show("fade");
}

function sendMessage(topic, content){
	// Send an mqtt message
	message = new Paho.MQTT.Message(content);
	message.destinationName = topic;
	mqtt.send(message);
}

function messageRecieved(message){
	// Recieve true or false from the server for the name
	console.log(message.destinationName + message.payloadString);
	if(message.destinationName == "check/player/" + $("#name").val() + randID){
		// if the topic is correct and for this user
		if(message.payloadString == "n"){
			// Name is a duplicate
			$(".error").hide("fade");
			$("#nameUsed").show("fade");
		}else{
			// The payload defines the gamemode
			performRequest(message.payloadString);
		}
	}
}

function performRequest(game){
	// Game is a string from server denoting the correct control scheme
	var url = "";
	switch(game){
		case "frogger":
			url = "frogger/frogger.php";
			break;
		case "dod":
			url = "dod/dod.php";
			break;
		case "boss":
			url = "boss/boss.php";
			break;
		default:
			throw "Invalid game mode reponse!";
			break;
	}

	// Construct POST request to game controls
	var form = document.createElement('form');
    document.body.appendChild(form);
    form.method = 'post';
    form.action = url;

    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = "name";
    input.value = $("#name").val();
    form.appendChild(input);

    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = "host";
    input.value = $("#host").val();
    form.appendChild(input);
    
    form.submit();

}