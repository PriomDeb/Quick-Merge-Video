# from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, vfx

# def create_transition_clips(clips, overlap_duration):
#     """Creates a video with transition between clips using overlap and fade."""
#     final_clips = []
    
#     for i in range(len(clips) - 1):
#         # Apply fade out to the end of the current clip
#         current_clip = clips[i].fx(vfx.fadeout, overlap_duration)
        
#         # Apply fade in to the start of the next clip
#         next_clip = clips[i + 1].fx(vfx.fadein, overlap_duration)
        
#         # next_clip = next_clip.set_start(t=2)
        
#         # Overlap the two clips
#         overlapped_clip = CompositeVideoClip([current_clip.set_end(current_clip.duration), next_clip.set_start(current_clip.duration - overlap_duration)])
        
#         # Add the overlapped clip to the list
#         final_clips.append(overlapped_clip)
    
#     # Append the last clip without fading out
#     final_clips.append(clips[-1])
    
#     # Concatenate all the clips
#     final_video = concatenate_videoclips(final_clips)
#     return final_video

# # Example usage
# # clips = [VideoFileClip("204307-923909646.mp4").subclip(0, 4), VideoFileClip("38891-418897479.mp4").subclip(0, 4)]
# # overlap_duration = 2  # seconds

# # final_clip = create_transition_clips(clips, overlap_duration)
# # final_clip.write_videofile("output_video.mp4")

# import sys

# def main():
#     if len(sys.argv) > 1:
#         # The first argument is always the script name
#         script_name = sys.argv[0]
#         # Arguments start from sys.argv[1]
#         arguments = sys.argv[1:]
#         print(f"Script name: {script_name}")
#         print(f"Arguments: {arguments}")
#     else:
#         print("No arguments provided.")

# if __name__ == "__main__":
#     main()


import argparse

# Initialize the parser
parser = argparse.ArgumentParser(description="Process and upload a video with QuickVideo")

# Add arguments for add_clips
parser.add_argument('--clips', nargs='+', required=True, help='List of clips to add')

# Add arguments for set_properties
parser.add_argument('--fadein', type=int, default=1, help='Fade-in duration')
parser.add_argument('--fadeout', type=int, default=1, help='Fade-out duration')
parser.add_argument('--subclip', action='store_true', help='Enable subclipping')
parser.add_argument('--subclip_start', type=int, default=0, help='Start time for subclip')
parser.add_argument('--subclip_end', type=int, default=5, help='End time for subclip')

# Add arguments for upload_audio
parser.add_argument('--audio_file', type=str, required=True, help='Audio file to upload')
parser.add_argument('--audio_subclip', action='store_true', help='Enable audio subclipping')
parser.add_argument('--audio_subclip_start', type=int, default=0, help='Start time for audio subclip')
parser.add_argument('--audio_subclip_end', type=int, default=10, help='End time for audio subclip')

# Add argument for magic_quick
parser.add_argument('--save', action='store_true', help='Save the quick video')

# Parse the arguments
args = parser.parse_args()

# Print the parsed arguments (for demonstration purposes)
print(f"Clips: {args.clips}")
print(f"Fade-in: {args.fadein}")
print(f"Fade-out: {args.fadeout}")
print(f"Subclip: {args.subclip}")
print(f"Subclip Start: {args.subclip_start}")
print(f"Subclip End: {args.subclip_end}")
print(f"Audio File: {args.audio_file}")
print(f"Audio Subclip: {args.audio_subclip}")
print(f"Audio Subclip Start: {args.audio_subclip_start}")
print(f"Audio Subclip End: {args.audio_subclip_end}")
print(f"Save: {args.save}")
