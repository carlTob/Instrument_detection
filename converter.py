# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
from os import listdir
from os.path import join

import argparse
import glob 

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--image_folder', required=True, action='store', default='.', help="folder")
    
    return parser.parse_args()

classes = [ "diatermi", "forceps"] # own data sets which classes which category to write, in the order



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
 
def convert_annotation(img_dir, label_dir, image_id):
    in_file = open(img_dir + '/%s.xml'%(image_id), encoding = 'utf-8')
    out_file = open(label_dir + '%s.txt'%(image_id), 'w')
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

def convert_all(img_dir):
    label_dir = img_dir
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)
    image_ids =[os.path.basename(f) for f in glob.glob(img_dir + '*.jpg')]
    
    for image_id in image_ids:
        convert_annotation(img_dir, label_dir, image_id[:-4])
    
def main():
    args = get_args()
    convert_all(args.image_folder)

if __name__ == '__main__':
    main()
