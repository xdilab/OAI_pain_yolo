import os
import argparse

import torch
import torchvision.transforms as T
from torch.utils.data import DataLoader

# from yolov7.datasets import CustomDataset
# from yolov7.utils import load_classes
# from yolov7.models import YOLOv7
# from yolov7.train import train

import train as t
t("train.py --workers 1 --device 0 --batch-size 16 --epochs 100 --img 640 640 --hyp data/hyp.scratch.custom.yaml --name yolov7-custom --weights yolov7.pt".split())