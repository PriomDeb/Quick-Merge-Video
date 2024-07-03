from pydub import AudioSegment
import os


files = [f for f in os.listdir("./") if f.endswith(".wav")]

audio1 = AudioSegment.from_mp3(files[0])[:10000]
audio2 = AudioSegment.from_mp3(files[1])[:10000]

# Define the duration of the overlap (in milliseconds)
overlap_duration = 2000

# Calculate the start time for the overlap in both audios
start_time_audio1 = len(audio1) - overlap_duration
start_time_audio2 = 0

# Extract the overlapping segments
overlap_audio1 = audio1[start_time_audio1:].fade_out(2000)
overlap_audio2 = audio2[start_time_audio2:overlap_duration].fade_in(2000)

# Merge the overlapping segments
merged_overlap = overlap_audio1.overlay(overlap_audio2)

# Create the final merged audio
final_audio = audio1[:start_time_audio1] + merged_overlap + audio2[overlap_duration:]

# Export the final audio
final_audio.export("merged_audio.mp3", format="mp3")
