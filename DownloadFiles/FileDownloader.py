import logging
import os
import subprocess
import threading
import tkinter as tk
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Set up logging to print to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def update_gui_message(message):
    """Update the GUI message on the main thread."""
    root.after(0, lambda: label.config(text=message))


def process_url(url):
    try:
        logging.info(f'Processing URL: {url}')
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links to files
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and (href.endswith('.pdf') or href.endswith('.txt') or href.endswith('.zip')):
                file_url = urljoin(url, href)
                logging.info(f'Found: {file_url}')

                # Save each file URL as an Internet Shortcut file
                file_name = os.path.basename(href) + '.url'
                url_file_path = os.path.join('export', file_name)

                # Write the URL in the correct format
                with open(url_file_path, 'w') as url_file:
                    url_file.write("[InternetShortcut]\n")
                    url_file.write(f"URL={file_url}\n")

                logging.info(f'Saved URL to {url_file_path}')

    except Exception as e:
        logging.error(f'Error processing {url}: {e}')


def process_urls():
    """Process the URLs from the text file."""
    # Remove the existing 'export' directory if it exists
    if os.path.exists('export'):
        import shutil
        shutil.rmtree('export')  # Remove the directory and all its contents

    # Create a new directory to save the file URLs
    os.makedirs('export', exist_ok=True)

    # Read URLs from a text file
    with open('urls.txt', 'r') as file:
        urls = [line.strip() for line in file.readlines()]

    update_gui_message("Processing URLs, please wait...")

    try:
        # Process URLs in parallel
        with ThreadPoolExecutor() as executor:
            executor.map(process_url, urls)

        update_gui_message("Processing complete!")  # Final message
    except Exception as e:
        update_gui_message(f"Error: {str(e)}")  # Error message for the user


def start_processing():
    """Start processing URLs in a separate thread."""
    threading.Thread(target=process_urls).start()


# Set up the tkinter window
root = tk.Tk()
root.title("URL Exporter")

# Center the window
window_width = 400
window_height = 150

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate x and y coordinates to center the window
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Set window size and position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

label = tk.Label(root, text="Press 'Start' to process URLs and save file URLs in the 'exports' folder.", wraplength=350)
label.pack(pady=20)

progress_label = tk.Label(root, text="Processing...", fg="blue", wraplength=350)

start_button = tk.Button(root, text="Start", command=start_processing)
start_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
