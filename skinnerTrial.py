import time
import os
import random
import numpy as np

# STIMULUS
# simple : left,right,both
# extinction : eleft,eright,eboth
# reversal : rleft,rright

# MENAGAMENTS OF TRIALS AND PROCEDURES

TRAINING = 1        # ASSISTED PROCEDURE (see paper)
PERMUTATION = 2     # BALANCED PERMUTATED PROCEDURE 
EXT = '.txt'        # Output file extension

# Trial contains the representation of a trial
class Trial():
    def __init__(self,event=None,answer=None,rt=None):
        self.event = event
        self.answer = answer
        self.rt = rt
        self.time=time.strftime("%H:%M:%S_%d/%m/%Y")
        
    def getStr(self,sep = '\t'):
        if self.event is None:
            event='NaN'
        else:
            event=self.event
        
        if self.answer is None:
            answer='NaN'
        else:
            answer=self.answer
        
        if self.rt is None:
            rt='NaN'
        else:
            rt=str(self.rt)
            
        st='Event: ' + event + sep +'Answer: ' + answer + sep +'RT: ' + rt + sep +'Time: '+ self.time
        return st

#  ListTrial represents an array of trials
class ListTrial():
    def __init__(self,trial=None):
        self.trials=list()
        self.positive=0.0
        if trial is not None:
            self.trials.append(trial)
    # ADD A TRIAL
    def add(self,trial):
        self.trials.append(trial)
        if trial.answer == 'yes':
            self.positive=self.positive+1

    # NUMBER OF TRIALS
    def tot(self):
        return len(self.trials)

    # CALCULATE PERFORMANCE
    def performance(self):
        return self.positive/self.tot()
    
    # REMOVE TRIAL
    def remove(self,ind):
        self.trials.pop(ind)

    # RETURNS A LIST OF EVENTS
    def getEvents(self):
        ev=list()
        for t in self.trials:
            ev.append(t.event)
        return ev
    
    # RETURNS A LIST OF ASNWERS
    def getAnswers(self):
        ans=list()
        for t in self.trials:
            if t.answer is not None:
                ans.append(t.answer)
        return ans
    
    # RETURNS A LIST OF REACTION TIMES
    def getRT(self):
        rt=list()
        for t in self.trials:
            if t.rt is not None:
                rt.append(int(t.rt))
        return rt
    
    # RETURNS A ListTrial WITH SPECIFIED CONDITIONS
    def getSelection(self,event=None,answer=None):
        tr = ListTrial()
        for t in self.trials:
            
            if event is not None and answer is not None:
                
                if t.event.lower() == event.lower() and t.answer.lower() == answer.lower():
                    tr.add(t)
                    
            elif event is not None:
                
                if t.event.lower() == event.lower():
                    tr.add(t)
                    
            elif answer is not None:
                
                if t.answer.lower() == answer.lower():
                    tr.add(t)
                    
        return tr
    
    # COUNTS THE NUMBER OF TRIALS WITH SPECIFIED CONDITIONS
    def getCount(self,event=None,answer=None):
        return self.getSelection(event, answer).tot()
    
    # RETURNS A TRIAL AS STRING
    def str(self,ind):
        return self.trials[ind].getStr()
    
    # WRITES TRIALS
    def toFile(self,filename=None,path=None):
        if filename is None:
            filename=time.strftime("%Y%m%d_%H%M-") + EXT
        else:
            filename=time.strftime("%Y%m%d_%H%M-") + filename + EXT
            
        if path is None:
            path = os.path.join(os.getcwd(),'DATA')
            
        if not os.path.exists(path):
            os.makedirs(path)
            
        with open(os.path.join(path,filename),"w") as f:
            for t in self.trials:
                f.write(t.getStr() + "\n") 
       

