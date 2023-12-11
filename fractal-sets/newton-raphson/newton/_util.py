import numpy as np
import matplotlib.pyplot as plt


def NR_coord_axis(ax, alpha=0.5):

  ax.axhline(0, color='grey', ls='--', lw=3, alpha=alpha)
  ax.axvline(0, color='grey', ls='--', lw=3, alpha=alpha)

  return ax


def NR_roots(ax, P, alpha=0.8):

    # Get roots
    roots = P.roots()

    # Plot roots on a real or complex plane
    ax.scatter(x=roots.real, y=roots.imag, label='Roots',
               color='tab:green', ec='black', s=15**2, alpha=alpha,zorder=3)
    return ax, roots


def NR_complex_fig_setup(nrows, ncols, grid_lim, axis=True):

    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols*10, nrows*10),
                             facecolor='0.96')
    fig.subplots_adjust(wspace=0.15, hspace=0.15)

    if type(axes) is np.ndarray:
        axes = axes.flatten()
    else:
        axes = np.array((axes))

    for i, ax in enumerate(axes):
        ax.set_xlim(grid_lim)
        ax.set_ylim(grid_lim)

        if i+ncols >= len(axes):
            ax.set_xlabel('Real [$\mathfrak{R}$]', fontsize=25, fontweight='bold')
        if i%ncols == 0:
            ax.set_ylabel('Imag [$\mathfrak{I}$]', fontsize=25, fontweight='bold')
        ax.tick_params(axis='both', which='major', labelsize=15)

        if axis:
            ax = NR_coord_axis(ax, alpha=0.5)
    return fig, axes