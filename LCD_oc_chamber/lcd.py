
# This class is a proof of principle on how to manage a LCD display
# to show visual stimuli

from psychopy import core, visual
import os

# convenience variable to default image paths
KANITSA_SQUARE = os.getcwd() + os.path.sep + "test_images" + os.path.sep + "iSquare.png"
KANITSA_TRIANGLE = os.getcwd() + os.path.sep + "test_images" + os.path.sep + "iTriangle.png"
CIRCLE =  os.getcwd() + os.path.sep + "zener" + os.path.sep + "circle.png"
CROSS =  os.getcwd() + os.path.sep + "zener" + os.path.sep + "cross.png"
SQUARE =  os.getcwd() + os.path.sep + "zener" + os.path.sep + "square.png"
STAR =  os.getcwd() + os.path.sep + "zener" + os.path.sep + "star.png"
WAVES =  os.getcwd() + os.path.sep + "zener" + os.path.sep + "waves.png"

class LCD:
    
    def __init__(self,fullscr=False,res=(200,200)):
        self.win = visual.Window(res, monitor="testMonitor",fullscr=fullscr) # open window
        self.size = (.6,1) # stimulus size in norm units
    
    # draw stimulus at location ["both":two visual stimuli "left": stimulus in the left side "right": stimulus in the right side]
    # what is the path to image 
    def stim(self,where="both", what=WAVES):
        if where == "both":
            self.stimBoth(what)
        if where == "left":
            self.stimLeft(what)
        if where == "right":
            self.stimRight(what)
        self.win.flip()
    
    # draw stimulus at location "both" without showing 
    def stimBoth(self,what = WAVES):
        (h,w) = self.win.size
        print("size w: ", h,w)
        self.stim1 = visual.ImageStim(self.win, image=what,pos=(-0.5,0),size=self.size) 
        self.stim2 = visual.ImageStim(self.win, image=what,pos=(0.5,0),size=self.size) 
        self.stim1.draw()
        self.stim2.draw()
    # draw stimulus at location "right" without showing 
    def stimRight(self,what=WAVES):
        self.stim1 = visual.ImageStim(self.win, image=what,pos=(0.5,0),size=self.size) 
        self.stim1.draw()
    
    # draw stimulus at location "left" without showing 
    def stimLeft(self,what=WAVES):
        self.stim1 = visual.ImageStim(self.win, image=what,pos=(-0.5,0),size=self.size) 
        self.stim1.draw()

     
    # refresh monitor 
    def flip(self):
        self.win.flip()

    # close window
    def close(self):
        self.win.close()
    
    def wait(sec=0):
        core.wait(sec)

# EXAMPLE ON HOW TO USE LCD CLASS
if __name__=='__main__':
    lcd = LCD(fullscr=True) # fullscr= True for full screen
    lcd.stimBoth(KANITSA_TRIANGLE)
    lcd.flip() # refresh to show stimuli
    lcd.wait(3)
    lcd.flip() # refresh to show background
    lcd.wait(0.5)
    lcd.stimLeft(KANITSA_TRIANGLE)
    lcd.flip()
    lcd.wait(4)
    lcd.flip()
    lcd.wait(0.5)
    lcd.stimRight(KANITSA_TRIANGLE)
    lcd.flip()

    lcd.wait(4)
    lcd.flip()
    lcd.wait(6)
    
    lcd.close()

