from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from Evaluator.ContextDetection.ppt_to_images import convert_ppt_to_images
from Evaluator.ContextDetection.images_to_text import extract_text_from_images
from Evaluator.ContextDetection.audio_to_text import extract_text_from_audio

import os
import speech_recognition as sr
from moviepy.editor import VideoFileClip
import ffmpeg 
app = Flask(__name__)

CORS(app)

IMAGES_DIRECTORY = './slides_images'
UPLOADED_VIDEOS_DIRECTORY = './uploaded_videos'
UPLOAD_FOLDER='./uploaded_videos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# upload presentation
@app.route("/upload", methods=['POST'])
def upload_file():
    print(request.files)
    if 'file' not in request.files:
        return {"error": "No file part"}, 400
    file = request.files['file']
    if file.filename == '':
        return {"error": "No selected file"}, 400
    if file:
        ppt_path = './uploaded_presentation/presentation.pptx'  # Replace with the path to your PowerPoint file
       
        slides_text_dir = './slides_text/'
        extract_text_from_images(IMAGES_DIRECTORY, slides_text_dir)
        return {"message": f"{file.filename} uploaded successfully"}, 200
    return {"error": "An error occurred during file upload"}, 500

@app.route('/slide/count/', methods=['GET'])
def count_images():
    try:
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        files = os.listdir(IMAGES_DIRECTORY)
        image_files = [file for file in files if file.lower().endswith(image_extensions)]
        count = len(image_files)
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# get the related images
@app.route('/slide/<int:index>', methods=['GET'])
def get_slide_image(index):
    try:
        image_files = os.listdir(IMAGES_DIRECTORY)
        if index < 0 or index >= len(image_files):
            return jsonify({'error': 'Invalid index'}), 400
        filename = image_files[index]
        filepath = os.path.join(IMAGES_DIRECTORY, filename)
        return send_file(filepath, mimetype='image/jpeg')  # Adjust mimetype if your images are of a different type
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_video', methods=['POST'])
def upload_video():
    try:
        if 'video' not in request.files:
            app.logger.error('No video part in the request')
            return jsonify({'error': 'No video part in the request'}), 400
        
        video = request.files['video']
        # print("video data --",video.__dir__)
        if video.filename == '':
            app.logger.error('No selected video file')
            return jsonify({'error': 'No selected video file'}), 400
        
        # Ensure the upload directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Save the video file
        filename = secure_filename(video.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        video.save(filepath)
     # Perform any additional processing or validation here

        # Convert the video to MP4
        output_filename = os.path.splitext(filename)[0] + ".mp4"
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        print("I am herer")
        try:
            (
                ffmpeg
                .input(filepath)
                .output(
                    output_filepath,
                    vcodec='libx264',    # Video codec
                    acodec='aac',        # Audio codec
                    vf='scale=1280:720', # Scale video to 1280x720 resolution
                    preset='fast',       # Encoding preset for faster conversion
                    crf=28,              # Constant Rate Factor (quality vs size, lower is better quality)
                    b='128k'           # Audio bitrate
                )
                .run(capture_stdout=True, capture_stderr=True)
            )
            print(f"Conversion successful: {output_filepath}")
        except ffmpeg.Error as e:
            print(f"Error during video conversion: {e.stderr.decode()}")

        # Optionally, delete the original WebM file after conversion

        # Directory containing the video files
        input_directory = "./uploaded_videos/"
        output_directory = "./extracted_audio/"

        # Create the output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        # Process each video file in the input directory
        for filename in os.listdir(input_directory):
            if filename.endswith(".mp4"):  # Check if the file is a .mp4 file
                mp4_file = os.path.join(input_directory, filename)
                mp3_file = os.path.join(output_directory, os.path.splitext(filename)[0] + ".mp3")

                # Load the video clip
                video_clip = VideoFileClip(mp4_file)

                # Extract the audio from the video clip
                audio_clip = video_clip.audio

                # Write the audio to a separate file
                audio_clip.write_audiofile(mp3_file)

                # Close the video and audio clips
                audio_clip.close()
                video_clip.close()

        #all mp3 into txt.
        extract_text_from_audio()
        return jsonify({'message': 'Video uploaded successfully', 'filename': filename}), 200
    except Exception as e:
        app.logger.error(f'Error occurred : {str(e)}')
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
if __name__ == "__main__":
    app.run(debug=True)
