import sys
import time
import math as m
import numpy as np
import matplotlib.pyplot as mpl
from scipy import interpolate
from scipy.optimize import leastsq
from os import chdir

import IceChronoModule as icm

###Registration of start time
start_time = time.clock()

##Global
list_drillings=['EDC', 'VK', 'TALDICE', 'EDML']
#list_drillings=['EDML']
variables=np.array([])
D={}
DC={}

##Functions
def residuals(var):
    resi=np.array([])
    index=0
    for i,dlabel in enumerate(list_drillings):
        D[dlabel].variables=var[index:index+np.size(D[dlabel].variables)]
        index=index+np.size(D[dlabel].variables)
        D[dlabel].model(D[dlabel].variables)
        resi=np.concatenate((resi,D[dlabel].residuals()))
        for j,dlabel2 in enumerate(list_drillings):
            if j<i:
                resi=np.concatenate((resi,DC[dlabel2+'-'+dlabel].residuals()))
    return resi

##MAIN

##Initialisation
for i,dlabel in enumerate(list_drillings):

#    print dlabel
        
    D[dlabel]=icm.Drilling(dlabel)
    D[dlabel].model(D[dlabel].variables)
    D[dlabel].a_init=D[dlabel].a
    D[dlabel].display_init()
    variables=np.concatenate((variables,D[dlabel].variables))

    for j,dlabel2 in enumerate(list_drillings):
        if j<i:
            DC[dlabel2+'-'+dlabel]=icm.DrillingCouple(D[dlabel2],D[dlabel])
            DC[dlabel2+'-'+dlabel].display_init()


##Optimization
print 'Optimization'
variables,hess,infodict,mesg,ier=leastsq(residuals, variables, full_output=1)
print 'Calculation of confidence intervals'
index=0
for dlabel in list_drillings:
    D[dlabel].variables=variables[index:index+np.size(D[dlabel].variables)]
    D[dlabel].hess=hess[index:index+np.size(D[dlabel].variables),index:index+np.size(D[dlabel].variables)]
    index=index+np.size(D[dlabel].variables)
    D[dlabel].sigma()

###Final display and output
print 'Display of results'
for i,dlabel in enumerate(list_drillings):
    D[dlabel].save()
    D[dlabel].display_final()
    for j,dlabel2 in enumerate(list_drillings):
        if j<i:
            DC[dlabel2+'-'+dlabel].display_final()
            
###Program execution time
print 'program execution time: ', time.clock() - start_time, 'seconds'


