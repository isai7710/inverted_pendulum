# ----------------------
# Date: 6/8/2023
# Name: Isai Sanchez
# Purpose: Develop python class that plots data using the matplotlib library
# (inspiration and some code from BYU Introduction to Feedback Control book)
# Description: data plotter class
# ----------------------

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

plt.ion()   # enables interactive drawing

class dataPlotter:
    def __init__(self):
        # Number of subplots = num_of_rows*num_of_cols
        self.num_rows = 3 # Number of subplot rows
        self.num_cols = 1 # Number of subplot columns
        # Crete figure and axes handles
        self.fig, self.ax = plt.subplots(self.num_rows,
        self.num_cols,
        sharex=True)
        # Instantiate lists to hold the time and data histories
        self.time_history = [] # time
        self.r_history = [] # reference r
        self.y_history = [] # output y
        self.ydot_history = [] # velocity ydot
        self.u_history = [] # input u
        # create a handle for every subplot.
        self.handle = []
        self.handle.append(subplotWindow(self.ax[0], ylabel='y', title='Simple System'))
        self.handle.append(subplotWindow(self.ax[1], ylabel='ydot'))
        self.handle.append(subplotWindow(self.ax[2], xlabel='t(s)', ylabel='u'))       

    def update(self, time, reference, state, control):
        # update the time history of all plot variables
        self.time_history.append(time)
        self.r_history.append(reference)
        self.y_history.append(state.item(0))
        self.ydot_history.append(state.item(1))
        self.u_history.append(control)

        # update the plots with associated histories
        self.handle[0].update(self.time_history, [self.r_history, self.y_history])
        self.handle[1].update(self.time_history, [self.ydot_history])
        self.handle[1].update(self.time_history, [self.u_history])

# Create each individual subplot using this class
class subplotWindow:
    def __init__(self, ax, xlabel='', ylabel='', title='', legend=None):
        '''
        ax - This is a handle to the axes of the figure
        xlable - Label of the x-axis
        ylable - Label of the y-axis
        title - Plot title
        legend - A tuple of strings that identify the data, EX: ("data1","data2", ... , "dataN")
        '''
        self.legend = legend
        self.ax = ax                # axes handle
        self.colors = ['b', 'g', 'r', 'c', 'm', 'y']    # list of colors
        # ’b’ - blue, ’g’ - green, ’r’ - red, ’c’ - cyan,
        # ’m’ - magenta, ’y’ - yellow, ’k’ - black
        self.line_styles = ['-', '--', '-.', ':']       # list of line styles
        # ’-’ solid, ’--’ dashed, ’-.’ dash_dot, ’:’ dotted
        self.line = []
        # Configure the axes here:
        self.ax.set_ylabel(ylabel)
        self.ax.set_xlabel(xlabel)
        self.ax.set_title(title)
        self.ax.grid(True)
        # keep track of initialization
        self.init = True

    # Adds data to the plot
    def update(self, time, data):
        # initialize the plot the first time routine is called
        if self.init==True:
            for i in range(len(data)):
                # instantiate line object and add it to the axes
                self.line.append(Line2D(time, data[i], 
                                        color=self.colors[np.mod(i, len(self.colors)-1)],
                                        ls=self.line_styles[np.mod(i, len(self.line_styles) - 1)],
                                        label=self.legend if self.legend!=None else None))
                self.ax.add_line(self.line[i])
            self.init=False
            # add legend if one is specified
            if self.legend!=None:
                plt.legend(handles=self.line)
        # add new data to the plot after initializing 
        else: 
            # update the x and y data of each line with the following
            for i in range(len(self.line)):
                self.line[i].set_xdata(time)
                self.line[i].set_ydata(data[i])

        # Adjusts the axis to fit all of the data
        self.ax.relim()
        self.ax.autoscale()