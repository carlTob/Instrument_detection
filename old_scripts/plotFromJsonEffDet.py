from re import A
from sunau import AUDIO_FILE_ENCODING_ADPCM_G721
import cv2
import matplotlib.pyplot as plt
import json
import numpy as np
from PIL import Image
import os.path
from os import path
import argparse
import shutil

import xml.etree.cElementTree as ET


import json
 
# Opening JSON file
import pandas as pd
fWr= open("/home/serge/exjobb/detectron2/metrics/metrics.txt","w+")
fWr.write("[ \n")
shutil.copyfile('/home/serge2/Documents/Exjobb1/EfficientDet/Efficientdet/log.json', '/home/serge2/Documents/Exjobb1/EfficientDet/testLog.txt')

with open('/home/serge/exjobb/detectron2/metrics/temp_metrics.txt', "r") as a_file:
    nonempty_lines = [line.strip("\n") for line in a_file if line != "\n"]
    line_count = len(nonempty_lines)
    print(line_count)
with open('/home/serge/exjobb/detectron2/metrics/temp_metrics.txt', "r") as a_file:

    c = 1
    for l in a_file:
        fWr.write(l.replace("DLLL",""))
        if c<line_count:

            fWr.write(",")
        c = c+1
fWr.write("] \n")
fWr.close()
shutil.copyfile('/home/serge/exjobb/detectron2/metrics/metrics.txt', '/home/serge/exjobb/detectron2/metrics/metrics.json')
# Opening JSON file
f = open('/home/serge/exjobb/detectron2/metrics/metrics.json')
 
# returns JSON object as
# a dictionary
data = json.load(f)
vals = []
valLoss =[]
map = []
time=[]
timeVal=[]
timeMap=[]
iterations=[]
total_loss=[]
# Iterating through the json
# list
for i in data:
    '''
    if "train_loss" in i["data"]:
        time.append(float(i["elapsedtime"])/60)
        vals.append(i["data"]["train_loss"])
    if "eval_loss" in i["data"]:
        timeVal.append(float(i["elapsedtime"])/60)
        valLoss.append(i["data"]["eval_loss"])
    if "map" in i["data"]:
        timeMap.append(float(i["elapsedtime"])/60)
        map.append(i["data"]["map"])
    '''
    pairs = []
    if "iteration" in i:
        if "total_loss" in i:
            if i["iteration"] < 20:
                print("iterantion: ", float(i["iteration"]))
                if i["iteration"] in pairs:
                    print(i["iteration"], " already exystst" )
                else:
                    pairs.append(i["iteration"])
                iterations.replace(i["iteration"])
                total_loss.replace(i["total_loss"])

    
 

 
# Closing file

import numpy as np
from matplotlib import pyplot as plt
print(len(time))
print(len(vals))
fig, ax = plt.subplots()
ax.plot(time,vals,color="green",label="Training loss")
#ax.plot(timeVal,valLoss,color="blue",label="Validation loss")

#ax2 = ax.twinx()

#ax2.plot(timeMap,map,color="red",label="map")
#ax2.tick_params(axis='y', labelcolor='red')
#ax.legend(loc = 'upper right')
plt.scatter(iterations, total_loss)
plt.ylabel('Loss')
plt.xlabel('iterations')
plt.show()
f.close()

