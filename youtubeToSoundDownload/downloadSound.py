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
        print("❌ 'ffmpeg' is not installed or not found in PATH.")
        print("Please install it to enable audio conversion.\n")
        sys.exit(1)

def read_urls(file_path):
    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def sanitize_title(title):
    # Remove emojis & special characters from filenames
    clean = re.sub(r'[^\w\s-]', '', title, flags=re.UNICODE)
    clean = re.sub(r'\s+', '_', clean)
    return clean.strip('_')

def progress_hook(d):
    if d['status'] == 'downloading':
        total = d.get('_total_bytes_str', 'unknown')
        speed = d.get('_speed_str', '...')
        eta = d.get('_eta_str', '...')
        print(f"📥 {d['_percent_str'].strip()} of {total} at {speed} ETA {eta}", end='\r')
    elif d['status'] == 'finished':
        print(f"\n🔄 Converting audio...")

def download_audio(urls, output_dir, audio_format, allow_playlists):
    os.makedirs(output_dir, exist_ok=True)
    log_path = os.path.join(output_dir, 'download_log.txt')
    log_file = open(log_path, 'a', encoding='utf-8')
    log_file.write(f"\n=== Download Session: {datetime.now()} ===\n")

    def sanitize_hook(info):
        title = sanitize_title(info.get('title', 'audio'))
        ext = audio_format
        return {'filepath': os.path.join(output_dir, f"{title}.{ext}")}

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': '192',
        }],
        'noplaylist': not allow_playlists,
        'quiet': True,
        'logger': yt_dlp.utils.StdLogger(),
        'outtmpl': sanitize_hook,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            try:
                print(f"\n🎧 Downloading from: {url}")
                ydl.download([url])
                log_file.write(f"✅ {url}\n")
                print("✅ Done\n")
            except Exception as e:
                print(f"❌ Failed: {e}")
                log_file.write(f"❌ {url} — {e}\n")

    log_file.close()
    print(f"\n📜 Download log saved to: {log_path}")

def main():
    parser = argparse.ArgumentParser(description="Batch audio downloader with yt-dlp.")
    parser.add_argument('--file', '-f', required=True, help="Text file with video URLs")
    parser.add_argument('--output', '-o', default='soundsDownloads', help="Download directory")
    parser.add_argument('--format', choices=['mp3', 'wav'], default='mp3', help="Audio format")
    parser.add_argument('--allow-playlists', action='store_true', help="Allow playlist downloads")

    args = parser.parse_args()

    check_ffmpeg()
    urls = read_urls(args.file)

    if not urls:
        print("⚠️ No URLs found.")
        sys.exit(1)

    download_audio(urls, args.output, args.format, args.allow_playlists)

if __name__ == "__main__":
    main()
