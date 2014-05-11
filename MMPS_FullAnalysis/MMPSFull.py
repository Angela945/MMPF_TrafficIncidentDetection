import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D
from numpy import *
from random import choice
from copy import deepcopy


## This upper class defines all the inputs for the model
class Input(object):
        def __init__(self):
                self.noiseCTM=1.0
                self.noiseDensityMea=7.5
                self.noiseVelocityMea=4.4
                self.mu=0.0
                
## set the numerical simulation
                self.sample=1000
                self.timeStepNumber=180
                self.laneNumber=3.0

        def setLeftGhost(self,counter):
                self.leftGhost=6900+random.normal(0,250)
                return self.leftGhost
        
                
class Link(Input):
        def __init__(self):
                Input.__init__(self)
## Define the traffic parameters for the fundamental diagram(1 lane open)
                self.qmax=2400.0
                self.JamDensity=240.0
                self.Vmax=65.0

## Define the geometry of the road
                self.length=4.0
                self.timeStep=20.0/3600.0

                self.computeParameter()
                self.initializeGamma()
                self.initializeDensity(inputDensity)
                self.initializeSpeed(inputSpeed)
                self.getRegimeNumber()

## This function computes the parameter (delta X and delta T) of the traffic model               
        def computeParameter(self):
                self.CriticalDensity=self.qmax/self.Vmax
                self.spaceStep=self.Vmax*self.timeStep
                self.cellNumber=floor(self.length/self.spaceStep)
                self.spaceStep=self.length/self.cellNumber

## This function initializes the regime varialbe Gamma (number of lanes open at each discretized location)
        def initializeGamma(self):
                self.vectorGamma=self.laneNumber*ones((self.sample,1,self.cellNumber))
                self.vectorGammaInitial=self.vectorGamma.copy()

## This function initializes the density condition along the freeway
        def initializeDensity(self,inputDensity):
                self.cellDensity=zeros((self.sample,1,self.cellNumber))
                densitySensor=[1,self.cellNumber-2]
                mean=(inputDensity[0,1]+inputDensity[0,self.cellNumber-2])/2
                std=mean*0.05
                for i in range(int(self.sample)):
                        for j in range(len(self.cellDensity[i,0,:])):
                                self.cellDensity[i,0,j]=random.normal(mean, std)
                self.updateCellDensity=zeros((self.sample,1,self.cellNumber))

## This function initializes velocity for each cell                
        def initializeSpeed(self,inputSpeed):
                self.cellSpeed=zeros((self.sample,1,self.cellNumber))

## This function define the right boundary condition of the traffic model
        def setRightGhost(self):
                self.rightGhost=inf
                return self.rightGhost

## This is the sending function of CTM
        def sending(self, density, gamma):
                CriticalDensity=self.qmax*gamma/self.Vmax
                JamDensity=gamma*self.JamDensity

                if density<0:
                        density=0.001 ## this is to avoid numerical issue if the model noise makes the density smaller than 0
                if density<=CriticalDensity:
                        qSend=density*self.Vmax
                else:
                        qSend=self.qmax*gamma
                if qSend<0:
                        print 'qSend is small than 0, sth is wrong with the CTM, please check'
                        print 'the qSend value is', qSend
                return qSend

## This is the receiving function of CTM
        def receiving(self, density, gamma):
                CriticalDensity=self.qmax*gamma/self.Vmax
                JamDensity=gamma*self.JamDensity
                
                if density>JamDensity:
                        density=JamDensity-0.001  ## this is to avoid numerical issue if density is greater than jam density
                if gamma==1.0:
                        a=-0.0582
                        b=4.31
                        c=2320.27
                elif gamma==2.0:
                        a=-0.02911
                        b=4.31
                        c=4640.53
                else:
                        a=-0.0194
                        b=4.31
                        c=6960.80
                
                if density<=CriticalDensity:
                        qReceive=gamma*self.qmax
                else:
                        qReceive=a*density*density+b*density+c
                if qReceive<0:
                        print 'qReceive is small than 0, sth is wrong with the CTM, please check'
                        print 'the qReceive value is', qReceive
                return qReceive

