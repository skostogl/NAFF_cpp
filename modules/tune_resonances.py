import numpy as np
from fractions import gcd
import matplotlib.pyplot as plt


def make_resonance_diagram(order,x_range=[0,1],y_range=[0,1]):
  coeff_x = np.arange(-order, order, dtype = "float" )
  coeff_y = np.arange(-order, order, dtype = "float" )
  c = np.arange(-order, order, dtype = "float" )
  x_range = np.array(x_range)
  xmin = x_range[0]
  xmax = x_range[1]
  y_range = np.array(y_range)
  ymin = y_range[0]
  ymax = y_range[1]
  lines = {}
  vertical_lines = {}
  n_lines=0
  for a in coeff_x: #Bulding a*x+b*y=i with abs(a)<order, abs(b)<order, abs(i)<order and abs(a)+abs(b)<=order
    for b in coeff_y:
      for i in c:
        current_order = abs(a)+ abs(b)
        if (current_order<=order):
          n_lines = n_lines + 1
          if (b!=0): 
            max_Y = (i-a*xmin)/b
            min_Y = (i-a*xmax)/b
            if (ymin <= max_Y and ymax >= min_Y) or (ymax >= max_Y and ymin <= min_Y):
              cmp_gcd =gcd (abs(i),abs(a))

              if (max_Y in lines):
                if (min_Y in lines[max_Y]) and (lines[max_Y][min_Y]["order"]<current_order): #Already exists, update order
                  lines[max_Y][min_Y]={"order": current_order, "label":"%d x+ %d y=%d" %(a,b,i) }
                else:
                  lines[max_Y][min_Y]={"order": current_order, "label":"%d x+ %d y=%d" %(a,b,i)} 
              else:
                lines[max_Y]={} 
                lines[max_Y][min_Y]={"order":current_order,"label":"%d x+ %d y=%d" %(a,b,i)}
          elif a!=0 and b==0: # x=i/a
            const_term = 1.0 *i/a
            if xmin<=const_term<=xmax: # xmin<=x<=xmax
              cmp_gcd = gcd(abs(i),abs(a))
              if (const_term) in vertical_lines:
                const_term_order = vertical_lines[const_term]["order"]
                if const_term_order > current_order:
                  vertical_lines[const_term]={"order":max(const_term_order,order),"label":"x=%d/%d" %(i,a)}
                else:
                  vertical_lines[const_term]={"order": current_order,"label":"x=%d/%d" %(i,a) }
              else:
                  vertical_lines[const_term]={}
                  vertical_lines[const_term]={"order": current_order, "label":"x=%d/%d" %(i,a)}
  for max_Y in lines:
    for min_Y in lines[max_Y]:
        plt.plot(x_range,[max_Y, min_Y], linewidth=1, color="darkgrey")
  for const_term in vertical_lines:
        plt.axvline(const_term, linewidth=1, color="darkgrey")

  #plt.xlim(x_range)
  #plt.ylim(y_range)
  plt.xlim(0.24,0.36)
  plt.ylim(0.26, 0.36)

