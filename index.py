import os
import yt_dlp
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def download_youtube_audio(url, save_path="downloads"):
    # Ensure the downloads directory exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{save_path}/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True, "Download successful!"
    except yt_dlp.utils.DownloadError as e:
        return False, f"Error downloading {url}: {e}"

@app.route('/process', methods=['POST'])
def process():
    input_value = request.form.get('inputField')  # Get the value of the input field

    if not input_value or not input_value.startswith("http"):
        return render_template('success.html', message="Invalid input. Please provide a valid YouTube URL."), 400

    success, message = download_youtube_audio(input_value)
    if success:
        return render_template('success.html', message=message)
    else:
        return render_template('success.html', message=message), 500

if __name__ == '__main__':
    app.run(debug=True)