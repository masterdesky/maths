import numpy as np

import seaborn as sns
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from ..newton import *
from .._util import NR_coord_axis, NR_roots, NR_complex_fig_setup


#
# 0. Demo function with real and complex roots
#
# P = Polynomial(coeff=[1, 0, 0, 1, -1, 1])


#
# 1. An example polynomial with both real and complex roots
#
def NR_complex_ax1(ax, P, x):

    ax = NR_coord_axis(ax, alpha=0.5)
    ax.plot(x, P.f(x), label='${}$'.format(P.f_str()),
            color='royalblue', lw=4)
    ax.plot(x, P.fprime(x), label='${}$'.format(P.fprime_str()),
            color='tab:orange', lw=4, ls='-.', alpha=0.7)

    ax.set_xlabel('X', fontsize=25, fontweight='bold')
    ax.set_ylabel('Y', fontsize=25, fontweight='bold')

    ax.tick_params(axis='both', which='major', labelsize=15)

    ax.legend(loc='upper center', fontsize=18)
    return ax

def NR_complex_ax2(ax, P, grid_lim):

    ax = NR_coord_axis(ax, alpha=0.5)

    ax, _ = NR_roots(ax, P, alpha=0.8)

    ax.set_xlim(*grid_lim)
    ax.set_ylim(*grid_lim)

    ax.set_xlabel('Real [$\mathfrak{R}$]', fontsize=25, fontweight='bold')
    ax.set_ylabel('Imag [$\mathfrak{I}$]', fontsize=25, fontweight='bold')

    ax.tick_params(axis='both', which='major', labelsize=15)

    ax.legend(loc='upper left', fontsize=18)

    return ax

def NR_complex_example(P,
                       grid_lim=None):

    if grid_lim is None:
        grid_lim = NR_missing_grid_lim(P)

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(2*10, 1*10),
                             facecolor='0.96')
    fig.subplots_adjust(wspace=0.25)

    x = np.linspace(-2, 2, 100)
    _ = NR_complex_ax1(ax=axes[0], P=P, x=x)
    _ = NR_complex_ax2(ax=axes[1], P=P, grid_lim=grid_lim)

    plt.suptitle('Fig. 4. An example polynomial with both real and complex roots',
                 fontsize=20, fontweight='bold', y=0.02)
    plt.show()


#
# 2. Newton-Raphson method on complex roots
#
def NR_complex_annotate(ax, text, xy, xytext, alpha=1.0):

    ax.annotate(text,
                xy=(xy.real, xy.imag), xycoords='data', xytext=xytext,
                fontsize=28, horizontalalignment='right', verticalalignment='top',
                alpha=alpha
               )
    return ax

def NR_complex_points(ax, P, x, idx=0, alpha=1.0):

    ax.scatter(x.real, x.imag,
               color='tab:red', s=12**2, alpha=alpha)
    ax.scatter(P.f(x).real, P.f(x).imag,
               color='mediumorchid', s=12**2, alpha=alpha)

    ax = NR_complex_annotate(ax=ax,
                             text=f'$z_{{{idx}}}$',
                             xy=x,
                             xytext=(x.real, x.imag),
                             alpha=alpha)
    ax = NR_complex_annotate(ax=ax,
                             text=f'$\mathcal{{P}} \\left( z_{{{idx}}} \\right)$',
                             xy=x,
                             xytext=(P.f(x).real, P.f(x).imag),
                             alpha=alpha)
    return ax

def NR_complex_method_ax(ax, P, x_0, idx=1, alpha=1.0, title=None):

    if idx <= 0:
        idx_old = idx
        alpha_old = 1.0
    else:
        idx_old = idx - 1
        alpha_old = 0.2

    ax = NR_complex_points(ax, P, x_0, idx=idx_old, alpha=alpha_old)

    ax.set_title(title, fontsize=20, fontweight='bold')

    if idx <= 0:
        return ax

    x_1 = NR_step(P, x_0)
    ax = NR_complex_points(ax, P, x_1, idx=idx, alpha=alpha)

    # Draw arrow between old z_{n-1} and new z_{n} points
    l = x_1 - x_0
    arrow_s = x_0+l/10
    arrow_e = l-3*l/10
    ax.arrow(arrow_s.real, arrow_s.imag,
             arrow_e.real, arrow_e.imag,
             lw=3, width=0.01)
    # Draw arrow between old P(z_{n-1}) and new P(z_{n}) points
    l = P.f(x_1) - P.f(x_0)
    arrow_s = P.f(x_0)+l/10
    arrow_e = l-2.5*l/10
    ax.arrow(arrow_s.real, arrow_s.imag,
             arrow_e.real, arrow_e.imag,
             lw=3, width=0.01)
    return ax, x_1

def NR_complex_method(P, x_0=(0.47+0.56j), grid_lim=None):

    if grid_lim is None:
        grid_lim = NR_missing_grid_lim(P)

    nr, nc = 2, 2
    fig, axes = NR_complex_fig_setup(nr, nc, grid_lim=grid_lim, axis=True)

    for i, ax in enumerate(axes):
        alpha = 0.8 if i == 0 else 0.3
        ax, _ = NR_roots(ax, P, alpha=alpha)

    title = "Step 0: Select an arbitrary point ($\mathbf{z_{0}}$) and the\n" + \
            "corresponding function value ($\mathbf{P \\left( z_{0} \\right)}$)"
    _ = NR_complex_method_ax(axes[0], P=P, x_0=x_0, idx=0, title=title)

    title = "Step 1: Iterate the starting point using the\nNR method: " + \
            "$\mathbf{z_{n+1} = z_{n} - P \\left( z_{n} \\right) / P\,\' \\left( z_{n} \\right)}$"
    _, x_1 = NR_complex_method_ax(axes[1], P=P, x_0=x_0, idx=1, title=title)

    title = "Step $\\mathbf{2 \\to N}$: Repeat the iterative step\nmultiple times"
    _, x_2 = NR_complex_method_ax(axes[2], P=P, x_0=x_1, idx=2, title=title)

    title = "Step $\\mathbf{N + 1}$: Iterate until the method converges\nto an arbitrary root"
    _, x_3 = NR_complex_method_ax(axes[3], P=P, x_0=x_2, idx=3, title=title)

    fig.suptitle('Fig. 5. Operation of the Newton$-$Raphson method ' +
                 'for complex functions',
                 fontsize=20, fontweight='bold', y=0.07)
    plt.show()