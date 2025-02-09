import os
from PIL import Image
import PyPDF2
import numpy as np

def read_file(file_path):
    """Reads a file (PDF or image) and does nothing for now."""
    if file_path.lower().endswith('.pdf'):
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            print(f"Read PDF with {len(reader.pages)} pages. Doing nothing...")
    elif file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        img = Image.open(file_path)
        print(f"Read image with size {img.size}. Doing nothing...")
    else:
        raise ValueError("Unsupported file type")

def save_dummy_images(output_folder, num_images=3):
    """Saves a few dummy image files to a local path."""
    os.makedirs(output_folder, exist_ok=True)
    for i in range(num_images):
        dummy_image = Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
        output_path = os.path.join(output_folder, f"dummy_image_{i+1}.png")
        dummy_image.save(output_path)
        print(f"Saved {output_path}")

if __name__ == "__main__":
    input_file = "one_page.pdf" 
    output_directory = "output_images"
    
    read_file(input_file)
    save_dummy_images(output_directory)