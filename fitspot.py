import os
import sys
import requests
import spotipy
from flask import Flask, redirect, render_template, request, session, abort, url_for
from werkzeug.utils import secure_filename
from backend import *
import base64
import pprintpp
import subprocess

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

scope = 'user-library-read'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

key_id = os.environ.get('SPOTIFY_CLIENT_ID')
key_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
redirect_url = 'http://localhost:8000/callback'

sp = spotipy.Spotify(key_secret)

app = Flask('flaskapp')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(url_for('failure'))
        file = request.files['file']
        # if user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            return redirect(url_for('failure'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            # return redirect(url_for('upload_file', filename=filename))
            return redirect(url_for('playlist', filename=filename))     # Change for login
        else:
            return redirect(url_for('failure'))
    return render_template('index.html')

@app.route('/success', methods=['GET', 'POST'])
def success():
    if request.method == 'GET':
        return render_template('success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        print(str(username))
        scope = 'playlist-modify-public'
        client_credentials_manager = SpotifyClientCredentials(client_id=key_id, client_secret=key_secret)
        token = util.prompt_for_user_token(username, scope, client_id=key_id, client_secret=key_secret, redirect_uri=redirect_url)
        if token:
            sp = spotipy.Spotify(auth=token, client_credentials_manager=client_credentials_manager)
            sp.trace = False
            results = sp.user_playlist_add_tracks(username, 'spotify:user:lightknight:playlist:0NPyMjih5FPrbFUqMl4uAH', 'spotify:track:4KANJH1baadr3U7XsVbM17')
            pprint.pprint(results)
        # user = user(username, '123')

@app.route('/failure', methods=['GET', 'POST'])
def failure():
    return render_template('failure.html')

@app.route('/playlist/<filename>', methods=['GET','POST'])
def playlist(filename):
    pl = make_playlist(filename)
    return render_template('playlist.html', items=pl)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    # HOST = '10.7.68.124'
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host=HOST, port=PORT)
