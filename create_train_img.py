import numpy as np
import cv2
import argparse
import os

STEP = 1000
NAME_PREFIX = 'a'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', required=True, action='store', default='.', help="video")
    parser.add_argument('-f', '--image_folder', required=True, action='store', default='.', help="folder")
    return parser.parse_args()

def get_frame(frame_no, cap):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    return cap.read()

def create_imgs(video, out_folder):
    folder =out_folder
    cap = cv2.VideoCapture(video)
    tot  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('Tot ', tot)
    if not os.path.exists(folder):
        os.makedirs(folder)
    for k in range(1, tot, STEP):
        _, frame = get_frame(k, cap)
        lname = folder + '/{}{}.jpg'.format(NAME_PREFIX, k)
        #print(frame.shape)
        
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
    create_imgs(args.video, args.image_folder)

if __name__ == '__main__':
    main()
