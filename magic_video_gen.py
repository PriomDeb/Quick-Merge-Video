import math
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx, CompositeVideoClip, AudioFileClip
import time
from pymediainfo import MediaInfo
import sys
from proglog import ProgressBarLogger
import argparse
import os
from moviepy.editor import *
import moviepy
import ast

parser = argparse.ArgumentParser(description="Generate music videos using images and audio.")

parser.add_argument('--rename_images', type=bool, default=False, help='Rename all images in a directory.')
parser.add_argument('--rename_images_dir', type=str, default="./", help='Directory of images.')
parser.add_argument('--rename_images_name', type=str, help='Add a name to all images.')

parser.add_argument('--audio_dir', type=str, default="./", help='Directory of audio.')
parser.add_argument('--images_dir', type=str, default="./", help='Directory of images for making videos.')
parser.add_argument('--render_dir', type=str, default="./", help='Directory to save videos.')

parser.add_argument('--audio_list', type=str, help='List of audio.')
parser.add_argument('--image_list', type=str, help='List of images for making videos.')


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

def text_position(video_x, video_y, text_x, text_y):
    x = (video_x - text_x) / 2
    y = (video_y - text_y) / 2
    
    return x, y

def magic_music_video_gen(image_path, 
                          audio_path, 
                          video_text,
                          artist_text, 
                          video_filename,
                          credit, 
                          fadein=1, 
                          fadeout=8, 
                          absolute_render_directory=None,
                          ):
    image = ImageClip(image_path)
    audio = AudioFileClip(audio_path)
    audio = moviepy.audio.fx.all.audio_fadein(audio, fadein)
    audio = moviepy.audio.fx.all.audio_fadeout(audio, fadeout)
    
    images = [image.set_duration(audio.duration).fx(vfx.fadein, fadein).fx(vfx.fadeout, fadeout)]
    
    final_video = concatenate_videoclips(images, method='compose')
    final_video.audio = audio
    
    text_font_size = 66
    video_x, video_y = image.size
    
    text = TextClip(video_text, 
                    fontsize=text_font_size, color="white", 
                    font='Lofi').set_duration(audio.duration).fx(vfx.fadein, fadein).fx(vfx.fadeout, fadeout)
    text_artist = TextClip(artist_text, 
                    fontsize=text_font_size, color="white", 
                    font='Lofi').set_duration(audio.duration).fx(vfx.fadein, fadein).fx(vfx.fadeout, fadeout)
    
    video_text_width, video_text_height = text.size
    video_text_x, video_text_y = text_position(video_x, video_y, video_text_width, video_text_height)
    text = text.set_position((video_text_x, video_text_y - 300))
    
    shadow_offset = 3
    opacity = 0.5
    
    
    video_text_shadow = TextClip(video_text, 
                                 fontsize=text_font_size, color="black", 
                                 font='Lofi').set_duration(audio.duration).fx(vfx.fadein, fadein).fx(vfx.fadeout, fadeout)
    video_text_shadow = video_text_shadow.set_position((video_text_x + shadow_offset, video_text_y - 300 + shadow_offset))
    video_text_shadow = video_text_shadow.set_opacity(opacity)
    
    
    text_artist_width, text_artist_height = text_artist.size
    text_artist_x, text_artist_y = text_position(video_x, video_y, text_artist_width, text_artist_height)
    text_artist = text_artist.set_position((text_artist_x, text_artist_y + 400))
    
    text_artist_shadow = TextClip(artist_text, 
                                 fontsize=text_font_size, color="black", 
                                 font='Lofi').set_duration(audio.duration).fx(vfx.fadein, fadein).fx(vfx.fadeout, fadeout)
    text_artist_shadow = text_artist_shadow.set_position((text_artist_x + shadow_offset, text_artist_y + 400 + shadow_offset))
    text_artist_shadow = text_artist_shadow.set_opacity(opacity)
    
    credit_text = TextClip(credit, font="Lofi", fontsize=10, color="white").set_position((10, 1000)).set_duration(audio.duration).fx(vfx.fadein, fadein).fx(vfx.fadeout, fadeout)
    
    final_video = CompositeVideoClip([final_video, video_text_shadow, text, text_artist_shadow, text_artist, credit_text]).subclip(0, 5)
    
    start = time.time()
    if absolute_render_directory:
        render_directory = absolute_render_directory
    else:
        render_directory = "./"
    print("--------------------")
    print(render_directory)
    print(f"{video_filename}.mp4")
    print("--------------------")
    final_video.write_videofile(f"{video_filename}.mp4", fps=30)
    end = time.time()
    print(f"\nTotal time taken to render the video: {(end - start):.2f}s.")

def magic_video_render(image_dir=None, 
                       audio_dir=None, 
                       image_list=None, 
                       audio_list=None, 
                       render_directory=None,
                       video_album_title=None,
                       video_track_title=None,
                       artist_name=None,
                       track_number_start=None,
                       credit_text=None
                       ):
    if image_dir and audio_dir:
        image_list = [f for f in os.listdir(image_dir) if f.lower().endswith('.jpg')]
        audio_list = [f for f in os.listdir(audio_dir) if f.lower().endswith('.wav')]
    
    if image_list and audio_list:
        image_list = image_list
        audio_list = audio_list
    
    if image_list and audio_list:
        for i, filename in enumerate(audio_list):
            magic_music_video_gen(image_path=f"{image_list[i]}",
                                  audio_path=f"{audio_list[i]}",
                                  video_text=f"{video_album_title} \n{video_track_title} #{i + int(track_number_start)}",
                                  artist_text=artist_name,
                                  credit=credit_text,
                                  video_filename=f"{audio_list[i][:-8]}",
                                  absolute_render_directory=render_directory
                                  )
        return
    
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
    
    image_dir, image_list,  audio_dir, audio_list, render_dir = args.images_dir, args.image_list, args.audio_dir, args.audio_list, args.render_dir
    
    if args.image_list: actual_image_list = ast.literal_eval(args.image_list)
    if args.audio_list: actual_audio_list = ast.literal_eval(args.audio_list)
    
    # print(f"Magic Video Gen \nAudio Files: {actual_audio_list} \nImage Files: {actual_image_list} \nRender Directory: {args.render_dir}")
    
    # magic_video_render(image_dir=image_dir, audio_dir=audio_dir, render_directory=render_dir)
    # magic_video_render(image_list=actual_image_list, audio_list=actual_audio_list, render_directory=render_dir)
