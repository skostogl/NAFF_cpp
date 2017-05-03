import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pylab import *

from NAFF import *
from modules.exp_fit import *

data = []
data2 = []
f = open('LHC_Data','r')
for line in f:
    parts=line.split()
    data.append(float(parts[0]))
x = np.arange(len(data))
x,data2 = exp_fit(x,data)

tunes = []
turns = []
for p in xrange(6, 500, 6):
  min_value = 0
  max_value = p+1
  coord = Vec_cpp()
  zero = Vec_cpp()
  coord.extend(j for j in data2[min_value:max_value])
  zero.extend(0*j for j in data2[min_value:max_value])
  naff = NAFF()
  naff.set_window_parameter(1,'h')
  naff.set_interpolation(True)
  naff.set_upsampling(True,'spline')
  #naff.set_merit_function("minimize_RMS_frequency")
  tune=(naff.get_f1(coord,zero))
  for k in tune:
    print "Tune: ", k,"Turns: ", p
    tunes.append(k)
    turns.append(p)   
    fig = plt.figure(0)
plt.plot(turns,tunes,marker='o',ms=3,color='k',linestyle='-')
plt.xlabel(r'Turns', fontsize=20)
plt.ylabel(r'Tune from NAFF', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.show()
