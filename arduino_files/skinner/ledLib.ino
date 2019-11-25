#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6

Adafruit_NeoPixel strip = Adafruit_NeoPixel(64, PIN, NEO_GRB + NEO_KHZ800);

int brightness =60;
int redIntensity = 255;
int blueIntensity=255;  // 0.22 cd/m2
int greenIntensity = 255;


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

void drawRight(){
  drawBlueDot(6,6);
}

void drawLineH(){
  drawBlueDot(1,2);
  drawBlueDot(2,2);
  drawBlueDot(3,2);
  drawBlueDot(4,2);
  drawBlueDot(5,2);
  drawBlueDot(6,2);

  drawBlueDot(1,5);
  drawBlueDot(2,5);
  drawBlueDot(3,5);
  drawBlueDot(4,5);
  drawBlueDot(5,5);
  drawBlueDot(6,5);
}

void drawLineV(){
  drawBlueDot(2,1);
  drawBlueDot(2,2);
  drawBlueDot(2,3);
  drawBlueDot(2,4);
  drawBlueDot(2,5);
  drawBlueDot(2,6);

  drawBlueDot(5,1);
  drawBlueDot(5,2);
  drawBlueDot(5,3);
  drawBlueDot(5,4);
  drawBlueDot(5,5);
  drawBlueDot(5,6);
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

void line2number(int *lineIndexes, int startingPixelRow, int startingPixelColumn, int orientation, int lineLength, int matrixOrientation){
  
  // Cycle for all the pixels
  switch(orientation){
    case 0:
      for(int i=0; i<lineLength; i++){
        lineIndexes[i] = matrix2number(startingPixelRow,startingPixelColumn+i,matrixOrientation);
      }
      break;
    case 45:
      for(int i=0; i<lineLength; i++){
        lineIndexes[i] = matrix2number(startingPixelRow-i,startingPixelColumn+i,matrixOrientation);
      }
      break;
    case 90:
      for(int i=0; i<lineLength; i++){
        lineIndexes[i] = matrix2number(startingPixelRow-i,startingPixelColumn,matrixOrientation);
      }
      break;
    case 135:
      for(int i=0; i<lineLength; i++){
        lineIndexes[i] = matrix2number(startingPixelRow-i,startingPixelColumn-i,matrixOrientation);
      }
      break;
    case 180:
      for(int i=0; i<lineLength; i++){
        lineIndexes[i] = matrix2number(startingPixelRow,startingPixelColumn-i,matrixOrientation);
      }
      break;
    case -135:
      for(int i=0; i<lineLength; i++){
        lineIndexes[i] = matrix2number(startingPixelRow+i,startingPixelColumn-i,matrixOrientation);
      }
      break;
    case -90:
      for(int i=0; i<lineLength; i++){
        lineIndexes[i] = matrix2number(startingPixelRow+i,startingPixelColumn,matrixOrientation);
      }
      break;
    case -45:
      for(int i=0; i<lineLength; i++){
        lineIndexes[i] = matrix2number(startingPixelRow+i,startingPixelColumn+i,matrixOrientation);
      }
      break;
  }
}

void drawLine(int *lineIndexes, int lineLength , int R, int G, int B){

  for(int i=0; i<lineLength; i++){
    strip.setPixelColor(lineIndexes[i],R,G,B);
  }
  strip.show();
}

void clearScreen(){
    for(int i=0;i<strip.numPixels();i++){
      strip.setPixelColor(i,0, 0, 0);    
    }
    strip.show();
}

void square2number(int *squareIndexes, int startingPixelRow, int startingPixelColumn, int width, int height, int matrixOrientation){
  for(int w=0; w<width; w++){
    for(int h=0; h<height; h++){
      squareIndexes[(w*height)+h] = matrix2number(startingPixelRow+h,startingPixelColumn+w,matrixOrientation);
    }
  }
}

