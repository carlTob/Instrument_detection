from zipfile import ZIP_MAX_COMMENT
import cv2
from matplotlib.transforms import Bbox
import numpy as np
from scipy import ndimage
import random
import cv2
import matplotlib.pyplot as plt
import json
import numpy as np
from PIL import Image
import os.path
from os import path
import argparse
import os
import numpy as np
import argparse
import os


import xml.etree.cElementTree as ET


def alphaMerge(small_foreground, background, top, left):

    result = background.copy()
    fg_b, fg_g, fg_r, fg_a = cv2.split(small_foreground)
    fg_a = fg_a / 255.0
    label_rgb = cv2.merge([fg_b * fg_a, fg_g * fg_a, fg_r * fg_a])

    height, width = small_foreground.shape[0], small_foreground.shape[1]
    part_of_bg = result[top:top + height, left:left + width, :]
    bg_b, bg_g, bg_r = cv2.split(part_of_bg)
    part_of_bg = cv2.merge([bg_b * (1 - fg_a), bg_g * (1 - fg_a), bg_r * (1 - fg_a)])

    cv2.add(label_rgb, part_of_bg, part_of_bg)
    result[top:top + height, left:left + width, :] = part_of_bg
    return result


def addOverLap(img2,result, nbrIt,bBox,root,name,filename2,w,backH, backW):
    for i in range(0,nbrIt):
        w = w+1
        copyImg2 = ndimage.rotate(img2, 45*w)
        dh, dw, _ = copyImg2.shape
        xMax = (backH/dh)
        yMax = (backW/dw)

        if yMax < xMax:
            fac=round(random.uniform(yMax/3, yMax/2), 2)
        elif yMax > xMax:
            fac=round(random.uniform(xMax/3,  xMax/2), 2)
        copyImg2 = cv2.resize(copyImg2, (0, 0), fx=fac, fy=fac)
        dh, dw, _ = copyImg2.shape
        maxH = backH - dh
        hStart=round(random.uniform(0, maxH))
        maxW = backW - dw
        wStart=round(random.uniform(0, maxW))
        if bBox:

            #cv2.rectangle(result, (wStart,hStart),(wStart +dw,hStart + dh), (0,0,255), 4)

            objectx = ET.SubElement(root, "object")

            ET.SubElement(objectx, "name").text = name
            ET.SubElement(objectx, "pose").text = "Unspecified"
            ET.SubElement(objectx, "truncated").text = "0"
            ET.SubElement(objectx, "difficult").text = "0"

            bndbox = ET.SubElement(objectx, "bndbox")
            ET.SubElement(bndbox, "xmin").text = str(wStart)
            ET.SubElement(bndbox, "ymin").text = str(hStart)
            ET.SubElement(bndbox, "xmax").text = str(wStart +dw)
            ET.SubElement(bndbox, "ymax").text = str(hStart + dh)
        result = alphaMerge(copyImg2, result, hStart, wStart)
    return result,root,w

