import numpy as np
import matplotlib.pyplot as plt
from NAFF import *

t = np.arange(0.0,1000.0,1)
data = []
for i in range (len(t)):
  data.append(40.0*np.cos(2*np.pi*0.31*t[i]))

coord = Vec_cpp()
zero  = Vec_cpp()
coord.extend(i for i in data)
zero.extend((0)*i for i in data)
naff = NAFF()
naff.fmax=1
naff.set_window_parameter(0, 'n')
naff.set_interpolation(True)
naff.set_upsampling(True, 'spline')
tune_all=naff.get_f(coord,zero)
counter = 0
for i in tune_all:
  counter += 1
  print "Frequency [",counter,"]= ",i


