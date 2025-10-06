import subprocess
import sys

from multiprocessing import Pool, TimeoutError
import time
import os

def download_video(link):
    illegal_characters = ["*", "<", ">", "]", "[", "(", ")", "|", "!", "?", "\\"]
    title = subprocess.run(["yt-dlp", "-e", link], stdout=subprocess.PIPE, text=True)
    title = str(title.stdout).strip()
    for i in illegal_characters:
        title = title.replace(i, "")
    print(title)
    command = ["yt-dlp", "-o", "./completed/%(uploader)s/" +title + ".%(ext)s", "-S", "res:+1080", link]
    subprocess.run(command)

def download_video_file():
    file = open("videos.txt")
    for line in file:
        download_video(line.strip())

def download_video_file_parallel():
    file = open("videos.txt")
    links = []
    for line in file:
        links.append(line.strip())
    
    pool = Pool(processes=5)
    pool.map(download_video, links)

if len(sys.argv) == 1:
    print("Supplying no arguments signals that you wish to download all videos in videos.txt. This can be resource intensive!!! Is this the case? ")
    while True:
        input = input("(y/n) :")
        if input == "y":
            download_video_file_parallel()
            break
        else:
            print("Okay. Supply a video file link instead.")
            break

else:
    download_video(sys.argv[1])
