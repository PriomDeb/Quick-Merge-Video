from pydub import AudioSegment
import os, sys
import argparse
from pydub.playback import play
from pydub.utils import mediainfo
import math

DEFAULT_EXTEND = 60
DEFAULT_OVERLAP = 4

parser = argparse.ArgumentParser(description="Extend a audio to given minutes.")

parser.add_argument('--audio', type=str, default=None, help='Audio path.')
parser.add_argument('--extend', type=int, default=DEFAULT_EXTEND, help='Extend the audio to that duration mentioning minutes.')
parser.add_argument('--overlap_duration', type=int, default=DEFAULT_OVERLAP, help='Overlapping duration in seconds.')

args = parser.parse_args()

def extend_audio(file_path=None, extend=60, overlap=4):
    if not file_path:
        print("Please pass a audio file. No file found.")
        return
    else:
        if file_path.endswith(".mp3"):
            print(".mp3 files are not supported.")
            return
    
    audio1 = AudioSegment.from_wav(file_path)
    extension = extend * 60 * 1000
    overlap_duration = overlap * 1000
    
    iteration = int(extension / len(audio1))
    start_time_audio_1 = len(audio1) - overlap_duration
    
    final_audio = audio1[:start_time_audio_1]
    
    for i in range(iteration):
        overlapped = audio1[start_time_audio_1:].fade_out(overlap_duration).overlay(audio1[0:overlap_duration].fade_in(overlap_duration))
        final_audio += overlapped + audio1[overlap_duration:]
        
        progress = min((i + 1) / iteration * 100, 100)
        sys.stdout.write(f"\rProgress: {progress:.2f}%")
        sys.stdout.flush()
    
    print("\nRendering audio. Please wait and don't close the program.")
        
    final_audio[:extension + 643].fade_out(5000).export("merged_audio.mp3", format="mp3", bitrate="320k")
    
    print("Rendering finished.")


if __name__ == "__main__":
    audio, extend, overlap = args.audio, args.extend, args.overlap_duration
    extend_audio(audio, extend, overlap)

