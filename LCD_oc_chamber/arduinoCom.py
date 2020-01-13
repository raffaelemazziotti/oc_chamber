
import libSerial
import time
from skinnerTrial import *
import threading

class Arduino():
    
    def __init__(self,port=None):
        # CONNECTION 
        self.com = libSerial.connect(port)
        time.sleep(1) # REQUIRED TO WAIT FOR ARDUINO CONNECTION 

        # THIS IS REQUIRED BECAUSE SOMETIMES ARDUINO RETURNS PARTIAL EVENTS
        self.casey = ['yes','y','e','s','ye','ys','es']  
        self.casen = ['no','n','o']
        self.caseBoth= ['both_dx', 'both_sx']

        self.answer=threading.Thread()
        self.session = ListTrial() # LIST OF TRIALS
        
    def disconnect(self):
        self.com.close

    ## RETURNS A TRIAL
    def read(self,event = None):
        libSerial.flushInput(self.com)
        time.sleep(.1)
        msg = libSerial.readline(self.com).decode("utf-8") 
        msg=msg.strip()
        res = msg.split(':')
        if len(res)==2:
            ## gestione risposte strane prima di assegnare il trial
            if res[0] and any(res[0].lower().strip() in s for s in self.casey):
                res[0]='yes'
            elif res[0] and any(res[0].lower().strip() in s for s in self.casen):
                res[0]='no'
            else:
                print('ARDUINO: strange message received: ',res[0])
            trial = Trial(event,res[0].strip(),res[1].strip())
            self.session.add(trial)
            print(trial.getStr())
        else:
            if msg.strip() == 'reward':
                trial = Trial(event,msg.strip())
                self.session.add(trial)
                print(trial.getStr())
            else:
                print(msg)
    # SEND EVENT
    def event(self,seq=None):
        if seq is not None:
            print('Sending event: ',seq)
            libSerial.write(self.com,self.seq2cmd(seq.lower()))
            if self.answer.is_alive():
                self.answer.join()
            self.answer=threading.Thread(target=self.read,kwargs=dict(event=seq))
            self.answer.start()

    # WAIT FOR RESPONSE
    def wait(self):
        if self.answer.isAlive():
            self.answer.join()
            
    def isWaiting(self):
        return self.answer.isAlive()
    
    # CONVENIENCE FUNCTION TO CONVERT STRINGS TO ARDUINO COMMANDS
    def seq2cmd(self,argument):
        switcher = {
            'l':'1','r':'2','b':'3','f':'5','m':'6','h':'7','v':'8',
            'left':'1','right':'2','both':'3','few':'5','many':'6',
            'hor':'7','vert':'8','stop':'0',
            'el':'11','er':'12','eb':'13','eleft':'11','eright':'12','eboth':'13',
            'rl':'21','rr':'22','rleft':'21','rright':'22',
            }
        return switcher.get(argument.lower(), 0)
    
    # CONVENIENCE FUNCTION TO CONVERT ARDUINO COMMANDS TO STRINGS
    def cmd2seq(self,argument):
        switcher = {
            '1':'left','2':'right','3':'both','5':'few','6':'many'
            ,'7':'hor','8':'vert','0':'stop'
            }
        return switcher.get(argument.lower(), 0)


# EXAMPLE ON HOW TO USE ARDUINO CLASS
if __name__=='__main__':
    print('Connecting...')
    arduino = Arduino()
    print('Sending an Event:')
    conds=['Left','right','hor']
    for i in range(0,len(conds)):
        arduino.event(conds[i])
        while arduino.isWaiting(): # TOUCH ONE OF THE BUTTONS ON THE OC BOX
            time.sleep(.1) 
        time.sleep(2)
        
    if arduino.session.tot():
        print('writing to file...')
        arduino.session.toFile('session')
    arduino.disconnect()

    
