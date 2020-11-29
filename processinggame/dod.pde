import mqtt.*;

MQTTClient client;




void playerConnected(String name){
  names.add(name);
  hasnamevoted.add(0);
  // Code here
  println("Player Connected: " + name);
}

void playerDisconnected(String name){
  println("Player Disconnected: " + name);
  int i = getNameIndex(name);
  names.remove(name);
  hasnamevoted.remove(i);
  
}

void playerVote(String name, int vote){
  println("Player Voted: " + name + " - " + vote);
   //get the players index for the bool arraylist
  int i = getNameIndex(name);
  //println("test");
  //println(i);
  //println(names.size());
  //println(hasnamevoted.size());
   //if they have voted they can revote
  int playersvote = hasnamevoted.get(i);
  if (playersvote>0){
    //println("Hello");
    votes[playersvote-1]--;
    //println("World");
    votes[vote-1]++;
    hasnamevoted.set(i, vote);
  }
  else{
    votes[vote-1]++;
    hasnamevoted.set(i,vote);
  }
}

void setVoteCount(int numButtons){
  // Set the number of buttons the player has access to
  sendMessage("move/player", String.valueOf(numButtons));
}

void disconnect(){
  // Send all users back to the home screen
  sendMessage("move/player", "disconnected");
}
