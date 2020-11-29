boolean inNames(String s){
  for(int i = 0; i < names.size(); i++){
    if(names.get(i).equals(s)) return true;
  }
  return false;
}
int getNameIndex(String s){
  for(int i = 0; i < names.size(); i++){
    if(names.get(i).equals(s)) return i;
  }
  return -1;
}

void sendMessage(String topic, String message){
  client.publish(topic, message);
}

void messageReceived(String topic, byte[] payload) {
  String payloadStr = new String(payload);
  print(topic + payloadStr);
  if(topic.equals("check/server")){
    if(inNames(payloadStr.substring(0, payloadStr.length() - 3))){
      sendMessage("check/player/" + payloadStr, "n");
    }else{
      playerConnected(payloadStr.substring(0, payloadStr.length() - 3));
      sendMessage("check/player/" + payloadStr, "dod");
    }
  }else if(topic.equals("move/server")){
    if(payloadStr.length() >= 4){
      if(payloadStr.substring(payloadStr.length() - 4, payloadStr.length()).equals("lost")){
        // The player has disconnected ("lost" at the end of the string)
        playerDisconnected(payloadStr.substring(0, payloadStr.length()- 4));
      }else{
        // The player has made a move, the last character is the name
        playerVote(payloadStr.substring(0, payloadStr.length() - 1),
        Integer.valueOf(payloadStr.substring(payloadStr.length() - 1, payloadStr.length())));
      }
    }else{
      // The player has made a move, the last character is the name
      playerVote(payloadStr.substring(0, payloadStr.length() - 1),
      Integer.valueOf(payloadStr.substring(payloadStr.length() - 1, payloadStr.length())));
    }
  }
}

void subscriptions(){
  client.subscribe("check/server");
  client.subscribe("move/server");
  print("subscribed");
}

void clientConnected() {
  println("client connected");
  subscriptions();
}

void connectionLost() {
  println("connection lost");
}
