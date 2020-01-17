import imutils
from VideoStream import PiVideoStream
import cv2
import time
from arduinoCom import *
from skinnerTrial import *
import form
import sys
import numpy
import os
import cooTracker as trk

#------ EDIT THE FOLLOWING CONSTANTS TO TUNE YOUR EXPERIMENT ------

# CHOOSE THE EXPERIMENTAL TASK
task = PERMUTATION   # can be PERMUTATION or TRAINING (assisted procedure)
# COMPUTER VISION PARAMETERS
deltaThresh=50      # THRESHOLD OF BITMAP IMAGE FOR MOUSE SEGMENTATION
smallestObj=300     # THE MINIMUM AREA FOR A VALID MOUSE CONTOUR
biggestObj=20000    # THE MAXIMUM AREA FOR A VALID MOUSE CONTOUR
# TRACKING MARKER (customize the appearence of the circle showing the mouse's position)
radius=25           
color=(0,0,255)
thickness=1

#------ END OF EDITABLE CODE ------

# load the GUI to select procedure preferences
frm = form.Form() 
prefs =frm.results()
if not prefs:
    print('Aborted by user.')
    sys.exit()

# IMAGE RESOLUTION
resolution=(208,208)
history=int(prefs['history'])

# ACTIVE ZONE BORDER 
lev=resolution[0]*float(prefs['level'])
posTracker= True

criterion = prefs['criterion'] # Number of frames required to trigger a trial
if prefs['recfile']:
    recording = True
    print('recording enabled')
    filename = prefs['recfile'] # video file name
    videopath = prefs['recpath'] 
else:
    recording = False
    filename = None
    
if prefs['filename']:    
    sessionFile= prefs['filename'] # default session name
    sessionpath = prefs['filepath'] # default path

# maximal framerate
framerate=30
conditions = prefs['conditions'] # left,right,both

# CAMERA INITIALIZATION
print('Initializing:')
print('- camera')
cap = PiVideoStream(resolution=resolution,framerate=framerate)
cap.start()
time.sleep(1.0)
print('- CV objects')
fgbg = cv2.createBackgroundSubtractorKNN(history=history,detectShadows=False)
erodeKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))

# Arduino INITIALIZATION
print('- Arduino Connection')
arduino = Arduino()
# Trainer INITIALIZATION
trainer = Trainer(conditions,task)


## TRACKING FILENAME
if filename is None:
    filename ='/home/pi/Videos/' + time.strftime("%Y%m%d_%H%M%S-") + 'tracker'
## RECORDING FILENAME 
if recording:
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter( os.path.join(videopath,time.strftime("%Y%m%d_%H%M%S-") + filename +'.avi'), fourcc, framerate, resolution )


currentTime=time.time()
prevTime = time.time()
fps=None
counter=0
TTLactive = True
cv2.namedWindow('Frame', cv2.WINDOW_FREERATIO)
# VIDEOTRACKING CALIBRATION
if posTracker:
    print('- Tracking Variables')
    print('     Finding arena: please wait...')
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(5,5))
    x,y,w,h=0,0,0,0
    while (x,y,w,h)==(0,0,0,0):
        frame = cap.read()
        frame = imutils.rotate(frame,180)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = clahe.apply(frame)
        x,y,w,h = trk.templateArena(frame)
        cv2.putText(frame,'AREA DETECTION',(int(resolution[0]/5),int(resolution[1]/2)),cv2.FONT_HERSHEY_PLAIN,1,color,2,cv2.LINE_AA)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key==ord('p'):
            print('- Skipping arena detection...')
            x,y,w,h=0,0,resolution[0],resolution[1]
            break
    print('Arena position: ')
    print((x,y,w,h))
    xytracking = trk.coolist(rect=(x,y,w,h))
    
