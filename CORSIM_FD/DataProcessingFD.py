import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy import *
from random import choice
from random import sample
from copy import deepcopy

## process KeyData for fundamental diagram calibration.
## notation is the same as KeyDataProcessingPR.The only difference is this file assumes full penetation rate.

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

def buildFD(cellDensity,cellSpeed,CELL):
        FD=zeros((10000000,2))
        m=0
        for i in range(len(cellDensity[:,0])):
                for j in range(int(CELL)):
                        FD[m,:]=[cellDensity[i,j],cellSpeed[i,j]]
                        m=m+1
        for i in reversed(range(len(FD[:,0]))):
                if FD[i,0] != 0:
                        FD=FD[0:i+1,:].copy()
                        break
        return FD


## Here starts the main code

FileList=['3laneF5000S65','3laneF5000S60','3laneF5000S50','3laneF5000S40','3laneF5000S30','3laneF5000S20','3laneF5000S10','3laneF5000S5','3laneF5000S1','3laneF4000S65','3laneF3000S65','3laneF2000S65','3laneF1000S65','3laneF500S65']

NUM=1
for filename in FileList:
        print 'This is file', NUM
        NUM=NUM+1

        keyData=load(filename+'key.npy')

        Vmax=65.0  
        length=1.0 

        TimeInterval=20
        timeStep=TimeInterval/3600.0
        SimulationTime=3600

        spaceStep=Vmax*timeStep
        cellNumber=floor(length/spaceStep)
        spaceStep=length/cellNumber

        CELL=1

        

        DataTime=buildDataTime(keyData)
        print 'Finish DataTime'

        VehTrajectory=buildVehTrajectory(keyData)
        print 'Finish vehTrajectory'

        NoVeh, cellDensity=calculateCellDensity(SimulationTime, TimeInterval, cellNumber, keyData, spaceStep,length)
        print 'Finish cellDensity'

        TimeCell=calculateTimeCell(DataTime, spaceStep, length)
        print 'Finish TimeCell'

        cellSpeed=calculateCellSpeed(SimulationTime, TimeInterval, cellNumber, TimeCell)
        print 'Finish cellSpeed'

        FD=buildFD(cellDensity, cellSpeed, CELL)
        print 'Finish FD'


        save(filename+'FD',FD)
        save(filename+'densityData',cellDensity)
        save(filename+'speedData',cellSpeed)


        #### Here ends the main code

        vehID=list(VehTrajectory)

        plt.hold(True)
        for i in vehID:
                try:
                        plt.plot(VehTrajectory[i][:,0],VehTrajectory[i][:,1])
                except IndexError:
                        pass
        plt.xlabel('Time')
        plt.ylabel('Space')
        plt.savefig(filename+'diagram.pdf')
        plt.hold(False)
        plt.clf()


        imgplot2=plt.imshow(cellDensity,aspect='auto',origin='lower',interpolation='none')
        plt.ylabel('Time Step')
        plt.xlabel('Cell Number')
        plt.colorbar()
        plt.savefig(filename+'Density.pdf')
        ##plt.show()
        plt.clf()

        imgplot3=plt.imshow(cellSpeed,aspect='auto',origin='lower',interpolation='none')
        plt.ylabel('Time Step')
        plt.xlabel('Cell Number')
        plt.colorbar()
        plt.savefig(filename+'Speed.pdf')
        ##plt.show()
        plt.clf()

