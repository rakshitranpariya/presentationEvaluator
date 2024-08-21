import re
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def extract_first_digit(filename):
    for char in filename:
        if char.isdigit():
            return int(char)
    return float('inf')  # If no digit is found, return infinity to place it at the end

def combine_video():
    print("Hey")
    video_dir = "./uploaded_videos"
    combined_video_path = os.path.join(video_dir, "combined_video.mp4")
    
    try:
        # Delete existing combined video file if it exists
        if os.path.exists(combined_video_path):
            os.remove(combined_video_path)
            print(f"Deleted existing file: {combined_video_path}")
        
        # List all video files
        video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
        
        # Sort files based on the first digit
        video_files.sort(key=lambda x: extract_first_digit(os.path.basename(x)))
        
        if not video_files:
            raise ValueError("No video files found in the directory")
        
        # Load video clips
        video_clips = [VideoFileClip(video) for video in video_files]
        
        # Combine clips
        final_clip = concatenate_videoclips(video_clips)
        
        # Save combined video
        final_clip.write_videofile(combined_video_path, codec="libx264", fps=24)
        
        # Close all video clips
        for clip in video_clips:
            clip.close()
        
        print(f"All videos combined and saved to {combined_video_path}")
        return combined_video_path
    
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
