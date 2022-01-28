import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from tqdm.notebook import tqdm

import gc
import os
import copy
from glob import glob

import cv2
from PIL import Image

import random

from collections import deque, defaultdict
from multiprocessing import Pool, Process
from functools import partial

import torch
import torch.nn as nn

import pycocotools
import detectron2
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor, DefaultTrainer
from detectron2.utils.visualizer import Visualizer, ColorMode
from detectron2.structures import BoxMode
from detectron2.data import datasets, DatasetCatalog, MetadataCatalog, build_detection_train_loader, build_detection_test_loader
from detectron2.data import transforms as T
from detectron2.data import detection_utils as utils
from detectron2.evaluation import COCOEvaluator, verify_results
from detectron2.modeling import GeneralizedRCNNWithTTA
from detectron2.data.transforms import TransformGen
from detectron2.utils.logger import setup_logger
setup_logger()

from fvcore.transforms.transform import TransformList, Transform, NoOpTransform
from contextlib import contextmanager
cfg = get_cfg()
print(cfg.keys())
train_df = pd.read_csv("data.csv")
print(train_df.head())