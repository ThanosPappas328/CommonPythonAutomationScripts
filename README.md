# Common Python Automation Scripts

This repository contains a collection of Python automation scripts that simplify everyday tasks. I created these scripts to save time, increase productivity, and make repetitive processes easier. These tools can be useful for anyone looking to automate common tasks like downloading files, processing images, and scraping URLs. Obviously these are made for some repetitive tasks I needed to do. Not meant for everyone.

## Scripts Overview

1. **Download Audio/Video with yt-dlp**  
   Downloads and converts audio or video files from URLs in a text file. Supports MP3 and WAV formats.

2. **URL Exporter with Web Scraping (Tkinter GUI)**  
   Scrapes webpages for downloadable files (e.g., PDFs, ZIPs) and saves them as `.url` shortcut files. Includes a simple GUI built with Tkinter.

3. **Resize and Crop Images**  
   Resizes and crops images to specific dimensions while maintaining the aspect ratio. Prevents overwriting files by generating unique filenames.

4. **Background Removal from Images**  
   Removes the background from images using `rembg`. Processes images in bulk and logs errors.

5. **Download Files from Web URLs**  
   Downloads PDF, TXT, and ZIP files from webpages listed in a text file and saves them in an organized folder.

6. **📁 Folder Structure Generator (GUI)**  
  Simple drag-and-type GUI app to generate folder structures — useful for project scaffolding or organization.

7. ## 📁 Project Boilerplate Generator

A simple GUI tool that helps you scaffold basic folder structures for common web and mobile development frameworks. Ideal for quickly spinning up a new project with a clean, organized directory layout.

### 🔧 Supported Project Types:
- **React**
- **Next.js**
- **Express**
- **Flutter**

## 🖥️ Convert to Executable (Optional)

You can convert any of these scripts into a `.exe` app for easier usage on Windows:

```bash
pyinstaller --onefile your_script.py
## Technologies Used

- **yt-dlp** for downloading audio/video
- **requests** and **BeautifulSoup** for web scraping
- **Tkinter** for GUI development
- **Pillow** and **rembg** for image processing
- **tqdm** for progress bars

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
