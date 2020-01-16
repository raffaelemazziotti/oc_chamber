// This file contains the code to control Adafruit NeoPixel LED matrix
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6 // connected to pin 6

// setting variables
Adafruit_NeoPixel strip = Adafruit_NeoPixel(64, PIN, NEO_GRB + NEO_KHZ800);

int brightness =60;
int redIntensity = 255;
int blueIntensity=255;  // 0.9 cd/m2, for brightness = 60
int greenIntensity = 255;

// initialization
void ledInit(){
  randomSeed(analogRead(0));
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  clearScreen();
  strip.setBrightness(brightness);
}

void setBright(int bright){
  strip.setBrightness(bright);
}

// LEFT and RIGHT dot stimuli
void drawRight(){
  drawBlueDot(6,6);
}

void drawLeft(){
  drawBlueDot(1,6);
}

void drawBlueDot(int x, int y){
  int num = matrix2number(y,x,2);
  strip.setPixelColor(num,0,0,blueIntensity);
  strip.show();
}

void drawBlueDot(int x, int y,int luminance){
  int num = matrix2number(y,x,2);
  strip.setPixelColor(num,0,0,luminance);
  strip.show();
}

void drawGreenDot(int x, int y){
  int num = matrix2number(x,y,2);
  strip.setPixelColor(num,0,255,0);
  strip.show();
}

void drawRedDot(int x, int y){
  int num = matrix2number(x,y,2);
  strip.setPixelColor(num,redIntensity,0,0);
  strip.show();
}

void drawRGBDot(int x, int y,int red,int green,int blue){
  int num = matrix2number(x,y,2);
  strip.setPixelColor(num,red,green,blue);
  strip.show();
}

int matrix2number(int row, int column, int matrixOrientation){
  /*  Reurns a led number for low level led driving starting from row and column
   *  indexes (row and column are indexed starting from 0)
   *  
   *  Orientation means where is the position of LED number 0:
   *  1 = NE(north-east)
   *  2 = SE(southeast)
   *  3 = SW(southwest)
   *  4 = NW(northwest)  
  */

  row %= 8;
  column %= 8;
  
  int ledNumber = 64;
  switch (matrixOrientation){
    case 1:
      break;
    case 2:
      if(column%2 == 0){
      ledNumber -= (column*8);
      ledNumber -= (8-row);
      }
      else if(column%2 == 1){
      ledNumber -= (column*8);
      ledNumber -= (row+1);
      }
      break;
    case 3:
      break;
    case 4:
      break;
  }
  return ledNumber;
}


// switch all LED off
void clearScreen(){
    for(int i=0;i<strip.numPixels();i++){
      strip.setPixelColor(i,0, 0, 0);    
    }
    strip.show();
}


