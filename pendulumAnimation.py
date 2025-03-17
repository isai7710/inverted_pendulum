import numpy as np
from matplotlib import patches as mpatches
from matplotlib import pyplot as plt
from matplotlib import transforms

import pendulumParam as P


class pendulumAnimation:
    def __init__(self):
        self.flag_init = True  # Flag used to indicate initialization
        # Initialize a figure and axes object
        self.fig, self.ax = plt.subplots()
        # Initializes a list of objects (matplotlib patches objects used for animation drawings)
        self.handle = []
        # Specify the x,y axis limits
        plt.axis([-3 * P.ell, 3 * P.ell, -0.1, 3 * P.ell])
        # Draw line for the ground
        plt.plot([-2 * P.ell, 2 * P.ell], [0, 0], "b--")
        # label axes
        plt.xlabel("z")

        # Set pendulum rod properties
        self.rod_width = 0.1  # Width of the pendulum rod

        # Cross hair properties
        self.cross_size = 0.01  # Size of the cross hair
        self.cross_color = "green"  # Color of the cross hair

    def update(self, state):
        theta = state[0][0]  # Angle of pendulum, rads
        z = state[1][0]  # Horizontal position of cart, m
        # draw plot elements: cart, rod, and cross hair
        self.draw_cart(z)
        self.draw_rod(z, theta)
        self.draw_wheels(z)
        self.ax.axis("equal")
        # Set initialization flag to False after first call
        if self.flag_init:
            self.flag_init = False

    def draw_cart(self, z):
        # specify bottom left corner of rectangle
        x = z - P.w / 2.0
        y = P.wheel_radius
        corner = (x, y)
        # create rectangle on first call, update on subsequent calls
        if self.flag_init:
            # Create the Rectangle patch and append its handle
            # to the handle list
            self.handle.append(
                mpatches.Rectangle(corner, P.w, P.h, fc="blue", ec="black")
            )
            # Add the patch to the axes
            self.ax.add_patch(self.handle[0])
        else:
            self.handle[0].set_xy(corner)  # Update patch

    def draw_rod(self, z, theta):
        """
        Draw the pendulum as a rod with round ends attached to the center of the cart.
        Uses a thick line with round caps instead of a rectangle.
        """
        # The pivot point is at the center of the cart
        pivot_x = z
        pivot_y = P.wheel_radius + P.h / 2  # Center of the cart

        # Calculate the end point of the rod
        end_x = pivot_x + P.ell * np.sin(theta)
        end_y = pivot_y + P.ell * np.cos(theta)

        if self.flag_init:
            # Create a thick line with round caps
            (rod,) = self.ax.plot(
                [pivot_x, end_x],
                [pivot_y, end_y],
                linewidth=self.rod_width * 50,  # Scale up for visibility
                color="saddlebrown",
                solid_capstyle="round",  # This gives the round ends
            )

            # Add the rod to the handle list
            self.handle.append(rod)
        else:
            # Update the line data points
            self.handle[1].set_xdata([pivot_x, end_x])
            self.handle[1].set_ydata([pivot_y, end_y])

    def draw_wheels(self, z):
        # specify center of wheels
        left_wheel_center = (z - P.w / 2.0, P.wheel_radius)
        right_wheel_center = (z + P.w / 2.0, P.wheel_radius)
        # create circle on first call, update on subsequent calls
        if self.flag_init is True:
            # Create the CirclePolygon patch and append its handle
            # to the handle list
            left_wheel = mpatches.CirclePolygon(
                left_wheel_center,
                radius=P.wheel_radius,
                resolution=15,
                fc="limegreen",
                ec="black",
            )
            self.handle.append(left_wheel)
            self.ax.add_patch(left_wheel)

            right_wheel = mpatches.CirclePolygon(
                right_wheel_center,
                radius=P.wheel_radius,
                resolution=15,
                fc="limegreen",
                ec="black",
            )
            self.handle.append(right_wheel)
            self.ax.add_patch(right_wheel)
        else:
            # current handle list has the following indeces
            # cart is 0, rod is 1, left wheel is 2, right wheel is 3
            self.handle[2].xy = left_wheel_center
            self.handle[3].xy = right_wheel_center
