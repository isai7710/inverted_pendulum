# ----------------------
# Date: 6/8/2023
# Name: Isai Sanchez
# Purpose: Develop python class that implements dynamics of a system
# (inspiration and some code from BYU Introduction to Feedback Control book)
# Description: Euler-Lagrange methods used to implement dynamics of a system
# ----------------------

import numpy as np
import pendulumParam as P

class pendulumDynamics:
    def __init__(self):
        # initial state conditions stored here
        self.state = np.array([
            [P.z0],             # initial condition for z
            [P.theta0],         # initial condition for theta
            [P.zdot0],          # initial condition for z dot
            [P.thetadot0]       # initial condition for theta dot
            ])
        self.Ts = P.Ts          # sample rate of system
        self.limit = 1.0        # input saturation limit
        # system parameters to be used in this class (modified by alpha to account for uncertainty)
        self.m1 = P.m1 * (1.+P.alpha*(2.*np.random.rand()-1.))
        self.m2 = P.m2 * (1.+P.alpha*(2.*np.random.rand()-1.))
        self.b  = P.b  * (1.+P.alpha*(2.*np.random.rand()-1.))
        self.l  = P.ell * (1.+P.alpha*(2.*np.random.rand()-1.))
        self.g  = P.g
        self.force_limit = P.F_max

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