print('- CV calibration')
vis = True
for c in range(0,history):
    frame = cap.read()
    frame = imutils.rotate(frame,180)
    fps = 1.0/(currentTime-prevTime)
    prevTime = currentTime
    currentTime=time.time()
    fgmask = fgbg.apply(frame)
    if not c % 30:
        vis = not vis
    if vis:
        perc = (c/float(history))*100
        cv2.putText(frame,'CALIBRATION ' + str(int(perc)) + '%',(int(resolution[0]/5),int(resolution[1]/2)),cv2.FONT_HERSHEY_PLAIN,1,color,2,cv2.LINE_AA)
    if posTracker:
        cv2.rectangle(frame,(xytracking.rect[0],xytracking.rect[1]),(xytracking.rect[2],xytracking.rect[3]),(127,200,0),2)
    cv2.putText(frame,'fps: ' + str(round(fps,1)),(1,20), cv2.FONT_HERSHEY_PLAIN, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key==ord('p'):
        print('- Skipping calibration...')
        break
ttl=0

# PROCEDURE
while True:
    frame = cap.read()
    frame = imutils.rotate(frame,180)

    fps = 1.0/(currentTime-prevTime)
    prevTime = currentTime
    currentTime=time.time()
    
    fgmask = fgbg.apply(frame,learningRate=0)
    thresh = cv2.threshold(fgmask, deltaThresh, 255,cv2.THRESH_BINARY)[1]
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_ERODE, kernel=erodeKernel)
    
    (_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    largestArea=0
    largestObject=None
    for c in cnts:
        # SIZE EXCLUSION
        if cv2.contourArea(c) < smallestObj or cv2.contourArea(c) > biggestObj:
            continue
        if cv2.contourArea(c) > largestArea:
            largestArea=cv2.contourArea(c)
            largestObject=c
    if largestObject is not None:
        M = cv2.moments(largestObject)
        X = int(M["m10"] / M["m00"])
        Y = int(M["m01"] / M["m00"])
        if Y >=lev and TTLactive:
            cv2.circle(frame,(X,Y),radius,(0,255,0),thickness+1)
            counter=counter+1
        elif Y<lev and not(arduino.isWaiting()):
            cv2.circle(frame,(X,Y),radius,(0,0,255),thickness+1)
            counter=0
            TTLactive=True
            ttl=0
            
        else:
            if arduino.isWaiting():
                if ttl=='left':
                    cv2.putText(frame,ttl,(int((resolution[0]/2)-60),40), cv2.FONT_HERSHEY_PLAIN, 1,(0,255,255),2,cv2.LINE_AA)
                elif ttl=='right':
                    cv2.putText(frame,ttl,(int((resolution[0]/2)+40),40), cv2.FONT_HERSHEY_PLAIN, 1,(0,255,255),2,cv2.LINE_AA)
            cv2.circle(frame,(X,Y),radius,(255,0,0),thickness+1)
            counter=0
        if posTracker:
            xytracking.add(X,Y,info=ttl)
            
    # ACTION
    if counter >=criterion:
        print('TTL')
        ttl = trainer.next(arduino.session)
        print(ttl)

        arduino.event(ttl)
        counter=0
        TTLactive=False
            
    cv2.line(frame,(1,int(lev)),(int(resolution[1]),int(lev)),(255,0,0),thickness)
    cv2.putText(frame,'fps: ' + str(round(fps,1)),(1,20), cv2.FONT_HERSHEY_PLAIN, 1,(255,255,255),2,cv2.LINE_AA)
    ## RECORDING
    if recording:
        out.write(frame)
        cv2.putText(frame,'REC',(int(resolution[0]/2.0),20), cv2.FONT_HERSHEY_PLAIN, 1,(0,0,255),2,cv2.LINE_AA)
    if arduino.session.tot():
        cv2.putText(frame,'Hits: ' + str(round(arduino.session.performance()*100,1)),(int(resolution[1]-100),int(resolution[1]-20)), cv2.FONT_HERSHEY_PLAIN, 1,(143,244,66),2,cv2.LINE_AA)
    cv2.putText(frame,'Trials: ' + str(arduino.session.tot()),(10,resolution[1]-20), cv2.FONT_HERSHEY_PLAIN, 1,(143,244,66),2,cv2.LINE_AA)
    if posTracker and key==ord('b'):
        cv2.rectangle(frame,(xytracking.rect[0],xytracking.rect[1]),(xytracking.rect[0]+xytracking.rect[2],xytracking.rect[1]+xytracking.rect[3]),(127,200,0),2)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key==ord('p'):
        break
    elif key==ord('s'):
        arduino.event('stop')
        TTLactive=False

# Releasing resources and closing   
if recording:
    out.release()
if arduino.session.tot() and prefs['filename']:
    print('writing session to file...')
    arduino.session.toFile(path=sessionpath,filename=sessionFile)
    
if posTracker and prefs['filename'] and xytracking.tot():
    print('writing xy tracking to file...')
    xytracking.write(prefs['filename'])
    
arduino.event('stop')
arduino.disconnect()

cv2.startWindowThread()
cv2.destroyAllWindows()

cap.stop()
