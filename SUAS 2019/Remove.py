import os
import numpy as np
import cv2
import time


def Removed(FileName,path1):
    
    print("----------------------------Masking Processing----------------------------")
    start = time.time()
    ##load input image
    imageorg = cv2.imread(path1+FileName)
    out = np.zeros_like(imageorg)
    
    NameImg = os.path.splitext(FileName)[0]

    ##Filter background using colored mask

    light_green = (9,0,0)
    dark_green = (71,255,235)

    light_brown = (10,0,0)
    dark_brown = (30,255,219)

    light_ground = (16,66,0)#yellow line
    dark_ground = (26,154,255)

    light_road = (0,0,0)
    dark_road = (255,91,221)
    
    ##light_white = (0, 0, 116)
    ##dark_white = (180, 57, 255)

    hsv = cv2.cvtColor(imageorg,cv2.COLOR_BGR2HSV)

    mask_green = cv2.inRange(hsv,light_green,dark_green)
    mask_brown = cv2.inRange(hsv,light_brown,dark_brown)
    mask_ground = cv2.inRange(hsv,light_ground,dark_ground)
    mask_road = cv2.inRange(hsv,light_road,dark_road)
    ##mask_white = cv2.inRange(hsv,light_white,dark_white)
    mask = mask_green +  mask_road + mask_ground  # + mask_brown 

    mask2 = cv2.bitwise_not(mask)

    #Mask ROI
    out[mask2 == 255] = imageorg[mask2 == 255]
##    out = cv2.bitwise_and(imageorg,imageorg, mask = mask2)

    cv2.imwrite("[removed]BG/%s-Remove.jpg" % NameImg,out)
##    cv2.imwrite("[removed]BG/%s-Remove(mask).jpg" % NameImg,mask)
##    cv2.imwrite("[removed]BG/%s-Remove(mask_green).jpg" % NameImg,mask_green)
##    cv2.imwrite("[removed]BG/%s-Remove(mask_brown).jpg" % NameImg,mask_brown)
##    cv2.imwrite("[removed]BG/%s-Remove(mask_ground).jpg" % NameImg,mask_ground)
    cv2.imwrite("[removed]BG/%s-Remove(mask2).jpg" % NameImg,mask2)

    Imgremove =("%s-Remove.jpg" % NameImg)
    end = time.time()
    return Imgremove


        
        
        
        
