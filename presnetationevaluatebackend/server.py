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

import logging
import os
import speech_recognition as sr
from moviepy.editor import VideoFileClip
app = Flask(__name__)

CORS(app)

IMAGES_DIRECTORY = './slides_images'
UPLOADED_VIDEOS_DIRECTORY = './uploaded_videos'
EXTRACTED_AUDIO_DIRCETORY = './extracted_audio'
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
        file.save(ppt_path)#save the file to the path
        convert_ppt_to_images(ppt_path,IMAGES_DIRECTORY)
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
        mp4_file_path = convert_video_to_mp4(UPLOADED_VIDEOS_DIRECTORY, filename)
        logging.info(f"MP4 file path: {mp4_file_path}")
        mp3_file_path = extract_audio_from_video(mp4_file_path, EXTRACTED_AUDIO_DIRCETORY)
        logging.info(f"MP3 file path: {mp3_file_path}")

        extract_text_from_audio()
        # ppt_text = "PPT Slide 1: Introduction to Climate Change What is Climate Change? Long-term change in Earth's climate Caused by natural processes and human activities Impact of Climate Change Rising global temperatures Melting polar ice caps Increased frequency of extreme weather events"
        # audio_text = "Hello everyone, today we are going to discuss climate change. Climate change refers to the long-term alteration in Earth's climate due to various factors. It includes both natural causes, such as volcanic eruptions and changes in solar radiation, and human activities like greenhouse gas emissions and deforestation.The impacts of climate change are significant. We are seeing rising global temperatures, melting polar ice caps, and an increase in extreme weather events. These changes are affecting ecosystems and human societies worldwide."
        # evaluation = compare_texts(ppt_text, audio_text)
        # print(evaluation)
        compare_texts()

        return jsonify({'message': 'Video uploaded successfully', 'filename': filename}), 200
    except Exception as e:
        app.logger.error(f'Error occurred : {str(e)}')
        return jsonify({'error': str(e)}), 500
   

if __name__ == "__main__":
    app.run(debug=True)
