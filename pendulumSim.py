# ----------------------
# Date: 6/8/2023
# Name: Isai Sanchez
# Purpose: Develop python code that simulates feedback control of a dynamic system using a PID controller
# (inspiration and some code from BYU Introduction to Feedback Control book)
# Description: ouput of the system is y(t), input of the system is u(t) yet there is an external 
#   disturbance signal d(t), output of the system is corrupted by zero-mean noise n(t), the input to the
#   controller is the reference signal r(t) along with the output whichi is corrupted by noise. 
#   TODO: write block diagram in notebook and put on website
# ----------------------

import matplotlib.pyplot as plt 
from pendulumDynamics import Dynamics
from Controller import Controller
from signalGenerator import signalGenerator
from pendulumAnimation import pendulumAnimation
from dataPlotter import dataPlotter

# simulation parameters
t_start = 0.0   # start time
t_end = 20.0    # end time
t_plot = 0.1    # sample rate for plotter and animation
Ts = 0.01       # sample rate for dynamics and controller

# instantiate system, controller, and reference classes
system = Dynamics(sample_rate=Ts)
controller = Controller(sample_rate=Ts)
reference = signalGenerator(amplitude=0.5, frequency=0.05)
disturbance = signalGenerator(amplitude=1.0, frequency = 0.0)
noise = signalGenerator(amplitude=0.01)

# instantiate the simulation plots and animation
dataPlot = dataPlotter()
animation = pendulumAnimation()

t = t_start
y = system.h()  # output of system at start of simulation
# main simulation loop
while t < t_end:
    # set time for next plot
    t_next_plot = t + t_plot
    # Propagate dynamics and controller at fast rate Ts
    while t < t_next_plot:
        r = reference.square(t) # assign reference
        d = disturbance.step(t) # simulate input disturbance
        n = noise.random(t) # simulate sensor noise
        u = controller.update(r, y + n) # update controller
        y = system.update(u + d) # Propagate the dynamics
        t = t + Ts # advance time by Ts
    # update animation and data plots
    animation.update(system.state)
    dataPlot.update(t, reference, system.state, u)
    # pause causes the figure to be displayed during the simulation
    plt.pause(0.0001)

# keep the program from closing until the user presses a button
print('Press key to close')
plt.waitforbuttonpress()
plt.close()