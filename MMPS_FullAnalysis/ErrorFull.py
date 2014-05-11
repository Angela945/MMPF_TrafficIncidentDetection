import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy import *
from random import choice
from copy import deepcopy

TrueParameter=load('TrueParameter.npy')
TrueParameter=TrueParameter[0:180:]

ErrorS20=zeros(10)
ErrorS40=zeros(10)
ErrorS60=zeros(10)
ErrorS80=zeros(10)
ErrorS100=zeros(10)
ErrorS120=zeros(10)

ErrorP20=zeros(10)
ErrorP40=zeros(10)
ErrorP60=zeros(10)
ErrorP80=zeros(10)
ErrorP100=zeros(10)
ErrorP120=zeros(10)

SErrorS20=zeros(10)
SErrorS40=zeros(10)
SErrorS60=zeros(10)
SErrorS80=zeros(10)
SErrorS100=zeros(10)
SErrorS120=zeros(10)

SErrorP20=zeros(10)
SErrorP40=zeros(10)
SErrorP60=zeros(10)
SErrorP80=zeros(10)
SErrorP100=zeros(10)
SErrorP120=zeros(10)


smoothing='NS'
for headway in [20,40,60,80,100,120]:
    for GPSvariation in range(10):
        TrueDensity=load('RawDensity'+str(headway)+str(GPSvariation)+'.npy')
        TrueDensity=TrueDensity[0:180:]
        DensityFocus=load('Result'+str(headway)+str(GPSvariation)+smoothing+'StateEstimate'+'.npy')
        ParameterFocus=load('Result'+str(headway)+str(GPSvariation)+smoothing+'ParameterEstimate'+'.npy')
        ErrorS=average(abs(DensityFocus-TrueDensity))
        ErrorP=sum(abs(ParameterFocus-TrueParameter))
        if headway==20:
            ErrorS20[GPSvariation]=ErrorS
            ErrorP20[GPSvariation]=ErrorP
        elif headway==40:
            ErrorS40[GPSvariation]=ErrorS
            ErrorP40[GPSvariation]=ErrorP
        elif headway==60:
            ErrorS60[GPSvariation]=ErrorS
            ErrorP60[GPSvariation]=ErrorP
        elif headway==80:
            ErrorS80[GPSvariation]=ErrorS
            ErrorP80[GPSvariation]=ErrorP
        elif headway==100:
            ErrorS100[GPSvariation]=ErrorS
            ErrorP100[GPSvariation]=ErrorP
        elif headway==120:
            ErrorS120[GPSvariation]=ErrorS
            ErrorP120[GPSvariation]=ErrorP

for headway in [20,40,60,80,100,120]:
    smoothing='WS4'
    lag=4
    for GPSvariation in range(10):
        TrueDensity=load('RawDensity'+str(headway)+str(GPSvariation)+'.npy')
        TrueDensity=TrueDensity[0:180:]
        DensityFocus=load('Result'+str(headway)+str(GPSvariation)+smoothing+'StateEstimate'+'.npy')
        ParameterFocus=load('Result'+str(headway)+str(GPSvariation)+smoothing+'ParameterEstimate'+'.npy')
        ErrorS=average(abs(DensityFocus-TrueDensity))
        ErrorP=sum(abs(ParameterFocus-TrueParameter))
        if headway==20:
            SErrorS20[GPSvariation]=ErrorS
            SErrorP20[GPSvariation]=ErrorP
        elif headway==40:
            SErrorS40[GPSvariation]=ErrorS
            SErrorP40[GPSvariation]=ErrorP
        elif headway==60:
            SErrorS60[GPSvariation]=ErrorS
            SErrorP60[GPSvariation]=ErrorP
        elif headway==80:
            SErrorS80[GPSvariation]=ErrorS
            SErrorP80[GPSvariation]=ErrorP
        elif headway==100:
            SErrorS100[GPSvariation]=ErrorS
            SErrorP100[GPSvariation]=ErrorP
        elif headway==120:
            SErrorS120[GPSvariation]=ErrorS
            SErrorP120[GPSvariation]=ErrorP
    



plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)
plt.hold(True)
StateNS=plt.plot([20,40,60,80,100,120],[average(ErrorS20),average(ErrorS40),average(ErrorS60),average(ErrorS80),average(ErrorS100),average(ErrorS120)],marker='v',linestyle='--',color='r',label='$e_x$ filter')
ParameterNS=plt.plot([20,40,60,80,100,120],[average(ErrorP20),average(ErrorP40),average(ErrorP60),average(ErrorP80),average(ErrorP100),average(ErrorP120)],marker='d',linestyle='-.',color='r',label='$e_\gamma$ filter')
StateWS=plt.plot([20,40,60,80,100,120],[average(SErrorS20),average(SErrorS40),average(SErrorS60),average(SErrorS80),average(SErrorS100),average(SErrorS120)],marker='v',linestyle=':', color='b',label='$e_x$ smoother')
ParameterWS=plt.plot([20,40,60,80,100,120],[average(SErrorP20),average(SErrorP40),average(SErrorP60),average(SErrorP80),average(SErrorP100),average(SErrorP120)],marker='d',linestyle='-', color='b',label='$e_\gamma$ smoother')
plt.legend(loc=1,prop={'size':20})
plt.xlim([10,130])
plt.ylim([0,350])
plt.xlabel('Headway (seconds)',fontsize=20)
plt.ylabel('Error',fontsize=20)
plt.savefig('AllError.pdf',bbox_inches='tight')
plt.show()
plt.hold(False)
