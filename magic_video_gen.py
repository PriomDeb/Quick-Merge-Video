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

parser.add_argument('--audio_dir', type=str, default="./", help='Directory of audio.')
parser.add_argument('--images_dir', type=str, default="./", help='Directory of images for making videos.')
parser.add_argument('--render_dir', type=str, default="./", help='Directory to save videos.')


args = parser.parse_args()


def rename_image_files(directory, rename=None):
    files = [f for f in os.listdir(directory) if f.lower().endswith('.jpg')]
    files.sort()
    
    for i, filename in enumerate(files):
        if i < 9:
            name = f"0{i + 1}"
        else:
            name = f"{i + 1}"
        if args.rename_images_name:
            new_name = f"{args.rename_images_name} - {name}.jpg"
        else:
            new_name = f"{name}.jpg"
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {old_path} to {new_path}")

def magic_music_video_gen(image_path, audio_path, video_text, video_filename, fadein=5, fadeout=8, render_directory="./"):
    image = ImageClip(image_path)
    audio = AudioFileClip(audio_path)
    
    images = [image.set_duration(audio.duration).fx(vfx.fadein, fadein).fx(vfx.fadeout, fadeout)]
    
    final_video = concatenate_videoclips(images, method='compose')
    final_video.audio = audio
    
    text_font_size = 66
    text_x, text_y = image.size
    text_position_x, text_position_y = text_x / 4 - text_font_size, text_y / 8
    
    text = TextClip(video_text, 
                    fontsize=text_font_size, color="white", 
                    font='Lofi').set_position((text_position_x, text_position_y), relative=False).set_duration(audio.duration).fx(vfx.fadein, fadein).fx(vfx.fadeout, fadeout)
    final_video = CompositeVideoClip([final_video, text])
    
    start = time.time()
    final_video.write_videofile(f"{render_directory}/{video_filename}.mp4", fps=30)
    end = time.time()
    print(f"\nTotal time taken to render the video: {(end - start):.2f}s.")

def magic_video_render(image_dir, audio_dir, render_directory):
    image_list = [f for f in os.listdir(image_dir) if f.lower().endswith('.jpg')]
    audio_list = [f for f in os.listdir(audio_dir) if f.lower().endswith('.wav')]
    
    for i, filename in enumerate(audio_list):
        magic_music_video_gen(image_path=f"{image_dir}/{image_list[i]}",
                              audio_path=f"{audio_dir}/{audio_list[i]}",
                              video_text=f"Ultimate Lofi Pack Vol 01 \nLofi #{i + 1}",
                              video_filename=f"{audio_list[i][:-8]}",
                              render_directory=render_directory
                              )


if __name__ == "__main__":
    if args.rename_images:
        if args.rename_images_name:
            rename_image_files(directory=args.rename_images_dir, rename=args.rename_images_name)
        else:
            rename_image_files(directory=args.rename_images_dir)
    
    image_dir, audio_dir, render_dir = args.images_dir, args.audio_dir, args.render_dir
    
    magic_video_render(image_dir=image_dir, audio_dir=audio_dir, render_directory=render_dir)
