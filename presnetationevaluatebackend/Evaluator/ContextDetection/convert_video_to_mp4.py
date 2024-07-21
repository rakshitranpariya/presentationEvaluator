import ffmpeg
import logging
import os

def convert_video_to_mp4(filepath, filename):
    input_filepath = os.path.join(filepath, filename)  # Combine directory and filename
    output_filename = os.path.splitext(filename)[0] + ".mp4"
    output_filepath = os.path.join(filepath, output_filename)
    logging.info(f"Starting conversion: {filepath} to {output_filepath}")

    try:
        (
            ffmpeg
            .input(input_filepath)
            .output(
                output_filepath,
                vcodec='libx264',
                acodec='aac',
                vf='scale=1280:720',
                preset='fast',
                crf=28,
                b='128k'
            )
            .run(capture_stdout=True, capture_stderr=True)
        )
        logging.info(f"Conversion successful: {output_filepath}")

        # Optionally delete the original file
        if os.path.isfile(input_filepath):
            os.remove(input_filepath)
            logging.info(f"Original file deleted: {input_filepath}")

        return output_filepath

    except ffmpeg.Error as e:
        logging.error(f"Error during video conversion: {e.stderr.decode()}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return None
