import os
import pytesseract
import shutil

from PIL import Image
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
            
def extract_text_from_images(slides_images_dir, slides_text_dir):
    if os.path.exists(slides_text_dir):
        empty_directory(slides_text_dir)
    # Ensure the output directory exists
    os.makedirs(slides_text_dir, exist_ok=True)

    # Function to extract text from an image using OCR
    def extract_text_from_image(image_path):
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()  # Strip any leading/trailing whitespace

    # Iterate through each image in slides_images directory
    for filename in os.listdir(slides_images_dir):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            image_path = os.path.join(slides_images_dir, filename)
            slide_number = os.path.splitext(filename)[0]  # Extract slide number from filename
            
            # Extract text from the image
            extracted_text = extract_text_from_image(image_path)
            
            # Write the extracted text to a text file in slides_text directory
            text_file_path = os.path.join(slides_text_dir, f'{slide_number}.txt')
            with open(text_file_path, 'w', encoding='utf-8') as text_file:
                text_file.write(extracted_text)
            
            print(f'Text extracted from {filename} and saved to {text_file_path}')





