import math
import sys
import fileinput
import numpy as np
import pandas as pd
from subprocess import call
import matplotlib.pyplot as plt

sys.path.append('../')
from NAFF import *

def naff_cpp(df, df_bpms, plane='x', fmax=30, write_file=False, label ="",xmin=0,xmax=0.5):
  zero  = Vec_cpp()
  coord = Vec_cpp()
  if (plane == 'x'):
    data = np.array(df['x'])
    data_prime = np.array(0.0*df['px'])
  elif (plane == 'y'):
    data = np.array(df['y'])
    data_prime = np.array(0.0*df['py'])
  elif (plane == 'z'):
    data = np.array(df['z'])
    data_prime = np.array(df['de_e'])
  coord.extend(i for i in data)
  zero.extend(i for i in data_prime)
  naff = NAFF()
  naff.set_window_parameter(1, 'h')
  if write_file == True:
    naff.set_file(label,xmin,xmax,1e-5)
  naff.fmax = fmax 
  tune=naff.get_f(coord,zero)
  tune = [i*len(df_bpms) for i in tune]
  amplitudes = naff.return_amplitudes()
  return tune,amplitudes

def fourier_integral(qx,z):
  cp = 0j
  N=len(z)
  z = np.hanning(len(z))*z
  for tt, zz in enumerate(z):
    cp+=zz*np.exp(-2j*math.pi*qx*tt)
  return abs(cp)

############# Sliding window
def myfunc(t,turn):
  y = t
  x = np.array(turn)
  mean = np.mean(y)
  y = [i-mean for i in y]
  abs_y = [abs(i) for i in y]
  return y;

def myfunc_x(df):
  df['x']  = (df['x']-df['x'].mean())
  df['px'] = (df['px']-df['px'].mean())
  df['y']  = (df['y']-df['y'].mean())
  df['py'] = (df['py']-df['py'].mean())
  df_bpms = [i for i,gr in df.groupby('nb_bpm')]
  print "BPM cleanup: ", df_bpms[0]
  df_new = clean_signal(df,df_bpms,len(df))
  return df_new

def sliding_window(dff, df_bpms, min_t = 1 ,lim = 100 ,sliding_window =30 ,plane='x',step=1,return_cleaned=False):

  fmax  = []
  turns = []

  if (plane == 'x'):
    dff['x']  = (dff.groupby("nb_bpm")['x'].transform(lambda x:( ( myfunc(x,dff[dff['nb_bpm'] ==x.name]['turn_nb']  )))))
    dff['px'] = (dff.groupby("nb_bpm")['px'].transform(lambda x:(( ( myfunc(x,dff[dff['nb_bpm'] ==x.name]['turn_nb']  ))))))
  elif (plane=='y'):
    dff['y']  = (dff.groupby("nb_bpm")['y'].transform(lambda x:( ( myfunc(x,dff[dff['nb_bpm'] ==x.name]['turn_nb']  )))))
    dff['py'] = (dff.groupby("nb_bpm")['py'].transform(lambda x:( ( myfunc(x,dff[dff['nb_bpm'] ==x.name]['turn_nb']  )))))

  if (return_cleaned == True):
    df = dff.groupby("nb_bpm").apply(lambda x:( ( myfunc_x(dff[dff['nb_bpm'] ==x.name]  ))))
  else:
    df=dff

  for min_turn in range(min_t,lim,step):
    max_turn = min_turn + sliding_window
    if (len(df_bpms)>1):
      df_copy = df[ (  (df['turn_nb'] >=min_turn) & (df['turn_nb']<=max_turn))     | ((df['turn_nb']==max_turn+1) & (df['nb_bpm'] == df_bpms[0]) )]
    else:
      df_copy = df[ ((df['turn_nb'] >=min_turn) & (df['turn_nb']<=max_turn))   ]
    turns.append(min_turn)

    if (plane=='x'):
      q_lask, amps_lask,re_lask,im_lask = naff_cpp(df_copy,df_bpms,plane='x')
      f=abs(q_lask[0])
      print "Plane x, Turns: ", min_turn,max_turn, " Tune: ", f, q_lask[0]
    elif (plane=='y'):
      q_lask, amps_lask,re_lask,im_lask = naff_cpp(df_copy,df_bpms,plane='y')
      f=abs(q_lask[0])
      print "Plane y, Turns: ", min_turn,max_turn, " Tune: ",f,q_lask[0]
    elif (plane=='z'):
      q_lask, amps_lask,re_lask,im_lask = naff_cpp(df_copy,df_bpms,plane='z')
      print "Plane z, Turns: ", min_turn,max_turn, " Tune: ",q_lask[0]
      f = q_lask[0]
    fmax.append(f)

  if (return_cleaned==True):
    return fmax,turns,df
  else:
    return fmax,turns

