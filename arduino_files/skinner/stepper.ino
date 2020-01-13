// This file contains the code to control reward delivery
#include "Stepper.h"
#define STEPS 32   // Number of steps per revolution of Internal shaft
//int  Steps2Take  Number of steps per revolution of Internal shaft 
// 2048 = 1 Revolution, 256=7 microliters
int REWARD = 256; // number of steps during reward

// Stepper initialization
Stepper small_stepper(STEPS, 8, 10, 9, 11);

// low level stepper movements
void moveCW(int Steps2Take){
  small_stepper.setSpeed(600); //Max seems to be 700
  small_stepper.step(Steps2Take);
}

void moveCCW(int Steps2Take){
  small_stepper.setSpeed(500); //Max seems to be 700
  small_stepper.step(-Steps2Take);
}

// high levele movements
void reward(){
  moveCW(REWARD);
}

// move piston back
void recharge(){
  moveCCW(2048);
}

// move push piston 
void fill(){
  moveCW(1024);
}

