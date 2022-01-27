import numpy as np
import cv2
import argparse
import os
import random
import string
from moviepy.editor import VideoFileClip
import math
#STEP = 1000
NAME_PREFIX = 'a'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', required=True, action='store', default='.', help="video")
    parser.add_argument('-f', '--image_folder', required=True, action='store', default='.', help="folder")
    parser.add_argument('-s', '--steps', action='store', default=1000, type=int,help="folder")
    parser.add_argument('-start', '--start', action='store', default=0.0, type=float,help="Minute to start")

    parser.add_argument('-end', '--end', action='store', default=10000.0,type=float, help="Minute to end")

    return parser.parse_args()

def get_frame(frame_no, cap):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    return cap.read()

def create_imgs(video, out_folder,STEP, start,end):
    fracS, wholeS = math.modf(start)
    fracE, wholeE = math.modf(end)

    minStart = wholeS + (fracS*100)/60
    minEnd = wholeE + (fracE*100)/60

    clip = VideoFileClip(video)
    minVideo = clip.duration/60
    folder =out_folder
    cap = cv2.VideoCapture(video)
    tot  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if minVideo < end:
        end= minVideo

    
    #print('Tot ', tot)
    if not os.path.exists(folder):
        os.makedirs(folder)
    #print(type(start))
    randString = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    for k in range(round((minStart/minVideo)*tot), round((minEnd/minVideo)*tot), STEP):
        _, frame = get_frame(k, cap)
        #print(frame.shape)
        lname = folder + '/{}{}.jpg'.format(randString, k)

        #diff =  frame.shape[1]-frame.shape[0]
        
	
        #frame = frame[0:frame.shape[0], (diff//2):(frame.shape[1]-(diff//2))]
        #dim = (frame.shape[1]-diff, frame.shape[0])
	# resize image
        #frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        if frame.shape[1]<frame.shape[0]:
            frame = frame.flip(frame,1)
        cv2.imshow('Testing', frame)
        key = cv2.waitKey(1)
        cv2.imwrite(lname, frame)
        print(lname)

    # Release everything if job is finished
    cap.release()
    cv2.destroyAllWindows()
def main():
    args = get_args()
    create_imgs(args.video, args.image_folder,args.steps,args.start, args.end)

if __name__ == '__main__':
    main()
