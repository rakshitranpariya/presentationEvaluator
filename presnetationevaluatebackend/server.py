from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from Evaluator.ContextDetection.ppt_to_images import convert_ppt_to_images
from Evaluator.ContextDetection.images_to_text import extract_text_from_images
from Evaluator.ContextDetection.audio_to_text import extract_text_from_audio
from Evaluator.ContextDetection.save_video_file import save_video_file
from Evaluator.ContextDetection.convert_video_to_mp4 import convert_video_to_mp4
from Evaluator.ContextDetection.extract_audio_from_video import extract_audio_from_video
from Evaluator.ContextDetection.text_comparison import compare_texts
from Evaluator.ContextDetection.combine_video import combine_video

import boto3
import config

import logging
import os
import speech_recognition as sr
from moviepy.editor import VideoFileClip
app = Flask(__name__)

CORS(app)

IMAGES_DIRECTORY = './slides_images'
UPLOADED_VIDEOS_DIRECTORY = './uploaded_videos'
EXTRACTED_AUDIO_DIRCETORY = './extracted_audio'
PRESENTATION_PATH = './uploaded_presentation/presentation.pptx'

# upload presentation
@app.route("/upload", methods=['POST'])
def upload_file():
    # print(request.files)
    print("Hey upload was called")
    if 'file' not in request.files:
        return {"error": "No file part"}, 400
    file = request.files['file']
    if file.filename == '':
        return {"error": "No selected file"}, 400
    if file:
        ppt_path = './uploaded_presentation/presentation.pptx'  # Replace with the path to your PowerPoint file
        file.save(PRESENTATION_PATH)#save the file to the path
        convert_ppt_to_images(PRESENTATION_PATH,IMAGES_DIRECTORY)

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
        return send_file(filepath, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_video', methods=['POST'])
def upload_video():
    try:
        if 'video' not in request.files:
            app.logger.error('No video part in the request')
            return jsonify({'error': 'No video part in the request'}), 400
        video = request.files['video']
        if video.filename == '':
            app.logger.error('No selected video file')
            return jsonify({'error': 'No selected video file'}), 400
        filename = video.filename
        filepath = os.path.join(UPLOADED_VIDEOS_DIRECTORY, filename)

        save_video_operation = save_video_file(video, UPLOADED_VIDEOS_DIRECTORY)
        logging.info(f"Save video operation result: {save_video_operation}")

        
        return jsonify({'message': 'Video uploaded successfully', 'filename': filename}), 200
    except Exception as e:
        app.logger.error(f'Error occurred : {str(e)}')
        return jsonify({'error': str(e)}), 500
    
@app.route('/start_processing', methods=['GET'])
def start_processing():
    slides_text_dir = './slides_text/'
    extract_text_from_images(IMAGES_DIRECTORY, slides_text_dir)
    convert_video_to_mp4(UPLOADED_VIDEOS_DIRECTORY)
    extract_audio_from_video(UPLOADED_VIDEOS_DIRECTORY, EXTRACTED_AUDIO_DIRCETORY)
    extract_text_from_audio()
    compare_texts()
    return jsonify({'message': 'Processing started'}), 200  

@app.route('/get_all_scores', methods=['POST'])
def get_all_scores():
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='us-east-2',
        aws_access_key_id=config.ACCESS_KEY,
        aws_secret_access_key=config.SECRET_ACCESS_KEY
    )
    table = dynamodb.Table('ContentResult')
    
    try:
        response = table.scan()
        items = response.get('Items', [])
        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
    
@app.route('/combine_videos', methods=['POST'])
def combine_videos():
    try:
        output_path = combine_video()
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        logging.error(f"Error combining videos: {str(e)}")
        return jsonify({'error': str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
