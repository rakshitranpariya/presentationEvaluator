from Evaluator.ContextDetection import SlidesDetector
from Evaluator.ContextDetection import TextExtractor
from flask import Flask, request  
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


#route
@app.route("/main")
def members():
    return {"members":["Members1","Members2","Members3"]}
@app.route("/upload", methods=['POST'])
def upload_file():
    print(request.files)
    if 'file' not in request.files:
        return {"error": "No file part"}, 400
    file = request.files['file']
    if file.filename == '':
        return {"error": "No selected file"}, 400
    if file:
        # Process the file here (e.g., saving it)
        file.save(f"./uploaded_video/{file.filename}")
        SlidesDetector.slidesDetector(file)
        print("before")
        TextExtractor.textExtraction()
        print("after")
        return {"message": f"{file.filename} uploaded successfully"}, 200
    return {"error": "An error occurred during file upload"}, 500


if __name__ == "__main__":
    app.run(debug=True)