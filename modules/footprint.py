##############################################
######### Taken from https://github.com/SixTrack/SixDeskDB/blob/master/sixdeskdb/footprint.py#####################
##############################################
######## Modified 07/03/2018

"""module to plot resonance lines"""

import matplotlib.pyplot as pl
import numpy as _np

mycolors=list('rgbcm')

def colorrotate():
  c=mycolors.pop(0);mycolors.append(c)
  return c

def getmn(order,kind='b'):
  """return resonance of order *order* of kind *kind*
  Parameters:
  -----------
  order: order of resonance
  as list of tuples (m,n) of * resonances of order o
  kind: 't': all resonances
        'a': skew multipoles n=odd
        'b': normal multipoles n=even
        's': sum resonances (m>0,n>0), loss of beam
        'd': difference resonances (m<0,n>0) or (m>0,n<0), exchange between planes
  Returns:
  --------
  list of tuples (m,n) with |m|+|n|=order and m*Qx+n*Qy
  """
  out=[]
  if 't' in kind: kind='ab'
  for m in range(0,order+1):
    n=order-m
    if 'b' in kind and n%2==0 or m==0:
      out.append( (m,n) )
      if n>0:
        out.append( (m,-n) )
    if 'a' in kind and n%2==1 and m>0:
      out.append( (m,n) )
      if n>0:
        out.append( (m,-n) )
    if 's' in kind and (n>0 and m>0):
      out.append( (m,n) )
    if 'd' in kind and (n>0 and m>0):
      out.append( (m,-n) )
  return list(set(out))

def find_res_xcross(m,n,q,xs,y1,y2,out):
  if n!=0:
    m,n,q,xs,y1,y2=map(float,(m,n,q,xs,y1,y2))
    ys=(q-m*xs)/n
    if ys>=y1 and ys<=y2:
      out.append((xs,ys))

def find_res_ycross(m,n,q,ys,x1,x2,out):
  if m!=0:
    m,n,q,ys,y1,y2=map(float,(m,n,q,ys,x1,x2))
    xs=(q-n*ys)/m
    if xs>=x1 and xs<=x2:
      out.append((xs,ys))

def get_res_box(m,n,l=0,qz=0,a=0,b=1,c=0,d=1):
  """get (x,y) coordinates of resonance lines with
     m,n,q:   resonance integers with m*qx+n*qy=q
     l,qz:    order l of resonance sideband with frequency qz
     a,b,c,d: box parameters=tune range, 
              explicitly a<qx<b and c<qy<d 
  """
  order=int(_np.ceil(abs(m)*max(abs(a),abs(b))+abs(n)*max(abs(c),abs(d))))
  out=[]
  mnlq=[]
  for q in range(-order,+order+1):
    q=q-l*qz
    points=[]
    find_res_xcross(m,n,q,a,c,d,points)#find endpoint of line (a,ys) with c<ys<d
    find_res_xcross(m,n,q,b,c,d,points)#find endpoint of line (b,ys) with c<ys<d
    find_res_ycross(m,n,q,c,a,b,points)#find endpoint of line (xs,c) with a<xs<b
    find_res_ycross(m,n,q,d,a,b,points)#find endpoint of line (xs,d) with a<xs<b
    points=list(set(points))
    if len(points)>1:
      out.append(points)
      mnlq.append((m,n,l,q+l*qz))
      if l==0:
        print '%2d*Qx%+2d*Qy=%2d' % (m,n,q)
      else:
        print '%2d*Qx%+2d*Qy+%+2d*Qz=%2d' % (m,n,l,q+l*qz)
  return out,mnlq

def plot_res_box(m,n,l=0,qz=0,a=0,b=1,c=0,d=1,color='b',linestyle='-'):
  """plot resonance (m,n,l) with sidesband of
  order l and frequency qz with qx in [a,b]
  and qy in [c,d]"""
  points,mnlq=get_res_box(m,n,l,qz,a,b,c,d)
  for p in points:
    x,y=zip(*p)
    pl.plot(x,y,color=color,linestyle=linestyle,linewidth=1)

def annotate_res_order_box(o,l=0,qz=0,a=0,b=1,c=0,d=1):
  """annotate the resonance lines of order *o*
  where annotations are (m,n,l). If the same
  resonance line occurs multiple times, only
  the first one is plotted"""
  l_points=[]
  l_mnlq =[]
  for m,n in getmn(o,'t'):
    points,mnlq=get_res_box(m,n,l,qz,a,b,c,d)
    for pp,oo in zip(points,mnlq):
      if pp not in l_points:
        x,y=zip(*pp)
        (x1,x2)=x
        (y1,y2)=y
        (xp,yp)=(x1+(x2-x1)/2.,y1+(y2-y1)/2.)
        if x2-x1==0: theta=90
        else: theta=_np.arctan((y2-y1)/(x2-x1))*360/(2*_np.pi)
        pl.gca().annotate(s='%s'%str(oo[:-1]),xy=(xp,yp),xytext=(xp,yp),xycoords='data',rotation=theta,fontsize=10,color='k',horizontalalignment='center',verticalalignment='center')
        l_points.append(pp)
        l_mnlq.append(oo)

