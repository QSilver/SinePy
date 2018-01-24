import numpy as np
import random as rand
import sounddevice as sd

from matplotlib import pyplot as plt
from matplotlib import animation

xlimit = 20
ylimit = 2
linewidth = 2
phaseconstant = 0.01

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, xlimit), ylim=(-ylimit, ylimit))
x = np.linspace(0, xlimit, xlimit*1000)
line1, = ax.plot([], [], lw=linewidth)
line2, = ax.plot([], [], lw=linewidth)

# initialization function: plot the background of each frame
def init():
        line1.set_data([], [])
        line2.set_data([], [])
        return line1, line2,

def create_sine(amplitude, phase, frequency, i):
        return np.sin(2 * np.pi * (x - phaseconstant * i + phase) * frequency) * amplitude

def random():
        amplitude_m1 = 0.8#rand.random() * 0.2 + 1.0 #1.0 - 1.2
        amplitude_m2 = 0.8#rand.random() * 0.2 + 0.3 #0.3 - 0.5

        frequency1 = 1#rand.random() * 0.5 + 0.25 #0.25 - 0.75
        frequency2 = 0.95#rand.random() * 1.0 + 1.0 #1.0 - 2.0

        phase_m1 = 0#rand.random() * phaseconstant
        phase_m2 = 0#rand.random() * phaseconstant

        return amplitude_m1, amplitude_m2, frequency1, frequency2, phase_m1, phase_m2

def master(i):
        m_sine1 = create_sine(amplitude_m1, phase_m1, frequency1, i)
        m_sine2 = create_sine(amplitude_m2, phase_m2, frequency2, i)
        return m_sine1 + m_sine2

# animation function.  This is called sequentially
def animate(i):
        master_sine = master(i)
        a1, f1, p1, a2, f2, p2 = file_input()
        gen_sine1 = create_sine(a1, p1, f1, i)
        gen_sine2 = create_sine(a2, p2, f2, i)
        generated = gen_sine1 + gen_sine2
        line1.set_data(x, master_sine)
        line2.set_data(x, generated)
        return line1, line2

def file_input():
        with open("input.txt") as f:
                lines = f.read()
                a1, f1, p1, a2, f2, p2 = lines.split()
                return float(a1), float(f1), float(p1), float(a2), float(f2), float(p2)

amplitude_m1, amplitude_m2, frequency1, frequency2, phase_m1, phase_m2 = random()
anim = animation.FuncAnimation(fig, animate, init_func=init, interval=10, blit=True)
plt.show()
