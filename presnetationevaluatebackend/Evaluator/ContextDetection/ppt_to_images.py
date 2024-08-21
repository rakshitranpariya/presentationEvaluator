import os
import sys
import shutil
import time
import subprocess
from pdf2image import convert_from_bytes

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

def convert_ppt_to_images(ppt_path, output_folder):
    img_format = "jpg"
    out_dir = output_folder
    pptfile_name = ppt_path

    empty_directory(out_dir)
    start = time.time()
    print("Start converting your PPT to {} images.".format(img_format))

    filename_base = os.path.basename(pptfile_name)
    filename_bare = os.path.splitext(filename_base)[0]

    # Specify the full path to soffice executable or add it to the system path
    soffice_path = "C:/Program Files/LibreOffice/program/soffice"  # Example path, adjust as necessary

    # Convert pptx to PDF using LibreOffice/OpenOffice
    command_list = [soffice_path, "--headless", "--convert-to", "pdf", pptfile_name]
    subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    pdffile_name = filename_bare + ".pdf"
    with open(pdffile_name, "rb") as f:
        pdf_bytes = f.read()
    images = convert_from_bytes(pdf_bytes, dpi=96)

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    for i, img in enumerate(images):
        im_name = os.path.join(out_dir, f"slide_{i}.{img_format}")
        img.save(im_name)

    elapse = time.time() - start
    print("Conversion done, images saved in dir {}. Time spent: {}".format(
        out_dir, elapse))
