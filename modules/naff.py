from NAFF import *
import numpy as np
import time
from decimal import *
import math


def naff(data, coord, coord_prime=0, second_half =False):
  tunes=[]
  n_particles = len(data[0].x)
  t0 = time.clock()
  for i in range (n_particles):
    print "Particle ",i
    naff = NAFF()
    naff.fmax = 1
    naff.set_window_parameter(1,'h')
    tune=naff.get_f1(coord(data,i),coord_prime(data,i))
    for j in (tune):
      if ((second_half == True)):
        j = 1-j
      print j, "python"  
      print 'NAFF for particle %i and for %i turns : %f' %(i+1,len(data), j)
      tunes.append(j)
      
  print time.clock() - t0, "seconds for NAFF"
  return tunes


#from NAFF import *
#import numpy as np
##from multiprocessing import Pool
##from multiprocessing.dummy import Pool as ThreadPool
#def naff(data, coord, coord_prime=0, second_half =False):
#  tunes=[]
#  n_particles = len(data[0].x)
#  for i in range (n_particles):
#    tune=NAFF_f1(coord(data,i),coord_prime(data,i))
#    #tune=NAFF.get_f1(coord(data,i),coord_prime(data,i))
#    if (second_half == True):
#      tune = 1-tune
#    print 'NAFF for particle %i and for %i turns : %f' %(i+1,len(data), tune)
#    tunes.append(tune)
#  return tunes

#def naff(data, coord, coord_prime=0, second_half =False):
#  tunes=[]
#  n_particles = len(data[0].x)
#  for i in range (n_particles):
#    tune=NAFF_f1(coord(data,i),coord_prime(data,i))
#    if (second_half == True):
#      tune = 1-tune
#    print 'NAFF for particle %i and for %i turns : %f' %(i+1,len(data), tune)
#    tunes.append(tune)
#  return tunes


