// variables to store background images
PImage lobbybg, bg4, bg3, bg2, bgend;
ArrayList<String> names = new ArrayList<String>();
ArrayList<Integer> hasnamevoted = new ArrayList<Integer>();
// main data structure to store the scenarios
ArrayList<Scenario> scenarios = new ArrayList<Scenario>();

// variable holds the currently displayed scenario
Scenario currentScenario;

// variable holds the timer
Timer timer;

// game states
boolean inLobby = true;

// voting structure initialisation
int[] votes = new int[4];

// structure that contains a description, text for four options, and the scenario number that each option leads to
class Scenario {
  String desc, opt1, opt2, opt3, opt4, end;
  int opt1Pointer, opt2Pointer, opt3Pointer, opt4Pointer;
  Scenario(String dsc, String o1, String o2, String o3, String o4, int o1p, int o2p, int o3p, int o4p, String ending) {
    desc = dsc;
    opt1 = o1;
    opt2 = o2;
    opt3 = o3;
    opt4 = o4;
    opt1Pointer = o1p;
    opt2Pointer = o2p;
    opt3Pointer = o3p;
    opt4Pointer = o4p;
    end = ending;
  }
  
  // returns the scenario pointer based on the numbered option
  int returnPointer(int pointerNumber){
  if (pointerNumber == 1){
    return opt1Pointer;
  }
  else if (pointerNumber == 2){
    return opt2Pointer;
  }
  else if (pointerNumber == 3){
    return opt3Pointer;
  }
  else if (pointerNumber == 4){
    return opt4Pointer;
  }
  return 0;
}
// returns the ending
  String returnEnding(){
    return end;
}
  // updates the graphics to accomodate the scenario
  void drawScenario() {
    // draw the description text
    clear();
    if (currentScenario.countOptions() == 4){
      background(bg4);
    }
    else if (currentScenario.countOptions() == 3){
      background(bg3);
    }
    else if (currentScenario.countOptions() == 2){
      background(bg2);
    }
    fill(50);
    textSize(20);
    text(desc, width*0.15, height*0.15, width*0.75, height*0.25);
    // display options that have text in
    if (end.equals("-")){
      if (opt1.length() > 0) {
        text(str(votes[0]), width*0.025, height*0.575, width*0.125, height*0.625);
        text(opt1, width*0.125, height*0.55, width*0.8, height*0.625);
      }
      if (opt2.length() > 0) {
        text(str(votes[1]), width*0.025, height*0.675, width*0.125, height*0.625);
        text(opt2, width*0.125, height*0.65, width*0.8, height*0.725);
      }
      if (opt3.length() > 0) {
        text(str(votes[2]), width*0.025, height*0.775, width*0.125, height*0.625);
        text(opt3, width*0.125, height*0.75, width*0.8, height*0.825);
      }
      if (opt4.length() > 0) {
        text(str(votes[3]), width*0.025, height*0.875, width*0.125, height*0.625);
        text(opt4, width*0.125, height*0.85, width*0.8, height*0.925);
      }
    }
    else{
      background(bgend);
      fill(255);
      textSize(30);
      text(desc, width*0.1,height*0.15,width*0.9, height*0.5);
      text(opt1, width*0.1,height*0.4,width*0.9, height*0.6);
      String help = "The host can click again to restart, or press q to exit.";
      text(help, width*0.1, height*0.7, width*0.9, height*0.9);
    }
  }
  // returns the number of possible options this scenario has
  int countOptions() {
    int c = 0;
    if (opt1.length() > 0) {
      c++;
    }
    if (opt2.length() > 0) {
      c++;
    }
    if (opt3.length() > 0) {
      c++;
    }
    if (opt4.length() > 0) {
      c++;
    }
    return c;
  }
}

// this class implements a circular timer with text in displaying the number of seconds left
class Timer{
  boolean running = false;
  int starttime = 0;
  int endtime = 0;
  int xpos;
  int ypos;
  int size;
  int secs;
  
  //constructor
  Timer(int x1, int y1, int s, int sec){
    xpos = x1;
    ypos = y1;
    size = s;
    secs = sec;
  }
  
  // returns if the timer is active
  boolean getRunning(){
    return running;
  }
  void stopRunning(){
    running = false;
  }
  
  // updates the graphics of the timer to accomodate the countdown changes
  void update(){
    circle(xpos, ypos, size);
    fill(255);
    if (secondsRemaining() >= 0){
      text(str(secondsRemaining()),xpos-10,ypos+5);
    }
    if (secondsRemaining() < 0){
      getRoundResults();
      this.startTimer();
    }
  }
  // starts the timer
  void startTimer(){
    running = true;
    starttime = millis();
    endtime = starttime+(secs*1000);
  }

