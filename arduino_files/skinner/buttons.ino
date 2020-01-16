
// This file contains the code dedicated to capacitive sensor and tone control 
#include <CapacitiveSensor.h>

const int buzzer = 7;           //buzzer connected to pin 7
const int tone_correct = 3300;  // frequency in Hz of 'correct' tone
const int tone_wrong = 2700;    // frequency in Hz of 'wrong' tone

// capacitive sensors initialization
CapacitiveSensor   dx = CapacitiveSensor(3,4);        // Right capacitive sensor with 25M resistor between pins
CapacitiveSensor   sx = CapacitiveSensor(2,5);        // Left capacitive sensor with 25M resistor between pins
int capTime= 10; // capacitive function time integration  

// Functions to check capacitive sensors
int checkDx(){
  return  dx.capacitiveSensor(capTime);
}

int checkSx(){
  return  sx.capacitiveSensor(capTime);
}

// Tones

void correct(){
  tone(buzzer, tone_correct); // 
  delay(100);   
  noTone(buzzer);
}
void wrong(){
  tone(buzzer, tone_wrong); // 
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


