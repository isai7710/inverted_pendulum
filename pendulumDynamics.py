# ----------------------
# Date: 6/8/2023
# Name: Isai Sanchez
# Purpose: Develop python class that implements dynamics of a system
# (inspiration and some code from BYU Introduction to Feedback Control book)
# Description: Euler-Lagrange methods used to implement dynamics of a system
# ----------------------

import numpy as np

class pendulumDynamics:
    def __init__(self, sample_rate):
        # initial state conditions
        y0 = 0.0
        ydot0 = 0.0
        self.state = np.array([
            [y0],       # initial condition for y
            [ydot0],    # initial condition for ydot
            ])
        self.Ts = sample_rate # sample rate of system
        self.limit = 1.0 # input saturation limit
        # nominal system parameters (i.e. important parameters like stiffness, mass, etc., dependent on
        # equations of motion converted to state space form)
        self.a0 = 3.0
        self.a1 = 2.0
        self.b0 = 4.0
        # modify the system parameters by random value to account for uncertainty in IRL systems
        alpha = 0.2 # Uncertainty parameter/percentage of deviation
        self.a1 = self.a1 * (1.+alpha*(2.*np.random.rand()-1.))
        self.a0 = self.a0 * (1.+alpha*(2.*np.random.rand()-1.))
        self.b0 = self.b0 * (1.+alpha*(2.*np.random.rand()-1.))

    # EOM here
    def f(self, state, u):
        # for the system with equations of motion in state space form, xdot = f(x,u), return the EOM f(x,u)
        y = state.item(0)
        ydot = state.item(1)
        # the equations of motion are the following:
        yddot = -self.a1 * ydot - self.a0 * y + self.b0 * u
        # build xdot and return
        xdot = np.array([[ydot], [yddot]])
        return xdot
    
    def h(self):
        # Returns the measured output y = h(x)
        y = self.state.item(0)
        # return output
        return y
    
    def update(self, u):
        # This is the external method that takes the input u(t)
        # and returns the output y(t).
        u = self.saturate(u, self.limit) # saturate the input
        self.rk4_step(u) # propagate the state by one time step
        y = self.h() # compute the output at the current state
        return y

    def rk4_step(self, u):
        # Integrate ODE using Runge-Kutta RK4 algorithm
        F1 = self.f(self.state, u)
        F2 = self.f(self.state + self.Ts / 2 * F1, u)
        F3 = self.f(self.state + self.Ts / 2 * F2, u)
        F4 = self.f(self.state + self.Ts * F3, u)
        self.state += self.Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)

    def saturate(self, u, limit):
        if abs(u) > limit:
            u = limit*np.sign(u)
        return u