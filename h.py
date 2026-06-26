import os
import time
import vlc
from pytube import YouTube

# URL of the YouTube video
video_url = "https://youtu.be/MKQ4bX141zM?si=gkvoW_Wt3o5ZueGt"

# Directory to save the downloaded video
download_directory = "C:\Program Files (x86)\VideoLAN\VLC"

# Download the video
yt = YouTube(video_url)
video_stream = yt.streams.filter(file_extension="mp4").first()
download_path = os.path.join(download_directory, video_stream.default_filename)
video_stream.download(output_path=download_directory)

# Path to the VLC installation directory
vlc_path ="C:\\Program Files (x86)\\VideoLAN\\VLC"

# Create VLC instance with the path to libvlc.dll
instance = vlc.Instance(f'--plugin-path={vlc_path}')

# Create VLC media player object
player = vlc.MediaPlayer(instance)

# Load the downloaded video into the player
media = vlc.Media(download_path)
player.set_media(media)

# Start playing the video
player.play()

# Wait for the video to finish
while player.get_state() != vlc.State.Ended:
    time.sleep(1)  # Sleep for a second to avoid high CPU usage

# Release the media player
player.release()
