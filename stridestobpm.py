import numpy
import matplotlib.pyplot as plt

def getx(data, horizontal = False):
    if horizontal == True:
        i = 1
    else:
        i = 2
    ans = []
    return [row[0][i] for row in data]

def xtoBpm(x, Fs=50, plot=False):
    # create array of frequencies
    Nx = len(x)
    fx = numpy.linspace(-Fs/2, Fs/2 - Fs/Nx, Nx)

    # find fourier transform of data and shift to correct
    X = numpy.fft.fft(x)
    X = numpy.fft.fftshift(X)

    # optional plotting
    if plot == True:
        plt.plot(fx, X)
        plt.show()

    max1ind = numpy.argmax(X) #find index of gravity frequency
    # print(max1ind)
    # print(type(X))
    # print(len(X))
    sort = numpy.sort(X)
    # print(sort[len(X)-1])
    X[max1ind] = 0 # minimize gravity frequency
    # sort[len(sort)-1] = 0
    max2ind = numpy.argmax(X) # find index of actual frequency max
    # max2ind = numpy.argmax(sort)
    # max2ind = len(sort)-1

    spm = fx[max2ind]*60 # find frequency value and convert to minutes
    bpm = round(spm/2) # divide by 2 for bpm

    return bpm

if __name__ == '__main__':
    # read txt file
    with open('xdata1.txt', 'r') as f:
        x = f.readlines()
    x = list(map(float, x))

    print(len(x))
    data = getx(x, horizontal=True)
    bpm = xtoBpm(data)
    print(bpm)
