import numpy as np

import matplotlib.cm as cm
import matplotlib.pyplot as plt

from ..newton import *
from .._util import NR_coord_axis, NR_roots


#
# 0. Demo function with real roots
#
# P = Polynomial(coeff=[2, 5, -14, -2])

def get_tangent_line(P, x):
    '''
    Returns the (m, b) parameters of the tangent line to a polynomial
    at a given x value.

    Parameters
    ----------
    P : newton.polynomial.Polynomial
    x : float
    '''
    return P.evald(x, 1), P.eval(x) - P.evald(x, 1)*x

#
# 1. Plot elements
#
def NR_intro_f(ax, P, X, alpha=1.0):
    '''
    TODO

    Parameters
    ----------
    ax : matplotlib.Axes.axis
    P : newton.polynomial.Polynomial
    x : float
    '''
    ax.plot(X, P.eval(X), label=f'${P.f_str()}$',
            color='royalblue', lw=4, alpha=alpha)
    return ax

def NR_intro_fprime(ax, P, X, alpha=0.7):

    ax.plot(X, P.evald(X, 1), label=f'${P.__strd__(1)}$',
            color='tab:orange', lw=4, ls='-.', alpha=alpha)
    return ax

def NR_intro_random_x(ax, P, x, alpha=0.8):

    ax.scatter(x=x,
               y=0,
               label='Arbitrary point',
               color='tab:red', ec='black', s=12**2, alpha=alpha, zorder=3)
    ax.axvline(x, color='tab:red', ls=':', lw=3, alpha=alpha*0.8)
    return ax

def NR_intro_tangent(ax, P, x, x_tg, alpha=0.8):
    # Tangent line
    m, b = get_tangent_line(P, x)
    x_tg = np.linspace(*x_tg, 20)
    ax.plot(x_tg, x_tg*m + b,
            label='Tangent line',
            color='tab:red', lw=4, ls='-', alpha=alpha)
    return ax

def NR_intro_tangent_ic(ax, P, x, alpha=0.8):

    m, b = get_tangent_line(P, x)
    # Where tangent intercept X-axis: x = -b/m
    ax.axvline(-b/m, color='black', ls='--', lw=3, alpha=alpha)
    return ax

def NR_intro_new_x(ax, P, x, alpha=0.8):

    m, b = get_tangent_line(P, x)
    ax.scatter(x=-b/m, y=0,
               label='New starting point',
               color='gold', ec='black', s=12**2, alpha=alpha, zorder=3)
    return ax

def NR_intro_arrow(ax, P, x, alpha):

    m, b = get_tangent_line(P, x)
    x_s, x_e = x, -b/m
    l = x_e - x_s
    arrow_s = x_s+l/8
    arrow_e = l-3*l/8

    ax.arrow(x=arrow_s, y=0,
             dx=arrow_e, dy=0,
             lw=8, head_width=1.0, head_length=0.06,
             length_includes_head=True)
    return ax


#
# 2. Construct individual axes
#
def NR_real_ax_1(ax, P, x):

    ax = NR_coord_axis(ax, alpha=0.5)

    ax = NR_intro_f(ax, P, x, alpha=1.0)
    ax = NR_intro_fprime(ax, P, x, alpha=0.7)
    ax, _ = NR_roots(ax, P,
                         alpha=0.8)

    ax.set_xlim(x[0]-(x[-1]-x[0])/6, x[-1]+(x[-1]-x[0])/6)

    ax.set_title('a) Where are the roots of this polynomial?',
                 fontsize=20, fontweight='bold')
    ax.tick_params(axis='both', which='major', labelsize=15)

    ax.legend(loc='upper left', fontsize=16)
    return ax

