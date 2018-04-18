import math
import itertools
import numpy as np
from itertools import product
import matplotlib.pyplot as plt
from matplotlib import collections as mc
from tune_resonances import *
import pylab

def cmp_index_segment(n_particles_x, n_particles_y):
  n_particles=int (n_particles_x * n_particles_y)
  indexes = []
  index_list  = []
  index_list_unq = []
  for index in range (n_particles):
    indexes=[ item for item in (index-1, index-n_particles_y, index+n_particles_y, index+1 ) if item >=0 and item < n_particles ]
    if  ( (index+1)%(n_particles_y) == 0):
      del indexes[-1:]
    elif ( index%(n_particles_y) == 0):
      del indexes[0]
    index_list.extend( list(product([index], indexes)) )
  index_list = [ sorted(item) for item in (index_list) ]
  index_list.sort()
  index_list_unq = list(index_list for index_list ,_ in itertools.groupby(index_list))
  return index_list_unq

def create_plot(data_x, data_y,index_list=0, diff_tunes=0, colorbar=False,resonance_diagram=False,order=0 ):
  segment=[]
  fig,ax=plt.subplots()
  if (index_list == 0):    
    if (colorbar == False):  
      for i in range (len(data_x)):  
        plt.plot(data_x[i], data_y[i], marker='o',ms=3, alpha=1, color='b')
  else:
    for element in index_list:
      segment.append( [ ( data_x[element[0]],data_y[element[0]] ) , ( data_x[element[1]],data_y[element[1]] ) ])
    lc = mc.LineCollection(segment, colors='navy', linewidths=1)
    ax.add_collection(lc)
    plt.plot()
  if (colorbar == True and diff_tunes != 0):
    x = data_x
    y = data_y
    z = diff_tunes
    #cax = plt.scatter(x, y, edgecolors='none', s=15, c=np.log10(z), cmap=plt.get_cmap("cubehelix"))
    #cax = plt.scatter(x, y, edgecolors='none', s=15, c=np.log10(z), cmap=plt.get_cmap("CMRmap"))
    cax = plt.scatter(x, y, edgecolors='none', s=15, c=np.log10(z))
    #cax = plt.scatter(x, y, edgecolors='none', s=15, c=np.log10(z), cmap=plt.get_cmap("gist_stern"))
    #cax = plt.scatter(x, y, edgecolors='none', s=15, c=np.log10(z), cmap=plt.get_cmap("brg"))
    cb =plt.colorbar(cax)
    cb.set_label(r'$log\sqrt{\Delta Q^2_x + \Delta Q^2_y}$', fontsize=25)
    cb.ax.tick_params(labelsize=20)
    plt.plot()
  if (resonance_diagram == True):
    if (order==0):
      print "Maximum order of resonance_diagram not defined!!"
    else:
      qx = np.sum(data_x)/len(data_x)
      qy = np.sum(data_y)/len(data_y)
      make_resonance_diagram(order, [0,1], [0,1])
      plt.plot()
  plt.axis('equal')
  return fig, ax


def cmp_grid(sigma_x_init, sigma_x_final, sigma_y_init, sigma_y_final, step,sigma_x, sigma_y, bunch): 
  n_particles_x =  int(round((sigma_x_final-sigma_x_init )/(step*sigma_x)))
  print sigma_y_init, sigma_y, sigma_y_init/sigma_y
  if (sigma_x_init+n_particles_x*step*sigma_x+step*sigma_x<sigma_x_final):
      n_particles_x=n_particles_x+1
  #n_particles_x =  int(round((sigma_x_final)/(step*sigma_x_init)))
  #n_particles_x = int (round(sigma_x_final/(sigma_x_init*step)))
  n_particles_y=n_particles_x

  n_particles   = int (n_particles_x * n_particles_y)
  b = bunch
  particle = 0
  #for i in range (1,n_particles_x+1):
  #  for j in range (1,n_particles_y+1):
  for i in range (n_particles_x):
    for j in range (n_particles_y):
      #b.x [particle] =  i*step*sigma_x_init
      #b.y [particle] =  j*step*sigma_y_init
      b.x [particle] = sigma_x_init+ i*step*sigma_x
      b.y [particle] = sigma_y_init+ j*step*sigma_y
      if ((j==0) and (i==0)):
          print b.x[particle]/sigma_x, b.y[particle]/sigma_y, sigma_x, sigma_y, sigma_x_init/sigma_x, sigma_y_init/sigma_y
      particle = particle + 1
  segment_indexes=cmp_index_segment(n_particles_x, n_particles_y)
  return b, segment_indexes

def cmp_polar_grid(sigma_x_init, sigma_x_final, sigma_y_init, sigma_y_final, step,bunch): 
  n_particles_x =  int(round((sigma_x_final-sigma_x_init)/(step*sigma_x)))
  print n_particles_x
  if (sigma_x_init+n_particles_x*step*sigma_x+step*bunch.sigma_x()<=sigma_x_final):
      n_particles_x=n_particles_x+1
  #n_particles_y=n_particles_x
  n_particles_y =  int(round((sigma_y_final-sigma_y_init)/(step*sigma_y)))

  n_particles   = int (n_particles_x * n_particles_y)
  b = HostBunch(n_particles)
  particle_count = 0
  
  r_a = sigma_x_init
  r_b = sigma_x_init+ n_particles_x*step*sigma_x

  r_a2 = sigma_y_init
  r_b2 = sigma_y_init+ n_particles_y*step*sigma_y
  
  circles = n_particles_x
  lines   = n_particles_x
  origin = (0, 0)
  r,t   = np.meshgrid(np.linspace(r_a, r_b, circles),np.linspace(0,  np.pi/2, lines))
  r2,t2   = np.meshgrid(np.linspace(r_a2, r_b2, circles),np.linspace(0,  np.pi/2, lines))
  x = r * np.cos(t)
  y = r2 * np.sin(t2)
  for i in range (n_particles_x):
    for j in range (n_particles_y):
      b.x[particle_count] = x[i][j]
      b.y[particle_count]  = y[i][j]
      particle_count = particle_count + 1 
  #pylab.plot(x, y, c='k')
  pylab.plot(x,y,c='k')
  pylab.plot(np.vstack((x[:,0], x[:, -1])),np.vstack((y[:,0], y[:, -1])), c='k')
  pylab.axis('scaled')
  pylab.show()
  return b

