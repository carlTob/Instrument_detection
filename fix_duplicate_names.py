import glob
import shutil

import os

def fix_jpg():
    PATH = '/home/serge/repos/TensorFlow/workspace/training_demo/new_imgs/'
    NEW_PATH = '/home/serge/repos/TensorFlow/workspace/training_demo/tmp_imgs/'
    img_files = glob.glob(PATH + '*.jpg')
    for img_f in img_files:
        base=os.path.basename(img_f).split('.')[0]
        print(f'Base {base}')
        original = PATH + base + '.jpg'
        target = NEW_PATH + base + '.jpg'
    
        if 'train' in base:
            abase = 'b' + base
            original = PATH + base + '.jpg'
            target = NEW_PATH + abase + '.jpg'
        
        shutil.copy(original, target)
        

def fix_trained():
    PATH = '/home/serge/repos/TensorFlow/workspace/training_demo/new_imgs/'
    NEW_PATH = '/home/serge/repos/TensorFlow/workspace/training_demo/op_img_atrain/'
    XML_PATH = '/home/serge/repos/TensorFlow/workspace/training_demo/op_img/*.xml'
    xml_files = glob.glob(XML_PATH)
    for xml_file in xml_files:
        with open(xml_file, 'r') as f:
            xml_as_txt = f.read()
            base=os.path.basename(xml_file).split('.')[0]
            print(f'Base {base}')
            abase = 'a' + base
            new_xml = xml_as_txt.replace(base, abase)
            new_xml_fname = NEW_PATH + abase + '.xml' 
            original = PATH + base + '.jpg'
            target = NEW_PATH + abase + '.jpg'
            shutil.copy(original, target)
            with open(new_xml_fname, 'w+') as nf:
                nf.write(new_xml)
        

fix_jpg()