def start_procc(directory,directoryOut):
    global w
    w=0 
    if not directory.endswith('/'):
        directory = directory + '/'
    if not directoryOut.endswith('/'):
        directoryOut = directoryOut + '/'

    forceps1 = cv2.imread('forceps/test1.png', cv2.IMREAD_UNCHANGED)
    forceps2 = cv2.imread('forceps/newforceps1.png', cv2.IMREAD_UNCHANGED)
    forceps3 = cv2.imread('forceps/newForceps2.png', cv2.IMREAD_UNCHANGED)


    diatermi1 = cv2.imread('diatermis/diatermi.png', cv2.IMREAD_UNCHANGED)
    diatermi2 = cv2.imread('diatermis/newDia1.png', cv2.IMREAD_UNCHANGED)
    diatermi3 = cv2.imread('diatermis/newDia2.png', cv2.IMREAD_UNCHANGED)
    diatermi4 = cv2.imread('diatermis/newDia3.png', cv2.IMREAD_UNCHANGED)


    needleDriver1 = cv2.imread('needleDrivers/newNeedle1.png', cv2.IMREAD_UNCHANGED)
    needleDriver2 = cv2.imread('needleDrivers/newNeedle2.png', cv2.IMREAD_UNCHANGED)
    needleDriver3 = cv2.imread('needleDrivers/newNeedle3.png', cv2.IMREAD_UNCHANGED)
    needleDriver4 = cv2.imread('needleDrivers/newNeedle4.png', cv2.IMREAD_UNCHANGED)




                                
    os.makedirs(directoryOut, exist_ok=True)
    for filename2 in os.listdir(directory):
        if filename2.endswith(".jpg"):
            background = cv2.imread(directory+filename2)
            for i in range(0,6):

                newImgName = str(i)+"-new"+str(filename2)
                backH, backW, depth = background.shape

                root = ET.Element("annotation")

                folder = ET.SubElement(root, "folder")
                folder.text = "testfolder"
                filename = ET.SubElement(root, "filename")
                filename.text = newImgName

                paths = ET.SubElement(root, "path")
                paths.text = directoryOut+newImgName


                source = ET.SubElement(root, "source")
                ET.SubElement(source, "database").text = "Unknown"

                size = ET.SubElement(root, "size")
                ET.SubElement(size, "width").text = str(backW)
                ET.SubElement(size, "height").text = str(backH)
                ET.SubElement(size, "depth").text = str(depth)


                segmented = ET.SubElement(root, "segmented")
                segmented.text = "0"
                w=w+1
                rest = i%3

                if (rest)==0:

                    result,root,w = addOverLap(forceps1,background,1,True,root,"forceps","forceps1",w,backH, backW)
                    result,root,w = addOverLap(needleDriver1,result,1,True,root,"needle driver","needleDriver1",w,backH, backW)
                    result,root,w = addOverLap(diatermi1,result,1,True,root,"diatermi","diatermi1",w,backH, backW)
                    result,root,w = addOverLap(needleDriver2,result,1,True,root,"needle driver","needledrivber2",w,backH, backW)
                    result,root,w = addOverLap(diatermi2,result,1,True,root,"diatermi","diatermi2",w,backH, backW)

                elif (rest)==1:

                    result,root,w = addOverLap(forceps2,background,1,True,root,"forceps","forceps2",w,backH, backW)
                    result,root,w = addOverLap(needleDriver3,result,1,True,root,"needle driver","needledriver3",w,backH, backW)
                    result,root,w = addOverLap(diatermi1,result,1,True,root,"diatermi","diatemri1",w,backH, backW)
                    result,root,w = addOverLap(needleDriver4,result,1,True,root,"needle driver","needledriver4",w,backH, backW)
                    result,root,w = addOverLap(diatermi2,result,1,True,root,"diatermi","dia2",w,backH, backW)
                elif (rest)==2:

                    result,root,w = addOverLap(forceps3,background,1,True,root,"forceps","forceps3",w,backH, backW)
                    result,root,w = addOverLap(needleDriver3,result,1,True,root,"needle driver","needledriver3",w,backH, backW)
                    result,root,w = addOverLap(diatermi3,result,1,True,root,"diatermi","diatermi3",w,backH, backW)
                    result,root,w = addOverLap(needleDriver1,result,1,True,root,"needle driver","needledriver1",w,backH, backW)
                    result,root,w = addOverLap(diatermi4,result,1,True,root,"diatermi","diatermi4",w,backH, backW)
                tree = ET.ElementTree(root)

                tree.write(directoryOut+newImgName.split(".")[0]+".xml")
                cv2.imwrite(directoryOut+newImgName, result)
            


                ##cv2.imshow("result", result)
                ##cv2.waitKey()



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--emptyDir', required=True, action='store', default='.', help="folder")
    parser.add_argument('-t', '--annotatedDir',required=True, action='store', default='.', help="folder")
    return parser.parse_args()
def main():
    args = get_args()
    start_procc(args.emptyDir,args.annotatedDir)

if __name__ == '__main__':
    main()