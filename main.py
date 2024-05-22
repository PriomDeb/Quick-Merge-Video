import math
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx, CompositeVideoClip, AudioFileClip
import time
from pymediainfo import MediaInfo
import sys
from proglog import ProgressBarLogger
import argparse

class QuickMergeVideo:
    def __init__(self):
        self.__bitrate = None
        self.__clips = []
        self.__video_clips = []
        self.__merged = None
        self.__fadein = 0
        self.__fadeout = 0
        self.__audio_clip = None
    
    def set_properties(self, fadein, fadeout, bitrate_k=2, threads=5, subclip=False, subclip_start=None, subclip_end=None):
        self.__fadein = fadein
        self.__fadeout = fadeout
        self.__bitrate = f"{bitrate_k * 10000}k"
        self.__threads = threads
        self.__subclip = subclip
        self.__subclip_start = subclip_start
        self.__subclip_end = subclip_end
    
    def get_bitrate(self, video_path, kbps=True):
        media_info = MediaInfo.parse(video_path)
        for track in media_info.tracks:
            if track.track_type == 'Video':
                if kbps:
                    self.__bitrate = math.ceil(track.bit_rate / 1024)
                    return self.__bitrate
                return track.bit_rate
        return None
    
    def add_clips(self, clip=None, clips_array=None):
        if type(clips_array) == list:
            self.__clips.extend(clips_array)
        else:
            self.__clips.append(clip)
    
    def get_clips_list(self):
        print(f"\nClips are: {self.__clips}\n")
        return self.__clips
    
    def read_clips(self, message=False, clip_address=False):
        if self.__subclip == True and not self.__subclip_start and not self.__subclip_end:
            return
        
        start = time.time()
        self.__video_clips = [VideoFileClip(i).without_audio().fx(vfx.fadein, self.__fadein).fx(vfx.fadeout, self.__fadeout) for i in self.__clips]
        if self.__subclip: self.__video_clips = [i.subclip(self.__subclip_start, self.__subclip_end) for i in self.__video_clips]
        end = time.time()
        
        if message: print(f"\nTotal time taken to read video files: {(end - start):.2f}s.")
        if clip_address: print(f"Video clips memory address: {self.__video_clips}.")
        
        return self.__video_clips
    
    
    def get_duration(self):
        self.read_clips()
        duration = [i.duration for i in self.__video_clips]
        return duration
    
    def upload_audio(self, audio_path, subclip=False, subclip_start=None, subclip_end=None):
        self.__audio_clip = AudioFileClip(audio_path)
        if subclip: self.__audio_clip = AudioFileClip(audio_path).subclip(subclip_start, subclip_end)
        
        self.__audio_duration = self.__audio_clip.duration
        
        return self.__audio_clip
    
    def read_audio(self):
        return self.__audio_clip
    
    def magic_quick(self, save=True):
        uploaded_clips = self.read_clips()
        uploaded_audio = self.read_audio()
        
        # Extending video duration based on audio duration
        video_duration = sum(i.duration for i in uploaded_clips)
        
        while video_duration <= self.__audio_duration:
            uploaded_clips.extend(uploaded_clips)
            video_duration += video_duration
        
        merged = concatenate_videoclips(uploaded_clips).subclip(0, self.__audio_duration)
        
        # Adding audio
        merged = merged.set_audio(uploaded_audio)
        print(merged.duration)
        
        if not save:
            return
        
        # Saving the video
        start = time.time()
        logger = CustomProgressBar()
        
        merged.write_videofile("Merged.mp4", 
                               bitrate=self.__bitrate)
        
        end = time.time()
        print(f"\nTotal time taken to merge videos: {(end - start):.2f}s.")
        
        # Saving the log
        log = open("log.txt", "+a")
        log.write(f"Time: {end - start} Threads: {self.__threads}\n")
        log.close()
        
        
        

class CustomProgressBar(ProgressBarLogger):
    def bars_callback(self, bar, attr, value, old_value=None):
        percentage = (value / self.bars[bar]['total']) * 100
        print(f"\rSaving video: {percentage:.2f}", end="\r")
        


if __name__ == "__main__":
    quick_video = QuickMergeVideo()
    
    # if len(sys.argv) > 1:
    #     clips = sys.argv[1:]
    #     quick_video.add_clips(clips_array=clips)
    #     quick_video.set_properties(fadein=1, fadeout=1, subclip=False, subclip_start=0, subclip_end=5)
    #     quick_video.upload_audio("Rain 1.wav", subclip=True, subclip_start=0, subclip_end=10)
    #     quick_video.magic_quick(save=False)
    
    
    # Initialize the parser
    parser = argparse.ArgumentParser(description="Process and upload a video with QuickVideo")
    
    # Add arguments for add_clips
    parser.add_argument('--clips', nargs='+', required=True, help='List of clips to add')
    
    # Add arguments for set_properties
    parser.add_argument('--fadein', type=int, default=0, help='Fade-in duration')
    parser.add_argument('--fadeout', type=int, default=0, help='Fade-out duration')
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
    

