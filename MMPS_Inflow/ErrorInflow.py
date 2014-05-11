import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy import *
from random import choice
from copy import deepcopy


TrueParameter=load('TrueParameter.npy')
TrueDensity7000=load('TrueDensity.npy')
TrueDensity6000=load('6000RawDensity20.npy')
TrueDensity5000=load('5000RawDensity20.npy')
TrueDensity4000=load('4000RawDensity20.npy')
TrueDensity3000=load('3000RawDensity20.npy')
TrueDensity2000=load('2000RawDensity20.npy')
TrueDensity1000=load('1000RawDensity20.npy')


TrueParameter=TrueParameter[0:180:]
TrueDensity7000=TrueDensity7000[0:180,:]
TrueDensity6000=TrueDensity6000[0:180,:]
TrueDensity5000=TrueDensity5000[0:180,:]
TrueDensity4000=TrueDensity4000[0:180,:]
TrueDensity3000=TrueDensity3000[0:180,:]
TrueDensity2000=TrueDensity2000[0:180,:]
TrueDensity1000=TrueDensity1000[0:180,:]



Sdensity7000=load('Result20WS1StateEstimate.npy')
Sdensity6000=load('6000Result20WS1StateEstimate.npy')
Sdensity5000=load('5000Result20WS1StateEstimate.npy')
Sdensity4000=load('4000Result20WS1StateEstimate.npy')
Sdensity3000=load('3000Result20WS1StateEstimate.npy')
Sdensity2000=load('2000Result20WS1StateEstimate.npy')
Sdensity1000=load('1000Result20WS1StateEstimate.npy')


Sparameter7000=load('Result20WS1ParameterEstimate.npy')
Sparameter6000=load('6000Result20WS1ParameterEstimate.npy')
Sparameter5000=load('5000Result20WS1ParameterEstimate.npy')
Sparameter4000=load('4000Result20WS1ParameterEstimate.npy')
Sparameter3000=load('3000Result20WS1ParameterEstimate.npy')
Sparameter2000=load('2000Result20WS1ParameterEstimate.npy')
Sparameter1000=load('1000Result20WS1ParameterEstimate.npy')



SErrorD7000=average(abs(Sdensity7000-TrueDensity7000))
SErrorD6000=average(abs(Sdensity6000-TrueDensity6000))
SErrorD5000=average(abs(Sdensity5000-TrueDensity5000))
SErrorD4000=average(abs(Sdensity4000-TrueDensity4000))
SErrorD3000=average(abs(Sdensity3000-TrueDensity3000))
SErrorD2000=average(abs(Sdensity2000-TrueDensity2000))
SErrorD1000=average(abs(Sdensity1000-TrueDensity1000))

SErrorP7000=sum(abs(Sparameter7000-TrueParameter))
SErrorP6000=sum(abs(Sparameter6000-TrueParameter))
SErrorP5000=sum(abs(Sparameter5000-TrueParameter))
SErrorP4000=sum(abs(Sparameter4000-TrueParameter))
SErrorP3000=sum(abs(Sparameter3000-TrueParameter))
SErrorP2000=sum(abs(Sparameter2000-TrueParameter))
SErrorP1000=sum(abs(Sparameter1000-TrueParameter))

plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)
plt.hold(True)
StateWS=plt.plot([7000,6000,5000,4000,3000,2000,1000],[SErrorD7000,SErrorD6000,SErrorD5000,SErrorD4000,SErrorD3000,SErrorD2000,SErrorD1000],marker='v',linestyle='-',color='b',label='$e_x$')
ParameterWS=plt.plot([7000,6000,5000,4000,3000,2000,1000],[SErrorP7000,SErrorP6000,SErrorP5000,SErrorP4000,SErrorP3000,SErrorP2000,SErrorP1000],marker='d',linestyle='--',color='r',label='$e_\gamma$')
plt.legend(loc=1,prop={'size':20})
plt.xlim([0,8000])
plt.ylim([0,200])
plt.xlabel('Inflow (veh/h)',fontsize=20)
plt.ylabel('Error',fontsize=20)
plt.savefig('AllInflowError.pdf',bbox_inches='tight')
plt.show()
plt.hold(False)
