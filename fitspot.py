import os
import requests
import spotipy
from flask import Flask, redirect, render_template, request, session, abort, url_for
from werkzeug.utils import secure_filename
from backend import *

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

key_id = os.environ.get('SPOTIFY_CLIENT_ID')
key_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')

sp = spotipy.Spotify(key_secret)

app = Flask('flaskapp')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def home():
    # url = 'https://accounts.spotify.com/authorize/?client_id=' + key_id + '&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%2Fcallback'
    # return render_template('home.html')

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            # return redirect(url_for('upload_file', filename=filename))
            return filename
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    dic = build_dict('top40')
    # print(dic)
    playlist = build_playlist(dic, 130)
    # print(playlist)

    # results = sp.search(q='weezer', limit=20)
    # for i, t in enumerate(results['tracks']['items']):
    #     print(' ', i, t['name'])


    app.secret_key = os.urandom(12)
    HOST = 'localhost'
    # HOST = '10.7.68.124'
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host=HOST, port=PORT)

    # res = requests.get("https://api.spotify.com/v1/search?q=album:arrival%20artist:abba&type=album", -H "Authorization: Bearer {key_id}")
    # res = requests.get("https://api.spotify.com/v1/artists/43ZHCT0cAZBISjO8DG9PnE/top-tracks?country=United+States", auth=(key_id, key_secret))
    # print(res)
    # url = 'https://accounts.spotify.com/authorize/?client_id=' + key_id + '&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%2Fcallback'
    # r = requests.get(url)
    # print(r.text)
    # r = requests.get('https://api.spotify.com/v1/search?q=album:arrival%20artist:abba&type=album')
    # print(r.text)
    # print(res)
    # data = res.json()
    # print(data)
