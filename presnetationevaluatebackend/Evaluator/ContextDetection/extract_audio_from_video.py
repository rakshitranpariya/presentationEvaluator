from moviepy.editor import VideoFileClip
import os
import logging

def extract_audio_from_video(mp4_file, output_directory):
    os.makedirs(output_directory, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(mp4_file))[0]
    mp3_file = os.path.join(output_directory, base_name + ".mp3")

    try:
        # Extract slide index from the base name
        slide_index = base_name.split('_')[0]

        # Remove existing files with the same slide index
        for file in os.listdir(output_directory):
            if file.startswith(slide_index + '_') and file.endswith('.mp3'):
                os.remove(os.path.join(output_directory, file))

        # Extract audio from video
        video_clip = VideoFileClip(mp4_file)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(mp3_file)
        audio_clip.close()
        video_clip.close()
        return mp3_file
    except Exception as e:
        logging.error(f"Error extracting audio: {str(e)}")
        return None
