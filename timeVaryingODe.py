# -*- coding: utf-8 -*-
"""
Tutorial on how to solve (simulate) ordinary differential equations (ODEs) in Python
Author: Aleksandar Haber 
Webpage tutorial: https://aleksandarhaber.com/solve-differential-equations-with-time-varying-inputs-and-coefficients-in-python/
May 2023
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# define the constants
gConstant=9.81 
lConstant=1
mConstant=5

###############################################################################
# first, let us test the interpolation

timeArray=np.linspace(0,2*np.pi,100)
sinArray=np.sin(timeArray)
plt.plot(timeArray, sinArray)

# interpolate the values
np.interp((timeArray[9]+timeArray[10])/2,timeArray, sinArray)

# compare the interpolated values with sinArray[9] and sinArray[10]
# the interpolated value should be between these two values
###############################################################################
# now simulate the dynamics

startTime=0
endTime=5
timeSteps=1000

# simulation time array 
# we will obtain the solution at the time points defined by 
# the vector simulationTime
simulationTime=np.linspace(startTime,endTime,timeSteps)

# define the force input 
forceInput = np.sin(simulationTime)+np.cos(2*simulationTime)
plt.plot(simulationTime, forceInput)
plt.xlabel('time')
plt.ylabel('Force - [N]')
plt.savefig('inputSequence.png',dpi=600)
plt.show()


# this function defines the state-space model, that is, its right-hand side
# x is the state 
# t is the current time - internal to solver
# timePoints - time points vector necessary for interpolation
# g,l,m constants provided by the user
# forceArray - time-varying input
def stateSpaceModel(x,t,timePoints,g,l,m,forceArray):
    # interpolate input force values
    # depending on the current time
    forceApplied=np.interp(t,timePoints, forceArray)
    # NOTE THAT IF YOU KNOW THE ANALYTICAL FORM OF THE INPUT FUNCTION 
    # YOU CAN JUST WRITE THIS ANALYTICAL FORM AS A FUNCTION OF TIME 
    # for example in our case, we can also write
    # forceApplied=np.sin(t)+np.cos(2*t)
    # and you do not need to specity forceArray as an input to the function
    # HOWEVER, IF YOU DO NOT KNOW THE ANALYTICAL FORM YOU HAVE TO USE OUR APPROACH 
    # AND INTERPOLATE VALUES
    
    # right-side of the state equation
    dxdt=[x[1],-(g/l)*np.sin(x[0])+(1/(m*l))*forceApplied]
    return dxdt

# define the initial state for simulation 
# position and velocity
initialState=np.array([0,0])
# generate the state-space trajectory
solutionState=odeint(stateSpaceModel,initialState,simulationTime,args=(simulationTime,gConstant,lConstant,mConstant,forceInput))


plt.plot(simulationTime, solutionState[:,0],'b',label='x1')
plt.plot(simulationTime, solutionState[:,1],'r',label='x2')
plt.xlabel('time')
plt.ylabel('States')
plt.legend()
plt.savefig('simulationResult.png',dpi=600)
plt.show()

