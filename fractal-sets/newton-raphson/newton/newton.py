import numpy as np
from functools import reduce


#######
#
#    NEWTON-RAPHSON METHOD IMPLEMENTATION
#
##########################################################################

def nr_step(P, X):
    '''
    Calculate a single step of the Newton-Raphson iterative method on
    a polynomial, evaluated at given X value(s).

    Parameters
    ----------
    P : newton.polynomial.Polynomial
        A polynomial instance to apply the Newton-Raphson iterative
        method on.
    X : float or array-like
        A value or an array of values to evaluate the input polynomial
        at.
    '''
    return X - P.eval(X)/P.evald(X, 1)

def nr_iter(P, X, N=20):
    '''
    Calculate multiple consecutive steps of the Newton-Raphson iterative
    method on a polynomial, evaluated at given X value(s).

    Parameters
    ----------
    P : newton.polynomial.Polynomial
        A polynomial instance to apply the Newton-Raphson iterative
        method on.
    X : float or array-like
        A value or an array of values to evaluate the input polynomial
        at.
    N : int, default=20
        Number of iteration to take.
    '''
    return reduce(lambda x, _: nr_step(P, x), range(N), X)


#######
#
#    NEWTON-RAPHSON GRID
#
##########################################################################

def get_even_points(N, limx, limy):
    '''
    Get the number of points along the X and Y dimensions of an
    arbitrary 2D grid, where the points are evenly distributed.

    Parameters
    ----------
    N : float
        Approximate number of points along the shorter side of the grid.
    limx : tuple
        The left and right limits of the border along the X dimension.
    limy : tuple
        The left and right limits of the border along the Y dimension.

    Returns
    -------
    (Nx, Ny) : tuple of ints
        The number of points along the X and Y dimension, respectively.
    '''
    dx = (limx[1]-limx[0]) / (limy[1]-limy[0])
    Nx, Ny = int(round(N * max(dx, 1))), int(round(N * max(1/dx, 1)))
    return Nx, Ny


#######
#
#    NEWTON-RAPHSON FRACTAL COLORING
#
##########################################################################

def closest_roots(P, X):
    '''
    Find the index of the closes root of a polynomial to a given X
    value(s).
    '''
    return np.argmin([np.abs(X - p) for p in P.roots()], axis=0)

def nr_colors(P, X, cmap=cm.viridis):
    '''
    Generate a list of color values sampled from a colormap for a given
    X value(s).

    Parameters
    ----------
    P : newton.polynomial.Polynomial
        A polynomial instance to get roots from.
    X : float or array-like
        A value or an array of values to get color values for.
    cmap : Callable or `~matplotlib.colors.Colormap`, default 'viridis'
        A colormap instance to sample values from or a function to get
        color values from.

    Returns
    -------
    list
        A list of RGBA color values sampled from a given colormap, each
        corresponding to the element(s) in the input X.
    '''
    return cmap((r:=closest_roots(P, X))/max(r))


#######
#
#    OTHER FUNCTIONS
#
##########################################################################

def NR_missing_grid_lim(P):

    roots = P.roots()
    lim = np.max((np.abs(roots.real), np.abs(roots.imag))) * 1.15

    return tuple((-lim, lim))

def NR_fractal_get_frames(gl_s, gl_e, n=50):

    v_s = np.array(list(product(*gl_s)))
    v_e = np.array(list(product(*gl_e)))

    v_coords = np.linspace(v_s, v_e, n)

    return v_coords

def NR_fractal_get_grid_lims(v_coords):
    # Shorten variable names
    v1, v2 = v_coords[:,0], v_coords[:,3]

    grid_lims =\
    tuple(
        tuple(
            ((xmin, xmax), (ymin, ymax))
        )
        for xmin, xmax, ymin, ymax in zip(v1[:,0], v2[:,0], v1[:,1], v2[:,1])
    )

    return grid_lims