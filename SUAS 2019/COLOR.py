import numpy as np
import cv2
import os
def color(SignSharpPath,NameImg):

    SignSharpFilesEx = os.path.basename(SignSharpPath)
    SignSharpFiles = os.path.splitext(SignSharpFilesEx)[0]
    
    image = cv2.imread(SignSharpPath)
    image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    TextImg = np.zeros_like(image)
    # TextForColor = np.zeros_like(image)
    # TextForColor[:] = (100, 100, 100)

    h,w = image.shape[:2]
##    print("SignSharpPath")
##    print(SignSharpPath)
    print("SignSharpFiles")
    print(SignSharpFiles)
    print("---------------------------------------")
    dictionary ={
'WHITE':([0, 0, 128], [255, 57, 255]),
'RED2':([170, 20, 10], [255, 255, 255]),
'RED':([0, 20, 10], [8, 255, 255]),
'ORANGE':([9, 104, 164], [22, 255, 255]),
'BROWN':([9, 0, 20], [23, 255, 167]),
'YELLOW':([23, 20, 10], [33, 255, 255]),
'GREEN':([34, 10, 10], [90, 255, 255]),
'BLUE':([91, 40, 18], [144, 255, 255]),
'PURPLE':([145, 30, 30], [169, 255, 255]),
'BLACK':([0, 0, 0], [180, 255, 26])                 }      

    ColorCountA = 0

    ColorNameA = ""

    ColorMaskA = image

    TextoutFiles=[]
               
    # loop over the boundaries
    for key,(lower,upper) in dictionary.items():
        
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
         
        # find the colors within the specified boundaries and apply
        # the mask
        
        mask = cv2.inRange(image_HSV, lower, upper)
        
        if key == "RED2":
            maskRED2=mask
        if key == "RED":
            mask=mask+maskRED2
        

        count = cv2.countNonZero(mask)
        if key == "RED2":
            count = 0
        print(key)
        print("count",count) 

        res = cv2.bitwise_and(image,image, mask= mask)

        #cv2.imwrite("Detected/%s/Sign/%s-%s.jpg"%(NameImg,SignSharpFiles,key),res)
        #print("Detected/%s/Sign/%s-%s.jpg"%(NameImg,SignSharpFiles,key))



        if count > ColorCountA:
            ColorCountA = count
            ColorNameA = key
            ColorMaskA = mask
        
    
    NotA = cv2.bitwise_not(ColorMaskA)

    # TextImg[NotA  == 255] = image[NotA == 255]
    # TextForColor[NotA  == 255] = image[NotA == 255]
    TextImg = cv2.bitwise_and(image,image, mask = NotA)
    # TextImg = cv2.bitwise_and(image,image, mask = ColorMaskB)
    cv2.imwrite("Detected/%s/Text/SharpText/%s-Text.jpg"%(NameImg,SignSharpFiles),TextImg)
    # cv2.imwrite("Detected/%s/Text/%s-Textcolor.jpg"%(NameImg,SignSharpFiles),TextForColor)
    
    # cv2.imwrite("JSON/%s-Text.jpg"%SignSharpFiles,TextImg)
        
    TextoutFile=("Detected/%s/Text/SharpText/%s-Text.jpg"%(NameImg,SignSharpFiles))
    print ("the dominant color is:", ColorNameA)
    print("---------------------------------------")
    
    return ColorNameA,TextoutFile,SignSharpFiles



# ------------------------Second Part text color

def color1(SignPath,NameImg):

    SignFilesEx = os.path.basename(SignPath)
    SignFiles = os.path.splitext(SignFilesEx)[0]
    
    image = cv2.imread(SignPath)
    image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # TextImg = np.zeros_like(image)
    TextForColor = np.zeros_like(image)
    TextForColor[:] = (100, 100, 100)

    h,w = image.shape[:2]
