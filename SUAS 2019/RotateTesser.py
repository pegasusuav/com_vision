import imutils
import pytesseract
import cv2
import numpy as np
import re

def TessRo(TextCleanFiles,SignImg,OldAngle):
    print("----Tesser Go----")

    RotateAngle = 90
    print("RotateAngle :",RotateAngle)

    image = cv2.imread(TextCleanFiles)

    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # check to see if we should apply thresholding to preprocess the image
    _, gray = cv2.threshold(gray,10,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV)
    
    #_,gray = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    gray = cv2.medianBlur(gray,1)

    Thresh = TextCleanFiles.replace(".jpg", "[THRESH].jpg")
    cv2.imwrite(Thresh, gray)
    
    print(Thresh)

    max = 0
    Angle = 0
    Percent = "None"
    Text = "None"
    RoText = "None"

    for angle in np.arange(0, 360, RotateAngle):
        rotated = imutils.rotate_bound(gray, angle)
        config=("-l eng --psm 10 --oem 3 -c tessedit_char_whitelist=")
        data = pytesseract.image_to_data(rotated, lang='eng',config=config)
##        OldAngle = int(OldAngle)
##        angle = int(angle)
        print("------------------------ %d - %d ------------------------"%(angle,OldAngle))
        print(data)
        if len(data) > 200:
            x = data.split()
            print(Thresh)
            print("angle :",angle)
            print("percent : %s" % x[len(x)-2])
            print("text :",x[len(x)-1])

            if int(x[len(x)-2]) > max:
                max = int(x[len(x)-2])
                Angle = int(angle - OldAngle)
                if Angle <= 0:
                    Angle += 360
                Percent = int(x[len(x)-2])
                Text = x[len(x)-1]
                RoText = rotated
    print("------------------------Most Confidence------------------------")
    print("Angle :",Angle)
    print("Percent :",Percent)
    print("Text :",Text)
    Text = Text.upper()
    Text = Text[:1]
    if re.match(r'^\w+$',Text):
        print("No need to Replace")
    else:
        Text = "H"
        print("Replace to H")
    print("Text :",Text)

        
    return Text,Angle,Percent
            
