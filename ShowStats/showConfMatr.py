import numpy as np
import cv2
import os
from progressbar import ProgressBar
from module import metric_module




import os
import re
from shutil import copyfile
import argparse
import math
import random
import glob
import os.path
import shutil
from xxlimited import Str
import xml.etree.ElementTree as ET


def showStats(FILENAME_GROUNDTRUTH,DIRNAME_NAME, DIRNAME_PREDICTION):
    # settings


    DICT_TEXTNAMES_PREDICTION = { os.path.splitext(p)[0] : os.path.join(DIRNAME_PREDICTION,p) for p in os.listdir(DIRNAME_PREDICTION)}
    #print(DICT_TEXTNAMES_PREDICTION)
    #print(DICT_TEXTNAMES_PREDICTION)



    with open(FILENAME_GROUNDTRUTH) as f:
        IMAGENAMES_GROUNDTRUTH = f.read().splitlines()
    #print(IMAGENAMES_GROUNDTRUTH)

    THRESH_CONFIDENCE      = 0.25
    THRESH_IOU_CONFUSION   = 0.5

    #NAMES_CLASS = [str(n) for n in range(80)]
    with open(DIRNAME_NAME) as f:
        NAMES_CLASS = f.read().splitlines()
    NUMBER_CLASSES = len(NAMES_CLASS)

    ###
    #print("# of data: %d"%len(IMAGENAMES_GROUNDTRUTH))

    metric = metric_module.ObjectDetectionMetric(names_class=NAMES_CLASS,
                                                check_class_first=False)

    pbar = ProgressBar().start()
    for index in range(len(IMAGENAMES_GROUNDTRUTH)):
        imagename = IMAGENAMES_GROUNDTRUTH[index]
        names = os.path.splitext( os.path.basename(imagename) )[0]
        if not os.path.isfile(os.path.join(DIRNAME_PREDICTION,names)+".txt" ):
            print("added",os.path.join(DIRNAME_PREDICTION,names))
            open(os.path.join(DIRNAME_PREDICTION,names)+".txt", "a")
            DICT_TEXTNAMES_PREDICTION[names] = os.path.join(DIRNAME_PREDICTION,names+".txt")

   
        textname_prediction = DICT_TEXTNAMES_PREDICTION[ os.path.splitext( os.path.basename(imagename) )[0] ]
        textname_groundtruth = imagename.replace("images","labels").replace("jpg","txt")
        textname_prediction = textname_prediction.split(".")[0] + ".txt"


        with open(textname_groundtruth) as f:
            info_groundtruth = f.read().splitlines()
        bboxes_groundtruth = []
        labels_groundtruth = []
        for bbox in info_groundtruth:
            bbox = bbox.split()
            label = int(bbox[0])
            #label = 0
            bboxes_groundtruth.append([float(c) for c in bbox[1:5]])
            labels_groundtruth.append(label)
      #  print(textname_prediction)
        if os.path.isfile(textname_prediction):
            print ("")
        else:
            open(textname_prediction, 'w')
        with open(textname_prediction) as f:
          
            info_prediction = f.read().splitlines()
        bboxes_prediction = []
        labels_prediction = []
        scores_prediction = []
        for bbox in info_prediction:
            bbox = bbox.split()
            label      = int(bbox[0])
            #label      = 0
            confidence = float(bbox[1])
            if confidence>=THRESH_CONFIDENCE:
                bboxes_prediction.append([float(c) for c in bbox[2:6]])
                labels_prediction.append(label)
                scores_prediction.append(confidence)

        metric.update(bboxes_prediction=bboxes_prediction,
                    labels_prediction=labels_prediction,
                    scores_prediction=scores_prediction,
                    bboxes_groundtruth=bboxes_groundtruth,
                    labels_groundtruth=labels_groundtruth)
        progress = 100*index/len(IMAGENAMES_GROUNDTRUTH)
        pbar.update(progress)
    pbar.finish()

    #metric.get_mAP(type_mAP="VOC07",
    #               conclude=True)
    print
    metric.get_mAP(type_mAP="VOC07",
                conclude=True)
    print
    metric.get_mAP(type_mAP="VOC12",
                conclude=True)
    print
    metric.get_mAP(type_mAP="COCO",
                conclude=True)
    print
    metric.get_confusion(thresh_confidence=THRESH_CONFIDENCE,
                        thresh_IOU=THRESH_IOU_CONFUSION,
                        conclude=True)

def main():

    # Initiate argument parser
    parser = argparse.ArgumentParser(description="Partition dataset of images into training and testing sets",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-txt', '--Testtxt',
        help='Path to the test.txt file is located.',
        type=str,
        default=None
    )
    parser.add_argument(
        '-name', '--nameFile',
        help='Path to the obj.names file.',
        type=str,
        default=None
    )
    parser.add_argument(
        '-pred', '--PredictFolder',
        help='Path to the output folder where predicted txt files ans jpgs are.',
        type=str,
        default=None
    )

        
        
    args = parser.parse_args()

    
    # Now we are ready to start the iteration
    showStats(args.Testtxt, args.nameFile,args.PredictFolder)


if __name__ == '__main__':
    main()