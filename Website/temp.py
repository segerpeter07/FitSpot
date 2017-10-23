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
        playlists = sp.user_playlist_create(username, playlist_name, playlist_description)
        # result = sp.search('Kygo')
        # pprint.pprint(result)
        tracks = ['spotify:track:7fwXWKdDNI5IutOMc5OKYw']
        results = sp.user_playlist_add_tracks(username, 'spotify:user:lightknight:playlist:0NPyMjih5FPrbFUqMl4uAH', tracks)

        pprint.pprint(results)

        # results = sp.current_user_saved_tracks()
        # results = sp.current_user_playlists()
        # for item in results['items']:
            # track = item['track']
            # playlist = item['snapshot_id']
            # print(track['name'] + ' - ' + track['artists'][0]['name'])
            # print(playlist)
    else:
        print('Can\' get token')
