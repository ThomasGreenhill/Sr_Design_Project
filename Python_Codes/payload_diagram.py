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
ax1.set_xlim([0, np.amax(Range)])
ax1.set_ylim([0, np.amax(Wp+Woe)*1.25])

#### Notations for Weight vs. Range part
ax1.arrow(Range[1],-np.amax(Wp+Woe)*0.25,0,np.amax(Wp+Woe)*0.2,length_includes_head=True,
    width=0.02, head_width=0.06, head_length=0.30, color='tab:gray')
ax1.arrow(Range[2],-np.amax(Wp+Woe)*0.25,0,np.amax(Wp+Woe)*0.2,length_includes_head=True,
    width=0.02, head_width=0.06, head_length=0.30, color='tab:gray')
ax1.annotate('Max Payload Range',(Range[1],-np.amax(Wp+Woe)*0.3))
ax1.annotate('Max Ferry Range',(Range[1],-np.amax(Wp+Woe)*0.3))
ax1.annotate("",
            xy=(Range[1]*0.8, 0), xycoords='data',
            xytext=(Range[1]*0.8,np.amax(Woe)), textcoords='data',
            arrowprops=dict(arrowstyle="<->",
                            connectionstyle="arc3", color=color1, lw=2),
            )
ax1.annotate("",
            xy=(Range[1]*0.6, np.amin(Wp+Woe)), xycoords='data',
            xytext=(Range[1]*0.6, np.amax(Wp+Woe)), textcoords='data',
            arrowprops=dict(arrowstyle="<->",
                            connectionstyle="arc3", color=color1, lw=2),
            )
ax1.text(Range[1]*0.75, np.amax(Woe), 'Operating Empty Weight', rotation = 90, fontsize = 12, color=color1)
ax1.text(Range[1]*0.55, np.amax(Woe+Wp), 'Payload Weight', rotation = 90, fontsize = 12, color=color1)

#### Adding Twin Axes to plot another datasets
ax2 = ax1.twinx() 
  
#### Battery Charge vs. Range
ax2.set_ylabel('Battery Charge (Unit)', color = color2) 
ax2.plot(Range, E_reserve, color = color1, linestyle='-')  
ax2.plot(Range, E_b, color = color1, linestyle='--') 
ax2.tick_params(axis ='y', labelcolor = color2) 
ax2.set_ylim([-np.amax(E_b)*1.25, np.amax(E_b)*1.25])

#### Reference Line
ax2.plot(Range, 0*Range, color = 'tab:gray', linestyle='.-') 


#### Notations for Battery Charge vs. Range part
ax2.annotate("",
            xy=(Range[1]*1.1, 0), xycoords='data',
            xytext=(Range[1]*1.1,np.amax(E_reserve)), textcoords='data',
            arrowprops=dict(arrowstyle="<->",
                            connectionstyle="arc3", color=color2, lw=2),
            )
ax2.annotate("",
            xy=(Range[1]*1.2, 0), xycoords='data',
            xytext=(Range[1]*1.2, np.amax(E_b)), textcoords='data',
            arrowprops=dict(arrowstyle="<->",
                            connectionstyle="arc3", color=color2, lw=2),
            )
ax2.text(Range[1]*1.05, np.amax(E_reserve), 'Reserve Charge', rotation = 90, fontsize = 12, color=color2)
ax2.text(Range[1]*1.15, np.amax(E_b), 'Battery Charge', rotation = 90, fontsize = 12, color=color2)

#### Final Step 
plt.title('Impact of range on payload of electric aircraft') 
plt.savefig('%s/Payload_Diagram.png'%(savedir))
plt.show()
