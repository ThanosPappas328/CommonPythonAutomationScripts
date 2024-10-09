import logging
import os
import subprocess  # Import subprocess to open the folder
import threading
import tkinter as tk
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# Set up logging to print to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def process_urls():
    # Remove the existing 'export' directory if it exists
    if os.path.exists('export'):
        import shutil
        shutil.rmtree('export')  # Remove the directory and all its contents

    # Create a new directory to save the file URLs
    os.makedirs('export', exist_ok=True)

    # Read URLs from a text file
    with open('urls.txt', 'r') as file:
        urls = [line.strip() for line in file.readlines()]

    for url in urls:
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

    logging.info('Export complete.')

    # Update the GUI to show completion
    label.config(text="Επεξεργασία τελείωσε!")
    progress_label.pack_forget()  # Hide the progress label

    # Open the export folder
    open_export_folder()


def open_export_folder():
    # Open the 'export' directory
    export_path = os.path.abspath('export')
    subprocess.Popen(f'explorer "{export_path}"')  # For Windows
    # For macOS, use: subprocess.Popen(['open', export_path])
    # For Linux, use: subprocess.Popen(['xdg-open', export_path])


def start_processing():
    # Update the GUI to show that processing has started
    label.config(text="Επεξεργασία URLs, παρακαλώ περιμένετε...")
    progress_label.pack(pady=10)  # Show the progress label
    threading.Thread(target=process_urls).start()  # Run processing in a separate thread


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

label = tk.Label(root, text="Πατώντας 'start', θα διαβάσει τα urls που είναι στο αρχείο urls.txt και"
                            " θα αποθηκεύσει τα url των αρχείων στον φάκελο 'exports'.", wraplength=350)
label.pack(pady=20)

progress_label = tk.Label(root, text="Επεξεργασία...", fg="blue", wraplength=350)

start_button = tk.Button(root, text="Start", command=start_processing)
start_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
