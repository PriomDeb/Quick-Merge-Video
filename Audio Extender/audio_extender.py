from pydub import AudioSegment
import os
import argparse
from pydub.playback import play
from pydub.utils import mediainfo
import math

files = [f for f in os.listdir("./") if f.endswith(".wav")]

audio1 = AudioSegment.from_wav(files[0])[:40000]
extension = 5 * 60 * 1000
overlap_duration = 4000

iteration = int(extension / len(audio1))

start_time_audio_1 = len(audio1) - overlap_duration

final_audio = audio1[:start_time_audio_1]

for i in range(iteration):
    overlapped = audio1[start_time_audio_1:].fade_out(overlap_duration).overlay(audio1[0:overlap_duration].fade_in(overlap_duration))
    final_audio += overlapped + audio1[overlap_duration:]

final_audio[:extension + 643].fade_out(5000).export("merged_audio.mp3", format="mp3", bitrate="320k")  # 580

# audio2 = AudioSegment.from_wav(files[2])  # 3600643
# audio2 = AudioSegment.from_mp3("Sleep Music 6 (1 Hour).mp3")  # 3600692
# print(len(audio2))

