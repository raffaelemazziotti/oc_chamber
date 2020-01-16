// This script is used to calibrate capacitive buttons
// It's helpful to set a proper threshold level of the capacitive sensors
// It prints sensor capacitive sensor values using serial port 

//------ EDITABLE CODE ------

int threshold = 500;        // threshold for the capacitive buttons
char buttonToCheck = 'l';   // char can be "l" to test the left button or "r" to test the right button

//------ END OF EDITABLE CODE ------

if(buttonToCheck=='l'){
  CapacitiveSensor   button = CapacitiveSensor(2,5);  // left
}elseif(buttonToCheck=='r'){
  CapacitiveSensor   button = CapacitiveSensor(3,4);  // right  
}

#include <CapacitiveSensor.h>

int buzzer=7; // buzzer pin number
int tonehz = 200;  // tone frequency
long val;

void setup() 
{
  Serial.begin(9600); // initialize serial communication
}

void loop() 
{
  val=button.capacitiveSensor(10);
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