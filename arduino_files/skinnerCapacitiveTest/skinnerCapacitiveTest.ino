
#include <CapacitiveSensor.h>


CapacitiveSensor   dx = CapacitiveSensor(3,4);       
CapacitiveSensor   sx = CapacitiveSensor(2,5); 

int buzzer=7;
long val;
void setup() {
  // put your setup code here, to run once:
  digitalWrite(12,HIGH);
  pinMode(12,OUTPUT);
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
val=dx.capacitiveSensor(10);
Serial.println(val);
if (val>500){
  tone(buzzer, 200); // 
  delay(100);
  digitalWrite(12,LOW);
}else{
  noTone(buzzer);
}
delay(2);

}

