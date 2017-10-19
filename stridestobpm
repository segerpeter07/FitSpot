import numpy
import matplotlib.pyplot as plt

# read txt file
with open('xdata1.txt', 'r') as f:
    x = f.readlines()
x = list(map(float, x))

def getx(data):
    return [row[1] for row in data]

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
    X[max1ind] = 0 # minimize gravity frequency
    max2ind = numpy.argmax(X) # find index of actual frequency max

    spm = fx[max2ind]*60 # find frequency value and convert to minutes
    bpm = round(spm/2) # divide by 2 for bpm

    return bpm

print(xtoBpm(x))
