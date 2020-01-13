
# This class is a proof of principle on how to manage a LCD display
# to show visual stimuli

from psychopy import core, visual
import os

KANITSA_SQUARE = os.getcwd() + os.path.sep + "test_images" + os.path.sep + "iSquare.png"
KANITSA_TRIANGLE = os.getcwd() + os.path.sep + "test_images" + os.path.sep + "iTriangle.png"
CIRCLE =  os.getcwd() + os.path.sep + "zener" + os.path.sep + "circle.png"
CROSS =  os.getcwd() + os.path.sep + "zener" + os.path.sep + "cross.png"
SQUARE =  os.getcwd() + os.path.sep + "zener" + os.path.sep + "square.png"
STAR =  os.getcwd() + os.path.sep + "zener" + os.path.sep + "star.png"
WAVES =  os.getcwd() + os.path.sep + "zener" + os.path.sep + "waves.png"

class LCD:
    
    def __init__(self,fullscr=False,res=(200,200)):
        self.win = visual.Window(res, monitor="testMonitor",fullscr=fullscr)
        self.size = (.6,1)
        
    def stim(self,where="both", what=WAVES):
        if where == "both":
            self.stimBoth(what)
        if where == "left":
            self.stimLeft(what)
        if where == "right":
            self.stimRight(what)
        self.win.flip()
            
    def stimBoth(self,what = WAVES):
        (h,w) = self.win.size
        print("size w: ", h,w)
        self.stim1 = visual.ImageStim(self.win, image=what,pos=(-0.5,0),size=self.size) 
        self.stim2 = visual.ImageStim(self.win, image=what,pos=(0.5,0),size=self.size) 
        self.stim1.draw()
        self.stim2.draw()
    
    def stimRight(self,what=WAVES):
        self.stim1 = visual.ImageStim(self.win, image=what,pos=(0.5,0),size=self.size) 
        self.stim1.draw()
        
    def stimLeft(self,what=WAVES):
        self.stim1 = visual.ImageStim(self.win, image=what,pos=(-0.5,0),size=self.size) 
        self.stim1.draw()

     
        
    def refresh(self):
        self.win.flip()
    
    def close(self):
        self.win.close()

# EXAMPLE ON HOW TO USE LCD CLASS
if __name__=='__main__':
    lcd = LCD(fullscr=True)
    lcd.stimBoth(KANITSA_TRIANGLE)
    lcd.refresh()
    core.wait(3)
    lcd.refresh()
    core.wait(0.5)
    lcd.stimLeft(KANITSA_TRIANGLE)
    lcd.refresh()
    core.wait(4)
    lcd.refresh()
    core.wait(0.5)
    lcd.stimRight(KANITSA_TRIANGLE)
    lcd.refresh()

    core.wait(4)
    lcd.refresh()
    core.wait(6)
    
    lcd.close()

