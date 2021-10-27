import os
import numpy as np

import seaborn as sns
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle

from newton_engine import *

outdir = './out/'
ffmt = 'png'
fdpi = 200


#######
#
#    NEWTON-RAPHSON GENERAL-PURPOSE PLOTTING FUNCTIONS
#
##########################################################################

def NR_coord_axis(ax, alpha=0.5):
  
  ax.axhline(0, color='grey', ls='--', lw=3, alpha=alpha)
  ax.axvline(0, color='grey', ls='--', lw=3, alpha=alpha)
  
  return ax



#######
#
#    NEWTON-FRACTAL STEPS FOR 3 DIFFERENT VIEWS
#
##########################################################################

def NR_fractal_mx(P,
                  N=128, n_steps=10,
                  grid_lim_x=None,
                  grid_lim_y=None):
  
  if grid_lim_x is None: grid_lim_x = NR_missing_grid_lim(P)
  if grid_lim_y is None: grid_lim_y = NR_missing_grid_lim(P)
  
  X_0 = get_starting_grid(N, grid_lim_x, grid_lim_y[::-1])
  X_n, C = NR_iter(P, X_0, n_steps)
  
  return X_n, C, grid_lim_x, grid_lim_y


def NR_fractal_image_ax(ax, P,
                        N, X_c, C,
                        grid_lim_x, grid_lim_y):

  X = get_NR_colors(P, X_c).reshape((N, N, 4))
  C = get_NR_brightness(C).reshape((N, N, 4))
  
  ax.imshow(X, extent=(*grid_lim_x, *grid_lim_y))
  ax.imshow(C, extent=(*grid_lim_x, *grid_lim_y))
  
  return ax


def NR_fractal(P,
               N=128, n_steps=10, figsize=(10,10),
               grid_lim_x=None,
               grid_lim_y=None,
               axis=True,
               save=False, outdir='./out/'):
  
  X_n, C, grid_lim_x, grid_lim_y = NR_fractal_mx(P=P,
                                                 N=N, n_steps=n_steps,
                                                 grid_lim_x=grid_lim_x,
                                                 grid_lim_y=grid_lim_y)
  
  fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
  ax.set_aspect('equal')
  if not axis:
    ax.axis('off')
  
  ax = NR_fractal_image_ax(ax=ax, P=P,
                           N=N, X_c=X_n, C=C,
                           grid_lim_x=grid_lim_x, grid_lim_y=grid_lim_y)
  
  fname = 'nrfractal|N{0}|ns{1}|x{2}_{3}|y{4}_{5}.'.format(N, n_steps,
                                                           *grid_lim_x,
                                                           *grid_lim_y)
  if save:
    if not os.path.exists(outdir):
      os.makedirs(outdir)

    plt.savefig(outdir + fname + ffmt,
                format=ffmt,
                dpi=fdpi,
                bbox_inches='tight')
  
  plt.show()