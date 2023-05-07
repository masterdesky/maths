import os
import sys

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

from typing import Callable, List


def circle(num : int=100) -> np.ndarray:
    """Creates an array from the Cartesian coordinates of points on the
    circumference of a circle with an arbitrary sampling frequency.

    Parameters
    ----------
    num : int
      Sampling frequency of the circle's circumference

    Returns
    -------
    cc : numpy.ndarray
      Points on the circumference of a circle with R=1.
    """
    phi = np.linspace(0, 2*np.pi, num=num)
    # Get Cartesian coprdinates of the circle's points
    cc = np.stack((np.sin(phi), np.cos(phi)), axis=1)
    return cc


def bertrand_1(N : int=1) -> np.ndarray:
    """Implements the "random endpoints" method in Bertrand's paradox.

    Tha algorithm chooses two random points on the circumference of the
    circle. These points will serve as the endpoints for the random
    chord.

    Parameters
    ----------
    N : int
        Number of chords to be randomly generated.

    Returns
    -------
    cc : numpy.ndarray
      The Cartesian coordinates of the two endpoints of the chord.
    """
    # Select two random endpoints for a chord
    phi = 2 * np.pi * np.random.random(size=N*2).reshape(-1, 2)
    # Get Cartesian coordinates of endpoints
    cc = np.stack((np.sin(phi), np.cos(phi)), axis=2)
    return cc


def bertrand_2(N : int=1) -> np.ndarray:
    """Implements the "random radial point" method in Bertrand's paradox.

    The algorithm randomly selects a radius of the circle, then chooses
    a random point on this radius. This point will serve as the midpoint
    for the random chord.

    Parameters
    ----------
    N : int
        Number of chords to be randomly generated.

    Returns
    -------
    cc : numpy.ndarray
      The coordinates of the two endpoints of the chord.
    """
    # Select a random radius of the circle
    phi = 2 * np.pi * np.random.random(size=N)
    # Get a random point on this radius that will serve as the midpoint
    mid = np.random.random(size=N)
    # Get endpoints of the random chord from the random midpoint
    t = np.stack((phi + np.arccos(mid), phi - np.arccos(mid)), axis=1)
    # Get Cartesian coordinates of endpoints
    cc = np.stack((np.sin(t), np.cos(t)), axis=2)
    return cc


def bertrand_3(N : int=1) -> np.ndarray:
    """Implements the "random midpoint" method in Bertrand's paradox.

    The algorithm randomly selects a point inside the circle. This point
    will serve as the midpoint for the random chord.

    Returns
    -------
    cc : numpy.ndarray
      The coordinates of the two endpoints of the chord.
    """
    # Select a random midpoint inside the circle
    phi = 2 * np.pi * np.random.random(size=N)
    mid = np.sqrt(np.random.random(size=N))
    # Get endpoints of the random chord from the random midpoint
    t = np.stack((phi + np.arccos(mid), phi - np.arccos(mid)), axis=1)
    # Get Cartesian coordinates of endpoints
    cc = np.stack((np.sin(t), np.cos(t)), axis=2)
    return cc


def calculate_p(cc):
    """Calculates what percentage of the chords are longer than the
    side of the inscribed triangle of the circle they belong to.

    Parameters
    ----------
    cc : numpy.ndarray of shape (-1, 2, 2)
      List of coordinates of the endpoints of chords.

    Returns
    -------
    P : float
      Percentage of chords longer than sqrt(3).
    """
    d = np.linalg.norm(cc[:, 1, :] - cc[:, 0, :], axis=1)
    P = np.sum(d > np.sqrt(3)) / len(cc)

    return P


def plot_midpoints(f, N, **kwargs) -> None:
    """
    Parameters
    ----------
    f : callable
        The function generating the random chords.
    N : int
        Number of chords to be generated.
    """

    fig, ax = plt.subplots(figsize=(5, 5), dpi=120)
    ax.set_aspect('equal')

    ax.plot(*circle(num=100).T,
            color='black', alpha=0.7, lw=2, zorder=2)

    cc = f(N)
    ax.scatter(*np.mean(cc, axis=1).T, **kwargs)

    P = calculate_p(cc)
    ax.set_title(f'Bertrand method #{f.__name__.split("_")[1]}\nP = {P:.3f}',
                 fontsize=16, fontweight='bold')

    ax.set_xticks([])
    ax.set_yticks([])

    os.makedirs('./out/', exist_ok=True)
    plt.savefig(f'{os.path.join("./out/", f.__name__)}-midpoints.png')
    plt.close(fig)

    return


def plot_chords(f, N, **kwargs) -> None:
    """
    Parameters
    ----------
    f : callable
        The function generating the random chords.
    N : int
        Number of chords to be generated.
    """
    fig, ax = plt.subplots(figsize=(5, 5), dpi=120)
    ax.set_aspect('equal')

    ax.plot(*circle(num=100).T,
            color='black', alpha=0.7, lw=2, zorder=2)

    cc = f(N)
    ax.plot(*cc.T, **kwargs)

    P = calculate_p(cc)
    ax.set_title(f'Bertrand method #{f.__name__.split("_")[1]}\nP = {P:.3f}',
                 fontsize=16, fontweight='bold')

    ax.set_xticks([])
    ax.set_yticks([])

    os.makedirs('./out/', exist_ok=True)
    plt.savefig(f'{os.path.join("./out/", f.__name__)}-chords.png')
    plt.close(fig)

    return

def main() -> None:
    n = int(sys.argv[1])

    fs = [bertrand_1, bertrand_2, bertrand_3]
    cs = ['#99004D', '#003CB3', '#226600']
    for f, c in zip(fs, cs):
        plot_chords(f, n, color=c, alpha=0.4, lw=1, zorder=1)
        plot_midpoints(f, n, color=c, alpha=0.6, s=2**2, zorder=1)

    return


if __name__ == '__main__':
    main()
