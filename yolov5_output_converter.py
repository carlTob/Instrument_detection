from anyio import sleep
import cv2
import matplotlib.pyplot as plt
import json
import numpy as np
from PIL import Image
import os.path
from os import path
import argparse
import re
import glob


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--input_folder', required=True, action='store', default='.', help="Folder with yolov5 predictions")
    parser.add_argument('-o', '--output_folder', required=True, action='store', default=None, help="Where to place the converted predictions")
    return parser.parse_args()



def convert_predictions(input_folder, output_folder):
    if not output_folder.endswith("/"):
        output_folder = output_folder + "/"
    if not input_folder.endswith("/"):
        input_folder = input_folder + "/"

    txt_paths =[f for f in glob.glob(input_folder + '*.txt')]
    for path in txt_paths:
        name = path.split("/")[-1]
        with open(path, "r") as f:
            lines = f.readlines()
            new_data = []
            for line in lines:
                l = line.split(" ")
                l[-1] = l[-1].replace("\n","")
                conf = l.pop()
                l.insert(1, conf)
                new_data.append(l)
            with open(output_folder+name, "w") as o:
                for line in new_data:
                    for e in line:
                        o.write(e + " ")
                    o.write("\n")

if __name__ == "__main__":
    args = get_args()
    convert_predictions(args.input_folder, args.output_folder)