// This is the main script
// load this script into Arduino UNO to control the OC box
// To test the proper functionality of the OC box write INPUT COMMANDS on the serial monitor
//
// INPUT COMMANDS: 
//  4   Reward
//  3   Dot Stim Both [ Double dots - No wrong response ]
//  1   Dot Stim Left [One dot on the left]
//  2   Dot Stim Right [One dot on the right]
//  5   LCD - BOTH no stimuli are shown but both buttons trigger a reward
//  6   LCD - LEFT no stimuli are shown but left button triggers a reward
//  7   LCD - RIGHT no stimuli are shown but right button triggers a reward
//  13  Dot Stim Both [Extinction] -stub [No reward]
//  11  Dot Stim Left [Extinction] -stub [One dot on the left - No reward]
//  12  Dot Stim Right [Extinction] -stub [One dot on the right - No reward]
//  21  Dot Stim Left [reverse criterion] -stub [One dot on the left - reward on the other side]
//  22  Dot Stim Right [reverse criterion] -stub [One dot on the right - reward on the other side]
//  50  Recharge [recharge syringe pump]
//  51  Refill [push continuously the syringe pump]
//  0   Stop 

//------ EDIT THE PARAMETERS BELOW TO CUSTOMIZE YOUR EXPERIMENT ------         

// BUTTONS CAPACITIVE THRESHOLDs (set this value using skinnerCapacitiveTest.ino) 
int thrsx=200;
int thrdx=200;
// PERMANENCE OF STIMULUS AFTER THE RESPONSE [milliseconds]
int stimPermanenceRight = 2500;
int stimPermanenceWrong = 1000;

//------ END OF EDITABLE CODE ------

unsigned long startTime;
unsigned long reactionTime;
int cdx;
int csx;

int resetPin=12;

void setup() {
  ledInit();
  Serial.begin(9600); // Initializzation of Serial communication
}

