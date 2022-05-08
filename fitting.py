# fitting.py
# Topic: Do fitting to get the width and the interval of double-slits
# Author: Mu-Hsin Chang
# Date: 2022-05-08

import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy.optimize import curve_fit

#read data from csv file
with open('data.csv', 'r') as f:
    row = f.read().splitlines() #kick out '\n' and make a list 

x = [] #position data
y = [] #luminous data
y_N = [] #normalized luminous
counter = 0
N_factor = 0.

for i in row:
    data = i.split(",") #kick out ',' and make a list
    x.append(float(data[0])) #change string into float type
    y.append(float(data[1]))
    
    #find maximum to do normalize later
    if y[counter] > N_factor:
        N_factor = y[counter]
    counter+=1

#Normalization
counter = 0
for i in y:
    y_N.append(y[counter]/N_factor)
    counter+=1

#Fitting fuction definition
def fit(X,p0,p1):
    C = np.pi * 1.E+3 / (630.*5.)
    cos_part = pow(np.cos(C * p0 * X),2)
    sin_part = pow(np.sin(C * p1 * X),2)
    bot_part = pow((C * p1 * X),2)
    Y = cos_part * (sin_part / bot_part)
    return Y
    
#Fitting
popt, pcov = curve_fit(fit,x,y_N)
print(popt) #fitting result: popt[0]=d, popt[1]=a
print(pcov) #covariance

#y data for fitting curve
#use to draw in the canvas later
y_Fit = []
counter = 0
for i in x:
    y_Fit.append(fit(x[counter],popt[0],popt[1]))
    counter+=1

#Plot
fig = plt.figure(figsize=(10,8)) #canvas size
plt.scatter(x,y_N,color='k',marker='o',label='data') #data

d = '\nd: %.4f' % popt[0]
a = '\na: %.4f' % popt[1]
plt.plot(x,y_Fit,color='r',label='fitting curve'+d+a) #fitting curve

#Decorate
plt.xlabel('Position of optical fiber [mm]')
plt.ylabel('Normalized luminous')
ax = plt.gca() #get canvas axis
ax.set_xlim(-22.,22.)
ax.set_ylim(0,1.2)
plt.legend(loc='best')
plt.tight_layout()

#Show the plot
plt.show()