def naff_on_naff(turns,fmax,step,lim, dc_flag=False, dc_component=[],sw=[],mean_component=[],save=False,plt_name =0,new_signal = [],method='lask'):
    if (method == 'lask'):
      call("rm solution_new", shell=True)
      f_copy = fmax
      turns_copy = turns
      turns_copy2=turns
      im_part = [i*0.0 for i in turns_copy2]
      flagg=False
      ttt = np.arange(len(turns_copy2),0,-1)
      for mul in ttt:
        if (flagg==False):
          if (mul%6 ==0):
            nn=mul
            flagg=True
      nn = int(nn)
      print "Size NAFF on NAFF: ",nn
      new_name = "KTABS="+str(nn)+",!\n"
      x = fileinput.input(files="nafaut.par", inplace=1)
      text='KTABS='
      for line in x:
        if text in line:
          line = new_name
        print line,
      x.close()
      dfx = pd.DataFrame({'fmax': f_copy,'im':im_part, 'turns': turns_copy2})
      xxx = [0*i for i in fmax]
      signal_f = pd.DataFrame({'x': fmax,'px':xxx})
      dfx.to_csv("datax", sep="\t", columns =["fmax","im"], header=False, index=False, float_format='%.15f')
      call("gfortran -w nafaut.f -o naff && ./naff > test", shell=True)
      sol = pd.read_csv("solution_new",skiprows=2, delim_whitespace=True, header=None)
      sol.columns = ["nb", "f", "amp", "re", "im"]
    elif (method=='cpp'):
      turns_copy2=turns
      im_part = [i*0.0 for i in turns_copy2]
      dfx = pd.DataFrame({'fmax': fmax,'im':im_part, 'turns': turns_copy2})
      nn = len(fmax)
      coord = Vec_cpp()
      zero  = Vec_cpp()
      coord.extend(i for i in fmax)
      zero.extend(i*0 for i in fmax)
      naff = NAFF()
      naff.keep_dc(1)
      naff.set_window_parameter(1, 'h')
      naff.fmax = 5
      tune=naff.get_f(coord,zero)
      amps = naff.return_amplitudes()
      amps[0] = amps[0]/2.0
      re=naff.return_re()
      im=naff.return_im()
      sol = pd.DataFrame({'f': tune,'amp':amps, 're':re,'im':im})
    counter_amp=0
    for i in np.array(sol["f"]):
       print i,np.array(sol["amp"])[counter_amp]
       counter_amp+=1
    title = " NAFF on NAFF: "+str(nn)+" turns"
    N=len(turns_copy2)
    reconstruct_f(sol,dfx,1,N,title,savefig=save,plot_name=plt_name,dc_flag=True, dc_component=dc_component,sw=sw ,mean_component=mean_component,new_signal=new_signal,step=step,lim=lim,method=method)


def k_closest(sample, pivot, k):
    return sorted(sample, key=lambda i: abs(i - pivot))[:k]

