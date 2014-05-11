import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy import *
from random import choice
from copy import deepcopy

## This file generates the fundamental diagram.

FileList=['3laneF5000S60','3laneF5000S50','3laneF5000S40','3laneF5000S30','3laneF5000S20','3laneF5000S10','3laneF5000S5','3laneF5000S1','3laneF4000S65','3laneF3000S65','3laneF2000S65','3laneF1000S65','3laneF500S65']

FD=load('3laneF5000S65FD.npy')

for filename in FileList:
    FDfocus=load(filename+'FD.npy')
    FD=vstack((FD,FDfocus))

    DS=FD.copy()


for i in range(len(FD[:,0])):
    FD[i,1]=FD[i,0]*FD[i,1]

Data=zeros((1000,2))
DataV=zeros((1000,2))
a=-0.0582
b=4.31
c=2315.07
n=0

for i in linspace(0,240,1000):
    if i<36.92:
        yv=65
        y=65*i
    else:
        y=a*i*i+b*i+c
        yv=a*i+b+c/i
    Data[n]=[i,y]
    DataV[n]=[i,yv]
    n=n+1


plt.rc('xtick',labelsize=30)
plt.rc('ytick',labelsize=30)
plt.hold(True)
plt.scatter(DS[:,0],DS[:,1],s=1,color='r')
plt.plot(DataV[:,0],DataV[:,1],linewidth=2.5,color='k')
plt.xlabel('Density (veh/mile/lane)',fontsize=30)
plt.ylabel('Speed (mph)',fontsize=30)
plt.ylim([0,100])
plt.xlim([0,300])
plt.savefig('DScorsimC.pdf',bbox_inches='tight')
plt.show()
plt.hold(False)
plt.clf()

#save('FDDensitySpeed',FD)



plt.rc('xtick',labelsize=30)
plt.rc('ytick',labelsize=30)
plt.hold(True)
plt.scatter(FD[:,0],FD[:,1],s=1,color='r')
plt.plot(Data[:,0],Data[:,1],linewidth=2.5,color='k')
plt.xlabel('Density (veh/mile/lane)',fontsize=30)
plt.ylabel('Flow (veh/h/lane)',fontsize=30)
plt.ylim([0,4000])
plt.xlim([0,300])
plt.savefig('FDcorsim.pdf',bbox_inches='tight')
plt.show()
plt.hold(False)
