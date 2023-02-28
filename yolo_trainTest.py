


import os
import argparse


# using #  OAI_pain\yolov7\data\coco.yaml


os.system("cd yolov7/ && py train.py --workers 1  --batch-size 16 --epochs 100 --img 640 640 --hyp data/hyp.scratch.custom.yaml  --name yolov7-custom --weights yolov7.pt")