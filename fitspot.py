import os
import sys
import requests
import spotipy
from flask import Flask, redirect, render_template, request, session, abort, url_for
from werkzeug.utils import secure_filename
from backend import *
import base64
import pprint
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
    # print(playlist)\

    '''
    key_id = key_id.encode('ascii')
    key_secret = key_secret.encode('ascii')

    auth_id = base64.b64encode(key_id)
    auth_key = base64.b64decode(key_secret)

    # print(auth_id)
    authOptions = {
        url: 'https://accounts.spotify.com/api/token',
        headers: {
            'Authorization': 'Basic ' + auth_id + ':' + auth_key
        }
        form: {
            grant_type: 'client_credentials'
        }
        json: True
    }
    # header = 'Authorization': 'Basic ' + auth_id + ':' + auth_key
    # print(authOptions)

    # r = requests.post(url='https://accounts.spotify.com/api/token', headers=header, grant_type='client_credentials', json=True)
    r = requests.post(authOptions)
    print(r)
    '''


    # app.secret_key = os.urandom(12)
    # HOST = 'localhost'
    # # HOST = '10.7.68.124'
    # PORT = int(os.environ.get('PORT', 5000))
    # app.run(host=HOST, port=PORT)

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



    '''
    WORKS!!!
    client_credentials_manager = SpotifyClientCredentials(client_id=key_id, client_secret=key_secret)

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    # spotify = spotipy.Spotify()
    res = sp.search(q='artist:MIKA', type='artist')
    print(res)


    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks()
        for item in results['items']:
            track = item['track']
            print(track['name'] + ' - ' + track['artists'][0]['name'])
    else:
        print("Can't get token for", username)
    '''

    client_credentials_manager = SpotifyClientCredentials(client_id=key_id, client_secret=key_secret)

    scope = ' playlist-modify-public'

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print('Usage %s username'%(sys.argv[0],))
        sys.exit()

    token = util.prompt_for_user_token(username, scope, client_id=key_id, client_secret=key_secret, redirect_uri=redirect_url)
    print(token)

    if token:
        sp = spotipy.Spotify(auth=token, client_credentials_manager=client_credentials_manager)
        sp.trace = False
        playlist_name = 'FitSpot'
        playlist_description = 'This playlist was made using FitSot'
        # playlists = sp.user_playlist_create(username, playlist_name, playlist_description)
        # result = sp.search('Kygo')
        # pprint.pprint(result)
        results = sp.user_playlist_add_tracks(username, 'spotify:user:lightknight:playlist:0NPyMjih5FPrbFUqMl4uAH', 'spotify:track:2UxfcZJCphbEkfbZ6nLiDx')

        # pprint.pprint(playlists)

        # results = sp.current_user_saved_tracks()
        # results = sp.current_user_playlists()
        # for item in results['items']:
            # track = item['track']
            # playlist = item['snapshot_id']
            # print(track['name'] + ' - ' + track['artists'][0]['name'])
            # print(playlist)
    else:
        print('Can\' get token')


    # playlists = sp.user_playlists('lightknight')
    # while playlists:
    #     for i, playlist in enumerate(playlists['items']):
    #         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    #     if playlists['next']:
    #         playlists = sp.next(playlists)
    #     else:
    #         playlists = None
