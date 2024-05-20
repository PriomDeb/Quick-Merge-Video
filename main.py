import math
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx, CompositeVideoClip
import time
from pymediainfo import MediaInfo
import sys

class QuickMergeVideo:
    def __init__(self):
        self.__bitrate = None
        self.__clips = []
        self.__video_clips = []
        self.__merged = None
        self.__fadein = 0
        self.__fadeout = 0
    
    def set_properties(self, fadein, fadeout, bitrate_k=200):
        self.__fadein = fadein
        self.__fadeout = fadeout
        self.__bitrate = f"{bitrate_k}k"
    
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
        start = time.time()
        self.__video_clips = [VideoFileClip(i).subclip(0, 5).fx(vfx.fadein, self.__fadein).fx(vfx.fadeout, self.__fadeout) for i in self.__clips]
        end = time.time()
        
        if message: print(f"\nTotal time taken to read video files: {(end - start):.2f}s.")
        if clip_address: print(f"Video clips memory address: {self.__video_clips}.")
    
    def merge_clips(self):
        self.__merged = concatenate_videoclips(self.__video_clips)
    
    def save_video(self):
        self.read_clips()
        self.merge_clips()
        
        start = time.time()
        self.__merged.write_videofile("Merged.mp4", bitrate=self.__bitrate)
        end = time.time()
        print(f"\nTotal time taken to merge videos: {(end - start):.2f}s.")
        
        log = open("log.txt", "+a")
        log.write(f"Time: {end - start} Threads: {threads}\n")
        log.close()
        
        

# clip1 = VideoFileClip("38891-418897479.mp4").subclip(0, 4).fx(vfx.fadein, 1)
# clip2 = VideoFileClip("204307-923909646.mp4").subclip(0, 4).fx(vfx.fadein, 1)


if __name__ == "__main__":
    quick_video = QuickMergeVideo()
    bitrate = quick_video.get_bitrate("204307-923909646.mp4")
    
    if len(sys.argv) > 1:
        clips = sys.argv[1:]
        quick_video.add_clips(clips_array=clips)
        quick_video.set_properties(fadein=1, fadeout=1)
        quick_video.save_video()
    

