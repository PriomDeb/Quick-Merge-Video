import math
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx, CompositeVideoClip
import time
from pymediainfo import MediaInfo
import sys
from proglog import ProgressBarLogger

class QuickMergeVideo:
    def __init__(self):
        self.__bitrate = None
        self.__clips = []
        self.__video_clips = []
        self.__merged = None
        self.__fadein = 0
        self.__fadeout = 0
    
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
    
    def merge_clips(self):
        self.__merged = concatenate_videoclips(self.__video_clips)
    
    def save_video(self, save=True):
        if not save: return
        
        self.read_clips()
        self.merge_clips()
        
        start = time.time()
        logger = CustomProgressBar()
        self.__merged.write_videofile("Merged.mp4", bitrate=self.__bitrate, logger=logger)
        end = time.time()
        print(f"\nTotal time taken to merge videos: {(end - start):.2f}s.")
        
        log = open("log.txt", "+a")
        log.write(f"Time: {end - start} Threads: {self.__threads}\n")
        log.close()
    
    def progress_callback(self, current, total):
        percentage = (current / total) * 100
        print(f"Progress: {percentage:.2f}% completed", end='\r')
    
    def get_duration(self):
        self.read_clips()
        duration = [i.duration for i in self.__video_clips]
        print(duration)
        print(max(duration))

class CustomProgressBar(ProgressBarLogger):
    # def callback(self, **changes):
    #     for (parameter, value) in changes.items():
    #         print(f"Parameter {parameter} is now {value}")
    
    def bars_callback(self, bar, attr, value, old_value=None):
        percentage = (value / self.bars[bar]['total']) * 100
        print(f"\rSaving video: {percentage:.2f}", end="\r")
        


if __name__ == "__main__":
    quick_video = QuickMergeVideo()
    bitrate = quick_video.get_bitrate("204307-923909646.mp4")
    print(bitrate)
    
    if len(sys.argv) > 1:
        clips = sys.argv[1:]
        quick_video.add_clips(clips_array=clips)
        quick_video.set_properties(fadein=1, fadeout=1, subclip=False, subclip_start=0, subclip_end=5)
        quick_video.get_duration()
        quick_video.save_video(save=False)
    

