import math
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx, CompositeVideoClip, AudioFileClip
import time
from pymediainfo import MediaInfo
import sys
from proglog import ProgressBarLogger
import argparse
import os
from moviepy.editor import *

parser = argparse.ArgumentParser(description="Generate music videos using images and audio.")

parser.add_argument('--rename_images', type=bool, default=False, help='Rename all images in a directory.')
parser.add_argument('--rename_images_dir', type=str, default="./", help='Directory of images.')
parser.add_argument('--rename_images_name', type=str, help='Add a name to all images.')


args = parser.parse_args()


def rename_image_files(directory, rename=None):
    files = [f for f in os.listdir(directory) if f.lower().endswith('.jpg')]
    files.sort()
    
    for i, filename in enumerate(files):
        if args.rename_images_name:
            new_name = f"{args.rename_images_name} - {i + 1}.jpg"
        else:
            new_name = f"{i + 1}.jpg"
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {old_path} to {new_path}")


if __name__ == "__main__":
    if args.rename_images:
        if args.rename_images_name:
            rename_image_files(directory=args.rename_images_dir, rename=args.rename_images_name)
        else:
            rename_image_files(directory=args.rename_images_dir)
