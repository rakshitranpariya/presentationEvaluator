import logging
from werkzeug.utils import secure_filename
import os
import re

# Configure logging
logging.basicConfig(level=logging.INFO)

def save_video_file(video, upload_folder):
    try:
        os.makedirs(upload_folder, exist_ok=True)
        filename = secure_filename(video.filename)
        filepath = os.path.join(upload_folder, filename)
        
        # Extract the slide index from the filename
        match = re.match(r'(\d+)_', filename)
        if match:
            slide_index = match.group(1)
            
            # Delete any existing files with the same slide index
            for existing_file in os.listdir(upload_folder):
                existing_file_path = os.path.join(upload_folder, existing_file)
                if existing_file.startswith(f"{slide_index}_"):
                    os.remove(existing_file_path)
                    logging.info(f"Deleted existing file with slide index {slide_index}: {existing_file_path}")
        
        # Save the video file
        video.save(filepath)
        logging.info(f"Video successfully saved at {filepath}")
        return True
    except Exception as e:
        logging.error(f"Failed to save video file: {str(e)}")
        return False
