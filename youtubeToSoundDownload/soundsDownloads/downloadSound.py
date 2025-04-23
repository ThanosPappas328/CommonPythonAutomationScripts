import os
import yt_dlp

# Input file
url_file = 'Url.txt'

# Output folder
download_folder = 'soundsDownloads'
os.makedirs(download_folder, exist_ok=True)

# Read URLs
with open(url_file, 'r') as file:
    urls = [line.strip() for line in file if line.strip()]

# Set yt-dlp options
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': False
}

# Download loop
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for url in urls:
        try:
            print(f"Downloading audio from: {url}")
            ydl.download([url])
            print("Download complete.\n")
        except Exception as e:
            print(f"Failed to download {url} — {e}")
