# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 17:02:36 2017

@author: dell
"""

import cv2
import numpy as np
import math

img_rgb = cv2.imread('12.jpg')


#for bringing down the size
ratio=1000.0/img_rgb.shape[0]
dimension=(540,int(ratio*img_rgb.shape[1]))

img_rgb=cv2.resize(img_rgb,dimension,interpolation=cv2.INTER_AREA)

img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

template = cv2.imread('template1.jpg',0)
w, h = template.shape[::-1]
#cv2.imshow('original',img_rgb)
#for mathing the squares
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.9
shapex=np.zeros((10),dtype=np.int32)
shapey=np.zeros((10),dtype=np.int32)
i=0
#for dRAWING OUT LOCATIONS
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 0)
    shapex[i]=pt[0] #for storing coordinates
    shapey[i]=pt[1]
    i=i+1
#TO HAVE just 2 unique coordinates
shapex=np.sort(shapex)
shapey=np.sort(shapey)

z=i#for removing unwanted coordinates which got repeated
for j in range (10-z,9):
    if shapex[j+1]-shapex[j]<4:
       shapex[j]=0
       i=i-1 
    if (shapey[j+1]-shapey[j])<4:
       shapey[j]=0         

shapex=np.sort(shapex)
shapey=np.sort(shapey)



if i==4 :
    pts1 = np.float32([[shapex[6]+h,shapey[7]+w],[shapex[8]+h,shapey[6]+w],[shapex[7]+h,shapey[9]+w],[shapex[9]+h,shapey[8]+w]])
  
           
if i==2 :
    pts1 = np.float32([[shapex[8]+h,shapey[8]+w],[shapex[9]+h,shapey[8]+w],[shapex[8]+h,shapey[9]+w],[shapex[9]+h,shapey[9]+w]])
   
    
pts2 = np.float32([[0,0],[700,0],[0,700],[700,700]])
M = cv2.getPerspectiveTransform(pts1,pts2)
img_rgb = cv2.warpPerspective(img_rgb,M,(700,700))

#cv2.imshow('Detected',img_rgb)
#cv2.imshow('Detected1',dst)


bubbletemplate=cv2.imread('bubbletemplate.png',0)

img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

w, h = bubbletemplate.shape[::-1]
res = cv2.matchTemplate(img_gray,bubbletemplate,cv2.TM_CCOEFF_NORMED)
threshold = 0.805 #to avoid faint marking put threshold=0.87 and half ellipse=0.80

bubx=np.zeros((1500),dtype=np.int32)
buby=np.zeros((1500),dtype=np.int32)
bub1x=np.zeros((1500),dtype=np.int32)
bub1y=np.zeros((1500),dtype=np.int32)

#for dRAWING OUT LOCATIONS
loc = np.where( res >= threshold)



i=0

for pt in zip(*loc[::-1]):
    bubx[i]=pt[0]
    buby[i]=pt[1]
    i=i+1

i=0  
k=0  


for pt in zip(*loc[::-1]):   
    
    j=0
    flag=1
    for j in range(1,20):
             if abs(bubx[i]-bubx[i+j])<3 and abs(buby[i]-buby[i+j])<3:
                 flag=0
    j=0
    if flag!=0: 
        #cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255,255,0), 0)
        bub1x[k]=pt[0]
        bub1y[k]=pt[1]
        k=k+1        
    i=i+1

#to read omr result

#for point in range(0,k):
 #   if abs(bub1y[point]-bub1y[point+1])>30:
  #      seperationpty=bub1y[point]
   #     seperationptx=bub1x[point]    
sepx=np.zeros(k,dtype=np.int32)
sepy=np.zeros(k,dtype=np.int32)

for i in range(0,k-1): 
    sepy[i]=abs(bub1y[i]-bub1y[i+1])
    


tempy=np.sort(sepy)
for z in range (0,k-1):
    if tempy[k-1]==sepy[z]:
            break
        
  
#for answer evaluation
omrsep=np.sort(sepy[z+1:k])  
quessep=omrsep[k-z-2]
#tempx=bub1x
#a= np.where(tempx==min(tempx[z+1:k]))
#tempx[a]=1000

#print min(tempx[z+1:k])
#print np.where(tempx==min(tempx[z+1:k]))
#2w for 1 , 3w for 2 .....5w for 4 , 8w for next block 1st
for y in range (z+1,k):
    
    if bub1x[y]>=min(bub1x[z+1:]) and bub1x[y]<min(bub1x[z+1:])+5*w:
           for n in range (1,21):   
               if bub1y[y]+h/2> bub1y[z+1]+(n-1)*h and bub1y[y]+h/2< bub1y[z+1]+(n)*h:
                   print "q" + str(n)
           
           cv2.rectangle(img_rgb, (bub1x[y],bub1y[y]), (bub1x[y]+ w,bub1y[y] + h), (255,255,0), 0)
           if bub1x[y]>=min(bub1x[z+1:]) and bub1x[y]<min(bub1x[z+1:])+2*w:        
                print "A"
           if bub1x[y]>=min(bub1x[z+1:])+2*w and bub1x[y]<min(bub1x[z+1:])+3*w:    
                print "B" 
           if bub1x[y]>=min(bub1x[z+1:])+3*w and bub1x[y]<min(bub1x[z+1:])+4*w:    
                print "C"     
           if bub1x[y]>=min(bub1x[z+1:])+4*w and bub1x[y]<min(bub1x[z+1:])+5*w:    
                print "D"        
for y in range (z+1,k):        
    if bub1x[y]>=min(bub1x[z+1:])+7*w and bub1x[y]<min(bub1x[z+1:])+11*w:
           for n in range (1,21):   
               if bub1y[y]+h/2> bub1y[z+1]+(n-1)*h and bub1y[y]+h/2< bub1y[z+1]+(n)*h:
                   print "q" + str(n+20)
           
           cv2.rectangle(img_rgb, (bub1x[y],bub1y[y]), (bub1x[y]+ w,bub1y[y] + h), (255,255,0), 0)
           if bub1x[y]>=min(bub1x[z+1:])+7*w and bub1x[y]<min(bub1x[z+1:])+8*w:        
                print "A"
           if bub1x[y]>=min(bub1x[z+1:])+8*w and bub1x[y]<min(bub1x[z+1:])+9*w:    
                print "B" 
           if bub1x[y]>=min(bub1x[z+1:])+9*w and bub1x[y]<min(bub1x[z+1:])+10*w:    
                print "C"     
           if bub1x[y]>=min(bub1x[z+1:])+10*w and bub1x[y]<min(bub1x[z+1:])+11*w:    
                print "D" 
for y in range (z+1,k):    
    if bub1x[y]>=min(bub1x[z+1:])+14*w and bub1x[y]<min(bub1x[z+1:])+18*w:
           for n in range (1,21):   
               if bub1y[y]+h/2> bub1y[z+1]+(n-1)*h and bub1y[y]+h/2< bub1y[z+1]+(n)*h:
                   print "q" + str(n+40)
           
           cv2.rectangle(img_rgb, (bub1x[y],bub1y[y]), (bub1x[y]+ w,bub1y[y] + h), (255,255,0), 0)
           if bub1x[y]>=min(bub1x[z+1:])+14*w and bub1x[y]<min(bub1x[z+1:])+15*w:        
                print "A"
           if bub1x[y]>=min(bub1x[z+1:])+15*w and bub1x[y]<min(bub1x[z+1:])+16*w:    
                print "B" 
           if bub1x[y]>=min(bub1x[z+1:])+16*w and bub1x[y]<min(bub1x[z+1:])+17*w:    
                print "C"     
           if bub1x[y]>=min(bub1x[z+1:])+17*w and bub1x[y]<min(bub1x[z+1:])+18*w:    
                print "D"   
for y in range (z+1,k):    
    if bub1x[y]>=min(bub1x[z+1:])+20*w and bub1x[y]<min(bub1x[z+1:])+24*w:
           for n in range (1,21):   
               if bub1y[y]+h/2> bub1y[z+1]+(n-1)*h and bub1y[y]+h/2< bub1y[z+1]+(n)*h:
                   print "q" + str(n+60)
           
           cv2.rectangle(img_rgb, (bub1x[y],bub1y[y]), (bub1x[y]+ w,bub1y[y] + h), (255,255,0), 0)
           if bub1x[y]>=min(bub1x[z+1:])+20*w and bub1x[y]<min(bub1x[z+1:])+21*w:        
                print "A"
           if bub1x[y]>=min(bub1x[z+1:])+21*w and bub1x[y]<min(bub1x[z+1:])+22*w:    
                print "B" 
           if bub1x[y]>=min(bub1x[z+1:])+22*w and bub1x[y]<min(bub1x[z+1:])+23*w:    
                print "C"     
           if bub1x[y]>=min(bub1x[z+1:])+23*w and bub1x[y]<min(bub1x[z+1:])+24*w:    
                print "D"
for y in range (z+1,k):
    if bub1x[y]>=min(bub1x[z+1:])+27*w and bub1x[y]<min(bub1x[z+1:])+31*w:
           for n in range (1,21):   
               if bub1y[y]+h/2> bub1y[z+1]+(n-1)*h and bub1y[y]+h/2< bub1y[z+1]+(n)*h:
                   print "q" + str(n+80)
           
           cv2.rectangle(img_rgb, (bub1x[y],bub1y[y]), (bub1x[y]+ w,bub1y[y] + h), (255,255,0), 0)
           if bub1x[y]>=min(bub1x[z+1:])+27*w and bub1x[y]<min(bub1x[z+1:])+28*w:        
                print "A"
           if bub1x[y]>=min(bub1x[z+1:])+28*w and bub1x[y]<min(bub1x[z+1:])+29*w:    
                print "B" 
           if bub1x[y]>=min(bub1x[z+1:])+29*w and bub1x[y]<min(bub1x[z+1:])+30*w:    
                print "C"     
           if bub1x[y]>=min(bub1x[z+1:])+30*w and bub1x[y]<min(bub1x[z+1:])+31*w:    
                print "D"               
     
cv2.imshow('bubbledetected',img_rgb)
cv2.waitKey(0)