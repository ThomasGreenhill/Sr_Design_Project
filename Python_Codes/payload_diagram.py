## Set-up

import numpy as np
import matplotlib.pyplot as plt
import os
savedir = os.path.abspath(os.path.dirname(__file__))

## Payload Diagram Calculation

Range = 
Wp =
Woe =
E_reserve =
E_b = 

## Payload Diagram Formulation
color1 = 'tab:blue'; color2 = 'tab:red'

fig, ax1 = plt.subplots() 

#### Weight vs. Range
ax1.set_xlabel('Range (Unit)') 
ax1.set_ylabel('Weight (Unit)', color = color1) 
ax1.plot(Range, Woe, color = color1, linestyle='-')  
ax1.plot(Range, Wp+Woe, color = color1, linestyle='--')  
ax1.tick_params(axis ='y', labelcolor = color1) 
ax1.set_xlim([0, np.amax(Range)*1.25])
ax1.set_ylim([0, np.amax(Wp+Woe)*1.25])

#### Notations for Weight vs. Range part
ax1.arrow(Range[1],-np.amax(Wp+Woe)*0.25,0,np.amax(Wp+Woe)*0.2,length_includes_head=True,
    width=0.02, head_width=0.06, head_length=0.30, color='tab:gray')
ax1.arrow(Range[2],-np.amax(Wp+Woe)*0.25,0,np.amax(Wp+Woe)*0.2,length_includes_head=True,
    width=0.02, head_width=0.06, head_length=0.30, color='tab:gray')
ax1.annotate('Max Payload Range',(Range[1],-np.amax(Wp+Woe)*0.3))
ax1.annotate('Max Ferry Range',(Range[1],-np.amax(Wp+Woe)*0.3))

#### Adding Twin Axes to plot another datasets
ax2 = ax1.twinx() 
  
#### Battery Charge vs. Range
ax2.set_ylabel('Battery Charge (Unit)', color = color2) 
ax2.plot(Range, E_reserve, color = color1, linestyle='-')  
ax2.plot(Range, E_b, color = color1, linestyle='--') 
ax2.tick_params(axis ='y', labelcolor = color2) 
ax2.set_ylim([0, np.amax(E_b)*1.25])

#### Final Step 
plt.title('Impact of range on payload of electric aircraft') 
plt.legend(loc='best')
plt.savefig('%s/Payload_Diagram.png'%(savedir))
plt.show()
