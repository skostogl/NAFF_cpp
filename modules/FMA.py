from naff import *
import numpy as np

def FMA (data1, data2, remove_coupling=False ,flag_frequency_interval = False, min_freq = 0, max_freq = 1,second_half_x=False, second_half_y= False ):
  data_x = []
  data_xp = []
  data_y = []
  data_yp = []
  for turn in range(len(data1)):
    data_x.append(data1[turn][0])
    data_xp.append(data1[turn][1])
    data_y.append(data1[turn][2])
    data_yp.append(data1[turn][3])
  data_x2 = []
  data_xp2 = []
  data_y2 = []
  data_yp2 = []
  for turn in range(len(data2)):
    data_x2.append(data2[turn][0])
    data_xp2.append(data2[turn][1])
    data_y2.append(data2[turn][2])
    data_yp2.append(data2[turn][3])
  tunes_x1 = naff(data_x, data_xp, remove_coupling, flag_frequency_interval, min_freq, max_freq, second_half_x)
  tunes_y1 = naff(data_y,data_yp, remove_coupling ,flag_frequency_interval, min_freq, max_freq, second_half_y)
  tunes_x2 = naff(data_x2, data_xp2,remove_coupling, flag_frequency_interval, min_freq, max_freq,second_half_x)
  tunes_y2 = naff(data_y2, data_yp2,remove_coupling, flag_frequency_interval, min_freq, max_freq,second_half_y)
  tune_diff_x = [i-j for i,j in zip(tunes_x1, tunes_x2)]
  tune_diff_y = [a-b for a,b in zip(tunes_y1, tunes_y2)]
  tune_diff_x2 = [a**2 for a in tune_diff_x]
  tune_diff_y2 = [b**2 for b in tune_diff_y]
  tune_diffusion = [i+j for i,j in zip(tune_diff_x2, tune_diff_y2)]
  tune_diffusion_sqrt = [np.sqrt(a) for a in tune_diffusion]
  #else:
  #  tunes_x1,amp_x1 = naff(data_x, data_xp, remove_coupling, flag_frequency_interval, min_freq, max_freq, second_half_x)
  #  tunes_y1, amp_y1 = naff(data_y,data_yp, remove_coupling ,flag_frequency_interval, min_freq, max_freq, second_half_y)
  #  tunes_x2,amp_x2 = naff(data_x2, data_xp2,remove_coupling, flag_frequency_interval, min_freq, max_freq,second_half_x)
  #  tunes_y2, amp_y2 = naff(data_y2, data_yp2,remove_coupling, flag_frequency_interval, min_freq, max_freq,second_half_y)
  #  if (amp_y2[1]/amp_y2[0]>0.7 and abs(tunes_y2[0] - tunes_x2[0])<1e-3) or (amp_y1[1]/amp_y1[0]>0.7 and abs(tunes_y1[0] - tunes_x1[0])<1e-3):
  #    print ''
  #    for ik in range (len(tunes_y1)):
  #      print tunes_y1[ik], tunes_y2[ik]
  #    print 'before'
  #    import itertools
  #    all_combinations =list(itertools.product(tunes_y1,tunes_y2))
  #    diff = [abs(a-b) for a,b in all_combinations]
  #    print ''
  #    #for ik in range (len(all_combinations)):
  #    #  print all_combinations[ik], diff[ik],'here'
  #    #print min(diff), all_combinations[np.argmin(diff)]
  #    tunes_y1[0] = all_combinations[np.argmin(diff)][0]
  #    tunes_y2[0] = all_combinations[np.argmin(diff)][1]
  #    for ik in range (len(tunes_y1)):
  #      print tunes_y1[ik], tunes_y2[ik]
  #    print 'after'
  #  if (amp_x2[1]/amp_x2[0]>0.7 and abs(tunes_x2[0] - tunes_y2[0])<1e-3) or (amp_x1[1]/amp_x1[0]>0.7 and abs(tunes_x1[0] - tunes_y1[0])<1e-3):
  #    print ''
  #    for ik in range (len(tunes_x1)):
  #      print tunes_x1[ik], tunes_x2[ik]
  #    print 'before'
  #    import itertools
  #    all_combinations =list(itertools.product(tunes_x1,tunes_x2))
  #    diff = [abs(a-b) for a,b in all_combinations]
  #    print ''
  #    #for ik in range (len(all_combinations)):
  #    #  print all_combinations[ik], diff[ik],'here'
  #    #print min(diff), all_combinations[np.argmin(diff)]
  #    tunes_x1[0] = all_combinations[np.argmin(diff)][0]
  #    tunes_x2[0] = all_combinations[np.argmin(diff)][1]
  #    for ik in range (len(tunes_y1)):
  #      print tunes_x1[ik], tunes_x2[ik]
  #    print 'after'
  #  tune_diff_x = [i-j for i,j in zip(tunes_x1, tunes_x2)]
  #  tune_diff_y = [a-b for a,b in zip(tunes_y1, tunes_y2)]
  #  tune_diff_x2 = [a**2 for a in tune_diff_x]
  #  tune_diff_y2 = [b**2 for b in tune_diff_y]
  #  tune_diffusion = [i+j for i,j in zip(tune_diff_x2, tune_diff_y2)]
  #  tune_diffusion_sqrt = [np.sqrt(a) for a in tune_diffusion]
  #  if abs(np.log10(tune_diffusion_sqrt[0])) <3:
  #    print "here"
  #    print tunes_x1[0], tunes_x2[0], tunes_y1[0], tunes_y2[0]
  return tunes_x1, tunes_y1, tunes_x2, tunes_y2, tune_diffusion_sqrt

