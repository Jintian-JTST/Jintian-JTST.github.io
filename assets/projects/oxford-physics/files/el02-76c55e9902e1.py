import numpy as np
import pandas as pd

df = pd.read_csv('RC.csv')
f=df.freq.values
v1=df.mv1.values
v2=df.mv2.values

import matplotlib.pyplot as plt
plt.scatter(f,v1, label='v1', color='blue')
plt.scatter(f,v2, label='v2', color='orange')
plt.xscale('log')
plt.title('Voltages V1 and V2 vs Frequency')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Voltage (V)')
plt.legend()
plt.savefig('EL02_Voltages.png')

plt.clf()
T2=(v2/v1)**2
plt.scatter(f,T2, label='T2', color='green')
plt.xscale('log')
plt.title('Transmission T2 vs Frequency')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Transmission T2')
plt.legend()
plt.savefig('EL02_T2.png')

dT2=(2/(12**0.5))*(v2**4/v1**6+v2**2/v1**4)**0.5
print(dT2)


from scipy.optimize import curve_fit
def RCfit1(f, a, c):
    return 1/(a+c*f**2)
p0=1,1.3e-6
popt,pcov=curve_fit(RCfit1, f, T2, p0, sigma=dT2)
print('a: ' +str(popt[0])+' c: '+str(popt[1]))
print('Errors(a,c): '+ str(np.sqrt(np.diag(pcov))))
print(popt+1.959964*np.sqrt(pcov.diagonal()))
print(popt-1.959964*np.sqrt(pcov.diagonal()))
