import numpy as np
import cv2
import argparse
import os
import random
import string
import moviepy.editor as mp
import math
#STEP = 1000
NAME_PREFIX = 'a'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', required=True, action='store', default='.', help="video")
    parser.add_argument('-o', '--out_folder', required=True, action='store', default='.', help="folder")
    parser.add_argument('-n', '--clip_name', required=True, action='store', default='.', help="clip name")

    return parser.parse_args()


def create_clip(video, out_folder, clip_name):
    if not out_folder.endswith('/'):
        out_folder = out_folder + '/'

    video = mp.VideoFileClip(video)

    # delete video fragment from 00:30 to 01:00
    segments = [(1738,4391)]

    clips = []  # list of all video fragments
    for start_seconds, end_seconds in segments:
        # crop a video clip and add it to list
        c = video.subclip(start_seconds, end_seconds)
        clips.append(c)

    final_clip = mp.concatenate_videoclips(clips)
    print("filepath to clip: ", out_folder + clip_name)
    final_clip.write_videofile(out_folder + clip_name)
    final_clip.close()

def main():
    args = get_args()
    create_clip(args.video, args.out_folder, args.clip_name)

if __name__ == '__main__':
    main()



for_glen_clip1_20210603 = [(0, 20),
                (1*60 +50, 2*60),
                (7*60+25, 7*60+30),
                (9*60+6, 9*60+10),
                (37*60+32, 37*60+37),
                (76*60+23, 76*60+47),
                (85*60+7, 85*60+13),
                (94*60+43,95*60+11),
                (104*60+33, 104*60+39)
                ]