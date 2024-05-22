from pydub import AudioSegment
import os
import argparse

parser = argparse.ArgumentParser(description="Convert .mp3 files to .wav files instantly.")

parser.add_argument('--source_directory', type=str, default="./", required=False, help='A directory that contains .mp3 files.')
parser.add_argument('--bitrate', type=int, default=16, help='Supported bitrate 16 and 32.')

args = parser.parse_args()

directory_path = args.source_directory
files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

mp3_files = [i for i in files if ".mp3" in i]
print(f"Converting these .mp3 files: {mp3_files}\n")

print(f"\nSource: {args.source_directory} \nBitrate: {args.bitrate}\n-----------------------------\n")

output_directory = os.path.join(directory_path, "WAV_OUTPUT")
os.makedirs(output_directory, exist_ok=True)


def convert_mp3_to_wav(input_file, output_file, bit_depth):
    audio = AudioSegment.from_mp3(input_file)
    
    if bit_depth == 16:
        sample_width = 2
    elif bit_depth == 24:
        sample_width = 3
    elif bit_depth == 32:
        sample_width = 4
    else:
        raise ValueError("Unsupported bit depth: choose 16, 24, or 32")
    
    audio.export(output_file, format="wav", parameters=["-acodec", "pcm_s" + str(bit_depth) + "le", "-sample_fmt", "s" + str(bit_depth), "-sample_rate", str(audio.frame_rate)])

input_file = "ULPV1 - Lofi 1.mp3"
output_file = f"{input_file}_WAV.wav"
bit_depth = args.bitrate

def convert_to_wav():
    for i in mp3_files:
        print(f"Converting {i} to .wav file.")
        convert_mp3_to_wav(i, f"{os.path.join(directory_path, 'WAV_OUTPUT')}/{i[:-4]}_WAV.wav", bit_depth)
        print("Converted successfully.\n")

convert_to_wav()
