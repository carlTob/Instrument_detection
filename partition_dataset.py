""" usage: partition_dataset.py [-h] [-i IMAGEDIR] [-o OUTPUTDIR] [-r RATIO] [-x]
python3 partition_dataset.py -x -i '/home/serge/repos/TensorFlow/workspace/training_demo/images' -r 0.1 -o '/home/serge/repos/TensorFlow/workspace/training_demo/images'
Partition dataset of images into training and testing sets

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGEDIR, --imageDir IMAGEDIR
                        Path to the folder where the image dataset is stored. If not specified, the CWD will be used.
  -o OUTPUTDIR, --outputDir OUTPUTDIR
                        Path to the output folder where the train and test dirs should be created. Defaults to the same directory as IMAGEDIR.
  -r RATIO, --ratio RATIO
                        The ratio of the number of test images over the total number of images. The default is 0.1.

  -e, --ending          The file ending of your annotation file, e.g. txt or xml
"""
import os
import re
from shutil import copyfile
import argparse
import math
import random
import glob


def iterate_dir(source, dest, ratio, ending):
    if not source.endswith('/'):
        source = source + '/'
    ending =ending.replace('.', '')
    source = source.replace('\\', '/')
    dest = dest.replace('\\', '/')
    train_dir = os.path.join(dest, 'train')
    test_dir = os.path.join(dest, 'test')

    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    xml_files = glob.glob(source + '*.{}'.format(ending))
    print(source + '*.{}'.format(ending))
    print(len(xml_files))
    num_images = len(xml_files)
    num_test_images = math.ceil(ratio*num_images)
    copy_xml = True

    
    for i in range(num_test_images):
        idx = random.randint(0, len(xml_files)-1)
        basename =os.path.basename(xml_files[idx]).split('.')[0]
        filename = basename + '.jpg'

        copyfile(os.path.join(source, filename),
                 os.path.join(test_dir, filename))
        if copy_xml:
            xml_filename = basename + '.{}'.format(ending)
            copyfile(os.path.join(source, xml_filename),
                     os.path.join(test_dir,xml_filename))
        xml_files.remove(xml_files[idx])

    for xml_file in xml_files:
        basename =os.path.basename(xml_file).split('.')[0]
        filename = basename + '.jpg'
        copyfile(os.path.join(source, filename),
                 os.path.join(train_dir, filename))
        if copy_xml:
            xml_filename =  basename + '.{}'.format(ending)
            copyfile(os.path.join(source, xml_filename),
                     os.path.join(train_dir, xml_filename))


def main():

    # Initiate argument parser
    parser = argparse.ArgumentParser(description="Partition dataset of images into training and testing sets",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-i', '--imageDir',
        help='Path to the folder where the image dataset is stored. If not specified, the CWD will be used.',
        type=str,
        default=os.getcwd()
    )
    parser.add_argument(
        '-o', '--outputDir',
        help='Path to the output folder where the train and test dirs should be created. '
             'Defaults to the same directory as IMAGEDIR.',
        type=str,
        default=None
    )
    parser.add_argument(
        '-r', '--ratio',
        help='The ratio of the number of test images over the total number of images. The default is 0.1.',
        default=0.1,
        type=float)
    parser.add_argument(
        '-e', '--ending',
        help='The file ending of your annotation file, e.g. txt or xml',
        action='store_true',
        default='txt'
    )
    args = parser.parse_args()

    if args.outputDir is None:
        args.outputDir = args.imageDir
    
    # Now we are ready to start the iteration
    iterate_dir(args.imageDir, args.outputDir, args.ratio, args.ending)


if __name__ == '__main__':
    main()