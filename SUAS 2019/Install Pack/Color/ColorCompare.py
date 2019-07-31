import numpy as np
import cv2
import os

LHtwo=0
LStwo=0
LLtwo=0
HHtwo=0
HStwo=0
HLtwo=0

def nothing(x):
  pass
add = False
on = False

path1 = "Img/"
for root, directory,filename in os.walk(path1):
  print(filename)

#Trackbar Image & Size
Imgwnd = 'Image & Size'
Imgwnd2 = 'Image & Size2'
cv2.namedWindow(Imgwnd,cv2.WINDOW_KEEPRATIO)
cv2.createTrackbar("Image", Imgwnd,0,len(filename)-1,nothing)
cv2.createTrackbar("Size", Imgwnd,1,99,nothing)

cv2.namedWindow(Imgwnd2,cv2.WINDOW_KEEPRATIO)
cv2.createTrackbar("Image", Imgwnd2,0,len(filename)-1,nothing)
cv2.createTrackbar("Size", Imgwnd2,1,99,nothing)

##cv2.createTrackbar("", wnd,0,255,nothing)
##cv2.createTrackbar("", wnd,0,255,nothing)
##cv2.createTrackbar("", wnd,0,255,nothing)
##cv2.createTrackbar("", wnd,0,255,nothing)
##cv2.createTrackbar("", wnd,0,255,nothing)
##cv2.createTrackbar("", wnd,0,255,nothing)


##cv2.createTrackbar("", wnd,0,255,nothing)
##cv2.createTrackbar("", wnd,0,255,nothing)
##cv2.createTrackbar("", wnd,0,255,nothing)
##cv2.createTrackbar("", wnd,0,255,nothing)
##cv2.createTrackbar("", wnd,0,255,nothing)
##cv2.createTrackbar("", wnd,0,255,nothing)

while(1):
    
  i=cv2.getTrackbarPos("Image", Imgwnd)
  Size=cv2.getTrackbarPos("Size", Imgwnd)
  image = cv2.imread(root+filename[i])
  img = cv2.resize(image, (0,0), fx = 1-0.01*Size, fy= 1-0.01*Size)
  cv2.namedWindow("img",cv2.WINDOW_AUTOSIZE)
  cv2.imshow("img",img)

  i2=cv2.getTrackbarPos("Image", Imgwnd2)
  Size2=cv2.getTrackbarPos("Size", Imgwnd2)
  image2 = cv2.imread(root+filename[i2])
  img2 = cv2.resize(image2, (0,0), fx = 1-0.01*Size2, fy= 1-0.01*Size2)
  cv2.namedWindow("img2",cv2.WINDOW_AUTOSIZE)
  cv2.imshow("img2",img2)

  if cv2.waitKey(1) == ord('y'):
    break
cv2.destroyAllWindows()
print("-Confirmed-")
print(filename[i])
#Image and Size
image = cv2.imread(root+filename[i])
img = cv2.resize(image, (0,0), fx=1-0.01*Size, fy=1-0.01*Size)
LeftALL = np.zeros_like(img)

image2 = cv2.imread(root+filename[i2])
img2 = cv2.resize(image2, (0,0), fx=1-0.01*Size2, fy=1-0.01*Size2)
LeftALL2 = np.zeros_like(img2)
#LeftALL[:] = (0, 0, 255)

image_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
maskALL = cv2.inRange(img, (0,0,0), (0,0,0))

image_HSV2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
maskALL2 = cv2.inRange(img2, (0,0,0), (0,0,0))

#Trackbar Color
wnd = 'H-S-L bar'
cv2.namedWindow(wnd,cv2.WINDOW_NORMAL)

cv2.createTrackbar("Low-H", wnd,0,255,nothing)
cv2.createTrackbar("Low-S", wnd,0,255,nothing)
cv2.createTrackbar("Low-L", wnd,0,255,nothing)

cv2.createTrackbar("High-H", wnd,0,255,nothing)
cv2.setTrackbarPos("High-H", wnd, 255)
cv2.createTrackbar("High-S", wnd,0,255,nothing)
cv2.setTrackbarPos("High-S", wnd, 255)
cv2.createTrackbar("High-L", wnd,0,255,nothing)
cv2.setTrackbarPos("High-L", wnd, 255)
old = 0
while(1):
  #Get Value
  LH = cv2.getTrackbarPos("Low-H", wnd)
  LS = cv2.getTrackbarPos("Low-S", wnd)
  LL = cv2.getTrackbarPos("Low-L", wnd)

  HH = cv2.getTrackbarPos("High-H", wnd)
  HS = cv2.getTrackbarPos("High-S", wnd)
  HL = cv2.getTrackbarPos("High-L", wnd)