def reconstruct_f(sol,signal,nb_bpms,N,title,savefig=False,plot_name=0, dc_flag=False, dc_component=[],sw=[],mean_component=[],new_signal = [],step=1,lim=100,method='lask'):
  if (method=='lask'):
    amp0=[float(i.replace('D', 'E')) for i in sol["amp"]]
    re0=[float(i.replace('D', 'E')) for i in sol["re"]]
    imag0=[float(i.replace('D', 'E')) for i in sol["im"]]
  elif (method=='cpp'):
    amp0=[float(i) for i in sol["amp"]]
    amp0[0]=amp0[0]
    for i in range (1,len(amp0)):
      amp0[i]*=1.0
    re0=[float(i) for i in sol["re"]]
    imag0=[float(i) for i in sol["im"]]
  f = [(i) for i in sol["f"]]
  f = [i/(step*1.0) for i in f]
  print "FINAL"
  phase = [math.atan2(i,j) for i,j in zip(imag0,re0)]
  s_tot = []
  tt=np.arange(0,lim,1.0/nb_bpms)
  tt2=np.arange(0,lim-step,step)
  freqs = []
  freqs.append(f[0])
  b = 1.0/556
  #freqs2 = k_closest(f[1:],b,2)[0]
  #######
  b2 = -1.0/556
  cc=0
  try:
    #freqs.append(k_closest(f[1:],b,2)[0])
    #freqs.append(k_closest((f[1:]),b,2)[0])
    for i in f:
      if ( ((method=='cpp') and ((abs(i) - 1.0/556.0) <1e-4) and (cc==0) and (abs(i)>1e-5)) or ((method=='lask') and ((abs(i) - 1.0/556.0) <1e-4) and (cc<=1) and (abs(i)>1e-5))):
        freqs.append(i)
        cc+=1
    #freqs.append(k_closest(f[1:],b2,2)[0])
    #freqs.append(k_closest(f[1:],b2,2)[0])
    #print freqs
  except:
    print freqs
  for t in tt:
    s=0
    for i in range (0,len(sol)):
      try:
        harmonics = f[i]/f[1]
      except:
        harmonics=f[i]
      #print "HARM"
      #if (t==0):
      #	print f[i]," ALL", harmonics
      #print f[i],harmonics
      #if (abs(round(harmonics) -harmonics)<1e-2) or (abs(harmonics)<1e-12):
      #if True:
      if f[i] in freqs:
        #if True:
        if (t==0):
          print f[i]," IN2", harmonics
        s+=amp0[i]*np.exp(1j* (2.0*np.pi*f[i]*t + phase[i] ) )
        #s+=amp0[i]*np.cos(1* (2.0*np.pi*f[i]*t + phase[i] ) )
    s_tot.append(s)
  sr = [i.real for i in s_tot]
  si = [i.imag for i in s_tot]
  sig = [x for x in signal['fmax']]
  s_tot_r= [i.real for i in s_tot]
  s_tot_i= [i.imag for i in s_tot]
  diff_r = [abs(x-y) for x,y in zip(s_tot_r,sig)]  
  s_tot_abs = [np.sqrt(x**2+y**2) for x,y in zip(s_tot_r,s_tot_i)]  
  for i in s_tot_abs:
    new_signal.append(i)
  plt.plot(tt,s_tot_r,c='b', label="real part reconstucted signal from NAFF")
  plt.plot(tt2,sig,c='k', label="initial signal")
  plt.grid()
  plt.xlabel("Min turn of sliding window")
  plt.ylabel("Qx")
  plt.title("With BB, without ripple, 4D, 200 BPMs, sw 30turns")
  plt.legend()
  plt.tight_layout()
  plt.show()
    
  if (dc_flag==True):
    dc_component.append(s_tot_r[0])
    mean_component.append(np.mean(sig))
  if (savefig ==True):
    filename = 'plots/turns' + str(plot_name)+'_' + str(nb_bpms) + 'bpms' + '.png'
    plt.savefig(filename)
    plt.close()
 
