import math
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx, CompositeVideoClip
import time
from pymediainfo import MediaInfo

class QuickMergeVideo:
    def __init__(self):
        self.__bitrate = None
        self.__clips = []
        self.__video_clips = []
        self.__merged = None
    
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
        self.__video_clips = [VideoFileClip(i) for i in self.__clips]
        end = time.time()
        
        if message: print(f"\nTotal time taken to read video files: {(end - start):.2f}s.")
        if clip_address: print(f"Video clips memory address: {self.__video_clips}.")
    
    def merge_clips(self):
        self.__merged = concatenate_videoclips(self.__video_clips)
    
    def save_video(self):
        self.read_clips()
        self.merge_clips()
        
        start = time.time()
        self.__merged.write_videofile("Merged.mp4")
        end = time.time()
        print(f"\nTotal time taken to merge videos: {(end - start):.2f}s.")

# clip1 = VideoFileClip("38891-418897479.mp4").subclip(0, 4).fx(vfx.fadein, 1)
# clip2 = VideoFileClip("204307-923909646.mp4").subclip(0, 4).fx(vfx.fadein, 1)

# start = time.time()
# combined = concatenate_videoclips([clip1, clip2])

# threads = 2

# combined.write_videofile("merged.mp4", threads=threads)
# end = time.time()

# log = open("log.txt", "+a")
# log.write(f"Time: {end - start} Threads: {threads}\n")
# log.close()

# print(end - start)

quick_video = QuickMergeVideo()
bitrate = quick_video.get_bitrate("204307-923909646.mp4")
quick_video.add_clips(clips_array=["204307-923909646.mp4", "38891-418897479.mp4"])
quick_video.save_video()