##  #add color
##  if add == True:
##    cv2.createTrackbar("2Low-H", wnd,0,255,nothing)
##    cv2.createTrackbar("2Low-S", wnd,0,255,nothing)
##    cv2.createTrackbar("2Low-L", wnd,0,255,nothing)
##
##    cv2.createTrackbar("2High-H", wnd,0,255,nothing)
##    cv2.setTrackbarPos("2High-H", wnd, 255)
##    cv2.createTrackbar("2High-S", wnd,0,255,nothing)
##    cv2.setTrackbarPos("2High-S", wnd, 255)
##    cv2.createTrackbar("2High-L", wnd,0,255,nothing)
##    cv2.setTrackbarPos("2High-L", wnd, 255)
##    add = False
    

      
  #Filter background using colored mask
  light_one = (LH, LS, LL)
  dark_one = (HH, HS ,HL)

  mask_one = cv2.inRange(image_HSV,light_one,dark_one)
  mask_two = cv2.inRange(image_HSV2,light_one,dark_one)
  
  mask = mask_one
  Getone = cv2.bitwise_and(img,img, mask= mask_one)

  mask2 = mask_two
  Gettwo = cv2.bitwise_and(img2,img2, mask= mask_two)

  Leftmask = cv2.bitwise_not(mask)
  Leftmask2 = cv2.bitwise_not(mask2)

  LeftALL[Leftmask == 255] = img[Leftmask == 255]
  LeftALL2[Leftmask2 == 255] = img2[Leftmask2 == 255]
##  if on == True:
##    LeftALL = np.zeros_like(img)
##    LHtwo = cv2.getTrackbarPos("2Low-H", wnd)
##    LStwo = cv2.getTrackbarPos("2Low-S", wnd)
##    LLtwo = cv2.getTrackbarPos("2Low-L", wnd)
##
##    HHtwo = cv2.getTrackbarPos("2High-H", wnd)
##    HStwo = cv2.getTrackbarPos("2High-S", wnd)
##    HLtwo = cv2.getTrackbarPos("2High-L", wnd)
##
##    light_two = (LHtwo, LStwo, LLtwo)
##    dark_two = (HHtwo, HStwo ,HLtwo)
##    mask_two = cv2.inRange(image_HSV,light_two,dark_two)
##
##    mask = mask_one + mask_two
##
##    Gettwo = cv2.bitwise_and(img,img, mask= mask_two)
##    GetALL = cv2.bitwise_and(img,img, mask= mask)
##    Leftmask = cv2.bitwise_not(mask)
##    
##    LeftALL[Leftmask == 255] = img[Leftmask == 255]
##
  cv2.imshow("Getone",Getone)
  cv2.imshow("Gettwo",Gettwo)
  
##  cv2.imshow("mask",mask)
##  cv2.imshow("GetALL",GetALL)
  cv2.imshow("Leftmask",Leftmask)
##  cv2.imshow("LeftALL",LeftALL)
  cv2.imshow("Leftmask2",Leftmask2)
##  cv2.imshow("LeftALL2",LeftALL2)
##  Getcount = cv2.countNonZero(mask)

##  if old != Getcount:
##    old = Getcount
##    print(Getcount)

##  if cv2.waitKey(1) == ord('+'):
##        add = True
##        on = True
##
  if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
print("LOW[%d,%d,%d] HIGH[%d,%d,%d]"%(LH,LS,LL,HH,HS,HL))
##print("2LOW[%d,%d,%d] 2HIGH[%d,%d,%d]"%(LHtwo,LStwo,LLtwo,HHtwo,HStwo,HLtwo))
##cv2.imwrite("result/LOW[%d,%d,%d] HIGH[%d,%d,%d]-2LOW[%d,%d,%d] 2HIGH[%d,%d,%d].jpg"%(LH,LS,LL,HH,HS,HL,LHtwo,LStwo,LLtwo,HHtwo,HStwo,HLtwo),LeftALL)
cv2.imwrite("result/LOW[%d,%d,%d] HIGH[%d,%d,%d].jpg"%(LH,LS,LL,HH,HS,HL),LeftALL)
