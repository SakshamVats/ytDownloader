import tkinter as tk
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import ffmpeg

class MyGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("720x360")
        self.root.configure(bg='black')
        self.root.title("Youtube Video Downloader")

        self.label = tk.Label(self.root, text="Youtube Video Downloader", font=('Arial', 40))
        self.label.configure(fg='black', bg='blue')
        self.label.pack(padx=20, pady=20)
        
        self.textbox = tk.Text(self.root, height=1, font=('arial', 16))
        self.textbox.pack(padx=100)
        
        self.button = tk.Button(self.root, height=1, text="Download Video", font=('Arial', 20), command=self.get_video_button)
        self.button.configure(fg='black', bg='blue')
        self.button.pack(pady=10)

        self.root.mainloop()

    def get_video_button(self):
        user_url = self.textbox.get('1.0', tk.END)
        get_max_quality_video(user_url)

        self.label = tk.Label(self.root, text="Video Downloaded!", font=('Arial', 20))
        self.label.pack(padx=20, pady=15)
        self.label.configure(fg='black', bg='green')


def download_video(url, output_dir = "downloads"):
    yt = YouTube(url, on_progress_callback = on_progress)
    video_title = ''.join(ch for ch in yt.title if (ch.isalnum() or ch == ' '))
    video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video_path = video_stream.download(output_path=output_dir, filename = 'video.mp4')

    return video_title, video_path

def download_audio(url, output_dir = "downloads"):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).first()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_path = audio_stream.download(output_path=output_dir, filename = 'audio.mp4')

    return audio_path

def merge_video_audio(video_title, video_path, audio_path, output_folder):
    input_video = ffmpeg.input(video_path)
    input_audio = ffmpeg.input(audio_path)

    output_path = output_folder + '\\' + video_title + '.mp4'
    ffmpeg.concat(input_video, input_audio, v = 1, a = 1).output(output_path).run()

    os.remove(video_path)
    os.remove(audio_path)

def get_max_quality_video(url, output_folder = r'C:\Users\Saksham Vats\Downloads'):

    video_title, video_path = download_video(url)
    audio_path = download_audio(url)

    merge_video_audio(video_title, video_path, audio_path, output_folder)

MyGUI()
