import pytesseract
import PIL
import cv2
import os
# def textExtraction():
#     path = f"./output/Test Video 2/000_0.11.png"
#     myconfig = r"--psm 6 --oem 3"

#     text = pytesseract.image_to_string(PIL.Image.open(path), config = myconfig)
#     print(text)

def textExtraction():
    print("inside the function")
    input_dir = "./output/slides"
    output_dir = "./output/slidetext"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_files = [f for f in os.listdir(input_dir) if f.endswith('.png')]

    myconfig = r"--psm 6 --oem 3"

    for idx, image_file in enumerate(sorted(image_files), start=1):
        image_path = os.path.join(input_dir, image_file)
        text = pytesseract.image_to_string(PIL.Image.open(image_path), config=myconfig)
        
        output_file = os.path.join(output_dir, f"{idx}.txt")
        with open(output_file, 'w') as f:
            f.write(text)
    
    print(f"Extracted text from {len(image_files)} images and saved to {output_dir}")