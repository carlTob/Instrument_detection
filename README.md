# Instrument_detection
Scripts and other helpful files

# dataConverterFormat.py is the master script. It takes a folder with annotated images as input and outputs divided training and validation data folders. It has an option between Retinanet, SSD, EfficientDet and fasterRCNN. This is all you need.

# removeUnrelatedXml.py takes folder as input and look though all xml files for related jpg. If no image is found, the xml file is erased.

# lurkForNewImages.py takes input folder as argument and wait for new image to apear and then copy the image to new output folder.

# label_to_csv.py Convert xml files into a csv format.

# list_files.py Takes folder with images and create text file with all paths to images.

# convertJsonToXmls.py.py Takes yolov4 resulting .json file and convertsto multiple xml files in same directory as images tested on.

# imgChangeName.py takes folder as input and changes all .JPG to .jpg

# flipPictures.py flips picture so that all has the same dimensions.


# create_train_img.py Takes video as input and allow user to extract one frame per X frames in a specific intervall.

# countOccInst.py Take a folder as input and count all class occurences and provide it as output.

# convertXmlStrucToCoco.py Take xml folder as input and outputs as COCO format.

# old_scripts folder contain old scripts which is not in use anymore.