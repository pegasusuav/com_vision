import cv2
import numpy as np
import os
def fit(TextoutFile,TextColorFile,PathClean):

    TextoutFileEx = os.path.basename(TextoutFile)
    TextFile = os.path.splitext( TextoutFileEx)[0]

    TextColorFileEx = os.path.basename(TextColorFile)
    TextCFile = os.path.splitext( TextColorFileEx)[0]
    print("------------------------- Fit & Crop -------------------------")
    print(TextFile)
    
    img = cv2.imread(TextoutFile)
    img2 = cv2.imread(TextColorFile)
    rows,cols = img.shape[:2]
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 20, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    print("contours :",len(contours))
    minpass = rows*cols
    check = 0
    stand = 0
    OldAngle =0
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 200 < area < 0.4*rows*cols:
            if area < minpass:
                print("--------------------------")
                print("ALL :",0.4*rows*cols)
                print("Letter :",area)
                rect = cv2.minAreaRect(cnt)
                #print(rect)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
    ##            cv2.drawContours(threshold,[box],0,(0,0,255),2)
    ##            cv2.imshow("threshold",threshold)
                ellipse = cv2.fitEllipse(cnt)
                (x,y),(MA,ma),OldAngle = cv2.fitEllipseAMS(cnt)


                # get width and height of the detected rectangle
                width = int(rect[1][0])
                height = int(rect[1][1])

                src_pts = box.astype("float32")
                # corrdinate of the points in box points after the rectangle has been straightened
                dst_pts = np.array([[0, height-1],
                                    [0, 0],
                                    [width-1, 0],
                                    [width-1, height-1]], dtype="float32")

                # the perspective transformation matrix
                M = cv2.getPerspectiveTransform(src_pts, dst_pts)

                # directly warp the rotated rectangle to get the straightened rectangle
                warped = cv2.warpPerspective(img, M, (width, height))
                warped2 = cv2.warpPerspective(img2, M, (width, height))
                # put warped in bigger black picture

                
                h,w = warped.shape[:2]
                
                if h>w:
                    size = h+50
                else:
                    size = w+50

                Black = np.zeros((size,size,3), np.uint8)
                Grey = np.zeros((size,size,3), np.uint8)
                Grey[:] = (100, 100, 100)
                try:
                    Black[int(size/2-h/2):int(size/2+h/2),int(size/2-w/2):int(size/2+w/2)]=warped
                    # kernel_sharpening = np.array([[-1,-1,-1],[-1, 9,-1],[-1,-1,-1]])
                    # Black = cv2.filter2D(Black, -1, kernel_sharpening)
                    Grey[int(size/2-h/2):int(size/2+h/2),int(size/2-w/2):int(size/2+w/2)]=warped2

                    
                    cv2.imwrite("%s/%sclean.jpg"%(PathClean,TextFile),Black)
                    print("%s/%sclean.jpg"%(PathClean,TextFile))
                    TextClean = ("%s/%sclean.jpg"%(PathClean,TextFile))

                    cv2.imwrite("%s/%scolor.jpg"%(PathClean,TextFile),Grey)
                    print("%s/%scolor.jpg"%(PathClean,TextFile))
                    Textcolor = ("%s/%scolor.jpg"%(PathClean,TextFile))
                except Exception:
                    print("------------ Error! Error! Error! Error! Error! ------------")
                    continue
                check += 1
                minpass = area
    stand += 1
    if stand > check:
        print("ALL :",0.6*rows*cols)
        print("***No Text Found!!!!***")
        print("Letter :",area)
        check = stand
        size=400
        Black = np.zeros((size,size,3), np.uint8)
        Grey = np.zeros((size,size,3), np.uint8)
        Grey[:] = (100, 100, 100)
        cv2.imwrite("%s/%s[Not]clean.jpg"%(PathClean,TextFile),Black)
        print("Not Found :%s/%sOverclean.jpg"%(PathClean,TextFile))
        TextClean = ("%s/%s[Not]clean.jpg"%(PathClean,TextFile))

        cv2.imwrite("%s/%s[Not]color.jpg"%(PathClean,TextFile),Grey)
        print("%s/%sOvercolor.jpg"%(PathClean,TextFile))
        Textcolor = ("%s/%s[Not]color.jpg"%(PathClean,TextFile))      

    return TextClean,Textcolor,OldAngle