def reconstruct_signal(sol,signal,nb_bpms,N,title='',savefig=False,plot_name=0,plane = 'x',name=[]):
  #amp0=[float(i.replace('D', 'E')) for i in sol["amp"]]
  #re0=[float(i.replace('D', 'E')) for i in sol["re"]]
  #imag0=[float(i.replace('D', 'E')) for i in sol["im"]]
  amp0=[i for i in sol["amp"]]
  re0=[i for i in sol["re"]]
  imag0=[i for i in sol["im"]]
  f = [i for i in sol["f"]]
  phase = [math.atan2(i,j) for i,j in zip(imag0,re0)]
  s_tot = []
  tt=np.arange(0,N,1.0/nb_bpms) 
  b = 1.0/556
  b1 = -1.0/556
  rf = []
  cc = 0
  for k in range(1,len(f)):
    if (cc<=1):
      if abs(round(abs(f[0]-f[k])/0.0017)-abs(f[0]-f[k])/0.0017)<1e-2:
        rf.append(f[k])
        cc+=1
  for t in tt:
    s=0
    counter_f=0
    f2=0
    #for i in range (len(sol)):
    for i in range (0,len(sol)):
     #if ( (f[i] in rf) or (counter_f==0) ):
     
     if True:
        if True:
          #if ( (abs(f[i])>0.1) ):
          counter_f+=1
        if (t==tt[0]):
          print plane," Keeping frequency:", f[i]
        s+=amp0[i]*np.exp(1j* (2.0*np.pi*(f[i])*t + phase[i] ) )
        #s+=amp0[i]*np.cos(1.0* (2.0*np.pi*(f[i])*t + phase[i] ) )
    s_tot.append(s)
  sr = [i.real for i in s_tot]
  si = [i.imag for i in s_tot]
  s_tot_abs = [abs(i) for i in s_tot]
  s_tot_r= [i.real for i in s_tot]
  if (plane=='x'):
    sig_r = [(x+1j*y).real for x,y in zip(signal['x'],signal['px'])]
    s = [(abs(x+1j*y)) for x,y in zip(signal['x'],signal['px'])]
  else: 
    sig_r = [(x+1j*y).real for x,y in zip(signal['y'],signal['py'])]
    s = [(abs(x+1j*y)) for x,y in zip(signal['y'],signal['py'])]
  s_tot_i = [i.imag for i in s_tot]
  names = [name[0]*i for i in s_tot]
  if (plane=='x'):
    sig_i = [(x+1j*y).imag for x,y in zip(signal['x'],signal['px'])]
  else:
    sig_i = [(x+1j*y).imag for x,y in zip(signal['y'],signal['py'])]
  #diff_i = [(x-y) for x,y in zip(s_tot_i,sig_i)] 
  diff_i = [(y-x) for x,y in zip(s_tot_i,sig_i)] 
  #diff_r = [(x-y) for x,y in zip(s_tot_r,sig_r)]  
  diff_r = [(y-x) for x,y in zip(s_tot_r,sig_r)]  
  if (plane=='x'):
    new_signal = pd.DataFrame({'x': sr, 'px': si,'turn_nb':signal['turn_nb'], 'nb_bpm': signal['nb_bpm'],'bpm_name':names})
    #new_signal = pd.DataFrame({'x':diff_r, 'px': diff_i,'turn_nb':signal['turn_nb'], 'nb_bpm': signal['nb_bpm'],'bpm_name':names})
  else:
    new_signal = pd.DataFrame({'y': sr, 'py': si,'turn_nb':signal['turn_nb'], 'nb_bpm': signal['nb_bpm'],'bpm_name':names})
    #new_signal = pd.DataFrame({'y': diff_r, 'py': diff_i,'turn_nb':signal['turn_nb'], 'nb_bpm': signal['nb_bpm'],'bpm_name':names})
  return new_signal


