#!/usr/bin/env python3

import argparse
import os
import sys
from yt_dlp import YoutubeDL

def download_video(url: str, output_dir: str = "."):
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': False,
        'noplaylist': True
    }

    try:
        print(f"🎬 Downloading: {url}")
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ Done\n")
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}\n")

def read_urls_from_file(file_path: str):
    try:
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
            return urls
    except Exception as e:
        print(f"❌ Failed to read file '{file_path}': {e}")
        return []

def main():
    parser = argparse.ArgumentParser(
        description="Download video(s) from URL(s) using yt-dlp"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', help="Single video URL to download")
    group.add_argument('--file', help="Text file containing multiple video URLs")

    parser.add_argument(
        '--output', '-o',
        default=".",
        help="Output directory (default: current directory)"
    )

    args = parser.parse_args()

    if not os.path.exists(args.output):
        print("📁 Output directory does not exist. Creating it...")
        os.makedirs(args.output)

    if args.url:
        download_video(args.url, args.output)

    elif args.file:
        urls = read_urls_from_file(args.file)
        if not urls:
            print("⚠️ No URLs found in the file.")
            sys.exit(1)
        for url in urls:
            download_video(url, args.output)

if __name__ == "__main__":
    main()
