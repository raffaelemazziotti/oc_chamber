import time
from math import hypot
import numpy as np
import os
import csv
import random
import imutils
import cv2

SUM=1
MEAN=2
MEDIAN=3
DIFFS=4
MAX=5
MIN=6
EXT='.txt'  # Output file extension

# THIS CLASS MANAGE TRACKING DATA 
#



# COORDINATES WITH TIMESTAMP
class coo():
    def __init__(self,x=0,y=0,t=None,info='NaN'):
        self.x = x
        self.y = y
        
        if t:
            self.time = t
        else:
            self.time = time.time()

        self.info = info
        
    def tostr(self):
        if type(self.info) != str:
            info = str(self.info)
        else:
            info = self.info
        return str(self.time) + '\t' + str(self.x) + '\t' + str(self.y) + '\t' + info

# LIST OF COORDINATES WITH TIMESTAMP  
class coolist():
    def __init__(self,coo = None,rect=None):
        self.coos=list()
        self.rect=rect
        if coo:
            self.coos.append(coo)
            
    def append(self,coo):
        if self.rect is not None:
            if coo.x<self.rect[0]:
               coo.x=self.rect[0]
            if coo.y<self.rect[1]:
                coo.y=self.rect[1]
            if coo.x>self.rect[2]:
                coo.x=self.rect[2]
            if coo.y>self.rect[3]:
                coo.y=self.rect[3]
        self.coos.append(coo)
        
    def add(self,x,y,t=None,info='NaN'):
        if self.rect is not None:
            if x<self.rect[0]:
               x=self.rect[0]
            if y<self.rect[1]:
                y=self.rect[1]
            if x>self.rect[2]:
                x=self.rect[2]
            if y>self.rect[3]:
                y=self.rect[3]
        self.coos.append(coo(x,y,t,info=info))
        
    def tot(self):
        return len(self.coos)
    
    # vettore xy    
    
    def xy(self):
        res= list()
        for ci in self.coos:
            res.append((ci.x,ci.y))
        return res
    
    def x(self):
        return [x[0] for x in self.xy()]
    
    def y(self):
        return [y[1] for y in self.xy()]
    
    # vettore time
    
    def t(self):
        res= list()
        for ci in self.coos:
            res.append(ci.time)
        return res
    
    def path(self,mode = MEAN):
        ptdiff = lambda p1,p2: (p1[0]-p2[0], p1[1]-p2[1])
        diffs = map(ptdiff, zip(self.xy(),self.xy()[1:]))
        eucli=[hypot(*d) for d in  diffs]
        
        if mode==SUM:
            path = sum(eucli)
        elif mode==MEAN:
            path = np.mean(eucli)
        elif mode==MEDIAN:
            path = np.median(eucli)
        elif mode==DIFFS:
            path = eucli
            
        return path
    
    def speed(self,mode=MEAN):
        time = np.diff(self.t())
        path = self.path(DIFFS)
        
        if mode==MEAN:
            res = np.mean(path/time)
        elif mode==MEDIAN:
            res = np.median(path/time)
        elif mode==MAX:
            res = np.max(path/time)
        elif mode==MIN:
            res = np.min(path/time)
        elif mode==DIFFS:
            res = path/time
        
        return res
        
    def write(self,filename=None,path=None):
        if filename is None:
            filename=time.strftime("%Y%m%d_%H%M-tracker") + EXT
        else:
            filename=time.strftime("%Y%m%d_%H%M-tracker-") + filename + EXT
            
        if path is None:
            path = os.path.join('/home/pi/Documents/cvConditioningData/','trackerDATA')
            
        if not os.path.exists(path):
            os.makedirs(path)
            
        with open(os.path.join(path,filename),"w") as f:
            f.write('rect\t' + str(self.rect[0]) + '\t' + str(self.rect[1]) + '\t' + str(self.rect[2]) + '\t' + str(self.rect[3]) + '\t' + "\n") 
            for t in self.coos:
                f.write(t.tostr() + "\n") 
                
    def read(self,filepath=None):
        with open(filepath , 'rb') as csvfile:
            txt = csv.reader(csvfile,delimiter='\t')
            for l in txt:
                if l[0] =='rect':
                    self.rect=(int(l[1]),int(l[2]),int(l[3]),int(l[4]))
                    continue
                self.add(int(l[1]),int(l[2]),t=float(l[0]),info=l[3])



def templateArena(img,template='template.jpg'):
    template = cv2.imread(template,0)
    wi, he = template.shape[::-1]
    method=cv2.TM_CCOEFF_NORMED
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
        
    bottom_right = (top_left[0] + wi, top_left[1] + he)
    x,y,w,h = top_left[0],top_left[1],bottom_right[0],bottom_right[1]

    return (x,y,w,h)

    


    
