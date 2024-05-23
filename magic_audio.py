from pydub import AudioSegment
import os
import argparse
from pydub.playback import play

parser = argparse.ArgumentParser(description="Convert .mp3 files to .wav files instantly.")

parser.add_argument('--source_directory', type=str, default="./", required=False, help='A directory that contains .mp3 files.')
parser.add_argument('--bitrate', type=int, default=16, help='Supported bitrate 16 and 32.')
parser.add_argument('--fade', type=bool, default=True, help='Enable fade in and out.')
parser.add_argument('--fadein', type=str, default="4s", help='Support fade in format of \'4s\'')
parser.add_argument('--fadeout', type=str, default="4s", help='Support fade out format of \'4s\'')

args = parser.parse_args()

directory_path = args.source_directory
bit_depth = args.bitrate

files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

mp3_files = [i for i in files if ".mp3" in i]
print(f"Converting these .mp3 files: {mp3_files}\n")
print(f"\nSource: {args.source_directory} \nBitrate: {args.bitrate}\n-----------------------------\n")

output_directory = os.path.join(directory_path, "WAV_OUTPUT")
os.makedirs(output_directory, exist_ok=True)


def convert_mp3_to_wav(input_file, output_file, bit_depth, fade=False, fade_in="4s", fade_out="4s"):
    audio = AudioSegment.from_mp3(input_file)
    
    if bit_depth == 16:
        sample_width = 2
    elif bit_depth == 24:
        sample_width = 3
    elif bit_depth == 32:
        print("Don't support 32 bit .wav files.")
        return
        sample_width = 4
    else:
        raise ValueError("Unsupported bit depth: choose 16, 24, or 32")
    
    if fade and fade_in and fade_out:
        fade_in = int(fade_in[:-1])
        fade_out = int(fade_out[:-1])
        audio = audio.fade_in(fade_in * 1000).fade_out(fade_out * 1000)
    
    audio.export(output_file, format="wav", parameters=["-acodec", "pcm_s" + str(bit_depth) + "le", "-sample_fmt", "s" + str(bit_depth), "-sample_rate", str(audio.frame_rate)])


def convert_to_wav():
    for i in mp3_files:
        print(f"Converting {i} to .wav file.")
        convert_mp3_to_wav(input_file=i, 
                           output_file=f"{os.path.join(directory_path, 'WAV_OUTPUT')}/{i[:-4]}_WAV.wav", 
                           bit_depth=bit_depth, 
                           fade=args.fade,
                           fade_in=args.fadein,
                           fade_out=args.fadeout
                           )
        print("Converted successfully.\n")

convert_to_wav()

audio = AudioSegment.from_file("ULPV1 - Lofi 2.mp3", format="mp3")
audio = audio.fade_in(4000).fade_out(4000)
play(audio)


