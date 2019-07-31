import json
import os
def write(SignPath,SHAPE,SignColorName,TextColorName,TEXT,Heading,Percent,Lat,Long):

    SignPath = os.path.splitext(SignPath)[0]
    print(SignPath)

    Data = {
    "alphanumeric": TEXT,
    "alphanumeric_color": TextColorName,
    "autonomous": True,
    "latitude": Lat,
    "longitude": Long,
    "mission": 3,
    "orientation": Heading,
    "shape": SHAPE,
    "shape_color": SignColorName,
    "type": "STANDARD"
}
    with open(SignPath + ".json",'w') as outfile:
        json.dump(Data, outfile,indent=4)
        print(SignPath + ".json")
