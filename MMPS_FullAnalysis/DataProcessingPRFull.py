import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy import *
from random import choice
from random import sample
from copy import deepcopy


filename='3lane1blockS65F7000'
keyData=load(filename+'key.npy')



## Define functions

def buildDataTime(keyData):
        DataTime=dict()
        for i in range(int(len(keyData[:,0]))):
                if str(int(keyData[i,0])) not in DataTime:
                        DataTime[str(int(keyData[i,0]))]=keyData[i,[1,2,3]]
                else:
                        DataTime[str(int(keyData[i,0]))]=vstack((DataTime[str(int(keyData[i,0]))],keyData[i,[1,2,3]]))
        return DataTime

def buildVehTrajectory(keyData):
        VehTrajectory=dict()
        for i in range(int(len(keyData[:,1]))):
                if str(int(keyData[i,1])) not in VehTrajectory:
                        VehTrajectory[str(int(keyData[i,1]))]=keyData[i,[0,2,3]]
                else:
                        VehTrajectory[str(int(keyData[i,1]))]=vstack((VehTrajectory[str(int(keyData[i,1]))],keyData[i,[0,2,3]]))
        return VehTrajectory

def getGPSDataTime(headway, DataTime, GPSvariation):       
        DataTimeSelected=dict()
        GPSlist=[]
        for i in list(DataTime):
                if mod(int(i)-GPSvariation,headway)==0:
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

## This function calculates the cellSpeed, where the TimeCell dictionary is: time->cells->[vehID,speed]
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

def SpeedSensorLocation(SimulationTime, TimeInterval, cellNumber, cellSpeed):
        speedSensorLocation=dict()
        for i in range(int(SimulationTime/TimeInterval)):
                for j in range(int(cellNumber)):
                        if cellSpeed[i,j] != 0:
                                if i not in speedSensorLocation:
                                        speedSensorLocation[i]=[j]
                                else:
                                        speedSensorLocation[i].append(j)
        return speedSensorLocation


## Here starts the main code


Vmax=65.0  
length=4.0 

TimeInterval=20
timeStep=TimeInterval/3600.0
SimulationTime=3800

spaceStep=Vmax*timeStep
cellNumber=floor(length/spaceStep)
spaceStep=length/cellNumber 

headway=100

DataTime=buildDataTime(keyData)
print 'Finish DataTime'

VehTrajectory=buildVehTrajectory(keyData)
print 'Finish vehTrajectory'

NoVeh, cellDensity=calculateCellDensity(SimulationTime, TimeInterval, cellNumber, keyData, spaceStep,length)
print 'Finish cellDensity'


for GPSvariation in range(10):

        
        GPSlist, GPSDataTime=getGPSDataTime(headway, DataTime,GPSvariation)
        print 'Finish GPSDataTime'


        TimeCell=calculateTimeCell(GPSDataTime, spaceStep, length)
        print 'Finish TimeCell'


        cellSpeed=calculateCellSpeed(SimulationTime, TimeInterval, cellNumber, TimeCell)
        print 'Finish cellSpeed'

        save('RawDensity'+str(headway)+str(GPSvariation), cellDensity)
        save('RawSpeed'+str(headway)+str(GPSvariation), cellSpeed)


