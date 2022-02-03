import cv2
import matplotlib.pyplot as plt
import json
import numpy as np
from PIL import Image
import os.path
from os import path
import argparse


import xml.etree.cElementTree as ET




root = ET.Element("annotation")

folder = ET.SubElement(root, "folder")
folder.text = "testfolder"

filename = ET.SubElement(root, "filename")
filename.text = "testfolder"

path = ET.SubElement(root, "path")
path.text = "testfolder"


source = ET.SubElement(root, "source")
ET.SubElement(source, "database").text = "Unknown"

size = ET.SubElement(root, "size")
ET.SubElement(size, "width").text = "Unknown"
ET.SubElement(size, "height").text = "Unknown"
ET.SubElement(size, "depth").text = "Unknown"


segmented = ET.SubElement(root, "segmented")
segmented.text = "0"

#For all objects

objectx = ET.SubElement(root, "object")
ET.SubElement(objectx, "name").text = "Unknown"
ET.SubElement(objectx, "pose").text = "Unspecified"
ET.SubElement(objectx, "truncated").text = "0"
ET.SubElement(objectx, "difficult").text = "0"

bndbox = ET.SubElement(objectx, "bndbox")
ET.SubElement(bndbox, "xmin").text = "Unknown"
ET.SubElement(bndbox, "ymin").text = "Unspecified"
ET.SubElement(bndbox, "xmax").text = "0"
ET.SubElement(bndbox, "ymax").text = "0"


tree = ET.ElementTree(root)
tree.write("filename.xml")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--result_path', required=True, action='store', default='.', help="Where to retrieve pictures")
    parser.add_argument('-t', '--put_path',action='store', default='a', help="Where to put results")
    return parser.parse_args()

def draw_boxes(resultPath,putPath):

    image_path = putPath
    if not path.exists(image_path):
        os.mkdir(image_path)


    f = open(resultPath)
    data = json.load(f)
    for p in range(0, len(data)):

        imgName = data[p]['filename'].split('/')[-1]
        imgOrig = cv2.imread(data[p]['filename'])
        img = np.copy(imgOrig)
        dh, dw, _ = img.shape
        for i in data[p]['objects']:
            
            name = i['name']
            print(i['name'])
            cords = i["relative_coordinates"]
            print(cords)
            x= cords["center_x"]
            y= cords["center_y"]
            w= cords["width"]
            h= cords["height"]
            

            # Taken from https://github.com/pjreddie/darknet/blob/810d7f797bdb2f021dbe65d2524c2ff6b8ab5c8b/src/image.c#L283-L291
            # via https://stackoverflow.com/questions/44544471/how-to-get-the-coordinates-of-the-bounding-box-in-yolo-object-detection#comment102178409_44592380
            nx = int(float(x)*dw - dw*(w/2))
            ny = int(float(y)*dh - dh*(h/2))
            nw = int(float(w)*dw)
            nh = int(float(h)*dh)
            if name == "forceps":
                cv2.rectangle(img, (nx,ny), (nx+nw,ny+nh), (0,0,255), 4)
                cv2.putText(img, i['name']+ "  Confidence score: " + str(i['confidence']), (nx, ny-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 4)
            if name == "head":
                cv2.rectangle(img, (nx,ny), (nx+nw,ny+nh), (146, 43, 33), 4)
                cv2.putText(img, i['name'] + "  Confidence score: " + str(i['confidence']), (nx, ny-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 4)
            if name == "diatermi":
                cv2.rectangle(img, (nx,ny), (nx+nw,ny+nh), (39, 174, 96), 4)
                cv2.putText(img, i['name']+ "  Confidence score: " + str(i['confidence']), (nx, ny-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 4)

        cv2.imwrite(os.path.join(image_path , "bound_box_"+ imgName),img)
        #cv2.waitKey(0)
        #plt.imshow(img)
        #plt.show()

    f.close()

def main():
    args = get_args()
    draw_boxes(args.result_path,args.put_path)

if __name__ == '__main__':
    main()


