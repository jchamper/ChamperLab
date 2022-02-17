import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy import linspace
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches

plt.rcParams.update({'font.size': 30,
                     'font.family': "Times New Roman",
                     "axes.titlesize": 2,
                     "axes.labelsize": 30,
                     
                     "legend.fontsize": 2,
                     "axes.labelpad": 1.0,
                     "axes.linewidth":1.2,
                     "axes.labelcolor": "black",
                     "xtick.color": "black",
                     "ytick.color": "black",
                     "xtick.major.size": 6.0,
                     "xtick.major.width":0.9,
                     "xtick.major.pad":1.8,
                     "xtick.direction":'inout',
                     "ytick.direction":'inout',
                     "ytick.major.size": 6.0,
                     "ytick.major.width":0.9,
                     "ytick.major.pad":1.5,
                     "legend.framealpha": 0,
                     "patch.facecolor": "white"})
df = pd.read_csv("./plot.csv")

x1 = df['ID']
y1 = df['1']
y2 = df['2']

font1 = {'family' : 'Times New Roman','weight' : 'normal',
         'size' : 10,}
font2 = {'family' : 'Times New Roman','weight' : 'normal',
         'size' : 16,}
font3 = {'family' : 'Times New Roman','weight' : 'normal',
         'size' : 6,}

figsize = 8,8
figure, ax = plt.subplots(figsize=(8,8))
plt.subplots_adjust(bottom=0.15)

plt.plot(x1, y1, linewidth = '0.8', linestyle='-', color='#800000',label = 'Diploid')
plt.plot(x1, y2, linewidth = '0.8', linestyle='-', color='#808080',label = 'Haplodiploid')
plt.xlabel("Generation")
plt.ylabel("Drive frequency")

plt.legend(loc='best',fontsize=22,frameon=False,labelspacing=0.2)

plt.xticks(np.linspace(0,40,5),fontproperties = 'Times New Roman', size=34)
plt.yticks(np.linspace(0,1,6),fontproperties = 'Times New Roman', size=34)
plt.tick_params(labelsize=30, pad=3, width=2, direction='inout') 


plt.xlim((0,45))
plt.ylim((0,1.05))

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_position(('data',0))
ax.spines['left'].set_position(('data',0.15))
plt.subplots_adjust(left=0.20)
plt.show()