## This function describes the density evolution of the CTM model 
        def updateDensity(self, counter,inputDensity):
                for j in range(self.sample):
                        for i in range(0,int(self.cellNumber)):
                                if i==0:
                                        self.updateCellDensity[j,0,i]=self.cellDensity[j,0,i]+(self.timeStep/self.spaceStep)*\
                                                               (min(self.setLeftGhost(counter),self.receiving(self.cellDensity[j,0,i],self.vectorGamma[j,0,i]))-\
                                                                min(self.sending(self.cellDensity[j,0,i],self.vectorGamma[j,0,i]),self.receiving(self.cellDensity[j,0,i+1],self.vectorGamma[j,0,i+1])))
                                elif i>0 and i<int(self.cellNumber-1):
                                        self.updateCellDensity[j,0,i]=self.cellDensity[j,0,i]+(self.timeStep/self.spaceStep)*\
                                                               (min(self.sending(self.cellDensity[j,0,i-1],self.vectorGamma[j,0,i-1]),self.receiving(self.cellDensity[j,0,i],self.vectorGamma[j,0,i]))-\
                                                                min(self.sending(self.cellDensity[j,0,i],self.vectorGamma[j,0,i]),self.receiving(self.cellDensity[j,0,i+1],self.vectorGamma[j,0,i+1])))
                                else:
                                        self.updateCellDensity[j,0,i]=self.cellDensity[j,0,i]+(self.timeStep/self.spaceStep)*\
                                                               (min(self.sending(self.cellDensity[j,0,i-1],self.vectorGamma[j,0,i-1]),self.receiving(self.cellDensity[j,0,i],self.vectorGamma[j,0,i]))-\
                                                                min(self.sending(self.cellDensity[j,0,i],self.vectorGamma[j,0,i]),self.setRightGhost()))
                self.cellDensity=self.updateCellDensity.copy()+random.normal(self.mu, self.noiseCTM,(self.sample,1,self.cellNumber))

## This function computes the speed at each cell
        def updateSpeed(self):
                for j in range(int(self.sample)):
                        for i in range(int(self.cellNumber)):
                                gamma=self.vectorGamma[j,0,i]
                                CriticalDensity=self.qmax*gamma/self.Vmax
                                JamDensity=gamma*self.JamDensity
                                if gamma==1.0:
                                        a=-0.0582
                                        b=4.31
                                        c=2320.27
                                elif gamma==2.0:
                                        a=-0.02911
                                        b=4.31
                                        c=4640.53
                                else:
                                        a=-0.0194
                                        b=4.31
                                        c=6960.80
                                if self.cellDensity[j,0,i]<CriticalDensity:
                                        self.cellSpeed[j,0,i]=self.Vmax
                                else:
                                        self.cellSpeed[j,0,i]=(a*self.cellDensity[j,0,i]*self.cellDensity[j,0,i]+b*self.cellDensity[j,0,i]+c)/self.cellDensity[j,0,i]

## This function computes the toal number of regime the system could have
        def getRegimeNumber(self):
                self.regimeNumber=(self.cellNumber-4.0)*(self.laneNumber-1)+1

## Given the Gammavector, this function tells which regime the system is on
        def gammaToReg(self, gammaCell):
                regime=1  ## when regime is 1, it indicates no incident
                for i in range(int(self.cellNumber)):
                        if gammaCell[i] != self.laneNumber:
                                regime=i
                return regime                                        

## This function describes the transition of regime variable (switching between incident and no incident)		
        def regimeTransition(self, Ptran):
                for i in range(self.sample):
                        regime=self.gammaToReg(self.vectorGamma[i,0,:])
                        if regime==1:
                                if random.random()>Ptran:
                                        incidentPosition=int((self.cellNumber-4)*random.random()+2)
                                        if self.laneNumber==3.0:
                                                self.vectorGamma[i,0,incidentPosition]=choice([1.0, 2.0])
                                        elif self.laneNumber==2.0:
                                                self.vectorGamma[i,0,incidentPosition]=1.0
                                else:
                                        pass
                        else:
                                if random.random()>Ptran:
                                        self.vectorGamma[i,0,:]=self.vectorGammaInitial[i,0,:]
                                else:
                                        pass



if __name__ == '__main__':


## This function specifies the position where sensors are available
        def SensorLocationDensity(ScellNumber):
                DensitySensorLocation=[1, ScellNumber-2]
                return DensitySensorLocation

