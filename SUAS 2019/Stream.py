import os
import shutil
import time
import Remove
import Shape
import COLOR
import fitcrop
import RotateTesser
import geo_with_no_heading
import writeJSON
start = time.time()
path1= "\\\\10.42.0.1\\Share\\Img/"
path2= "\\\\10.42.0.1\\Share\\Location/"
# path3= "\\\\10.42.0.1\\Share\\Imgbackup/"
# path4= "\\\\10.42.0.1\\Share\\Locationbackup/"
# path1= "try/Img/"
# path2= "try/Location/"
path3= "zbackup/Imgbackup/"
path4= "zbackup/Locationbackup/"
Current=0

PathMake = ("Detected")
PathMake0 = ("SUAS")
PathMake1 = ("[removed]BG")
print(PathMake)
print(PathMake0)
print(PathMake1)
try:
        os.mkdir(PathMake)
        os.mkdir(PathMake0)
        os.mkdir(PathMake1)
except OSError:
        print ("Creation of the directory %s failed" % PathMake)
        print ("Creation of the directory %s failed" % PathMake0)
        print ("Creation of the directory %s failed" % PathMake1)
else:
        print ("Successfully created the directory %s " % PathMake)
        print ("Successfully created the directory %s " % PathMake0)
        print ("Successfully created the directory %s " % PathMake1)

while True:
    startin = time.time()
##    filename = []
##    for root, directory,filenames in os.walk(path1):
##        for file in filenames:
##                if file.endswith(".jpg"):
##                        filename.append(file)
##        filename = natsort.natsorted(filename)


    
    try:
           filename = os.listdir(path1)[0]
           locatonfile = os.listdir(path2)[0]
           print(filename)
           print(locatonfile)

    except Exception:
        filename = ""
        locatonfile = ""
        print("--- NO file ---")
        time.sleep(1)
        continue        
        
    if filename != "" and locatonfile != "" :
        
        print(filename)
        print("------------------------Start Removing Background------------------------")
        RemoveImg = Remove.Removed(filename,path1)
        print(RemoveImg)

        print("------------------------Start Dectecting Shape------------------------")
        SignSharpImg,NameImg,SHAPEALL,SignPath,PathClean,CX,CY,H,W,PathMake6 = Shape.con(filename,RemoveImg,path1)

        print("-NameImg-")
        print(NameImg) 
        print("-SignSharpImg-")
        print(*SignSharpImg, sep = "\n")
        print("-SHAPEALL-")
        print(*SHAPEALL, sep = "\n")
##        if len(SignSharpImg)==0:
##                Current+=1
##                continue
            


        print("------------------------Start Color Masking------------------------")
        # Get color
        #print(SignSharpImg)
        t=0
        TextoutFiles=[]
        TextColorFiles=[]
        ColorTextALL=[]
        ColorSignALL=[]
        SignFilesNameALL=[]
        SignSharpFilesNameALL=[]
        
        for t in range (len(SignSharpImg)):
                print("Picture :",t+1)
                ColorA,TextoutFile,SignSharpFiles = COLOR.color(SignSharpImg[t],NameImg)
                TextoutFiles.append(TextoutFile)
                ColorSignALL.append(ColorA)
                SignSharpFilesNameALL.append(SignSharpFiles)
        print("-ColorSignALL-")
        print(*ColorSignALL, sep = "\n")

        for t in range (len(SignPath)):
                print("Picture :",t+1)
                ColorB,TextColorFile,SignFiles = COLOR.color1(SignPath[t],NameImg)
                TextColorFiles.append(TextColorFile)
                ColorTextALL.append(ColorB)
                SignFilesNameALL.append(SignFiles)
        print("-ColorTextALL-")
        print(*ColorTextALL, sep = "\n")
     
        

        print("------------------------Start Letters Masking------------------------")
        t=0
        TextCleanFiles= []
        TextcolorFiles= []
        OldAngles = []
        for t in range (len(TextoutFiles)):
                print("Picture :",TextoutFiles[t])
                TextClean,TextColor,OldAngle = fitcrop.fit(TextoutFiles[t],TextColorFiles[t],PathClean)
                TextCleanFiles.append(TextClean)
                TextcolorFiles.append(TextColor)
                OldAngles.append(OldAngle)
        print("-TextCleanFiles-")
        print(*TextCleanFiles, sep = "\n")
        print("-TextColorFiles-")
        print(*TextColorFiles, sep = "\n")
        print("-OldAngles-")
        print(*OldAngles, sep = "\n")

        print("------------------------Start Letters Defining------------------------")
        TextColorNameALL = []
        for t in range (len(TextcolorFiles)):
                print("Picture :",t+1)
                TextColorName = COLOR.colortext(TextcolorFiles[t])
                TextColorNameALL.append(TextColorName)
        print("TextColorNameALL")
        print(*TextColorNameALL, sep = "\n")

        print("------------------------Start OCR------------------------")
        # Get TEXT
        t=0
        TextALL =[]
        TextSignALL =[]

        AngleALL =[]
        PercentALL =[]
            
        print("Len[TextCleanFiles]",len(TextCleanFiles))
        for t in range (len(TextCleanFiles)):
            print("Picture#%d-%s"%(t,SignSharpImg[t])) 
            text,Angle,Percent = RotateTesser.TessRo(TextCleanFiles[t],SignSharpImg[t],OldAngles[t])

            TextALL.append(text)

            AngleALL.append(Angle)
            PercentALL.append(Percent)

            
            print("-TextALL-")
            print(*TextALL, sep = "\n")

        print("------------------------Start Geotgging------------------------")
        LatALL = []
        LongALL = []
        HeadingALL = []
        for t in range (len(CX)):
                print("Picture#",t)
                Lat,Long,heading = geo_with_no_heading.tag(path2+locatonfile,CX[t],CY[t],H,W,AngleALL[t])
                LatALL.append(Lat)
                LongALL.append(Long)
                HeadingALL.append(heading)
        
        
        print("------------------------Start Writing JSON Files------------------------")
        t=0
        print(len(SignPath))
        for t in range (len(SignPath)):
            print("Picture#",t)
            writeJSON.write(SignPath[t],SHAPEALL[t],ColorSignALL[t],TextColorNameALL[t],TextALL[t],HeadingALL[t],PercentALL[t],LatALL[t],LongALL[t])#LatALL[t],LongALL[t])

        shutil.copy(path1+filename, path3)
        os.remove(path1+filename)
        shutil.copy(path2+locatonfile,path4)
        os.remove(path2+locatonfile)
end = time.time()
print("->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->")
print("Time :",end - start)
print("Number of Images :",len(filename))
    
    
    
    
