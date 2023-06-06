import numpy as np


class Nose:
    """
    Object containing the points for the rocket's nose.

    Attributes:
        out_points (numpy.array): Points of the outer side of the nose.
        in_points (numpy.array): Points of the inner side of the nose.
    """

    def __init__(self, out_points, in_points) -> None:
        self.out_points = out_points
        self.in_points = in_points


# Function used to normalize a list of vector
def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2 == 0] = 1
    return a / np.expand_dims(l2, axis)


def create_nose(x, y_out, y_prime, L, thick):
    """
    Create a Nose object given the basic coordinates of the points of a nose shape.

    Args:
        x (numpy.array): x-coordinates of points on the nose.
        y_out (numpy.array): y-coordinates of points on the outer side of the nose.
        y_prime (numpy.array): derivatives of the shape along the x-axis (used to translate the outer side to create the inner side of the nose).
        L (float): Length of the nose
        thick (float): Thickness of the nose.

    Returns:
        A Nose object containing 3D vectors corresponding to both outer and inner side of the nose.
    """
    n = len(y_out)
    out_points = np.array([x, y_out]).T
    in_points = out_points + thick * normalized(np.array([y_prime, -np.ones(n)]).T)

    first = -1
    while in_points[first + 1, 1] <= 0:
        first += 1
    in_points = in_points[first:]
    in_points = in_points[in_points[:, 0] < L]
    last = first + len(in_points) - 1

    # Add the first point (y = 0) and the last point (x = L)
    if len(in_points) >= 2:
        # First point
        # This special case is for elliptic,haack and power series noses which do not have finite derivative when x=0
        if y_prime[0] == -1:
            first_point = np.array([thick, 0])
        else:  # General case
            x1, y1 = in_points[0, 0], in_points[0, 1]
            x2, y2 = in_points[1, 0], in_points[1, 1]
            xvalue = x1 - y1 * (x2 - x1) / (y2 - y1)
            first_point = np.array([xvalue, 0])
        in_points[0] = first_point

        # Last point
        x1, y1, y_p = in_points[-1, 0], in_points[-1, 1], y_prime[last]
        yl = y_p * (L - x1) + y1
        # To avoid the last point from crossing over outer points
        last_point = (
            np.array([[L, yl]])
            if yl < out_points[-1, 1] - thick / 2
            else np.array([[L, out_points[-1, 1] - thick]])
        )
        in_points = np.concatenate((in_points, last_point))

    out_points = np.pad(out_points, [(0, 0), (0, 1)], mode="constant")
    in_points = np.pad(in_points, [(0, 0), (0, 1)], mode="constant")

    return Nose(out_points=out_points, in_points=in_points)


# Different equations for nose shape (all nose equation equal 0 at the origin)


def tangent_ogive(x, R, L, thick=0.01, C=0):
    rho = (R**2 + L**2) / (2 * R)
    y_out = np.sqrt(rho**2 - (L - x) ** 2) + R - rho
    # Calculate the derivative of the function
    y_prime = (L - x) / np.sqrt(rho**2 - (L - x) ** 2)

    return create_nose(x, y_out, y_prime, L, thick)


def ellipse(x, R, L, thick=0.01, C=0):
    y_out = R * np.sqrt(1 - ((L - x[1:]) / L) ** 2)
    y_out = np.concatenate((np.array([0.0]), y_out))
    # Calculate the derivative of the function
    y_prime = R / L**2 * (L - x[1:]) / np.sqrt(1 - ((L - x[1:]) / L) ** 2)
    y_prime = np.pad(y_prime, (1, 0), mode="constant", constant_values=-1)

    return create_nose(x, y_out, y_prime, L, thick)


def parabole(x, R, L, C=0.0, thick=0.01):
    # C in [0,1]
    y_out = R * ((2 * (x / L) - C * (x / L) ** 2) / (2 - C))
    # Calculate the derivative of the function
    y_prime = 2 * R / (L * (2 - C)) * (1 - C * x)

    return create_nose(x, y_out, y_prime, L, thick)


def power_series(x, R, L, C=0.0, thick=0.01):
    # C in (0,1)
    y_out = R * (x / L) ** C
    y_prime = R * C * (x[1:] / L) ** (C - 1)
    y_prime = np.pad(y_prime, (1, 0), mode="constant", constant_values=-1)

    return create_nose(x, y_out, y_prime, L, thick)


def haack_series(x, R, L, C=0.0, thick=0.01):
    # If C = 0, LD-Haack (Von Kármán), if C=1/3, LV-Haack, minimum drag, if C=2/3, tangent to the body at the base
    theta = np.arccos(1 - 2 * x / L)
    y_out = (
        R
        / np.sqrt(np.pi)
        * np.sqrt(theta - np.sin(2 * theta) / 2 + C * np.sin(theta) ** 3)
    )
    # Calculate the derivative of the function
    xL = x * (L - x) / L**2
    A = 2 * R * ((3 * C + 2) * L - 6 * C * x) * np.sqrt(2 / np.pi) / L**2
    B = np.sqrt(xL)
    C = np.sqrt(16 * C * xL**1.5 + np.sin(2 * theta) + 2 * theta)
    C[0] = 1
    y_prime = A * B / C

    return create_nose(x, y_out, y_prime, L, thick)


def cone(x, R, L, thick=0.01, C=0):
    y_out = x * R / L
    # Calculate the derivative of the function
    y_prime = R / L * np.ones(len(x))

    return create_nose(x, y_out, y_prime, L, thick)
