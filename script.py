from flask import Flask, request, jsonify, send_file
import yt_dlp as ydl
import subprocess

app = Flask(__name__)

def download_music_from_url(url):
    try:
        subprocess.run(['yt-dlp', '-x', '--audio-format', 'mp3', '--audio-quality', '192K', '-o', '~/Downloads/%(title)s.%(ext)s', url], check=True)
        return "Download completed successfully!"
    except subprocess.CalledProcessError as e:
        return f"An error occurred during download: {e}"

def get_download_url(song_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with ydl.YoutubeDL(ydl_opts) as ydl_instance:
            info_dict = ydl_instance.extract_info(f"ytsearch1:{song_name}", download=False)
            if 'entries' in info_dict:
                download_url = info_dict['entries'][0]['url']
                return download_url
            else:
                return None
    except Exception as e:
        return None

@app.route('/download', methods=['POST'])
def download_handler():
    data = request.get_json()

    if 'input' in data:
        input_value = data['input']
        if input_value.startswith('http'):
            result = download_music_from_url(input_value)
        else:
            download_url = get_download_url(input_value)
            if download_url:
                result = download_url
            else:
                result = "No results found."
    else:
        result = "Input parameter missing."

    return jsonify({"result": result})

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
