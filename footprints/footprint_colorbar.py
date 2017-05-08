from grid import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import collections as mc

mpl.rc('text', usetex=True)
mpl.rc('font',family='Times')

infile=open("footprint.dat")
per_row=[]
for line in infile:
    per_row.append(line.strip().split(' '))
per_column=zip(*per_row)
x2=[float(i) for i in per_column[0]]
y2=[float(i) for i in per_column[1]]
z2=[float(i) for i in per_column[2]]

infile=open("configuration_space.dat")
per_row=[]
for line in infile:
        per_row.append(line.strip().split(' '))
per_column=zip(*per_row)
x=[float(i)/(0.00018733990017) for i in per_column[0]] 
y=[float(i)/(0.000251207) for i in per_column[1]]

f = plt.figure(figsize=(9,6))
gs = gridspec.GridSpec(1, 2,width_ratios=[1,1.1])
ax1 = plt.subplot(gs[0], aspect = 'equal', adjustable='box-forced')
ax1 = plt.scatter(x2, y2, edgecolors='none', s=15, c=np.log10(z2))
data_x = x2
data_y = y2
qx = np.sum(data_x)/len(data_x)
qy = np.sum(data_y)/len(data_y)
make_resonance_diagram(15, [0,1], [0,1])
plt.xlabel(r'$\boldsymbol{\mathrm{Horizontal} \ \mathrm{Tune} \ \mathrm{Q_x}}$', fontweight='bold', fontsize=18)
plt.ylabel(r'$\boldsymbol{\mathrm{Vertical} \ \mathrm{Tune} \ \mathrm{Q_y}}$', fontweight='bold', fontsize=18)
plt.xlim([0.301,0.321])
plt.ylim([0.313,0.333])
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
axes = plt.subplot(gs[1], aspect = 'equal', adjustable='box-forced')
ax2 = plt.scatter(x, y, edgecolors='none', s=15, c=np.log10(z2))
cb = plt.colorbar(ax2, fraction = 0.046, pad=0.04,ax=axes)
cb.set_label(r'$\boldsymbol{\mathrm{log\sqrt{\Delta Q^2_x + \Delta Q^2_y}}}$', fontweight='bold', fontsize=16)
cb.ax.tick_params(labelsize=14)
plt.xlabel(r'$\boldsymbol{\mathrm{x}[\mathrm{\sigma}]}$', fontweight='bold', fontsize=18)
plt.ylabel(r'$\boldsymbol{\mathrm{y}[\mathrm{\sigma}]}$', fontweight='bold', fontsize=18)
plt.xlim([0,6])
plt.ylim([0,6])
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.tight_layout()
plt.show()
