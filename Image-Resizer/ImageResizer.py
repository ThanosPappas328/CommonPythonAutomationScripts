import os
import logging
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_unique_filename(output_folder, filename):
    """Generate a unique filename if the file already exists."""
    base, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    while os.path.exists(os.path.join(output_folder, unique_filename)):
        unique_filename = f"{base}_copy{counter}{ext}"
        counter += 1
    return unique_filename


def resize_and_crop(image_path, output_folder, target_width=2000, target_height=1200):
    """Resize and crop the image to the target dimensions while maintaining aspect ratio."""
    try:
        # Open the image
        img = Image.open(image_path)

        # Get the original dimensions
        width, height = img.size

        # Calculate aspect ratios
        target_ratio = target_width / target_height
        img_ratio = width / height

        # Resize the image while keeping the aspect ratio
        if img_ratio > target_ratio:
            # Image is wider than target ratio, resize based on height
            new_height = target_height
            new_width = int(new_height * img_ratio)
        else:
            # Image is taller than target ratio, resize based on width
            new_width = target_width
            new_height = int(new_width / img_ratio)

        # Resize the image
        img = img.resize((new_width, new_height), Image.LANCZOS)

        # Calculate cropping box
        left = (new_width - target_width) / 2
        top = (new_height - target_height) / 2
        right = (new_width + target_width) / 2
        bottom = (new_height + target_height) / 2

        # Crop the image to the target dimensions
        img = img.crop((left, top, right, bottom))

        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Get a unique filename to avoid overwriting
        output_filename = get_unique_filename(output_folder, os.path.basename(image_path))
        output_path = os.path.join(output_folder, output_filename)

        # Save the image to the output folder
        img.save(output_path)
        logging.info(f"Saved resized and cropped image to {output_path}")
    except Exception as e:
        logging.error(f"Failed to process {image_path}: {e}")


def process_images_in_parallel(input_folder, output_folder):
    """Process all images in the input folder in parallel."""
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    with ThreadPoolExecutor() as executor:
        executor.map(lambda image: resize_and_crop(os.path.join(input_folder, image), output_folder), image_files)


# Example usage
input_folder = "input"
output_folder = "output"

# Process images
process_images_in_parallel(input_folder, output_folder)
