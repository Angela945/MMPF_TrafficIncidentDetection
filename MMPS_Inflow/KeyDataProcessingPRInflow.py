import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy import *
from random import choice
from random import sample
from copy import deepcopy

## This file calculates the density and speed evolution for CORSIM
## The outputs from this file are used as measurment for the estimation algorithms
## Need to specify the headway value (penetration rate)

filename='3lane1blockS65F6000'
keyData=load(filename+'key.npy')
flow=6000


## Define functions

## Construct the DataTime dictionary. Key: time. Values: VehID/Position/Speed
def buildDataTime(keyData):
        DataTime=dict()
        for i in range(int(len(keyData[:,0]))):
                if str(int(keyData[i,0])) not in DataTime:
                        DataTime[str(int(keyData[i,0]))]=keyData[i,[1,2,3]]
                else:
                        DataTime[str(int(keyData[i,0]))]=vstack((DataTime[str(int(keyData[i,0]))],keyData[i,[1,2,3]]))
        return DataTime

## Construct the VehTrajectory dictionaray. Key: VehID. Values: Time/Position/Speed
def buildVehTrajectory(keyData):
        VehTrajectory=dict()
        for i in range(int(len(keyData[:,1]))):
                if str(int(keyData[i,1])) not in VehTrajectory:
                        VehTrajectory[str(int(keyData[i,1]))]=keyData[i,[0,2,3]]
                else:
                        VehTrajectory[str(int(keyData[i,1]))]=vstack((VehTrajectory[str(int(keyData[i,1]))],keyData[i,[0,2,3]]))
        return VehTrajectory

## Identify GPS vehicles
## Construct DataTimeSelected dictionary, DataTimeSelected is a subset of DataTime, when GPS vehicles present
def getGPSDataTime(headway, DataTime):       
        DataTimeSelected=dict()
        GPSlist=[]
        for i in list(DataTime):
                if mod(int(i),headway)==0:
                        try:
                                j=DataTime[i][:,1].argmin()
                                GPSlist.append(DataTime[i][j,0])
                        except IndexError:
                                GPSlist.append(DataTime[i][0])
        for i in list(DataTime):
                try:
                        for j in range(len(DataTime[i][:,0])):
                                if DataTime[i][j,0] in GPSlist:
                                        if i not in DataTimeSelected:
                                                DataTimeSelected[i]=DataTime[i][j,:]
                                        else:
                                                DataTimeSelected[i]=vstack((DataTimeSelected[i],DataTime[i][j,:]))
                except IndexError:
                        if DataTime[i][0] in GPSlist:
                                DataTimeSelected[i]=DataTime[i][:]
        return GPSlist, DataTimeSelected


## Calculate cellDensity
def calculateCellDensity(SimulationTime, TimeInterval, cellNumber, keyData, spaceStep,length):       
        NoVeh=zeros((int(SimulationTime/TimeInterval),cellNumber))
        for k in range(int(len(keyData[:,0]))):
                if mod(int(keyData[k,0]),TimeInterval)==0:
                        if keyData[k,2]>=length*5280:
                                pass
                        else:
                                j=int(keyData[k,2]/(spaceStep*5280))
                                NoVeh[int(keyData[k,0])/TimeInterval,j]=NoVeh[int(keyData[k,0])/TimeInterval,j]+1
        cellDensity=NoVeh/spaceStep
        return NoVeh, cellDensity


## Construct TimeCell dictionary Key-Value(Key)-Value time->cells->[vehID,speed]
def calculateTimeCell(DataTime,spaceStep,length):
        TimeCell=dict()
        for i in list(DataTime):
                CellVehSpeed=dict()
                try:
                        for j in range(len(DataTime[i][:,1])):
                                position=DataTime[i][j,1]
                                if position>=length*5280:
                                        pass
                                else:                                       
                                        cell=int(position/(spaceStep*5280))
                                        if str(cell) not in CellVehSpeed:
                                                CellVehSpeed[str(cell)]=DataTime[i][j,[0,2]]
                                        else:
                                                CellVehSpeed[str(cell)]=vstack((CellVehSpeed[str(cell)],DataTime[i][j,[0,2]]))
                except IndexError:
                        position=DataTime[i][1]
                        if position>=length*5280:
                                pass
                        else:
                                cell=int(position/(spaceStep*5280))
                                if str(cell) not in CellVehSpeed:
                                        CellVehSpeed[str(cell)]=DataTime[i][[0,2]]
                                else:
                                        CellVehSpeed[str(cell)]=vstack((CellVehSpeed[str(cell)],DataTime[i][[0,2]]))                       
                TimeCell[i]=CellVehSpeed
        return TimeCell

## Calculate cellSpeed
def calculateCellSpeed(SimulationTime, TimeInterval, cellNumber, TimeCell):       
        cellSpeed=zeros((int(SimulationTime/TimeInterval),cellNumber))
        for i in list(TimeCell):
                if mod(int(i),TimeInterval)==0:
                        for j in list(TimeCell[i]):
                                try:
                                        cellSpeed[int(i)/TimeInterval,int(j)]=average(TimeCell[i][j][:,1])
                                except IndexError:
                                        cellSpeed[int(i)/TimeInterval,int(j)]=TimeCell[i][j][1]
        return cellSpeed




## Here starts the main code


Vmax=65.0
length=4.0

TimeInterval=20
timeStep=TimeInterval/3600.0
SimulationTime=3800

spaceStep=Vmax*timeStep
cellNumber=floor(length/spaceStep)
spaceStep=length/cellNumber ## this is unitLength in terms of mile

## This is the penetration rate value
headway=20


DataTime=buildDataTime(keyData)
print 'Finish DataTime'

VehTrajectory=buildVehTrajectory(keyData)
print 'Finish vehTrajectory'

GPSlist, GPSDataTime=getGPSDataTime(headway, DataTime)
print 'Finish GPSDataTime'

NoVeh, cellDensity=calculateCellDensity(SimulationTime, TimeInterval, cellNumber, keyData, spaceStep,length)
print 'Finish cellDensity'

TimeCell=calculateTimeCell(GPSDataTime, spaceStep, length)
print 'Finish TimeCell'


cellSpeed=calculateCellSpeed(SimulationTime, TimeInterval, cellNumber, TimeCell)
print 'Finish cellSpeed'



save(str(flow)+'RawDensity'+str(headway), cellDensity)
save(str(flow)+'RawSpeed'+str(headway), cellSpeed)


#### Here ends the main code

vehID=list(VehTrajectory)

plt.hold(True)
for i in vehID:
        try:
                plt.plot(VehTrajectory[i][:,0],VehTrajectory[i][:,1])
        except IndexError:
                ## vehicle trajectory may contain single dot, for example, a vehicle enters at the end of the simulation
                pass
plt.xlabel('Time')
plt.ylabel('Space')
plt.savefig('Raw'+filename+str(headway)+'diagram.pdf')
plt.hold(False)
plt.clf()


imgplot1=plt.imshow(cellDensity,aspect='auto',origin='lower',interpolation='none')
plt.ylabel('Time Step')
plt.xlabel('Cell Number')
plt.colorbar()
##plt.show()
plt.savefig('TrueDensity.pdf')
plt.clf()


imgplot2=plt.imshow(cellSpeed,aspect='auto',origin='lower',interpolation='none')
plt.ylabel('Time Step')
plt.xlabel('Cell Number')
plt.colorbar()
##plt.show()
plt.savefig('Raw'+filename+str(headway)+'Speed.pdf')
plt.clf()
