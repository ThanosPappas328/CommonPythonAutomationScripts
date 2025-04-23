#!/usr/bin/env python3

import os
import re
import sys
import argparse
import yt_dlp
from shutil import which
from datetime import datetime

def check_ffmpeg():
    if not which("ffmpeg"):
        sys.exit("❌ 'ffmpeg' is not installed or not found in PATH. Please install it to enable audio conversion.")

def read_urls(file_path):
    if not os.path.isfile(file_path):
        sys.exit(f"❌ File not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def sanitize_filename(title):
    title = re.sub(r'[^\w\s-]', '', title, flags=re.UNICODE)
    title = re.sub(r'\s+', '_', title)
    return title.strip('_')

def progress_hook(d):
    if d['status'] == 'downloading':
        total = d.get('_total_bytes_str', '???')
        speed = d.get('_speed_str', '')
        eta = d.get('_eta_str', '')
        print(f"📥 {d['_percent_str'].strip()} of {total} at {speed} ETA {eta}", end='\r')
    elif d['status'] == 'finished':
        print("\n🔄 Download finished. Converting...")

def generate_output_template(output_dir, ext):
    def sanitize_path(info):
        title = sanitize_filename(info.get('title', 'audio'))
        return os.path.join(output_dir, f"{title}.{ext}")
    return sanitize_path

def download_audio(urls, output_dir, audio_format, allow_playlists):
    os.makedirs(output_dir, exist_ok=True)

    log_path = os.path.join(output_dir, 'download_log.txt')
    with open(log_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"\n=== Download Session: {datetime.now()} ===\n")

        ydl_opts = {
            'format': 'bestaudio/best',
            'progress_hooks': [progress_hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': '192',
            }],
            'noplaylist': not allow_playlists,
            'quiet': True,
            'outtmpl': generate_output_template(output_dir, audio_format),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for url in urls:
                try:
                    print(f"\n🎧 Downloading: {url}")
                    ydl.download([url])
                    print("✅ Success!\n")
                    log_file.write(f"✅ {url}\n")
                except Exception as e:
                    print(f"❌ Failed: {url} — {e}")
                    log_file.write(f"❌ {url} — {e}\n")

    print(f"\n📜 Log saved: {log_path}")

def main():
    parser = argparse.ArgumentParser(
        description="🎶 Batch download YouTube audio with yt-dlp."
    )
    parser.add_argument('--file', '-f', required=True, help="Path to text file with video URLs")
    parser.add_argument('--output', '-o', default='soundsDownloads', help="Target download directory")
    parser.add_argument('--format', choices=['mp3', 'wav'], default='mp3', help="Audio format")
    parser.add_argument('--allow-playlists', action='store_true', help="Enable playlist downloading")

    args = parser.parse_args()

    check_ffmpeg()
    urls = read_urls(args.file)
    if not urls:
        sys.exit("⚠️ No URLs found in the input file.")

    download_audio(urls, args.output, args.format, args.allow_playlists)

if __name__ == "__main__":
    main()