def clean_signal(df_all,df_bpms,N):
  '''
  call("rm solution_new", shell=True)
  naff_lask(df_all, df_bpms,mul_six=True,plane='x')  
  sol = pd.read_csv("solution_new",skiprows=2, delim_whitespace=True, header=None)
  sol.columns = ["nb", "f", "amp", "re", "im"]
  '''
  #print df_bpms

  q, amp,re,im = naff_cpp_l(df_all,df_bpms,plane='x',fi_flag=True)
  sol = pd.DataFrame({'f': q, 'amp':amp, 're':re,'im':im})
  print sol
  #print sol
  #quit()
  #plt.plot(abs(df_all['x'] + 1j*df_all['px']))
  data_x = reconstruct_signal(sol,df_all,len(df_bpms),N,plane='x',name = df_bpms)
  #plt.plot(abs(data_x))
  #plt.show()
  #sys.exit()
  #print " "
  #call("rm solution_new", shell=True)
  #naff_lask(df_all, df_bpms,mul_six=True,plane='y')  
  #sol = pd.read_csv("solution_new",skiprows=2, delim_whitespace=True, header=None)
  #sol.columns = ["nb", "f", "amp", "re", "im"]
  #print sol
  q, amp,re,im = naff_cpp_l(df_all,df_bpms,plane='y')
  sol = pd.DataFrame({'f': q, 'amp':amp, 're':re,'im':im})
  data_y = reconstruct_signal(sol,df_all,len(df_bpms),N,plane='y',name = df_bpms)
  final = pd.DataFrame({'turn_nb': data_x['turn_nb'],'nb_bpm':data_x['nb_bpm'], 'x':data_x['x'],'px':data_x['px'], 'y':data_y['y'],'py': data_y['py']})
  return final

def cmp_invariant(df,df_bpms):
  ex = []
  ey = []
  e_turns = []
  e_bpm = []
  dp=27e-5
  for i in range (len(df_bpms)):
    print "BPM: ", i
    df1 = df[df['nb_bpm'] == df_bpms[i]]
    madx = pd.read_csv("twiss_sof_6d_bb_100",delim_whitespace=True, header=None)
    madx.columns = ['s','name','betx','bety','alfx','alfy','mux','muy','x','y','px','p', 'dx','dpx','dy','dpy']
    madx1 = madx[madx['s'] == df_bpms[i]]
    bx = np.array(madx1['betx'])[0]*1e3
    ax = np.array(madx1['alfx'])[0]*1e3
    by = np.array(madx1['bety'])[0]*1e3
    ay =  np.array(madx1['alfy'])[0]*1e3
    gx = (1.0+ax**2)/bx
    gy = (1.0+ay**2)/by
    dx = np.array(madx1['dx'])[0]*1e3
    dpx = np.array(madx1['dpx'])[0]*1e3
    dy = np.array(madx1['dy'])[0]*1e3
    dpy = np.array(madx1['dpy'])[0]*1e3
    print dx, dpx, dy,dpy

    df1['x']  = (df1['x']-dx*df1['de_e'])
    df1['px'] = (df1['px']-dpx*df1['de_e'])
    df1['y']  = (df1['y']-dy*df1['de_e'])
    df1['py'] = (df1['py']-dpy*df1['de_e'])
    #plt.scatter(df1['x'],df1['px'])
    #plt.scatter(df1['y'],df1['py'])
    
    #plt.show()

    ex.append( (gx*np.array(df1['x'])**2 + 2.0*ax*np.array(df1['x'])*np.array(df1['px']) + bx*np.array(df1['px'])**2)/2.0)
    ey.append( (gy*np.array(df1['y'])**2 + 2.0*ay*np.array(df1['y'])*np.array(df1['py']) + by*np.array(df1['py'])**2)/2.0)
    e_turns.append(np.array(df1['turn_nb']))
    e_bpm.append(np.array(df1['nb_bpm']))
  exx = [y for x in ex for y in x]
  eyy = [y for x in ey for y in x]
  e_turnss = [y for x in e_turns for y in x]
  e_bpmm = [y for x in e_bpm for y in x] 
  e = pd.DataFrame({'ex': exx,'ey':eyy, 'turns':e_turnss ,'nb_bpm': e_bpmm})
  return e
 

