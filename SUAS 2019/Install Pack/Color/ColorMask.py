import numpy as np
import cv2

image = cv2.imread("Img/DSC00344.jpg")##image = cv2.imread("1.jpg")
LeftALL = np.zeros_like(image)

image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
maskALL = cv2.inRange(image, (0,0,0), (0,0,0))
##for x in range(120, 0, -5):
for x in range(0,1):
    dictionary ={
# 'White':([0, 0, 128], [255, 57, 255]),
# 'red2':([170, 20, 10], [255, 255, 255]),
# 'red':([0, 20, 10], [8, 255, 255]),
# 'orange':([9, 104, 164], [22, 255, 255]),
# 'Brown':([9, 0, 20], [23, 255, 167]),
# 'yellow':([23, 20, 10], [33, 255, 255]),
# 'green':([34, 10, 10], [90, 255, 255]),
# 'blue':([91, 40, 18], [144, 255, 255]),
# 'purple':([145, 30, 30], [169, 255, 255]),
# 'black':([0, 0, 0], [180, 255, 26])


'grass':([12,0,0], [67,255,192]),
# 'Brown':([10,0,0], [30,255,219]),
'ground':([0,0,0], [255,98,209]),
##'road':([19,0,0], [160,111,165]),

        }      
    color_name = []
    color_count =[]
                
    # loop over the boundaries
    for key,(lower,upper) in dictionary.items():
        
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        str(lower)
         
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image_HSV, lower, upper)
        count = cv2.countNonZero(mask)
        print(key)
        print(count)
        print("-------------------")
        maskALL = mask + maskALL
        res = cv2.bitwise_and(image,image, mask= mask)
        resALL = cv2.bitwise_and(image,image, mask= maskALL)
        Leftmask = cv2.bitwise_not(maskALL)
        LeftALL = cv2.bitwise_and(image,image, mask = Leftmask)
        # LeftALL[Leftmask == 255] = image[Leftmask == 255]
        #cv2.imshow('image',image)
        #cv2.imshow('res',res)
        cv2.imwrite("result\%s-L=%s-H=%s.jpg"%(key,str(lower),str(upper)),res)
##        cv2.imwrite("result\L=%s-H=%smask.jpg"%(str(lower),str(upper)),mask)
        cv2.imwrite("result\ALLmask.jpg",maskALL)
        cv2.imwrite("result\Leftmask.jpg",Leftmask)
        cv2.imwrite("result\ALL.jpg",resALL)
        cv2.imwrite("result\LeftALL.jpg",LeftALL)
        
        #cv2.imshow("mask", mask)
        #cv2.waitKey(1000) 
cv2.destroyAllWindows()

