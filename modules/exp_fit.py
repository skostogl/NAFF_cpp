import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from scipy.signal import hilbert, chirp
from matplotlib import rc
from matplotlib.ticker import MultipleLocator
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
from matplotlib.ticker import MultipleLocator

def exp_fit (x,y):
  x = np.array(x, dtype=float) 
  y = np.array(y, dtype=float)

  analytic_signal = hilbert(y)
  amplitude_envelope = np.abs(analytic_signal)
  amplitude_envelope2 = -np.abs(analytic_signal)

  def func(x, a, c, d):
      return a*np.exp(-c*x)+d

  def func2(x, a, c, d):
      return a*np.exp(c*x)+d

  popt, pcov = curve_fit(func, x, amplitude_envelope, p0=(1,1e-6,1))
  popt2, pcov = curve_fit(func2, x, amplitude_envelope2, p0=(1,1e-6,1))

  #print "TOP envelope: a = %s , c = %s, d = %s" % (popt[0], popt[1], popt[2])
  #print "Bottom envelope: a = %s , c = %s, d = %s" % (popt2[0], popt2[1], popt2[2])
  a = max(y)
  b = min(y)
  fig,(ax1,ax2) = plt.subplots(2,1, sharex=True)
  ax1.plot(x,y, lw=0.5, linestyle='-', color='gray', label = 'Initial data')
  ax1.plot(x,func(x, popt[0], popt[1], popt[2]), lw=3, linestyle='-', color='r', label = 'Exponential fit')
  ax1.plot(x,func2(x, popt2[0], popt2[1], popt2[2]), lw=3, linestyle='-', color='r')

  f0 =popt[0]+popt[2]
  for i in range (len(x)):
    fi =popt[0]*np.exp(-popt[1]*i)+popt[2]
    y[i] *= f0/fi
  ax2.plot(x,y, lw=0.5, linestyle='-', color='gray', label = 'Final data')


  ax1.set_title(r'Initial Signal', fontweight='bold', fontsize=18)
  ax1.set_xlabel(r'N', fontweight='bold', fontsize=14)
  ax1.set_ylabel(r'Amplitude', fontweight='bold', fontsize=14)
  ax2.set_xlabel(r'N', fontweight='bold', fontsize=14)
  ax2.set_title(r'Fitted Signal', fontweight='bold', fontsize=18)
  ax2.set_ylabel(r'Amplitude', fontweight='bold', fontsize=14)
  fig.tight_layout()
  ax1.legend(loc = 1,fontsize=14)
  ax2.legend(loc = 1,fontsize=14)
  #ax1.set_xlim([50,100])
  #plt.show()
  return x,y


