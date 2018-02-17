import matplotlib.animation as animation
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import matplotlib as mpl
import random as rand
import numpy as np
import serial
import sys
import os

### AUDIO LIBRARY
import pyaudio

#ser = serial.Serial("COM3", 57600)
ser = serial.Serial("/dev/ttyS0", 57600)

is_finished = False

xlimit = 20
ylimit = 2
linewidth = 5
phaseconstant = 0.015
mapping_max = 1023.0

# First set up the figure, the axis, and the plot element we want to animate
mpl.rcParams['toolbar'] = 'None'
plt.rcParams['axes.facecolor'] = 'black'
fig = plt.figure(0, facecolor='black')
ax = plt.axes(xlim=(0, xlimit), ylim=(-ylimit, ylimit))
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.rc('grid', linestyle="-", color='black')
plt.grid(True, alpha=0.4)
plt.box(False)
plt.xticks(np.arange(0,xlimit,1))
x = np.linspace(0, xlimit, xlimit*1000)
line1, = ax.plot([], [], lw=linewidth)
line2, = ax.plot([], [], lw=linewidth)


# MI - Will be replaced with sine data
aout = pyaudio.PyAudio()
astm = aout.open(format=aout.get_format_from_width(2),
                 channels=1,
                 rate=44100,
                 output=True)





# initialization function: plot the background of each frame
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2,

def create_sine(amplitude, phase, frequency, i):
    return np.sin(2 * np.pi * (x - phaseconstant * i + phase) * frequency) * amplitude

def generate_master():
    amplitude_m1 = 0.8#rand.random() * 0.2 + 1.0 #1.0 - 1.2
    amplitude_m2 = 0.8#rand.random() * 0.2 + 0.3 #0.3 - 0.5

    frequency1 = 0.8#rand.random() * 0.5 + 0.25 #0.25 - 0.75
    frequency2 = 0.75#rand.random() * 1.0 + 1.0 #1.0 - 2.0

    phase_m1 = 0#rand.random() * phaseconstant
    phase_m2 = 0#rand.random() * phaseconstant

    return amplitude_m1, amplitude_m2, frequency1, frequency2, phase_m1, phase_m2

def master(i):
    m_sine1 = create_sine(amplitude_m1, phase_m1, frequency1, i)
    m_sine2 = create_sine(amplitude_m2, phase_m2, frequency2, i)
    return m_sine1 + m_sine2

# animation function.  This is called sequentially
def animate(i):
    global is_finished
    master_sine = master(i)
    a1, f1, p1, a2, f2, p2 = file_input()
    if is_finished == True:
        a1, a2, f1, f2, p1, p2 = generate_master()
        p1 = p1 + 0.05
        p2 = p2 + 0.05
    gp = p1 + p2
    gen_sine1 = create_sine(a1, gp, f1, i)
    gen_sine2 = create_sine(a2, gp, f2, i)
    generated = gen_sine1 + gen_sine2
    line1.set_data(x, master_sine)
    line2.set_data(x, generated)

    data = generated.astype(np.int16)
    data = data[::45]
    data = data*32525
#    adata = ("{:0>2x}" * len(data)).format(*tuple(data[::-1]))
    astm.write(data)

    if equals(master_sine, generated, 200):
        is_finished = True
        display_win()
    return line1, line2


def file_input():
    ser.reset_input_buffer()
    line = ser.readline().split()
    #line = [818,818,0,818,767,0]
    #line = [1024,1204,0,1024,512,512]
    #for i in range(6):
    #    line[i] = rand.randint(0,1024)
    while len(line) != 6:
        line = ser.readline().split()
    a1, f1, p1, a2, f2, p2 = line
    return map_input(a1, f1, p1, a2, f2, p2)

def equals(graph1, graph2, errorMargin):
    difference = abs(graph1 - graph2)
    return all(arrayVal < errorMargin for arrayVal in difference)

def map_input(a1, f1, p1, a2, f2, p2):
    a1 = float(a1)/mapping_max
    f1 = float(f1)/mapping_max/5+0.7
    p1 = float(p1)/mapping_max*2
    a2 = float(a2)/mapping_max
    f2 = float(f2)/mapping_max/5+0.7
    p2 = float(p2)/mapping_max*2
    return a1, f1, p1, a2, f2, p2

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

@run_once
def display_win():
    print("Victory")
    print("5898")
    sys.exit(0)

amplitude_m1, amplitude_m2, frequency1, frequency2, phase_m1, phase_m2 = generate_master()
anim = animation.FuncAnimation(fig, animate, init_func=init, interval=10, blit=True)
plt.show()

