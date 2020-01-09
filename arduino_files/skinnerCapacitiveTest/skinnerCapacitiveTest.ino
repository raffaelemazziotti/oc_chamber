// This script is used to test capacitive buttons
// and prints using serial port values detected by capacitive sensors

#include <CapacitiveSensor.h>


CapacitiveSensor   right = CapacitiveSensor(3,4);       
CapacitiveSensor   left = CapacitiveSensor(2,5); 

int buzzer=7; // buzzer pin number
int tonehz = 200; 
int threshold = 500;
long val;

void setup() 
{
  Serial.begin(9600); // initialize serial communication
}

void loop() 
{
  // change between "left" and "right" sensor to print 
  // values from the corrispondent button
  val=right.capacitiveSensor(10);
  Serial.println(val);
  if (val>threshold){
      tone(buzzer, tonehz); // if the value excedes a threshold the buzzer will produce a tone
      delay(100);
  }
  else
  {
      noTone(buzzer);
  }
  
  delay(2);
  
}

