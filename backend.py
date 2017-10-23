import csv
import numpy
from stridestobpm import *

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

def readin_csv(filename):
    f = open('uploads/'+filename, 'r')
    reader = csv.reader(f)
    ans = []
    i = 0
    for row in reader:
        if i > 0:
            # ans.append(row)
            tmp = []

            if row[0] != '' and row[10] != '' and row[11] != '' and row[12] != '' \
                and row[7] != '' and row[8] != '' and row[9] != ''\
                and row[4] != '' and row[5] != '' and row[6] != '':
                    time = float((row[0]))
                    raw_accel_x = float(row[10])
                    raw_accel_y = float(row[11])
                    raw_accel_z = float(row[12])
                    g_x = float(row[7])
                    g_y = float(row[8])
                    g_z = float(row[9])
                    rot_x = float(row[4])
                    rot_y = float(row[5])
                    rot_z = float(row[6])


                    accel_x = (raw_accel_x)*-9.8+(g_x)
                    accel_y = (raw_accel_y)*-9.8*(g_y)
                    accel_z = (raw_accel_z)*-9.8*(g_z)

                    accel = [time, accel_x, accel_y, accel_z]
                    gyro = [time, rot_x, rot_y, rot_z]

                    tmp.append(accel)
                    tmp.append(gyro)
                    ans.append(tmp)
        i += 1
    f.close()
    return ans

def make_playlist(filename):
    data = readin_csv(filename)
    # print(data)
    x = getx(data, horizontal=True)
    bpm = xtoBpm(x)
    bpm = numpy.asscalar(bpm)
    bpm = int(bpm)
    print(bpm)
    songs = build_dict('top40')
    playlist = build_playlist(songs, bpm)
    return playlist


def readin_txt(filename):
    file = open('uploads/'+filename, 'r')
    ans = []
    for line in file:
        ans.append(line)
    print(ans[2])

class user:
    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id


class playlist:
    def __init__(self, name, description, uri):
        self.name = name
        self.description = description
        self.uri = uri

if __name__ == '__main__':
    # readin_txt('Recording1.txt')
    # readin_csv('testrun1.csv')

    print(make_playlist('testrun1.csv'))
