import logging
from werkzeug.utils import secure_filename
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

def save_video_file(video, upload_folder):
    try:
        os.makedirs(upload_folder, exist_ok=True)
        filename = secure_filename(video.filename)
        filepath = os.path.join(upload_folder, filename)
        
        # Save the video file
        video.save(filepath)
        logging.info(f"Video successfully saved at {filepath}")
        return True
    except Exception as e:
        logging.error(f"Failed to save video file: {str(e)}")
        return False
