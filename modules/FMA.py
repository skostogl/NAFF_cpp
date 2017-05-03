from naff import *
from  modules.tracker import *
import numpy as np

def FMA (data1, data2, second_half_x=False, second_half_y= False):
  tunes_x1 = naff(data1, vec_HostBunch.x, vec_HostBunch.xp, second_half_x)
  tunes_y1 = naff(data1, vec_HostBunch.y, vec_HostBunch.yp, second_half_y)
  tunes_x2 = naff(data2, vec_HostBunch.x, vec_HostBunch.xp, second_half_x)
  tunes_y2 = naff(data2, vec_HostBunch.y, vec_HostBunch.yp, second_half_y)
  tune_diff_x = [i-j for i,j in zip(tunes_x1, tunes_x2)]
  tune_diff_y = [a-b for a,b in zip(tunes_y1, tunes_y2)]
  tune_diff_x2 = [a**2 for a in tune_diff_x]
  tune_diff_y2 = [b**2 for b in tune_diff_y]
  tune_diffusion = [i+j for i,j in zip(tune_diff_x2, tune_diff_y2)]
  tune_diffusion_sqrt = [np.sqrt(a) for a in tune_diffusion]
  return tunes_x1, tunes_y1, tunes_x2, tunes_y2, tune_diffusion_sqrt