## This function initilizes weight for each particle
        def initializeWeight(Ssample):
                Weight=ones((Ssample))/Ssample
                return Weight
        
## This function calculates the likelihood of each particle        
        def calculateLikelihood(ScellDensity, XcellDensity,ScellSpeed, XcellSpeed,mu,stdD,stdS,ScellNumber,Ssample,SensorLocationSpeed, SensorLocationDensity):
                DifferenceDensity=XcellDensity-ScellDensity
                DifferenceSpeed=XcellSpeed-ScellSpeed
                likelihoodDensity=1/(stdD*sqrt(2*pi))*exp(-(DifferenceDensity-mu)*(DifferenceDensity-mu)/(2*stdD*stdD))
                likelihoodSpeed=1/(stdS*sqrt(2*pi))*exp(-(DifferenceSpeed-mu)*(DifferenceSpeed-mu)/(2*stdS*stdS))
                likelihood=ones((Ssample, 1, ScellNumber))
                for i in SensorLocationSpeed:
                        likelihood[:,:,i]=likelihoodSpeed[:,:,i]
                for j in SensorLocationDensity:
                        pass
                        if likelihood[0,0,j]==1:
                                likelihood[:,:,j]=likelihoodDensity[:,:,j]
                        else:
                                likelihood[:,:,j]=likelihoodDensity[:,:,j]*likelihoodSpeed[:,:,j]
                return likelihood

## This function updates the weight 
        def updateWeight(likelihood, Ssample, Weight):
                WeightCopy=Weight.copy()
                for i in range(int(Ssample)):
##                        print likelihood[i,0,:]
                        Weight[i]=exp(sum(log(likelihood[i,0,:])))*WeightCopy[i]
                return Weight

## This function calculates the cumulative distribtuion of weigh (used for resampling)
        def calculateCum(ScellNumber,Ssample,Weight):
                Sum=0
                Cum=zeros((Ssample))
                Sum=sum(Weight)
##                print Sum
                for i in range((int(Ssample))):
                        Weight[i]=Weight[i]/float(Sum)
                Cum=cumsum(Weight)
                return (Cum, Weight)

## This function does resampling
        def resampling(Ssample, ScellNumber, ScellDensity, Cum, gammaDistribution):
                cellDensityStore=ScellDensity.copy()
                gammaDistributionStore=gammaDistribution.copy()
                
                addit=1.0/s.sample
                stt=addit
                selection_points=linspace(stt,stt+(Ssample-1)*addit,Ssample)
                m=0
##                print 'Cum', Cum
##                print 'selection', selection_points
                for n in range(int(s.sample)):
                        while m<Ssample:
                                if selection_points[n]>Cum[m]+0.0000001:
                                        m=m+1
                                        if m==s.sample:
                                                print 'no particle matches the measurements at iteration:',counter
                                else:
                                        ScellDensity[n,0,:]=cellDensityStore[m,0,:]
                                        gammaDistribution[n]=gammaDistributionStore[m]
                                        break
                return (ScellDensity,gammaDistribution)


        def SpeedSensorLocation(TimeStep, cellNumber, cellSpeed):
                speedSensorLocation=dict()
                for i in range(int(TimeStep)):
                        for j in range(int(cellNumber)):
                                if cellSpeed[i,j] != 0:
                                        if i not in speedSensorLocation:
                                                speedSensorLocation[i]=[j]
                                        else:
                                                speedSensorLocation[i].append(j)
                return speedSensorLocation


