from moviepy.editor import VideoFileClip
import os
import logging
import shutil

def empty_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def extract_audio_from_video(video_directory, audio_directory):

    if os.path.exists(audio_directory):
        empty_directory(audio_directory)

    os.makedirs(audio_directory, exist_ok=True)

    for filename in os.listdir(video_directory):
        if filename.endswith('.mp4'):  # Assuming videos are in MP4 format
            mp4_file = os.path.join(video_directory, filename)
            base_name = os.path.splitext(os.path.basename(mp4_file))[0]
            print("base:",base_name)
            mp3_file = os.path.join(audio_directory, base_name + ".mp3")
   
        try:
                # Extract slide index from the base name
                slide_index = base_name.split('_')[0]

                # Remove existing files with the same slide index
                for file in os.listdir(audio_directory):
                    if file.startswith(slide_index + '_') and file.endswith('.mp3'):
                        os.remove(os.path.join(audio_directory, file))

                # Extract audio from video
                video_clip = VideoFileClip(mp4_file)
                audio_clip = video_clip.audio
                audio_clip.write_audiofile(mp3_file)
                audio_clip.close()
                video_clip.close()

                logging.info(f"Audio extracted and saved to: {mp3_file}")

        except Exception as e:
                logging.error(f"Error extracting audio from {mp4_file}: {str(e)}")
    