void loop() {
  delay(2);
 
    if (Serial.available()){ // check for Serial input
      
    
    int cmd = Serial.parseInt();
    // If a serial message is available, it is parsed in an integer and the following if, 
    // elseif statements guide the arduino behavior accordingly 
    
    if(cmd==4){                             // REWARD
      correct();
      Serial.println("reward");
      reward();
      clearScreen();
    }else if (cmd ==1){                     // Dot Stim Left
      clearScreen();
      drawLeft();
      startTime=millis();
      while (true){
        cdx = checkDx();
        csx = checkSx();
        if (csx >= thrsx | cdx >= thrdx){
          reactionTime = millis() - startTime;
          if (csx >= thrsx){
            correct();
            Serial.print("yes : ");
            Serial.println(reactionTime,DEC);
            reward();
            delay(stimPermanenceRight);
            
          }else if(cdx >= thrdx){
            wrong();
            Serial.print("no : ");
            Serial.println(reactionTime,DEC);
            delay(stimPermanenceWrong);
            
            }
          
          break;
          }else if(Serial.available()){
            Serial.println("skipped");
            break;
        }
      }
      clearScreen();
    }else if (cmd == 6){                          // LCD Stim Left
      startTime=millis();
      while (true){
        cdx = checkDx();
        csx = checkSx();
        if (csx >= thrsx | cdx >= thrdx){
          reactionTime = millis() - startTime;
          if (csx >= thrsx){
            correct();
            Serial.print("yes : ");
            Serial.println(reactionTime,DEC);
            reward();
            
          }else if(cdx >= thrdx){
            wrong();
            Serial.print("no : ");
            Serial.println(reactionTime,DEC);
            
            }
          
          break;
          }else if(Serial.available()){
            Serial.println("skipped");
            break;
        }
      }
      clearScreen();
    } else if (cmd ==11){                     // Dot Stim Left [Extinction] 
      clearScreen();
      drawLeft();
      startTime=millis();
      while (true){
        cdx = checkDx();
        csx = checkSx();
        if (csx >= thrsx | cdx >= thrdx){
          reactionTime = millis() - startTime;
          if (csx >= thrsx){
            correct();
            Serial.print("yes : ");
            Serial.println(reactionTime,DEC);
            //reward();
            delay(stimPermanenceRight);
            
          }else if(cdx >= thrdx){
            wrong();
            Serial.print("no : ");
            Serial.println(reactionTime,DEC);
            delay(stimPermanenceWrong);
            
            }
          
          break;
          }else if(Serial.available()){
            Serial.println("skipped");
            break;
        }
      }
      clearScreen();
    }else if (cmd ==21){                    // Dot Stim Left [Reversed criterion]
      clearScreen();
      drawLeft();
      startTime=millis();
      while (true){
        cdx = checkDx();
        csx = checkSx();
        if (csx >= thrsx | cdx >= thrdx){
          reactionTime = millis() - startTime;
          if (csx >= thrsx){
             wrong();
            Serial.print("no : ");
            Serial.println(reactionTime,DEC);
            delay(stimPermanenceWrong);
            
          }else if(cdx >= thrdx){
            correct();
            Serial.print("yes : ");
            Serial.println(reactionTime,DEC);
            reward();
            delay(stimPermanenceRight);
            }
          
          break;
          }else if(Serial.available()){
            Serial.println("skipped");
            break;
        }
      }
      clearScreen();
    } else if(cmd==2){                        // Dot Stim Right
      clearScreen();
      drawRight();
      startTime=millis();
      while (true){
        cdx = checkDx();
        csx = checkSx();
        if (csx >= thrsx | cdx >= thrdx){
          reactionTime = millis() - startTime;
          if (csx >= thrsx){
            wrong();
             Serial.print("no : ");
            Serial.println(reactionTime,DEC);
            delay(stimPermanenceWrong);
           
          }else if(cdx >= thrdx){
            correct();
            Serial.print("yes : ");
            Serial.println(reactionTime,DEC);
            reward();
            delay(stimPermanenceRight);
            
          }
          
          break;
          }else if(Serial.available()){
            Serial.println("skipped");
            break;
        }
      }
      clearScreen();
    } else if(cmd==7){                          // LCD Stim Right
      startTime=millis();
      while (true){
        cdx = checkDx();
        csx = checkSx();
        if (csx >= thrsx | cdx >= thrdx){
          reactionTime = millis() - startTime;
          if (csx >= thrsx){
            wrong();
             Serial.print("no : ");
            Serial.println(reactionTime,DEC);
           
          }else if(cdx >= thrdx){
            correct();
            Serial.print("yes : ");
            Serial.println(reactionTime,DEC);
            reward();
          }
          
          break;
          }else if(Serial.available()){
            Serial.println("skipped");
            break;
        }
      }
      clearScreen();
    }else if(cmd==12){                            // Dot Stim Right [Extinction]
      clearScreen();
      drawRight();
      startTime=millis();
      while (true){
        cdx = checkDx();
        csx = checkSx();
        if (csx >= thrsx | cdx >= thrdx){
          reactionTime = millis() - startTime;
          if (csx >= thrsx){
            wrong();
             Serial.print("no : ");
            Serial.println(reactionTime,DEC);
            delay(stimPermanenceWrong);
           
          }else if(cdx >= thrdx){
            correct();
            Serial.print("yes : ");
            Serial.println(reactionTime,DEC);
            
            delay(stimPermanenceRight);
            
          }
          
          break;
          }else if(Serial.available()){
            Serial.println("skipped");
            break;
        }
      }
      clearScreen();
    }else if(cmd==22){                            // Dot Stim Right [Reversed criterion]
      clearScreen();
      drawRight();
      startTime=millis();
      while (true){
        cdx = checkDx();
        csx = checkSx();
        if (csx >= thrsx | cdx >= thrdx){
          reactionTime = millis() - startTime;
          if (csx >= thrsx){
            correct();
            Serial.print("yes : ");
            Serial.println(reactionTime,DEC);
            reward();
            delay(stimPermanenceRight);
            
          }else if(cdx >= thrdx){
            wrong();
            Serial.print("no : ");
            Serial.println(reactionTime,DEC);
            delay(stimPermanenceWrong);
           
          }
          
          break;
          }else if(Serial.available()){
            Serial.println("skipped");
            break;
        }
      }
      clearScreen();
    }else if(cmd==3){                           // Dot Stim Both
      clearScreen();
      drawRight();
      drawLeft();
      startTime=millis();
       while (true){
        cdx = checkDx();
        csx = checkSx();
        if (csx >= thrsx | cdx >= thrdx){
          reactionTime = millis() - startTime;
          if (csx >= thrsx){
            correct();
            Serial.print("both_SX : ");
            Serial.println(reactionTime,DEC);
            reward();
            delay(stimPermanenceRight);
            
          }else if(cdx >= thrdx){
            correct();
            Serial.print("both_DX : ");
            Serial.println(reactionTime,DEC);
            reward();
            delay(stimPermanenceRight);
            
          }
          
          break;
          }else if(Serial.available()){
              Serial.println("skipped");
              break;
          }
      }
      clearScreen();
    }else if(cmd==5){                                   // LCD Stim Both
      startTime=millis();
       while (true){
        cdx = checkDx();
        csx = checkSx();
        if (csx >= thrsx | cdx >= thrdx){
          reactionTime = millis() - startTime;
          if (csx >= thrsx){
            correct();
            Serial.print("both_SX : ");
            Serial.println(reactionTime,DEC);
            reward();
            
          }else if(cdx >= thrdx){
            correct();
            Serial.print("both_DX : ");
            Serial.println(reactionTime,DEC);
            reward();
            delay(stimPermanenceRight);
            
          }
          
          break;
          }else if(Serial.available()){
              Serial.println("skipped");
              break;
          }
      }
      clearScreen();
    }else if(cmd==13){                        // Dot Stim Both [extinction]
      clearScreen();
      drawRight();
      drawLeft();
      startTime=millis();
       while (true){
        cdx = checkDx();
        csx = checkSx();
        if (csx >= thrsx | cdx >= thrdx){
          reactionTime = millis() - startTime;
          if (csx >= thrsx){
            correct();
            Serial.print("both_SX : ");
            Serial.println(reactionTime,DEC);
            delay(stimPermanenceRight);
            
          }else if(cdx >= thrdx){
            correct();
            Serial.print("both_DX : ");
            Serial.println(reactionTime,DEC);
            
            delay(stimPermanenceRight);
            
          }
          
          break;
          }else if(Serial.available()){
              Serial.println("skipped");
              break;
          }
      }
      clearScreen();
    }else if(cmd==50){                      // Recharge the reward tube
      Serial.println("recharging...");
      int count = 0;
      while (true){
     
        if(Serial.available()){
              Serial.println("stop");
              break;
          }else{
            recharge();
            if(count%5){
              warning();
            }
            count++;
          }
      }
    }else if(cmd==51){                    // Refill the reward tube
      Serial.println("refilling...");
      int count = 0;
      while (true){
        if(Serial.available()){
              Serial.println("stop");
              break;
          }else{
            fill();
            if(count%5){
              warning();
            }
            count++;
          }
      }
    }else{
      Serial.println("other");
      clearScreen();
    }

  }
}
