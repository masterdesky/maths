import os
import numpy as np
from itertools import product

import seaborn as sns
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from sklearn.datasets import make_regression
from sklearn.preprocessing import MinMaxScaler

#######
#
#    NEWTON-RAPHSON METHOD IMPLEMENTATION
#
##########################################################################

def NR_step(P, z):
  return z - P.f(z)/P.fprime(z)

def NR_close(R, Y, eps=1e-06):
  
  C = np.array([np.abs(Y - r) < eps for r in R])
  
  return np.logical_or.reduce(C)

def NR_iter(P, z, n_steps):
  assert type(n_steps) is int, 'N should be a positive integer!'
  assert n_steps > 0, 'N should be at least 1!'
  
  Y = z.copy()
  R = P.roots()
  C = np.zeros_like(Y).real
  
  for i in range(n_steps):
    Y = NR_step(P, Y)
    C += NR_close(R, Y)
  return Y, C



#######
#
#    FUNCTIONS TO ANALYZE WITH THE NEWTON-RAPHSON METHOD
#
##########################################################################

# Demo function with real roots
def demo_f(x):
  return 2*x**3 + 5*x**2 - 14*x - 2
def demo_fprime(x):
  return 6*x**2 + 10*x - 14

# Demo function with real and complex roots
def demo_fz(z):
  return z**5 + z**2 - z + 1
def demo_fzprime(z):
  return 5*z**4 + 2*z - 1



#######
#
#    NEWTON-FRACTAL INTRODUCTION
#
##########################################################################

def get_starting_grid(N, grid_lim_x, grid_lim_y):

  X = np.meshgrid(np.linspace(*grid_lim_x, N), np.linspace(*grid_lim_y, N))
  X = X[0].flatten() + X[1].flatten()*1j
  
  return X



#######
#
#    NEWTON-FRACTAL COLORING
#
##########################################################################
  
def closest_roots(X, roots):
  
  a = np.array([roots - x for x in X])
  closest = np.array(
    [np.argmin(np.abs(i)) for i in a]
  )
  return closest

def get_cmap():  
  return sns.color_palette("ch:s=-.2,r=.6", as_cmap=True)
  #return sns.color_palette("ch:start=-0.2,rot=-0.1", as_cmap=True)
  #return cm.bone
  
def get_NR_colors(P, X):
  
  # Get roots of the polynomial
  roots = P.roots()
  # Find closest root to each grid points
  closest = closest_roots(X, roots)

  # Get colors according to closest root
  cmap = get_cmap()
  colors = cmap(closest_roots(X, roots)/(len(P.coeff_())-1))

  return colors

def get_NR_brightness(C):
  
  C /= 4*np.max(C)
  C += 0.0

  return np.c_[(np.zeros((C.size,3)), C)]

#######
#
#    OTHER FUNCTIONS
#
##########################################################################

def NR_missing_grid_lim(P):
  
  # Get roots of the polynomial
  roots = P.roots()
  
  lim = np.max((np.abs(roots.real), np.abs(roots.imag))) * 1.15
  
  return tuple((-lim, lim))

def NR_fractal_get_frames(gl_s, gl_e, n_frames=50):
  
  v_s = np.array(list(product(*gl_s)))
  v_e = np.array(list(product(*gl_e)))

  sg = np.sign(v_s - v_e)
  f_s = v_s - v_e
  f_e = np.zeros_like(v_s) + 1e-15 * sg

  v_coords = np.geomspace(f_s, f_e, n_frames) + v_e
  
  return v_coords

def NR_fractal_get_grid_lims(v_coords):
  
  # Shorten variable names
  v1, v2 = v_coords[:,0], v_coords[:,3]
  
  grid_lims =\
  tuple(
    tuple(
      ( (xmin, xmax),(ymin, ymax) )
    )
    for xmin, xmax, ymin, ymax in zip(v1[:,0], v2[:,0], v1[:,1], v2[:,1])
  )
  
  return grid_lims

def NR_fractal_get_grid_lims(v_coords):
  
  # Shorten variable names
  v1, v2 = v_coords[:,0], v_coords[:,3]
  
  grid_lims =\
  tuple(
    tuple(
      ( (xmin, xmax),(ymin, ymax) )
    )
    for xmin, xmax, ymin, ymax in zip(v1[:,0], v2[:,0], v1[:,1], v2[:,1])
  )
  
  return grid_lims