  // returns the time remaining, in seconds
  int secondsRemaining(){
    int milli_left = endtime - millis();
    int sec_left = int(milli_left/1000);
    return sec_left;
  }
}

// setup function that takes in the formatted text file, and creates Scenario objects, putting them in the ArrayList scenarios
void setupScenarios(String[] masterStr) {
  // loops through every 5 lines to generate a scenario object that holds the position and 4 options
  int option1pointer=0, option2pointer=0, option3pointer =0, option4pointer = 0;
  for (int i=0; i<masterStr.length; i = i+5){
    //println(masterStr[i]);
    String[] linedata = split(masterStr[i], "|");
    /*int counter = 1;
    for (String line:linedata){
      print(str(counter));
      print(": " + line);
      println();
      counter++;
    }*/
    String[] o1 = split(masterStr[i+1], "|");
    String[] o2 = split(masterStr[i+2], "|");
    String[] o3 = split(masterStr[i+3], "|");
    String[] o4 = split(masterStr[i+4], "|");
    
    if (o1.length > 1){
      option1pointer = int(o1[1]);
    }
    if (o2.length > 1){
      option2pointer = int(o2[1]);
    }
    if (o3.length > 1){
      option3pointer = int(o3[1]);
    }
    if (o4.length > 1){
      option4pointer = int(o4[1]);
    }
    Scenario s = new Scenario(linedata[1],o1[0],o2[0],o3[0],o4[0], option1pointer, option2pointer, option3pointer, option4pointer, linedata[2]);
    scenarios.add(s);
   }
   currentScenario = scenarios.get(0);
}

// MAIN SETUP FUNCTION - one time setup
void setup() {
  // prepare screen size
  //fullScreen();
  size(1000, 800);
  
  client = new MQTTClient(this);
  client.connect("mqtt://test.mosquitto.org", "dod");
  client.setWill("move/player", "disconnected"); // Sent upon disconnect
  names.add("dod");
  hasnamevoted.add(0);
  
  // prepare backgrounds
  lobbybg = loadImage("lobbyscreennew.png");
  lobbybg.resize(width, height);
  bg4 = loadImage("scenariobg.png");
  bg4.resize(width, height);
  bg3 = loadImage("scenariobg3.png");
  bg3.resize(width, height);
  bg2 = loadImage("scenariobg2.png");
  bg2.resize(width, height);
  bgend = loadImage("endingbg.png");
  bgend.resize(width, height);
  
  // load scenario data
  String[] masterStrings = loadStrings("scenarios.txt");
  setupScenarios(masterStrings);
  
  //initialise timer object
  timer = new Timer(40, 40, 40, 30);
}

// MAIN DRAW FUNCTION - updates the game every frame
void draw() {
  if (keyPressed) {
    if (key == 'q' || key == 'Q') {
      disconnect();
      exit();
    }
  }
  if (inLobby){
    background(lobbybg);
    int counter = 0;
    textSize(20);
    fill(0);
    for (String name : names){
      if (counter==0){continue;}
      text(name, width*0.3, height*0.3+(30*counter), width*0.7, height);
      counter++;
    }
  }
  else {
    currentScenario.drawScenario();
    if (timer.getRunning()){
      timer.update();
    }
  }
}
void getRoundResults(){
  if (currentScenario.countOptions()==3){votes[3]= -1;}
  if (currentScenario.countOptions()==2){votes[2]= -1;}
  int chosenOutcome = 0;
  IntList possibleoptions = new IntList();
  int mostVotes = max(votes);
  for (int i=1;i <= 4; i++){
    if (votes[i-1] == mostVotes){
      possibleoptions.append(i);
    }
  }
  if (possibleoptions.size()==1){
    chosenOutcome = possibleoptions.get(0);
  }
  else{
    int index = int(random(possibleoptions.size()));
    chosenOutcome = possibleoptions.get(index);
  }
  
  int newPointer = currentScenario.returnPointer(chosenOutcome);
  currentScenario = scenarios.get(newPointer);

  votes = new int[] {0,0,0,0};
  for (int i=0; i < hasnamevoted.size(); i++){hasnamevoted.set(i,0);}
  setVoteCount(currentScenario.countOptions());
  if (currentScenario.returnEnding().equals("-")){
    timer.startTimer();
  }
}

void mousePressed(){
  if (inLobby){
    inLobby = false;
    timer.startTimer();
  }
  else{
    getRoundResults();
  }
}
