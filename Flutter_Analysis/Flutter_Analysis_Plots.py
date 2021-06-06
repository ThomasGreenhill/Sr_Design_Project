import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import pandas as pd
import os
savedir = os.path.abspath(os.path.dirname(__file__))

#### Extract information from txt file
rawfile = open('%s\\wing_dd_flutter.txt'%(savedir), 'r') # Open the entire file
rawinfo = rawfile.read()         # Read the entire file to string
rawfile.close()         # Close the entire file
rawinfo = rawinfo.split('\n')



#### Loop for separating the group and changing into usable list
flutter_list = {}
j = 1
for i in range(len(rawinfo)):    
    if 'FLUTTER  SUMMARY' in rawinfo[i]:
        X = [x.split() for x in rawinfo[(i+5):(i+17)]]
        flutter_list["group_%s"%(j)] = pd.DataFrame(data = [list(map(float, i)) for i in X[1:]], columns = X[0])
        j += 1

#### Plots set-up
colors = ['#EA0437', '#87D300', '#FFD100', '#4F1F91', 
    '#A24CC8', '#D71671', '#FF7200', '#009EDB', 
    '#78C7EB', '#BC87E6', '#7C2230', '#007B63', 
    '#F293D1', '#7F7800', '#BBA786', '#32D4CB']

#### Make plot (Frequnecy vs Speed)

ax1 = plt.subplot()
for i in range(1, j):  
    flutter_list["group_%s"%(i)].plot(kind='line', x='VELOCITY', y='KFREQ', ax = ax1, label = '%s' % i, color = colors[i-1])
ax1.set_xlabel('Velocity (m/s)')
ax1.set_ylabel('Frequency')
ax1.set_title('Frequency vs Speed')
ax1.legend(title='Point:', loc='best', ncol = 4, fontsize = 'small')
plt.show()


#### Make plot (Damping vs Speed, Raw Scale)

ax2 = plt.subplot()
for i in range(1, j):  
    flutter_list["group_%s"%(i)].plot(kind='line', x='VELOCITY', y='DAMPING', ax = ax2, label = '%s' % i, color = colors[i-1])
ax2.set_xlabel('Velocity (m/s)')
ax2.set_ylabel('Damping')  
ax2.grid() 
ax2.set_title('Damping vs Speed (Raw Scale)')
ax2.legend(title='Point:', loc='best', ncol = 4, fontsize = 'small')
plt.show()

#### Make plot (Damping vs Speed, Magnified Scale)

ax3 = plt.subplot()
for i in [ii for ii in range(1, j) if ii != 1]:  
    flutter_list["group_%s"%(i)].plot(kind='line', x='VELOCITY', y='DAMPING', ax = ax3, label = '%s' % i, color = colors[i-1])
ax3.set_xlabel('Velocity (m/s)')
ax3.set_ylabel('Damping')  
ax3.set_ylim([-0.01, 0.01])
ax3.grid() 
ax3.set_title('Damping vs Speed (Magnified Scale)')
ax3.legend(title='Point:', loc='best', ncol = 5, fontsize = 'small')
plt.show()