def annotate_specific(m,n,l=0,qz=0,a=0,b=1,c=0,d=1,xy_all = [], theta_all=[], l_points = [], l_mnlq = []):
  """annotate the resonance lines of order *o*
  where annotations are (m,n,l). If the same
  resonance line occurs multiple times, only
  the first one is plotted"""
  points,mnlq=get_res_box(m,n,l,qz,a,b,c,d)
  for pp,oo in zip(points,mnlq):
    if pp not in l_points:
      x,y=zip(*pp)
      (x1,x2)=x
      (y1,y2)=y
      (xp,yp)=(x1+(x2-x1)/2.,y1+(y2-y1)/2.)
      
      if x2-x1==0: 
        theta=90
        yp = max(y)
        if xp<=a:
          ha = 'left'
          va = 'top'
        else:
          ha = 'right'
          va = 'top'
        label = "          (%s,%s,%s,%s)       "%(oo)
      elif y2-y1 == 0:
        theta = 0
        xp = min(x)
        if yp<=c:
          ha = 'top'
          va = 'bottom'
        else:
          ha = 'top'
          va = 'top'
        label = "        (%s,%s,%s,%s)         "%(oo)
      else: 
        theta=_np.arctan((y2-y1)/(x2-x1))*360/(2*_np.pi)
        if theta>0:
          print 'okkk'
          xp = min(x)
          yp = y[_np.argmin(x)]
          ha = 'left'
          va = 'left'
          label = "                   (%s,%s,%s,%s)                        "%(oo)
        else:
          xp = max(x)
          yp = y[_np.argmax(x)]
          xp = max(x)
          yp = y[_np.argmax(x)]
          ha = 'right'
          va = 'right'
          label = "(%s,%s,%s,%s)                  "%(oo)
      
      annot = pl.gca().annotate(s=label,xy=(xp,yp),xytext=(xp,yp),xycoords='data',rotation=theta,fontsize=10,color='k',horizontalalignment=ha,verticalalignment=va, annotation_clip=True)
      l_points.append(pp)
      l_mnlq.append(oo)
      xy_all.append(annot)
      theta_all.append(theta)        

def plot_res_order_box(o,l=0,qz=0,a=0,b=1,c=0,d=1,c1='b',lst1='-',c2='b',lst2='--',c3='g', list=[], xy_total = [], theta_total = [], annotate=False,l_points=[], l_mnlq =[]):
  """plot resonance lines up to order o and 
  sidebands of order l for frequency qz
  which lie in the square described by
  x=[a,b] and y=[c,d]"""
  if not list:
    flag_specific = False
  else:
    flag_specific = True
  for m,n in getmn(o,'b'):
    # print 'b%s: m=%d n=%d'%(o,m,n)
    if ( (abs(m),abs(n) ) in list) or (flag_specific==False) :
      plot_res_box(m,n,l=0,qz=0,a=a,b=b,c=c,d=d,color=c1,linestyle=lst1)
      if(l!=0):#sidebands
        for ll in +abs(l),-abs(l):
          plot_res_box(m,n,l=ll,qz=qz,a=a,b=b,c=c,d=d,color=c3,linestyle=lst1)
      if annotate:
        annotate_specific(m,n,l,qz,a,b,c,d, xy_all=xy_total, theta_all = theta_total,l_points=l_points, l_mnlq=l_mnlq )

  for m,n in getmn(o,'a'):
    # print 'a%s: m=%d n=%d'%(o,m,n)
    if ( (abs(m),abs(n) ) in list) or (flag_specific==False) :
      plot_res_box(m,n,l=0,qz=0,a=a,b=b,c=c,d=d,color=c2,linestyle=lst2)
      if(l!=0):#sidebands
        for ll in +abs(l),-abs(l):
          plot_res_box(m,n,l=ll,qz=qz,a=a,b=b,c=c,d=d,color=c3,linestyle=lst2)
      if annotate:
        annotate_specific(m,n,l,qz,a,b,c,d, xy_all=xy_total, theta_all = theta_total,l_points=l_points, l_mnlq=l_mnlq )

def plot_res_order(o,l=0,qz=0,c1='b',lst1='-',c2='b',lst2='--',c3='g',annotate=False):
  """plot resonance lines of order o and sidebands
  of order l and frequency qz in current plot
  range"""
  a,b=pl.xlim()
  c,d=pl.ylim()
  plot_res_order_box(o,l,qz,a,b,c,d,c1,lst1,c2,lst2,c3)
  if annotate: annotate_res_order_box(o,l,qz,a,b,c,d)
  pl.xlim(a,b)
  pl.ylim(c,d)

def plot_res_upto_order(o,l=0,qz=0,c1='b',lst1='-',c2='b',lst2='--',c3='g',annotate=False):
  """plot resonance lines up to order o and sidebands
  of order l and frequency qz in current plot
  range"""
  for i in range (-o,+o+1):
    plot_res_order( i,l,qz,c1,lst1,c2,lst2,c3,annotate)

def plot_res(m,n,l=0,qz=0,color='b',linestyle='-'):
  """plot resonance of order (m,n,l) where l is
  the order of the sideband with frequency qz in
  the current plot range"""
  a,b=pl.xlim()
  c,d=pl.ylim()
  points,order=get_res_box(m,n,l,qz,a,b,c,d)
  for c in points:
    x,y=zip(*c)
    pl.plot(x,y,color=color,linestyle=linestyle)
  pl.xlim(a,b)
  pl.ylim(c,d)

def plot_res_order_specific(order,l=0,qz=0,c1='b',lst1='-',c2='b',lst2='--',c3='g',annotate=False, list = []):
  """plot resonance lines of order o and sidebands
  of order l and frequency qz in current plot
  range, but the ones that are only specified in list, where list is a list   of tuples"""
  a,b=pl.xlim()
  c,d=pl.ylim()
  xy_total = []
  theta_total = []
  l_points=[]
  l_mnlq =[]
  for o in order:
    plot_res_order_box(o,l,qz,a,b,c,d,c1,lst1,c2,lst2,c3,list=list, xy_total = xy_total, theta_total = theta_total, l_points = l_points, l_mnlq = l_mnlq,annotate=annotate)
  pl.xlim(a,b)
  pl.ylim(c,d)




