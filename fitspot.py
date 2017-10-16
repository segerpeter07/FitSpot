import os
import requests

key_id = os.environ.get('SPOTIFY_CLIENT_ID')
key_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')

def build_dict(filename):
    file = open(filename, 'r')
    ans = {}
    for line in file:
        data = line.split(', ')
        ans[data[0]] = data[1].split('\n')[0]
    return ans

def build_playlist(songs, desired_bpm):
    target_bpms = list(range(desired_bpm-10, desired_bpm+10))
    ans = []
    for key in songs:
        bpm = songs[key]
        if int(bpm) in target_bpms:
            ans.append(key)
    return ans

if __name__ == "__main__":
    dic = build_dict('top40')
    # print(dic)
    playlist = build_playlist(dic, 130)
    print(playlist)

    res = requests.get("https://api.spotify.com/v1/search?q=album:arrival%20artist:abba&type=album", auth=(key_id, key_secret))
    data = res.json()
    print(data)
