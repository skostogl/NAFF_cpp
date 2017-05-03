from grid import *

infile=open("/home/skostogl/cuTrack/dat_files/polar_grid.dat")
per_row=[]
for line in infile:
    per_row.append(line.strip().split(' '))
per_column=zip(*per_row)

counter=0
grid=[]
for i in (per_column[2]):
  print int(i),int(per_column[3][counter])
  grid.append([int(i),int(per_column[3][counter])])
  counter=counter+1
print grid
create_plot(per_column[0],per_column[1],grid) 
plt.plot()




quit()
infile=open("/home/skostogl/cuTrack/grid_pos_delta.dat")
per_row=[]
for line in infile:
    per_row.append(line.strip().split(' '))
per_column=zip(*per_row)
counter=0
grid=[]
for i in (per_column[2]):
  grid.append([int(i),int(per_column[3][counter])])
  counter=counter+1
print grid
create_plot(per_column[0],per_column[1],grid) 
plt.plot()


infile=open("/home/skostogl/cuTrack/grid_neg_delta.dat")
per_row=[]
for line in infile:
    per_row.append(line.strip().split(' '))
per_column=zip(*per_row)

counter=0
grid=[]
for i in (per_column[2]):
  grid.append([int(i),int(per_column[3][counter])])
  counter=counter+1
print grid
create_plot(per_column[0],per_column[1],grid) 
plt.plot()
plt.show()