##    print("SignPath")
##    print(SignPath)
    print("SignFiles")
    print(SignFiles)
    print("---------------------------------------")
    dictionary ={
'WHITE':([0, 0, 128], [255, 57, 255]),
'RED2':([170, 20, 10], [255, 255, 255]),
'RED':([0, 20, 10], [8, 255, 255]),
'ORANGE':([9, 104, 164], [22, 255, 255]),
'BROWN':([9, 0, 20], [23, 255, 167]),
'YELLOW':([23, 20, 10], [33, 255, 255]),
'GREEN':([34, 10, 10], [90, 255, 255]),
'BLUE':([91, 40, 18], [144, 255, 255]),
'PURPLE':([145, 30, 30], [169, 255, 255]),
'BLACK':([0, 0, 0], [180, 255, 26])                 }      

    ColorCountB = 0

    ColorNameB = ""

    ColorMaskB = image

    TextColorFiles=[]
               
    # loop over the boundaries
    for key,(lower,upper) in dictionary.items():
        
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
         
        # find the colors within the specified boundaries and apply
        # the mask
        
        mask = cv2.inRange(image_HSV, lower, upper)
        
        if key == "RED2":
            maskRED2=mask
        if key == "RED":
            mask=mask+maskRED2
        

        count = cv2.countNonZero(mask)
        if key == "RED2":
            count = 0
        print(key)
        print("count",count) 

        # res = cv2.bitwise_and(image,image, mask= mask)

        #cv2.imwrite("Detected/%s/Sign/%s-%s.jpg"%(NameImg,SignFiles,key),res)
        #print("Detected/%s/Sign/%s-%s.jpg"%(NameImg,SignFiles,key))



        if count > ColorCountB:
            ColorCountB = count
            ColorNameB = key
            ColorMaskB = mask
        
    
    NotB = cv2.bitwise_not(ColorMaskB)

    TextForColor[NotB  == 255] = image[NotB == 255]
    # TextImg = cv2.bitwise_and(image,image, mask = NotB)
    cv2.imwrite("Detected/%s/Text/ColorText/%s-Text.jpg"%(NameImg,SignFiles),TextForColor)
    TextColorFile=("Detected/%s/Text/ColorText/%s-Text.jpg"%(NameImg,SignFiles))
    print ("the Removed color is:", ColorNameB)
    print("---------------------------------------")
    
    return ColorNameB,TextColorFile,SignFiles


# -----------------------get text color

def colortext(ColorPath):
    
    image = cv2.imread(ColorPath)
    image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    print("ColorPath")
    print(ColorPath)
    print("---------------------------------------")
    dictionary ={
'WHITE':([0, 0, 128], [255, 57, 255]),
'RED2':([170, 20, 10], [255, 255, 255]),
'RED':([0, 20, 10], [8, 255, 255]),
'ORANGE':([9, 104, 164], [22, 255, 255]),
'BROWN':([9, 0, 20], [23, 255, 167]),
'YELLOW':([23, 20, 10], [33, 255, 255]),
'GREEN':([34, 10, 10], [90, 255, 255]),
'BLUE':([91, 40, 18], [144, 255, 255]),
'PURPLE':([145, 30, 30], [169, 255, 255]),
'BLACK':([0, 0, 0], [180, 255, 26])                 }      

    ColorCount = 0

    ColorName = "GRAY"
               
    # loop over the boundaries
    for key,(lower,upper) in dictionary.items():
        
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
         
        # find the colors within the specified boundaries and apply
        # the mask
        
        mask = cv2.inRange(image_HSV, lower, upper)
        
        if key == "RED2":
            maskRED2=mask
        if key == "RED":
            mask=mask+maskRED2
        

        count = cv2.countNonZero(mask)
        if key == "RED2":
            count = 0
        print(key)
        print("count",count) 




        if count > ColorCount:
            ColorCount = count
            ColorName = key
            ColorMask = mask
        
    print ("the Removed color is:", ColorName)
    print("---------------------------------------")
    
    return ColorName