#### main code starts here:
## need to specify the headway, smoothing and lag.
## specify NS or WS+number, the number is the value of lag.
        
        Ptran=0.99

        for smoothing in ['NS','WS']:
                for headway in [20,40,60,80,100,120]:
                        if smoothing !='NS':
                                smoothing='WS4'
                                lag=4
                        for GPSvariation in range(10):
                                inputDensity=load('RawDensity'+str(headway)+str(GPSvariation)+'.npy')
                                inputSpeed=load('RawSpeed'+str(headway)+str(GPSvariation)+'.npy')
        
                                densityMea=inputDensity
                                speedMea=inputSpeed
                                
                                
                                s=Link()
                                VelocitySensorLocation=SpeedSensorLocation(s.timeStepNumber,s.cellNumber, inputSpeed)
                                DensitySensorLocation=SensorLocationDensity(s.cellNumber)
                                Weight=initializeWeight(s.sample)

                                stateEstimate=zeros((s.timeStepNumber,s.cellNumber))
                                stateEstimate[0,:]=average(s.cellDensity,axis=0)

                                parameterEstimate=zeros((s.timeStepNumber,s.cellNumber))
                                parameterEstimate[0,:]=average(s.vectorGamma,axis=0)

                                for counter in range(1, s.timeStepNumber-1):
                                        if mod(counter,20)==0:
                                                print 'This is time iteration', counter
                                        if counter>20:
                                                s.regimeTransition(Ptran)

                                        s.updateDensity(counter,inputDensity)
                                        s.updateSpeed()

                                        Sdensity=s.cellDensity.copy()
                                        gammaDistribution=s.vectorGamma.copy()

                                        likelihood=calculateLikelihood(s.cellDensity, densityMea[counter,:],s.cellSpeed, speedMea[counter,:],s.mu, s.noiseDensityMea, s.noiseVelocityMea ,s.cellNumber,s.sample,VelocitySensorLocation[counter], DensitySensorLocation)
                                        Weight=updateWeight(likelihood, s.sample, Weight)
                                        Cum, Weight=calculateCum(s.cellNumber,s.sample,Weight)

                                        
                        ## Here starts the smoothing algorithm
                                        if smoothing != 'NS':
                                                if counter < s.timeStepNumber-5:
                                                        for i in range(lag):
                                                                s.updateDensity(counter+i+1,inputDensity)
                                                                s.updateSpeed()
                                                                VelocitySensorLocationSmooth=deepcopy(VelocitySensorLocation[counter+i+1])

                                                                likelihood=calculateLikelihood(s.cellDensity, densityMea[counter+i+1], s.cellSpeed, speedMea[counter+i+1],s.mu, s.noiseDensityMea, s.noiseVelocityMea, s.cellNumber,s.sample,VelocitySensorLocationSmooth, DensitySensorLocation)
                                                                Weight=updateWeight(likelihood, s.sample, Weight)
                                                                Cum, Weight=calculateCum(s.cellNumber,s.sample,Weight)
                                                                s.regimeTransition(Ptran)
                        ## Here ends the smoothing algorithm



                                        s.cellDensity=Sdensity.copy()
                                        s.vectorGamma=gammaDistribution.copy()


                                        s.cellDensity, s.vectorGamma=resampling(s.sample, s.cellNumber,s.cellDensity, Cum,s.vectorGamma)

                                        print 'particle filter finishes for iteration', counter




                                        stateEstimate[counter,:]=average(s.cellDensity,axis=0)

                                        parameterEstimate[counter,:]=average(s.vectorGamma,axis=0)

                                        Weight=initializeWeight(s.sample)
                                save('Result'+str(headway)+str(GPSvariation)+smoothing+'StateEstimate',stateEstimate)
                                save('Result'+str(headway)+str(GPSvariation)+smoothing+'ParameterEstimate',parameterEstimate)


## main code ends here




                                ## Plot section starts here                

                                plt.rc('xtick',labelsize=30)
                                plt.rc('ytick',labelsize=30)
                                imgplot=plt.imshow(stateEstimate,aspect='auto',origin='lower',interpolation='none')
                                plt.ylabel('Time Step',fontsize=30)
                                plt.xlabel('Cell Number',fontsize=30)
                                plt.colorbar()
                                plt.savefig('Result'+str(headway)+str(GPSvariation)+smoothing+'Density.pdf',bbox_inches='tight')
                                #plt.show()
                                plt.clf()



                                plt.rc('xtick',labelsize=30)
                                plt.rc('ytick',labelsize=30)
                                imgplot1=plt.imshow(parameterEstimate,aspect='auto',origin='lower',interpolation='none')
                                plt.ylabel('Time Step',fontsize=30)
                                plt.xlabel('Cell Number',fontsize=30)
                                plt.clim(1.0, 3.0)
                                plt.colorbar()
                                plt.savefig('Result'+str(headway)+str(GPSvariation)+smoothing+'Parameter.pdf',bbox_inches='tight')
                                #plt.show()
                                plt.clf()

