import glob
import os
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--data_folder', required=True, action='store', default='.', help="folder")
    parser.add_argument('-n', '--name', required=True, action='store', default='.', help="Either train or test")
    
    return parser.parse_args()

def create_file(data_folder, name):

    #DIR = '/home/serge/repos/yolov4_darknet/build/darknet/x64/data/obj/' 
    image_ids =[os.path.basename(f) for f in glob.glob(data_folder + '*.jpg')]
    print(glob.glob(data_folder + '*.jpg'));
    with open(f'{name}.txt', 'w') as list_file:
        for i, image_id in enumerate(image_ids):
            list_file.write(data_folder + image_id + '\n')

def main():
    args = get_args()
    create_file(args.data_folder, args.name)

if __name__ == '__main__':
    main()

