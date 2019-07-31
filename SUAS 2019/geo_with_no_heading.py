from pathlib import Path
import math

#focal length ได้มาจากกล้อง
#สูตรเเปลงค่าพิกัดจากภาพเป็นทศนิยม
def tag(Lofile,cX,cY,H,W,Angle):
    f = open(Lofile,"r")
    (f.readline())
    a=int(f.readline())
    b=int(f.readline())
    h=int(f.readline())
    
    #จะกำกับไว้เผื่อทดลองค่า
    Latofthemidpic=a/10000000
    Longofthemidpic=b/10000000
    headingnum=h/100 
    #####print("location from geo ",Latofthemidpic,Longofthemidpic)
    headingnum = headingnum + Angle
    if headingnum >= 360:
        headingnum -= 360

    if headingnum <=10 or headingnum >350:
        heading="N"
    if 10< headingnum <=80:
        heading="NE"
    if 80< headingnum <=100:
        heading="E"
    if 100< headingnum <=170:
        heading="SE"
    if 170< headingnum <=190:
        heading="S"
    if 190< headingnum <=260:
        heading="SW"
    if 260< headingnum <=290:
        heading="W"
    if 290< headingnum <=350:
        heading="NW"

    #dlat=1#minlat=1
    #seclat=1#dlong=1
    #minlong=1#seclong=1
    #DDlat = dlat + (minlat/60) + (seclat/3600)
    #DDlong = dlong + (minlong/60) + (seclong/3600)
    #print(DDlat,DDlong)

    #sony a5100
    FL=16
    #ไว้ได้ค่าเเล้วค่อยมาใส่ areapic(ฟุต)
    areaperpic=58125
    squareinch=areaperpic*144
    ppsi=FL*1000000/squareinch
    #px,pyได้มาจากalgo 
    pixelalgo_x=cX  
    pixelalgo_y=cY
    #px,pymidค่อยใส่เพิ่มเป็นh,ของป้าย
    pxmid=int(W/2)
    pymid=int(H/2)
    px=-(pixelalgo_x-pxmid)
    py=-(pixelalgo_y-pymid)
    ps=(px,py)
    #dx,dyระยะห่างจริงจากภาพ
    dx=px/math.sqrt(ppsi)
    dy=py/math.sqrt(ppsi)
    realdistance_inch=(dx,dy)
    #รัศมีโลก
    r0earth=250826270
    #ค่า Latofthemidpic,Longofthemidpic คือพิกัดของกลางรูป(13.919102, 100.628728)
    # Latofthemidpic=13.9192214
    # Longofthemidpic=100.6286963
    perdegree0earthrasdius=2*math.pi*r0earth/360
    change_lat=dy/perdegree0earthrasdius
    change_long=dx/((math.cos((change_lat+Longofthemidpic)/2))*perdegree0earthrasdius)
    label_gps_lat=Latofthemidpic+change_lat
    label_gps_long=Longofthemidpic+change_long
    #ได้พิกัดตรงปลายเรียบร้อย
    cs=(label_gps_lat,label_gps_long)
    

    print (cs)
    print  ('inch is ',realdistance_inch)
    print (ps)
    print (change_long)
    print (change_lat)
    print("---------------------------------------------------------------------------")
    return label_gps_lat,label_gps_long,heading



# Lofile = "try/Location/1BAK2C~1"
# cX=96
# cY=5583
# H=6000
# W=4000
# Angle=138
# tag(Lofile,cX,cY,H,W,Angle)