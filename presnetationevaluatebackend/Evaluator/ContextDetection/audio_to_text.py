import os
from pydub import AudioSegment
import speech_recognition as sr
from io import BytesIO

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


def extract_text_from_audio():
    # Directory containing the mp3 files
    input_directory = "./extracted_audio"
    output_directory = "./transcribed_texts"
    if not os.path.exists(input_directory):
        print(f"Input directory '{input_directory}' does not exist.")
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    # Process each audio file in the input directory
    for filename in os.listdir(input_directory):
        print("🚀 ~ output_directory:", output_directory)
        if filename.endswith(".mp3"):  # Check if the file is a .mp3 file
            mp3_file = os.path.join(input_directory, filename)
            wav_file = os.path.join(output_directory, os.path.splitext(filename)[0] + ".wav")
            txt_file = os.path.join(output_directory, os.path.splitext(filename)[0] + ".txt")

            # Convert MP3 to WAV
            convert_mp3_to_wav(mp3_file, wav_file)

            # Convert WAV to text
            text = convert_wav_to_text(wav_file)

            # Save the text to a file
            with open(txt_file, "w") as file:
                file.write(text)

            # Optional: Remove the wav file if no longer needed
            os.remove(wav_file)
