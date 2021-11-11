import os
import sys
import numpy as np
from tqdm import tqdm
from joblib import Parallel, delayed

import matplotlib.pyplot as plt

from polynomial import Polynomial

from newton_engine import (get_NR_colors,
                           NR_fractal_get_frames,
                           NR_fractal_get_grid_lims)
from newton_plots import NR_fractal_mx

def create_frame(i, P,
                 N, n_steps, gl,
                 outdir, ffmt, fdpi):
  X_n, _, _, _= NR_fractal_mx(P,
                              N=N, n_steps=n_steps,
                              grid_lim_x=gl[0],
                              grid_lim_y=gl[1])
  X = get_NR_colors(P, X_n).reshape((N, N, 4))

  fname = 'nrfractal_anim_frame-{:04d}.'.format(i)
  plt.imsave(fname=(outdir + fname + ffmt),
             arr=X, vmin=0, vmax=1,
             dpi=fdpi)

if __name__ == '__main__':
  
  assert len(sys.argv) == 5, 'USAGE: python newton_anim.py <N> <n_steps> <n_frames> <n_jobs>'
  
  N = int(sys.argv[1])
  n_steps = int(sys.argv[2])
  n_frames = int(sys.argv[3])
  n_jobs = int(sys.argv[4])
  ffmt = 'png'
  fdpi = 100
  
  outdir = './out/frames-N{}-ns{}/'.format(N, n_steps)
  if not os.path.exists(outdir):
      os.makedirs(outdir)
  
  P = Polynomial(c=[1,0,0,1,-1,1])
  
  # Predefined limits
  gl_s = ((-1.5,1.5),(-1.5,1.5))
  gl_e = ((-1.0092734515,-1.0092734495), (0.1473217440, 0.1473217460))
  
  v_coords = NR_fractal_get_frames(gl_s, gl_e, n_frames=n_frames)
  grid_lims = NR_fractal_get_grid_lims(v_coords)
  del v_coords
  
  _ = Parallel(n_jobs=n_jobs)(delayed(create_frame)(i, P,
                                                    N, n_steps, gl,
                                                    outdir, ffmt, fdpi) for i, gl in enumerate(tqdm(grid_lims)))
