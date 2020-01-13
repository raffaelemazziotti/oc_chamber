// This script is used to calibrate capacitive buttons
// It's helpful to set a proper threshold level of the capacitive sensors
// It prints sensor capacitive sensor values using serial port 

#include <CapacitiveSensor.h>

CapacitiveSensor   right = CapacitiveSensor(3,4);       
CapacitiveSensor   left = CapacitiveSensor(2,5); 

int buzzer=7; // buzzer pin number
int tonehz = 200;  // tone frequency
int threshold = 500; // threshold
long val;

void setup() 
{
  Serial.begin(9600); // initialize serial communication
}

void loop() 
{
  // change between "left"[sx] and "right"[dx] sensor to print 
  // values from the corrisponding button
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