def NR_real_ax_2(ax, P, x):

    ax = NR_coord_axis(ax, alpha=0.5)

    ax = NR_intro_f(ax, P, x, alpha=1.0)
    ax = NR_intro_fprime(ax, P, x, alpha=0.3)
    ax, _ = NR_roots(ax, P, alpha=0.8)
    ax = NR_intro_random_x(ax, P,
                           x=2.8,
                           alpha=0.8)
    ax = NR_intro_tangent(ax, P,
                        x=2.8,
                        x_tg=(2,3.15),
                        alpha=0.8)

    ax.set_xlim(x[0], x[-1]+(x[-1]-x[0])/6)
    ax.set_ylabel('$\Downarrow$', fontsize=60)

    ax.set_title('b) Select an arbitrary point and\ndraw a tangent line to the function',
                 fontsize=20, fontweight='bold')
    ax.tick_params(axis='both', which='major', labelsize=15)

    ax.legend(loc='upper left', ncol=2, fontsize=16)
    return ax

def NR_real_ax_3(ax, P, x):

    ax = NR_coord_axis(ax, alpha=0.9)

    ax = NR_intro_f(ax, P, x, alpha=0.3)
    ax = NR_intro_fprime(ax, P, x, alpha=0.3)
    ax, _ = NR_roots(ax, P, alpha=0.3)
    ax = NR_intro_random_x(ax, P,
                           x=2.8,
                           alpha=0.3)
    ax = NR_intro_tangent(ax, P,
                          x=2.8,
                          x_tg=(2,3.15),
                          alpha=0.8)
    ax = NR_intro_tangent_ic(ax, P, x=2.8, alpha=0.8)

    ax.set_xlim(x[0], x[-1]+(x[-1]-x[0])/6)

    ax.set_title('c) Where does the tangent line intersect\nthe x-axis?',
               fontsize=20, fontweight='bold')
    ax.tick_params(axis='both', which='major', labelsize=15)

    ax.legend(loc='upper left', ncol=2, fontsize=16)
    return ax

def NR_real_ax_4(ax, P, x):

    ax = NR_coord_axis(ax, alpha=0.3)

    ax = NR_intro_f(ax, P, x, alpha=0.3)
    ax = NR_intro_fprime(ax, P, x, alpha=0.3)
    ax, _ = NR_roots(ax, P, alpha=0.3)
    ax = NR_intro_random_x(ax, P,
                           x=2.8,
                           alpha=0.3)
    ax = NR_intro_tangent(ax, P,
                          x=2.8,
                          x_tg=(2, 3.15),
                          alpha=0.3)
    ax = NR_intro_tangent_ic(ax, P, x=2.8, alpha=0.8)
    ax = NR_intro_new_x(ax, P, x=2.8, alpha=1.0)
    ax = NR_intro_arrow(ax, P, x=2.8, alpha=0.9)

    ax.set_xlim(x[0], x[-1]+(x[-1]-x[0])/6)
    ax.set_ylabel('$\Downarrow$', fontsize=60)

    ax.set_title('d) The input of the next step of the\niteration is the new starting point',
                 fontsize=20, fontweight='bold')
    ax.tick_params(axis='both', which='major', labelsize=15)

    ax.legend(loc='upper left', ncol=2, fontsize=16)
    return ax


#
# 3. Build intro plot
#
def NR_real(P):

    nr, nc = 2, 2
    fig, axes = plt.subplots(nr, nc, figsize=(10*nc, 10*nr), facecolor='0.96')
    axes = axes.flatten()

    _ = NR_real_ax_1(axes[0], P, x=np.linspace(-5,3,100))
    _ = NR_real_ax_2(axes[1], P, x=np.linspace(0,3,100))
    _ = NR_real_ax_3(axes[2], P, x=np.linspace(0,3,100))
    _ = NR_real_ax_4(axes[3], P, x=np.linspace(0,3,100))

    fig.suptitle('Fig. 3. Operation of the Newton$-$Raphson method ' +
                 'for real functions',
                 fontsize=20, fontweight='bold', y=0.09)
    plt.show()