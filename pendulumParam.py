# Parameters of cart and inverted pendulum system
import numpy as np

# Physical parameters of the inverted pendulum known to the controller
m1 = 0.25  # Mass of the pendulum, kg
m2 = 1.0  # Mass of the cart, kg
ell = 1.0  # Length of the rod, m
g = 9.8  # Gravity, m/s**2
b = 0.05  # Damping coefficient, Ns
alpha = 0.0

# ----- parameters for animation -----
# width & height for the cart
w = 0.5
h = 0.15
wheel_radius = 0.05  # Radius of cart wheels

# Initial Conditions
z0 = 0.0  # ,m
theta0 = 0.01 * np.pi / 180  # ,rads
zdot0 = 0.0  # ,m/s
thetadot0 = 0.0  # ,rads/s

# Simulation Parameters
t_start = 0.0  # Start time of simulation
t_end = 50.0  # End time of simulation
Ts = 0.01  # sample time for simulation
t_plot = 0.1  # the plotting and animation is updated at this rate

# saturation limits
F_max = 5.0  # Max Force, N
