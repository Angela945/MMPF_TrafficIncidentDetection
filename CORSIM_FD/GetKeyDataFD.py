from numpy import *
from copy import deepcopy

## This file extracts data from CORSIM trajectory file
## The trajectory file is saved as keyData. [TimeIndex, VehID, VehPosition, Speed]
## This file is different from GetKeyData, In fundamental diagram calibration, a two-link freeway is built.The trajectory file structure is different from 1 link only.

FileList=['3laneF5000S65','3laneF5000S60','3laneF5000S50','3laneF5000S40','3laneF5000S30','3laneF5000S20','3laneF5000S10','3laneF5000S5','3laneF5000S1','3laneF4000S65','3laneF3000S65','3laneF2000S65','3laneF1000S65','3laneF500S65']


NUM=1
for filename in FileList:
        print 'This is file number', NUM
        NUM=NUM+1

        keyData=zeros((10000000,4))
        k=0 ##denote iteration
        m=0 ##denote keyData index
        f=open(filename+'.txt','r')
        for line in f:
                k=k+1
                count=0
                if mod(k,1000)==0:
                        print 'This is iteration', k
                initialList=[]
                myFocus = line.split()
                myFocus = [int(i) for i in myFocus]
                if len(myFocus)<10:
                        pass
                else:
                        for i in range(int(len(myFocus))):
                                if myFocus[i]==3001:
                                        count=count+1
                                if count==2:
                                        if myFocus[i]==3001:
                                                j=i
                                                initialList.append(myFocus[i+2])
                                        elif mod((i-j-17),19)==0:
                                                if myFocus[i+7]<5480 and myFocus[i+12]*3600/5280.0<90:
                                                        currentList=list(initialList)
                                                        currentList.append(myFocus[i])
                                                        currentList.append(myFocus[i+7])
                                                        currentList.append(myFocus[i+12]*3600/5280.0)
                                                        keyData[m,:]=array(currentList)
                                                        m=m+1
                                if count==3:
                                        break

        for i in reversed(range(len(keyData[:,0]))):
                if keyData[i,3]!=0:
                        keyData=keyData[0:i+1,:].copy()
                        break


        save(filename+'Key',keyData)
