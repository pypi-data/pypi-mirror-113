import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from .fit_tools import *

def banana_diagram (freq, psd, back, pkb, n=30, k=30, 
                    figsize=(9,6), shading='auto', marker_color='black',
                    cmap='plasma', contour_color='black', marker='o', 
                    **kwargs) :
  '''
  Compute banana diagram (see Ballot et al 2006) for a given
  set of fitted parameters. Parameters are fixed, except for
  angles and splittings which are set to vary between 0 and
  90 degrees and 0 and 2 muHz, respectively.

  :param freq: frequency vector.
  :type freq: ndarray

  :param psd: psd vector.
  :type psd: ndarray

  :param back: background vector.
  :type back: ndarray

  :param pkb: pkb array that will be used to compute the
    model and the likelihood.
  :type pkb: ndarray

  :param n: number of elements along angle axis. Optional,
     default 30.
  :type n: int

  :param k: number of elements along splittings axis.
    Optional, default 30.
  :type k: int
  '''

  grid = np.zeros ((k, n))
  angles = np.linspace (0, 90, n)
  splittings = np.linspace (0, 2, k)

  if pkb.shape[1]==20 :
    i_width = 8
  else :
    i_width = 6
  cond = (freq>pkb[0,2]-3*pkb[0,i_width])&(freq<pkb[-1,2]+3*pkb[-1,i_width])
  freq = freq[cond]
  psd = psd[cond]
  back = back[cond]
  
  for ii in tqdm (range (n)) :
    for jj in range (k) :
      pkb[:, 11] = angles[ii]
      pkb[:, 14] = splittings[jj]
      model = compute_model (freq, pkb)
      model = model / back
      model += 1
      aux = psd / model + np.log (model)
      log_l = np.sum (aux)
      grid[jj, ii] = log_l

  fig, ax = plt.subplots (figsize=figsize)
  ax.pcolormesh (angles, splittings, -grid, shading=shading, cmap=cmap, **kwargs)
  ax.contour (angles, splittings, -grid, colors=contour_color, **kwargs)
  ax.scatter (angles[np.unravel_index (np.argmin (grid), grid.shape)[1]], 
              splittings[np.unravel_index (np.argmin (grid), grid.shape)[0]], 
              marker=marker, color=marker_color, **kwargs)
  ax.set_ylabel (r'$\nu_s$ ($\mu$Hz)')
  ax.set_xlabel ('$i$ ($^{\circ}$)')

  return fig
