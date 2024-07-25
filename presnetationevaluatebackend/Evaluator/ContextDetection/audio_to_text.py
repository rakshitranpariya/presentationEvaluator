import os
from pydub import AudioSegment
import speech_recognition as sr
from io import BytesIO
import re

# Convert MP3 to WAV
def convert_mp3_to_wav(mp3_file, wav_file):
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format="wav")

# Convert WAV to text
def convert_wav_to_text(wav_file):
    recognizer = sr.Recognizer()
    # Read the entire WAV file into a buffer
    with open(wav_file, 'rb') as f:
        wav_data = f.read()
    # Use the buffer with AudioFile
    audio_buffer = BytesIO(wav_data)
    with sr.AudioFile(audio_buffer) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            print("Extracted text:", text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
    return ""

# Extract the slide index from the filename
def get_slide_index(filename):
    match = re.match(r"^(\d+)_", filename)
    return int(match.group(1)) if match else None

def extract_text_from_audio():
    # Directory containing the mp3 files
    input_directory = "./extracted_audio"
    output_directory = "./transcribed_texts"
    if not os.path.exists(input_directory):
        print(f"Input directory '{input_directory}' does not exist.")
        return
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Get existing files and their slide indexes
    existing_files = os.listdir(output_directory)
    
    # Process each audio file in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".mp3"):  # Check if the file is a .mp3 file
            slide_index = get_slide_index(filename)
            if slide_index is not None:
                # Delete all existing files with the same slide index
                for file in existing_files:
                    if file.endswith(".txt") and get_slide_index(file) == slide_index:
                        os.remove(os.path.join(output_directory, file))
                        print(f"Deleted existing file: {file}")
                # Delete all existing files with the same slide index (wav or other types)
                for file in existing_files:
                    if file.endswith(".wav") and get_slide_index(file) == slide_index:
                        os.remove(os.path.join(output_directory, file))
                        print(f"Deleted existing file: {file}")

                mp3_file = os.path.join(input_directory, filename)
                wav_file = os.path.join(output_directory, os.path.splitext(filename)[0] + ".wav")
                txt_file = os.path.join(output_directory, os.path.splitext(filename)[0] + ".txt")

                # Convert MP3 to WAV
                try:
                    convert_mp3_to_wav(mp3_file, wav_file)
                except Exception as e:
                    print(f"Error converting {mp3_file} to WAV: {e}")
                    continue

                # Convert WAV to text
                text = convert_wav_to_text(wav_file)

                # Save the text to a file
                with open(txt_file, "w") as file:
                    file.write(text)

                # Optional: Remove the wav file if no longer needed
                os.remove(wav_file)
