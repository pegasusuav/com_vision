import cv2
import os
import math
import numpy as np
import ShapeMatch
font = cv2.FONT_HERSHEY_COMPLEX
fontsize = 1
def con(OrgImage,Removed,path1):
    # OrgImage = "img20.jpg"
    # path1 = "ORG-IMG/"
    # Removed = "img20-Remove.jpg"

    NameImg = os.path.splitext(OrgImage)[0]
    ImageName = path1+OrgImage
    
    PathMake0 = ("Detected/"+NameImg)
    PathMake1 = ("Detected/"+NameImg+"/Sign")
    PathMake2 = ("Detected/"+NameImg+"/Text")
    PathMake3 = ("Detected/"+NameImg+"/Text/Clean")
    PathMake4 = ("Detected/"+NameImg+"/Text/SharpText")
    PathMake5 = ("Detected/"+NameImg+"/Text/ColorText")
    PathMake6 = ("SUAS/")
    print(PathMake0)
    print(PathMake1)
    print(PathMake2)
    print(PathMake3)
    print(PathMake4)
    print(PathMake5)
    
    try:
        os.mkdir(PathMake0)
        os.mkdir(PathMake1)
        os.mkdir(PathMake2)
        os.mkdir(PathMake3)
        os.mkdir(PathMake4)
        os.mkdir(PathMake5)
    except OSError:
        print ("Creation of the directory %s failed" % PathMake0)
        print ("Creation of the directory %s failed" % PathMake1)
        print ("Creation of the directory %s failed" % PathMake2)
        print ("Creation of the directory %s failed" % PathMake3)
        print ("Creation of the directory %s failed" % PathMake4)
        print ("Creation of the directory %s failed" % PathMake5)
    else:
        print ("Successfully created the directory %s " % PathMake0)
        print ("Successfully created the directory %s " % PathMake1)
        print ("Successfully created the directory %s " % PathMake2)
        print ("Successfully created the directory %s " % PathMake3)
        print ("Successfully created the directory %s " % PathMake4)
        print ("Successfully created the directory %s " % PathMake5)
        

    Display = cv2.imread(ImageName)
    Original = cv2.imread(ImageName)
    mask = np.zeros_like(Original)
    out = np.zeros_like(Original)
    out[:] = (100, 100, 100)
    cv2.imwrite("Detected/%s/%s-Detectedmask1.jpg" % (NameImg,NameImg), mask)

    ProcessImg = cv2.imread("[removed]BG/"+Removed)

    # read Image size
    H,W = ProcessImg.shape[:2]
    print(str(H) + "," + str(W))

    # Image Ratio
    REDUCE = 3
    h, w = H / REDUCE, W / REDUCE

    gray = cv2.cvtColor(ProcessImg, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    _, threshold = cv2.threshold(gray, 5, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imwrite("Detected/%s/%s-DetectedTHRESH.jpg" % (NameImg,NameImg), threshold)

    # threshold area--------------------------------------------------------
    threshold_min_area = 400
    threshold_max_area = 2500

    Rectangle_Expand = 10
##    Rectangle_Crop = 50
    Index = 0

    SignSharpImg = []
    SHAPEALL = []
    SignPath = []
    ShapeFormulaALL = []
    ShapeFormulaNewALL = []
    ShapeFormulaRatioALL = []

    lenapproxALL = []

    ShapeCircleALL = []
    ShapeRectALL = []

    CX = []
    CY = []

    WR = []
    HR = []
    Recheck = 0

    print("All Countours :",len(contours))
    print("--------------------------------------------------------------------------")
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if threshold_max_area > area > threshold_min_area:
            Recheck += 1
    if Recheck == 0 :
        print("-------------------------------------------- No sign FOUND!!! --------------------------------------------")
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if threshold_max_area > area > threshold_min_area:
            Index+=1
            perimeter = cv2.arcLength(cnt,True)
            print("----------------------------- Start Processing -----------------------------")
            print("%s-%d[SIGN].jpg" % (NameImg,Index))
            print("area :",area)
            print("perimeter :",perimeter)
            path = "/Detected/"+NameImg
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            print("cX :",cX)
            print("cY :",cY)
            cv2.circle(Display, (cX, cY), 7, (0, 0, 255), -1)
            cv2.putText(Display, "%d" % area, (cX, cY), font, fontsize, (0, 0, 255))
            print("OK-1")

##            # Outbounding Debug
##            MinY = cY-Rectangle_Crop
##            MaxY = cY+Rectangle_Crop
##
##            MinX = cX-Rectangle_Crop
##            MaxX = cX+Rectangle_Crop
            
##            if (MinY < 0):
##                MinY = 0
##            if (MaxY > H):
##                MaxY = H
##            if (MinX < 0):
##                MinX = 0
##            if (MaxX > W):
##                MaxX = W

            

            approx = cv2.approxPolyDP(cnt, 0.0005 * cv2.arcLength(cnt, True), True)
            #approx = cnt

            (xc,yc),radius = cv2.minEnclosingCircle(cnt)

            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            
            wr = rect[1][0]
            hr = rect[1][1]
            if wr > hr:
                save = hr
                hr = wr
                wr = save
            Areaminrec = wr*hr
            print("Areaminrec :",Areaminrec)
            print("wr,hr :",wr,hr)

            ellipse = cv2.fitEllipse(cnt)
            cv2.ellipse(ProcessImg,ellipse,(0,255,0),2)            

            cv2.drawContours(ProcessImg, [approx], -1, (0, 0, 255), 5)
            cv2.drawContours(Display, [approx], -1, (0, 255, 0), 5)

            cv2.drawContours(mask, [approx], -1, (255,255,255),cv2.FILLED)
            out[mask == 255] = Original[mask == 255]

            x,y,w2,h2 = cv2.boundingRect(cnt)

            if x < Rectangle_Expand or x < Rectangle_Expand:
                Rectangle_Expand=0

            MinYt = y-Rectangle_Expand
            MaxYt = y+h2+Rectangle_Expand

            MinXt = x-Rectangle_Expand
            MaxXt = x+w2+Rectangle_Expand
            
            if (MinYt < 0):
                MinYt = 0
            if (MaxYt > H):
                MaxYt = H
            if (MinXt < 0):
                MinXt = 0
            if (MaxXt > W):
                MaxXt = W
                
            
            #x = approx.ravel()[0]
            #y = approx.ravel()[1]
            

            ShapeFormula = math.sqrt(area)/perimeter
            ShapeFormulaNew = 4*math.pi*area/(perimeter*perimeter)
            ShapeFormulaRatio = area/(w2+20)/(h2+20)

            ShapeCircle = area/(math.pi*radius*radius)*100
            ShapeRect = area/Areaminrec*100

            print("ShapeFormula :",ShapeFormula)
            print("ShapeFormulaNew :",ShapeFormulaNew)
            print("ShapeFormulaRatio :",ShapeFormulaRatio)
            print("ShapeCircle :",ShapeCircle)
            print("ShapeRect :",ShapeRect)
            
            print("len(approx) :",len(approx))

            if 80 < ShapeCircle <=100:
                cv2.putText(Display, "CIRCLE", (x, y), font, fontsize, (0, 0, 255))
                print("CIRCLE")
                SHAPE=("CIRCLE")
            
            elif ShapeRect > 80:
                if 64.7 < ShapeCircle < 69:
                    cv2.putText(Display, "SQUARE", (x, y), font, fontsize, (0, 0, 255))
                    print("SQUARE")
                    SHAPE=("SQUARE")
                else:
                    cv2.putText(Display, "RECTANGLE", (x, y), font, fontsize, (0, 0, 255))
                    print("RECTANGLE")
                    SHAPE=("RECTANGLE")
                

            elif 38 < ShapeCircle < 44:
                cv2.putText(Display, "STAR", (x, y), font, fontsize, (0, 0, 255))
                print("STAR")
                SHAPE=("STAR")
            
            elif 48< ShapeCircle < 62: 
                if 0.99 < hr/wr < 1.17:
                    if ShapeFormula < 16:
                        cv2.putText(Display, "CROSS", (x, y), font, fontsize, (0, 0, 255))
                        print("CROSS")
                        SHAPE=("CROSS")

                    elif ShapeRect < 67:
                        cv2.putText(Display, "TRIANGLE", (x, y), font, fontsize, (0, 0, 255))
                        print("TRIANGLE")
                        SHAPE=("TRIANGLE")
                    
                    elif ShapeRect >= 67:
                        cv2.putText(Display, "QUARTER_CIRCLE", (x, y), font, fontsize, (0, 0, 255))
                        print("QUARTERCIRCLE")
                        SHAPE=("QUARTERCIRCLE")
                else:
                    result = ShapeMatch.Semitrape(cnt)
                    cv2.putText(Display, result, (x, y), font, fontsize, (0, 0, 255))
                    print(result)
                    SHAPE=(result)
            else:
                cv2.putText(Display, "Unknown", (x, y), font, fontsize, (0, 0, 255))
                print("Unknown")
                SHAPE=("Unknown")
                continue
            """
                cv2.putText(Display, "Trapezoid", (x, y), font, fontsize, (0, 0, 255))
                print("Trapezoid")
                SHAPE=("Trapezoid")

            elif 50 < ShapeCircle < 51.1 and ShapeRect > 85 :
                cv2.putText(Display, "Semi-Circle", (x, y), font, fontsize, (0, 0, 255))
                print("Semi-Circle")
                SHAPE=("Semi-Circle")

            elif 51 <= ShapeCircle  < 61:
                cv2.putText(Display, "Quarter-Circle", (x, y), font, fontsize, (0, 0, 255))
                print("Quarter-Circle")
                SHAPE=("Quarter-Circle")

            elif 49 <= ShapeCircle  < 50 :
                cv2.putText(Display, "Plus", (x, y), font, fontsize, (0, 0, 255))
                print("Plus")
                SHAPE=("Plus")
            """
                
##            elif len(approx) == 5:
##                cv2.putText(Display, "Pentagon", (x, y), font, 3, (0, 0, 255))
##                print("Pentagon")
##                SHAPE=("Pentagon")

##            elif len(approx) == 6:
##                cv2.putText(Display, "Hexagon", (x, y), font, 3, (0, 0, 255))
##                print("Hexagon")
##                SHAPE=("Hexagon")

              
                
            ShapeFormulaALL.append(ShapeFormula)
            ShapeFormulaNewALL.append(ShapeFormulaNew)
            ShapeFormulaRatioALL.append(ShapeFormulaRatio)

            ShapeCircleALL.append(ShapeCircle)
            ShapeRectALL.append(ShapeRect)
            
            lenapproxALL.append(len(approx))
            SHAPEALL.append(SHAPE)

            CX.append(cX)
            CY.append(cY)

            WR.append(wr)
            HR.append(hr)

            if y < Rectangle_Expand or x < Rectangle_Expand:
                Rectangle_Expand = 0

            print("------------------------- Write Image -------------------------")
            Sign = out[ y-Rectangle_Expand : y+h2+Rectangle_Expand, x-Rectangle_Expand : x+w2+Rectangle_Expand]
            cv2.imwrite("Detected/%s/Sign/%s-%d[SIGN].jpg" % (NameImg,NameImg,Index), Sign)
            cv2.imwrite(PathMake6+"%s-%d[SIGN].jpg" % (NameImg,Index), Sign)
            
            SignPath.append(PathMake6+"%s-%d[SIGN].jpg" % (NameImg,Index))
            print("OK-Written")

            #TEMP______________________________________________________________________________________________________________
            Mask = mask[ y-Rectangle_Expand : y+h2+Rectangle_Expand, x-Rectangle_Expand : x+w2+Rectangle_Expand]
            cv2.imwrite("Detected/%s/Sign/%s-%dMask.jpg" % (NameImg,NameImg,Index), Mask)
            print("OK-2")
            
            print("OK-2.5")
            # Create our shapening kernel, it must equal to one eventually-------------------------------------------------------------------------------------Sharp
            kernel_sharpening = np.array([[-1,-1,-1],[-1, 9,-1],[-1,-1,-1]])

            print("OK-2.7")
            # applying the sharpening kernel to the input image & displaying it.
            Signsharp = cv2.filter2D(Sign, -1, kernel_sharpening)
            print("OK-2.9")
            cv2.imwrite("Detected/%s/Sign/%s-%dSignsharp.jpg" % (NameImg,NameImg,Index), Signsharp)
            SignSharpImg.append("Detected/%s/Sign/%s-%dSignsharp.jpg" % (NameImg,NameImg,Index))

            #change to unsharp due to error-----------------------------------------------
            # SignSharpImg.append("Detected/%s/Sign/%s-%d[SIGN].jpg" % (NameImg,NameImg,Index))
            
            print("OK-3")
            

    
        

    
    cv2.imwrite("Detected/%s/%s-Detectedmask.jpg" % (NameImg,NameImg), mask)
    cv2.imwrite("Detected/%s/%s-Detectedout.jpg" % (NameImg,NameImg), out)

    
##    cv2.namedWindow("shapes", cv2.WINDOW_NORMAL)
##    cv2.resizeWindow("shapes", int(w), int(h))
##    #cv2.imshow("shapes", ProcessImg)
    cv2.imwrite("Detected/%s/%s-DetectedPro.jpg" % (NameImg,NameImg), ProcessImg)
##
##    cv2.namedWindow("show", cv2.WINDOW_NORMAL)
##    cv2.resizeWindow("show", int(w), int(h))
##    #cv2.imshow("show", Display)
    cv2.imwrite("Detected/%s/%s-DetectedDis.jpg" % (NameImg,NameImg), Display)
##
##    cv2.namedWindow("Threshold", cv2.WINDOW_NORMAL)
##    cv2.resizeWindow("Threshold", int(w), int(h))
##    #cv2.imshow("Threshold", threshold)
##
##    cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
##    cv2.resizeWindow("Original", int(w), int(h))
##    #cv2.imshow("Original",Original)

    cv2.destroyAllWindows()
    return SignSharpImg,NameImg,SHAPEALL,SignPath,PathMake3,CX,CY,H,W,PathMake6

# Testing zone
# con(1,2,3)
# print("Fuck you")
