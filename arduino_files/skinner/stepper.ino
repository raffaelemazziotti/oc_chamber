#include "Stepper.h"
#define STEPS 32   // Number of steps per revolution of Internal shaft
//int  Steps2Take;  // 2048 = 1 Revolution
Stepper small_stepper(STEPS, 8, 10, 9, 11);

void moveCW(int Steps2Take){
  small_stepper.setSpeed(600); //Max seems to be 700
  //Steps2Take  =  256;  // Rotate CW
  small_stepper.step(Steps2Take);
  //delay(1000); 
  //break;
}

void moveCCW(int Steps2Take){
  small_stepper.setSpeed(500); //Max seems to be 700
  //Steps2Take  =  -256;  // Rotate CW
  small_stepper.step(-Steps2Take);
  //delay(2000); 
 // break;
}

void reward(){
  moveCW(256);
}

void recharge(){
  //rechargingON();
  moveCCW(2048);
  //rechargingOFF();
}

void fill(){
  //rechargingON();
  moveCW(1024);
  //rechargingOFF();
}

