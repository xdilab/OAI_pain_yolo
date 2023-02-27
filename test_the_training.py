import os
import argparse

import torch
import torchvision.transforms as T
from torch.utils.data import DataLoader

from yolov7.datasets import CustomDataset
from yolov7.utils import load_classes
from yolov7.models import YOLOv7
from yolov7.train import train


def main(args):
    # Define device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load classes
    class_names = load_classes(args.class_file)

    # Define transforms
    transforms = T.Compose([
        T.Resize((args.image_size, args.image_size)),
        T.ToTensor(),
    ])

    # Define dataset
    dataset = CustomDataset(
        root_dir=args.data_dir,
        transform=transforms,
        image_size=args.image_size,
        class_names=class_names,
        mode="train",
        label_file="labelimg",  # change to your label format
    )

    # Define dataloader
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

    # Define model
    model = YOLOv7(num_classes=len(class_names)).to(device)

    # Define optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)

    # Define scheduler
    scheduler = torch.optim.lr_scheduler.StepLR(
        optimizer,
        step_size=args.lr_step_size,
        gamma=args.lr_gamma
    )

    # Train model
    train(model, dataloader, optimizer, scheduler, device, args.epochs, args.save_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, required=True, help="path to dataset directory")
    parser.add_argument("--class_file", type=str, required=True, help="path to class names file")
    parser.add_argument("--image_size", type=int, default=416, help="input image size")
    parser.add_argument("--batch_size", type=int, default=16, help="batch size")
    parser.add_argument("--learning_rate", type=float, default=1e-4, help="learning rate")
    parser.add_argument("--lr_step_size", type=int, default=10, help="learning rate scheduler step size")
    parser.add_argument("--lr_gamma", type=float, default=0.1, help="learning rate scheduler gamma")
    parser.add_argument("--epochs", type=int, default=100, help="number of epochs to train")
    parser.add_argument("--save_dir", type=str, default="checkpoints", help="path to save checkpoints")
    args = parser.parse_args()

    # main(args)
    main("test_the_training.py --data_dir ..\sample_knee_mri_localization\9009067_10287112_R_Progressed --class_file class_names.txt".split(" "))