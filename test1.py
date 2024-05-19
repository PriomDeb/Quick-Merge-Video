from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, vfx

def create_transition_clips(clips, overlap_duration):
    """Creates a video with transition between clips using overlap and fade."""
    final_clips = []
    
    for i in range(len(clips) - 1):
        # Apply fade out to the end of the current clip
        current_clip = clips[i].fx(vfx.fadeout, overlap_duration)
        
        # Apply fade in to the start of the next clip
        next_clip = clips[i + 1].fx(vfx.fadein, overlap_duration)
        
        # next_clip = next_clip.set_start(t=2)
        
        # Overlap the two clips
        overlapped_clip = CompositeVideoClip([current_clip.set_end(current_clip.duration), next_clip.set_start(current_clip.duration - overlap_duration)])
        
        # Add the overlapped clip to the list
        final_clips.append(overlapped_clip)
    
    # Append the last clip without fading out
    final_clips.append(clips[-1])
    
    # Concatenate all the clips
    final_video = concatenate_videoclips(final_clips)
    return final_video

# Example usage
clips = [VideoFileClip("204307-923909646.mp4").subclip(0, 4), VideoFileClip("38891-418897479.mp4").subclip(0, 4)]
overlap_duration = 2  # seconds

final_clip = create_transition_clips(clips, overlap_duration)
final_clip.write_videofile("output_video.mp4")
