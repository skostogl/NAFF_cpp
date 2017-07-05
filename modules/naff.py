from NAFF import *
import numpy as np
import time
from decimal import *
import math


def naff(data_x, data_xp = [0], remove_coupling = False, flag_frequency_interval = False, min_freq = 0, max_freq = 1,second_half =False):
  zero  = Vec_cpp()
  coord = Vec_cpp()
  coord.extend(i for i in data_x)
  zero.extend(i for i in data_xp)
  naff = NAFF()
  naff.set_window_parameter(1, 'h')
  #naff.set_window_parameter(0, 'n')
  if (flag_frequency_interval==True):
    naff.set_frequency_interval(min_freq,max_freq)
  naff.fmax = 1
  tune_all=naff.get_f1(coord,zero)
  print len(data_x), len(data_xp), "here!"
  for tune in tune_all:
    if (second_half == True):
      tune = 1-tune
  amplitudes = naff.return_amplitudes()
  #if (remove_coupling == True):
  #  amplitudes = naff.return_amplitudes()
  #  for kp in range (len(amplitudes)):
  #    print amplitudes[kp], tune_all[kp],'python'
  #  return tune_all, amplitudes
  #else:
  #  return tune_all
  return tune_all, amplitudes

    

