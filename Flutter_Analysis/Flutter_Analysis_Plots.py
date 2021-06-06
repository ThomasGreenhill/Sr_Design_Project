import numpy as np
import matplotlib.pyplot as plt
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


#### Make plot (Frequnecy vs Speed)

ax1 = plt.subplot()
for i in range(1, j):  
    flutter_list["group_%s"%(i)].plot(kind='line', x='VELOCITY', y='KFREQ', ax = ax1, label = '%s' % i)
ax1.set_xlabel('Velocity (m/s)')
ax1.set_ylabel('Frequency')
ax1.set_title('Frequency vs Speed')
ax1.legend(title='Point:', loc='best', ncol = 4, fontsize = 'small')
plt.show()


#### Make plot (Damping vs Speed)

ax2 = plt.subplot()
for i in range(1, j):  
    flutter_list["group_%s"%(i)].plot(kind='line', x='VELOCITY', y='DAMPING', ax = ax2, label = '%s' % i)
ax2.set_xlabel('Velocity (m/s)')
ax2.set_ylabel('Damping')
ax2.set_title('Damping vs Speed')
ax2.legend(title='Point:', loc='best', ncol = 4, fontsize = 'small')
plt.show()