# THIS CLASS MANAGES THE STIMULUS SEQUENCE
class Trainer():
    
    def __init__(self,conditions=['left','right'],type=TRAINING):
        self.conditions=conditions
        self.last=None
        self.type=type
        self.error = 0 # NUMBER OF COSECUTIVE ERRORS
        self.perseverance = 1  # NUMBER OF PREVIOUS TRIALS
        self.perseveranceThresh=3 # NUMBER OF HITS SWITCH TO PERMUTED SEQUENCE
        self.seq = None
        self.seqLength=10 # LENGTH OF THE PERMUTATION SEQUENCE
        self.seqInd = 0
        self.balancing=3 
    
    # RETURN THE NEXT TRIAL
    def next(self,trials=None):
        if len(self.conditions)==1:
            return self.conditions[0]
        elif self.type==TRAINING:
            return self.training(trials)
        elif self.type==PERMUTATION:
            return self.permutation()
        

    def training(self,trials):
        ## AT THE BEGINNING OF THE SESSION THE EVENT IS RANDOM
        if trials is None or self.last is None:
            self.last = random.choice((0,1))
            return self.conditions[self.last]
        else:
        # IN CASE OF WRONG ANSWER THE LAST STIMULUS IS REPEATED    
            if trials.getAnswers()[-self.perseverance:].count('no')>0:
                self.error = self.error +1
                return self.conditions[self.last] 
        # IN CASE OF RIGHT ANSWER THE LAST STIMULUS IS REPEATED UNTIL CRITERION IS REACHED    
            elif trials.getAnswers()[-1].count('yes')>0 and self.error>0 :
                self.perseverance=self.perseverance+1
                if self.perseverance >=self.perseveranceThresh:
                    self.perseverance=1
                    self.error=0 
                return self.conditions[self.last] 
            else:
                ev=[]
                for e in range(0,len(self.conditions)):
                    ev.append ( trials.getCount(self.conditions[e]) )
                minind = np.argmin(ev)
                maxind = np.argmax(ev)
                if ev[maxind]-ev[minind]>self.balancing :
                    self.last = minind
                    return self.conditions[self.last] 
                else:
                    self.last = random.choice((0,1))
                    return self.conditions[self.last]
        
                    
    # BALANCED PERMUTATED SEQUENCE  BASED ON self.seqLength     
    def permutation(self):
        if self.seq is None or self.seqInd==len(self.seq)-1:
            self.seq = self.getPerm(self.seqLength,self.conditions)
            self.seqInd = 0
        else:
            self.seqInd = self.seqInd +1
        return self.seq[self.seqInd]
    
    # RETURNS A SEQUENCE OF EVENTS WITH LENGTH seq
    def getPerm(self,seq,conds=['left','right']):
        res = conds * int(seq/len(conds))
        res = list(res)
        random.shuffle(res)
        return res


# EXAMPLE ON HOW TO USE TRAINER CLASS
if __name__=='__main__':
     numTrials = 30 # NUMBER OF TRIALS 
     # SIMULATED RESPONSE WITH KNOWN SUCCESS PROBABILITY
     response1 = ('yes','yes','yes','yes','yes','yes','yes','yes','no','no')
     trials = ListTrial() # INITIALIZE TRIAL LIST
     trainer = Trainer(['left','right'],type=TRAINING) # INITIALIZE TRAINER
     trials.add( Trial(trainer.next(),random.choice(response1) ) ) # FIRST TRIAL
     print(trials.str(-1))
     for i in range(0,numTrials):
         tr=trainer.next(trials)
         trials.add(Trial(tr, random.choice(response1)) )
             
         print(trials.str(-1))
    # PERFORMANCES 
     totaliSX  = trials.getCount('left')
     totaliDX  = trials.getCount('right')
     hitSX = trials.getCount('left','yes')
     hitDX = trials.getCount('right','yes')
     print( 'Correct total: ' + str( (hitSX+hitDX) / float(totaliDX+totaliSX) ))
     print('Left: ' + str(totaliSX) + ' ' + 'Right: ' + str(totaliDX))
     print('Left correct: ' + str(hitSX/float(totaliSX)) + ' ' + 'Right correct: ' + str(hitDX/float(totaliDX)))
    