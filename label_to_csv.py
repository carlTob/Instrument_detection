import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import argparse


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (path +"/"+root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():

    # Initiate argument parser
    parser = argparse.ArgumentParser(description="Partition dataset of images into training and testing sets",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-i', '--imageDir',
        help='Path to the folder where the image dataset is stored. ',
        type=str,
        default=os.getcwd()
    )
    parser.add_argument(
        '-o', '--outputDir',
        help='Path to the output folder where the data csv file should be stored',
        type=str,
        default=None
    )
    args = parser.parse_args()
    xml_df = xml_to_csv(args.imageDir)
    xml_df.to_csv(args.outputDir +"/data.csv", index=None)
    classes = [ "diatermi", "forceps","head","scalpel","needle driver", "retractor", "hl tube", "saw"] # own data sets which classes which category to write, in the order
    rub = [ "diatermi", "forceps","head","scalpel","needle driver", "retractor", "hl tube", "saw"] # own data sets which classes which category to write, in the order

    xml_list = []
    for ind in range(0,len(classes)):
        xml_list.append((classes[ind],ind))
        
    xml_df = pd.DataFrame(xml_list, columns=["class","index"])
    xml_df.to_csv(args.outputDir +"/classes.csv", index=None)

    print('Successfully converted xml to csv.')

main()