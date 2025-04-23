import os
from rembg import remove
from PIL import Image
from tqdm import tqdm  # For the progress bar
import logging

# Set up logging for error handling
logging.basicConfig(filename='error_log.txt', level=logging.ERROR)

# Define paths
input_folder = os.path.join(os.getcwd(), "input")
output_folder = os.path.join(os.getcwd(), "output")

# Make sure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Get list of images in input folder
image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

# Initialize progress bar
with tqdm(total=len(image_files), desc="Processing images") as pbar:
    for filename in image_files:
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.png")

        try:
            # Open and process the image
            with open(input_path, 'rb') as i:
                input_data = i.read()
                output_data = remove(input_data)

            with open(output_path, 'wb') as o:
                o.write(output_data)

            print(f"✅ Processed: {filename}")
        except Exception as e:
            # Log errors for any failed images
            logging.error(f"Error processing {filename}: {str(e)}")
            print(f"❌ Failed to process: {filename}")
        
        # Update the progress bar
        pbar.update(1)

# Final message
print("🎉 Done! All images processed. Check 'error_log.txt' for any issues.")
