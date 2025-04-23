import os
import logging
from rembg import remove
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Set up logging
logging.basicConfig(filename='background_removal_log.txt', level=logging.INFO)

def remove_background(input_path, output_path):
    """Remove the background from an image."""
    try:
        with open(input_path, 'rb') as i:
            input_data = i.read()
            output_data = remove(input_data)

        with open(output_path, 'wb') as o:
            o.write(output_data)

        logging.info(f"Successfully processed: {input_path}")
    except Exception as e:
        logging.error(f"Failed to process {input_path}: {str(e)}")


def process_images_parallel(input_folder, output_folder):
    """Process all images in the input folder to remove backgrounds in parallel."""
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    with ThreadPoolExecutor() as executor:
        for filename in image_files:
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.png")
            executor.submit(remove_background, input_path, output_path)

# Example usage
input_folder = "input"
output_folder = "output"

# Process images
process_images_parallel(input_folder, output_folder)
