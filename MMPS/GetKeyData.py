from numpy import *
from copy import deepcopy

## This file extracts data from CORSIM trajectory file
## The trajectory file is saved as keyData. [TimeIndex, VehID, VehPosition, Speed] 

filename='3lane1blockS65F7000'


keyData=zeros((10000000,4))
k=0 ##denote iteration
m=0 ##denote keyData index
f=open(filename+'.txt','r')
for line in f:
        k=k+1
        if mod(k,500)==0:
                print 'This is iteration', k
        initialList=[]
        myFocus = line.split()
        myFocus = [int(i) for i in myFocus]
        if len(myFocus)<10:
                pass
        else:
                for i in range(int(len(myFocus))):
                        if i==3:
                                initialList.append(myFocus[i])
                        elif mod((i-18),19)==0:
                                if i+10>len(myFocus):
                                        pass
                                else:
                                        currentList=list(initialList)
                                        currentList.append(myFocus[i])
                                        currentList.append(myFocus[i+7])
                                        currentList.append(myFocus[i+12]*3600/5280.0)
                                        keyData[m,:]=array(currentList)
                                        m=m+1
for i in reversed(range(len(keyData[:,0]))):
        if keyData[i,3]!=0:
                keyData=keyData[0:i+1,:].copy()
                break


save(filename+'Key',keyData)
