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

import pendulumParam as P
from dataPlotter import dataPlotter
from pendulumAnimation import pendulumAnimation
from pendulumDynamics import pendulumDynamics

# from Controller import Controller
from signalGenerator import signalGenerator

# instantiate system, controller, and reference classes
pendulum = pendulumDynamics()
# controller = Controller(sample_rate=Ts)
reference = signalGenerator(amplitude=0.5, frequency=0.02)
force = signalGenerator(amplitude=0, frequency=1)
# disturbance = signalGenerator(amplitude=1.0, frequency = 0.0)
# noise = signalGenerator(amplitude=0.01)

# instantiate the simulation plots and animation
dataPlot = dataPlotter()
animation = pendulumAnimation()

t = P.t_start
# main simulation loop
while t < P.t_end:
    # set time for next plot
    t_next_plot = t + P.t_plot
    # Propagate dynamics and controller at fast rate Ts
    while t < t_next_plot:
        r = reference.square(t)  # assign reference
        # d = disturbance.step(t)   # simulate input disturbance
        # n = noise.random(t)       # simulate sensor noise
        u = force.step(t)  # update controller
        y = pendulum.update(u)  # Propagate the dynamics
        t = t + P.Ts  # advance time by Ts
    # update animation and data plots
    animation.update(pendulum.state)
    dataPlot.update(t, r, pendulum.state, u)
    # pause causes the figure to be displayed during the simulation
    plt.pause(0.0001)

# keep the program from closing until the user presses a button
print("Press key to close")
plt.waitforbuttonpress()
plt.close()
