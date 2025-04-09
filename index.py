import os
import yt_dlp
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def download_youtube_video(url, save_path="downloads"):
    # Ensure the downloads directory exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",  # Download the best video and audio quality
        "outtmpl": f"{save_path}/%(title)s.%(ext)s",  # Save with the video title as the filename
        "merge_output_format": "mp4",  # Merge video and audio into an MP4 file
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True, "Video download successful!"
    except yt_dlp.utils.DownloadError as e:
        return False, f"Error downloading {url}: {e}. Ensure FFmpeg is installed and accessible in your PATH."

@app.route('/process', methods=['POST'])
def process():
    input_value = request.form.get('inputField')  # Get the value of the input field

    if not input_value or not input_value.startswith("http"):
        return render_template('success.html', message="Invalid input. Please provide a valid YouTube URL."), 400

    success, message = download_youtube_video(input_value)  # Call the updated function
    if success:
        return render_template('success.html', message=message)
    else:
        return render_template('success.html', message=message), 500
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