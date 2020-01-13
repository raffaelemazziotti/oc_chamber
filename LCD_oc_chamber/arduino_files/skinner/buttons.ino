
#include <CapacitiveSensor.h>
const int buzzer = 7; //buzzer to arduino pin 7
const int recharger = 12; // che anche reset
//CapacitiveSensor   licker = CapacitiveSensor(3,12);        // 20M resistor between pins 3 & 2, pin 2 is sensor pin, add a wire and or foil if desired
CapacitiveSensor   dx = CapacitiveSensor(3,4);        // 10M resistor between pins
CapacitiveSensor   sx = CapacitiveSensor(2,5);        // 10M resistor between pins
int capTime= 10; // time integration for se 

void initButtons(){
  pinMode(buzzer, OUTPUT);
  digitalWrite(recharger, HIGH);
  delay(200); 
  pinMode(recharger, OUTPUT);
}

int checkDx(){
  //dx.reset_CS_AutoCal();
  return  dx.capacitiveSensor(capTime);
}

int checkSx(){
  //sx. reset_CS_AutoCal();
  return  sx.capacitiveSensor(capTime);
}

//void recalbtn(){
  //dx = CapacitiveSensor(3,4);
  //sx = CapacitiveSensor(3,5);
  //digitalWrite(resetPin,LOW);
//}


 
//int checkReward(){
  //return  licker.capacitiveSensor(10);
//}

void correct(){
  tone(buzzer, 3300); // 
  delay(100);   
  noTone(buzzer);
}

void wrong(){
  tone(buzzer, 2700); // 
  delay(100);     
  noTone(buzzer);
}

void warning(){
  tone(buzzer, 400); // 
  delay(50);        
  tone(buzzer, 500);
  delay(50);
  noTone(buzzer);
}


void btnCheckRecharge(){
  if (!digitalRead(recharger)){
    correct();
    Serial.print("Recharging...");
    delay(1000);
    while (digitalRead(recharger)){
      recharge();
    }
    correct();
    Serial.println("end.");
    delay(1000);
  }
}

