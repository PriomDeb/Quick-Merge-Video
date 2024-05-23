from pydub import AudioSegment
import os
import argparse
from pydub.playback import play
from pydub.utils import mediainfo

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
print(f"Converting these .mp3 files: ")
for i in mp3_files:
    print(i)
print(f"\nSource: {args.source_directory} \nBitrate: {args.bitrate}\n-----------------------------\n")

output_directory = os.path.join(directory_path, "WAV_OUTPUT")
os.makedirs(output_directory, exist_ok=True)

def get_bitrate(file_path):
    return mediainfo(file_path)['bits_per_sample']


def convert_mp3_to_wav(input_file, output_file, bit_depth, fade=False, fade_in="4s", fade_out="4s"):
    audio = AudioSegment.from_mp3(input_file)
    
    if bit_depth == 16:
        sample_width = 2
    elif bit_depth == 24:
        sample_width = 3
        print("Don't support 24 bit .wav files.")
        return
    elif bit_depth == 32:
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
        bitrate = get_bitrate(f"{os.path.join(directory_path, 'WAV_OUTPUT')}/{i[:-4]}_WAV.wav")
        saved_directory = f"{os.path.join(directory_path, 'WAV_OUTPUT')}/{i[:-4]}_WAV.wav"
        print(f"Converted successfully. \nBitrate is {bitrate}. \nLocation: {saved_directory}.\n-----------------------------\n")

convert_to_wav()


# audio_1 = AudioSegment.from_file("ULPV1 - Lofi 2.mp3", format="mp3")
# audio_2 = AudioSegment.from_file("ULPV1 - Lofi 4.mp3", format="mp3")

# audio_3 = AudioSegment.from_wav("Relaxing and Meditation Music 1 (River and Birds, 70 BPM).wav")
# audio_4 = AudioSegment.from_file("Relaxing and Meditation Music 1 (River and Birds, 70 BPM)_24bit.wav", format="wav")

# print(f"Audio 3: {get_bitrate('Relaxing and Meditation Music 1 (River and Birds, 70 BPM).wav')}")
# print(f"Audio 4: {get_bitrate('Relaxing and Meditation Music 1 (River and Birds, 70 BPM)_24bit.wav')}")

# # combined_audio = audio_3[:4000].overlay(audio_3)

# # audio = audio_1.fade_in(4000).fade_out(4000)
# audio_4 = audio_4.set_sample_width(2)
# play(audio_4)
