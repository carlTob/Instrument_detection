# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
from os import listdir
from os.path import join
import glob 

classes = [ "diatermi", "forceps"] # own data sets which classes which category to write, in the order

TRAIN_DATA = '/home/serge/repos/TensorFlow/workspace/training_demo/images/train'
TEST_DATA = '/home/serge/repos/TensorFlow/workspace/training_demo/images/test'

LABEL_DIR = '/home/serge/repos/yolov4_darknet/build/darknet/x64/data/obj_validation/'
IMG_DIR = '/home/serge/repos/yolov4_darknet/build/darknet/x64/data/obj_validation/*.jpg'


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
 
def convert_annotation(image_id):
    in_file = open(TRAIN_DATA + '/%s.xml'%(image_id), encoding = 'utf-8')
    out_file = open(LABEL_DIR + '%s.txt'%(image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
 
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

val_percent = 0.1 # test set proportion of the total data set, the default 0.1, if the test set and the training set have been demarcated, the corresponding code is modified
data_path = 'data / excavator /' # darknet relative path folder, see description github, and they need to modify, according to note here the absolute path can also be used
if not os.path.exists('labels/'):
    os.makedirs('labels/')
image_ids =[os.path.basename(f) for f in glob.glob(IMG_DIR)]

with open('train.txt', 'w') as train_file:
for i, image_id in enumerate(image_ids):
    convert_annotation(image_id[:-4])
    train_file.write(LABEL_DIR + image_id + '\n')

train_file.close()
with open('test.txt', 'w') as val_file:
    for i, image_id in enumerate(image_ids):
        convert_annotation(image_id[:-4])
        val_file.write(LABEL_DIR + image_id + '\n')