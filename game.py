# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 14:39:46 2023

@author: Sharvil
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import cvzone
import cv2
import random
import numpy as np
import math
from cvzone.HandTrackingModule import HandDetector


c=cv2.VideoCapture(0)
c.set(3,640)
c.set(4,480)
detector=HandDetector(detectionCon=0.8,maxHands=1)

class game1:
    def __init__(self,foodpath):
        self.points=[]
        self.lengths=[]
        self.currentlength=0
        self.allowedlength=50
        self.previoushead=0,0
        self.score=0
        self.gameover=False
        
        self.foodimg= cv2.imread(foodpath, cv2.IMREAD_UNCHANGED)
        self.hfood,self.wfood,_=self.foodimg.shape
        self.foodpoint=0,0
        self.randomfood()
        
        
        
    def again(self):
        self.points = []
        self.lengths = []
        self.currentlength = 0
        self.allowedlength = 50
        self.previoushead = 0, 0
        self.score = 0
        self.gameover = False
        
    def randomfood(self):
        self.foodpoint= random.randint(100,600),random.randint(100,400)
          
    def update(self,imgmain,currenthead):
        
       if self.gameover:
            cvzone.putTextRect(imgmain,"Game Over",(20,100),scale=3,thickness=3,offset=10)
            cvzone.putTextRect(imgmain,f"Your Score:{self.score}",(20,200),scale=3,thickness=3,offset=10)
        
       else:
        px,py=self.previoushead
        cx,cy=currenthead
        
        self.points.append([cx,cy])
        distance=math.hypot(cx-px,cy-py)
        self.lengths.append(distance)
        self.currentlength+=distance
        self.previoushead=cx,cy
        
        if self.currentlength>self.allowedlength:
            for i,length in enumerate(self.lengths):
                self.currentlength-=length
                self.lengths.pop(i)
                self.points.pop(i)
                if self.currentlength<self.allowedlength:
                    break
        rx,ry=self.foodpoint        
        if rx-self.wfood//2<cx<rx+self.wfood//2 and  ry-self.hfood//2<cy<ry+self.hfood//2:
            self.randomfood()
            self.allowedlength +=5
            self.score+=1
            
        
        
        if self.points:
          for i,point in enumerate(self.points):
            if i!=0:
                cv2.line(imgmain,self.points[i-1],self.points[i],(0,0,255),10)
          cv2.circle(imgmain,self.points[-1],10,(0,200,0),cv2.FILLED)
        
        rx,ry=self.foodpoint
        imgmain=cvzone.overlayPNG(imgmain,self.foodimg,(rx-self.wfood//2,ry-self.hfood//2))
        cvzone.putTextRect(imgmain,f"Score:{self.score}",(20,40),scale=2,thickness=1,offset=10)
        
        
        pts=np.array(self.points[:-2],np.int32)
        pts=pts.reshape((-1,1,2))
        cv2.polylines(imgmain,[pts],False,(0,200,0),3)
        mindist=cv2.pointPolygonTest(pts,(cx,cy),True)
        
        if -1<=mindist<=1:
            self.gameover=True
            self.points = []  
            self.lengths = []  
            self.currentlength = 0  
            self.allowedlength = 50  
            self.previoushead = 0, 0  
            self.randomfood()
   
                                  
       return imgmain  
game=game1("Donut.png")
while True:
    success,img=c.read()
    img=cv2.flip(img,1)
    hands,img=detector.findHands(img,flipType=False)
    
    if hands:
        lmList= hands[0]['lmList']
        pointindex=lmList[8][0:2]
        img=game.update(img,pointindex)
    cv2.imshow("GAME",img)
    key=cv2.waitKey(1)
    if key==ord('r'):
        game.again()
