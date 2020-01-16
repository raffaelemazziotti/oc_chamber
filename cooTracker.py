import time
import numpy as np
import os
import csv
import cv2


# Output file extension
EXT='.txt'  


# THIS CLASS MANAGES TRACKING DATA 


# COORDINATES WITH TIMESTAMP AND INFO
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
    
    # RETURNS A LIST OF (X,Y) COORDINATES   
    def xy(self):
        res= list()
        for ci in self.coos:
            res.append((ci.x,ci.y))
        return res
    
    def x(self):
        return [x[0] for x in self.xy()]
    
    def y(self):
        return [y[1] for y in self.xy()]
    
    # RETURNS A LIST OF TIMESTAMPS
    def t(self):
        res= list()
        for ci in self.coos:
            res.append(ci.time)
        return res

    # WRITES TRACKING FILE  
    def write(self,filename=None,path=None):
        if filename is None:
            filename=time.strftime("%Y%m%d_%H%M-tracker") + EXT
        else:
            filename=time.strftime("%Y%m%d_%H%M-tracker-") + filename + EXT
            
        if path is None:
            path = os.path.join(os.getcwd(),'trackerDATA')
            
        if not os.path.exists(path):
            os.makedirs(path)
            
        with open(os.path.join(path,filename),"w") as f:
            f.write('rect\t' + str(self.rect[0]) + '\t' + str(self.rect[1]) + '\t' + str(self.rect[2]) + '\t' + str(self.rect[3]) + '\t' + "\n") 
            for t in self.coos:
                f.write(t.tostr() + "\n") 

    # READS TRACKING FILE           
    def read(self,filepath=None):
        with open(filepath , 'rb') as csvfile:
            txt = csv.reader(csvfile,delimiter='\t')
            for l in txt:
                if l[0] =='rect':
                    self.rect=(int(l[1]),int(l[2]),int(l[3]),int(l[4]))
                    continue
                self.add(int(l[1]),int(l[2]),t=float(l[0]),info=l[3])


#FIND ARENA BORDERS USING TEMPLATE MATCHING
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

if __name__=='__main__':
    c = coolist(rect=(2,2,10,7))
    c.append(coo(5,7,info="first"))
    c.append(coo(10,7,info="second"))
    print(c.xy())
    


    
