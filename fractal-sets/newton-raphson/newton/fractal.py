import numpy as np

import seaborn as sns
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from .newton import *

from ._util import NR_complex_fig_setup

out = './out/'
figsave_fmt = 'png'
figsave_dpi = 200


def NR_colored_roots(ax, P, alpha=0.8):

  # Get roots
  roots = P.roots()

  # Get different colors for different roots
  cmap = get_cmap()
  colors = cmap(np.linspace(0,1,len(P.coeff_())-1))

  # Plot roots on a real or complex plane
  ax.scatter(x=roots.real,
             y=roots.imag,
             label='Roots',
             c=colors, ec='black', s=15**2, alpha=alpha,
             zorder=3)
  return ax, roots


#
#  Function to display scatter points
#
def NR_fractal_ax(ax, X,
                  P=None, X_c=None):

  if (P is not None) & (X_c is not None):
    colors = get_NR_colors(P, X_c)
  else:
    colors = 'gray'

  ax.scatter(X.real, X.imag,
             c=colors, s=5**2, alpha=0.6)
  return ax


def NR_fractal_steps_gray(P, N=10,
                          steps=[1,3,6,10,15],
                          grid_lim=None):

    if grid_lim is None: grid_lim = NR_missing_grid_lim(P)

    fig, axes = NR_complex_fig_setup(nrows=2, ncols=3,
                                     grid_lim=grid_lim, axis=False)
    for ax in axes:
        ax, _ = NR_colored_roots(ax, P, alpha=0.8)

    # Plot NR steps
    X_0 = get_starting_grid(N, grid_lim, grid_lim)
    _ = NR_fractal_ax(axes[0], X=X_0)

    for i in range(1, len(axes)):
        X_1 = NR_iter(P, X_0, steps[i-1])
        _ = NR_fractal_ax(axes[i], X=X_1)
        X_0 = X_1

    fig.suptitle('Fig. 6. Newton$-$Raphson method on a grid of points',
                 fontsize=20, fontweight='bold', y=0.07)
    plt.show()

def NR_fractal_steps_colored(P, N=10,
                             steps=[1,3,6,10,15],
                             grid_lim=None):

    if grid_lim is None: grid_lim = NR_missing_grid_lim(P)

    fig, axes = NR_complex_fig_setup(nrows=2, ncols=3,
                                     grid_lim=grid_lim, axis=False)
    for ax in axes:
        ax, _ = NR_colored_roots(ax, P, alpha=0.8)

    # Plot NR steps
    X_0 = get_starting_grid(N, grid_lim, grid_lim)
    _ = NR_fractal_ax(axes[0], X=X_0, P=P, X_c=X_0)

    for i in range(1, len(axes)):
        X_1 = NR_iter(P, X_0, steps[i-1])
        _ = NR_fractal_ax(axes[i], X=X_1, P=P, X_c=X_1)
        X_0 = X_1

    fig.suptitle('Fig. 7. Newton$-$Raphson method on a colored grid of points',
                 fontsize=20, fontweight='bold', y=0.07)
    plt.show()

def NR_fractal_steps_reversed(P, N=100,
                              steps=[1,3,6,10,15],
                              grid_lim=None):

    if grid_lim is None: grid_lim = NR_missing_grid_lim(P)

    fig, axes = NR_complex_fig_setup(nrows=2, ncols=3,
                                     grid_lim=grid_lim, axis=False)

    # Plot NR steps with scatter points
    X_0 = get_starting_grid(N, grid_lim, grid_lim)
    ax = NR_fractal_ax(axes[0], X=X_0, P=P, X_c=X_0)

    for i in range(1, len(axes)):
        X_N = NR_iter(P, X_0, steps[i-1])
        ax = NR_fractal_ax(axes[i], X=X_0, P=P, X_c=X_N)

    fig.suptitle('Fig. 8. Newton$-$Raphson fractal on a grid of points',
                 fontsize=20, fontweight='bold', y=0.07)

    plt.show()


def NR_fractal_image_ax(ax, P, X_c,
                        grid_lim_x, grid_lim_y):

    colors = get_NR_colors(P, X_c)
    X = np.array(colors.reshape((int(np.sqrt(len(colors))),
                                 int(np.sqrt(len(colors))),
                                 4
                                ))
                )
    ax.imshow(X, extent=(*grid_lim_x, *grid_lim_y))
    return ax


def NR_fractal_steps_image(P, N=100,
                           steps=[1,3,6,10,15],
                           grid_lim=None):

    if grid_lim is None: grid_lim = NR_missing_grid_lim(P)

    fig, axes = NR_complex_fig_setup(nrows=2, ncols=3,
                                     grid_lim=grid_lim, axis=False)

    # Plot NR steps with scatter points
    X_0 = get_starting_grid(N, grid_lim, grid_lim)
    ax = NR_fractal_image_ax(ax=axes[0], P=P, X_c=X_0,
                             grid_lim_x=grid_lim, grid_lim_y=grid_lim)

    for i in range(1, len(axes)):
        X_N = NR_iter(P, X_0, steps[i-1])
        ax = NR_fractal_image_ax(axes[i], P=P, X_c=X_N,
                                 grid_lim_x=grid_lim, grid_lim_y=grid_lim)

    fig.suptitle('Fig. 9. Newton$-$Raphson factal now on a fine grid',
                 fontsize=20, fontweight='bold', y=0.07)
    plt.show()


def NR_fractal_plot(P, N=512, n_steps=10,
                    grid_lim=None):

    fig, axes = NR_complex_fig_setup(nrows=1, ncols=1,
                                     grid_lim=grid_lim, axis=False)

    X_0 = get_starting_grid(N, grid_lim, grid_lim)
    X_N = NR_iter(P, X_0, n_steps)
    ax = NR_fractal_image_ax(ax=axes[0], P=P, X_c=X_N,
                             grid_lim_x=grid_lim, grid_lim_y=grid_lim)

    fig.suptitle('Fig. 10. A Newton$-$Raphson fractal',
                 fontsize=20, fontweight='bold', y=0.02)
    plt.show()


def NR_fractal(P,
               N=150, n_steps=10, figsize=(10,10),
               grid_lim_x=None,
               grid_lim_y=None,
               axis=True, show=True,
               save=False, savedir='./out/'):

    if grid_lim_x is None: grid_lim_x = NR_missing_grid_lim(P)
    if grid_lim_y is None: grid_lim_y = NR_missing_grid_lim(P)

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    ax.set_aspect('equal')
    if not axis:
        ax.axis('off')

    X_0 = get_starting_grid(N, grid_lim_x, grid_lim_y[::-1])
    X_N = NR_iter(P, X_0, n_steps)
    ax = NR_fractal_image_ax(ax=ax, P=P, X_c=X_N,
                             grid_lim_x=grid_lim_x, grid_lim_y=grid_lim_y)

    gxl, gxr = grid_lim_x
    gyl, gyr = grid_lim_y
    fname = f'nrfractal|N{N}|ns{n_steps}|x{gxl}_{gxr}|y{gyl}_{gyr}.'
    if save:
        os.makedirs(savedir, exist_ok=True)
        plt.savefig(savedir + fname + figsave_fmt,
                    format=figsave_fmt,
                    dpi=figsave_dpi,
                    bbox_inches='tight')

    if show:
        plt.show()
    else:
        plt.clf()
        plt.close('all')