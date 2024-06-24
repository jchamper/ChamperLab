import pandas as pd
import matplotlib.pyplot as plt

column_names = [
    'Index', 'Population', 'Drive_Type', 'TARE_Carrier_Freq', 'TARE_Allele_Freq', 
    'Other1', 'Other2', 'Other3', 'Other4', 'Other5', 'Drive_Type2', 
    'Homing_Carrier_Freq', 'Homing_Allele_Freq', 'Other6', 'Other7', 
    'Other8', 'Other9', 'Other10'
]


try:
    df = pd.read_csv('./pan/double_second_drive/Tethered_pan_TAREdropratio_HOMSdropratio0.05/pan_TAREdropratio0.15_HOMSdropratio0.05_1.txt', sep='\s+', header=None, names=column_names, engine='python')
    print(df.head()) 
    print(df.describe()) 
except Exception as e:
    print(f"Error reading file: {e}")
    exit()

df['TARE_Carrier_Freq'] = df['TARE_Carrier_Freq'].astype(float)
df['TARE_Allele_Freq'] = df['TARE_Allele_Freq'].astype(float)
df['Homing_Carrier_Freq'] = df['Homing_Carrier_Freq'].astype(float)
df['Homing_Allele_Freq'] = df['Homing_Allele_Freq'].astype(float)

x = df['Index']
y1 = df['TARE_Carrier_Freq']
y2 = df['TARE_Allele_Freq']
y3 = df['Homing_Carrier_Freq']
y4 = df['Homing_Allele_Freq']

print("x (Generation):", x.head())
print("y1 (TARE carrier):", y1.head())
print("y2 (TARE allele):", y2.head())
print("y3 (Homing carrier):", y3.head())
print("y4 (Homing allele):", y4.head())

plt.figure(figsize=(10, 6))
plt.rcParams['svg.fonttype'] = 'none'
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 32,
                     'font.family': "Arial",
                     "axes.titlesize": 32,     
                     "axes.labelsize": 32,
                     "savefig.pad_inches": 0,
                     "legend.fontsize": 32,
                     "axes.labelpad": 0.1,
                     "axes.linewidth":1.2,
                     "text.color": "black",
                     "axes.labelcolor": "black",
                     "xtick.color": "black",
                     "ytick.color": "black",
                     "xtick.major.size": 5.0,
                     "xtick.major.width":1.5,
                     "xtick.major.pad":0.1,
                     "ytick.major.size": 5.0,
                     "ytick.major.width":1.5,
                     "ytick.major.pad":0.1,
                     "legend.frameon": False,  
                     "patch.facecolor": "white"})

plt.gca().patch.set_alpha(0)

plt.plot(x, y1, label='TARE carrier frequency', color="#EC5E00", linewidth=1, linestyle='--')
plt.plot(x, y2, label='TARE allele frequency', color="#EC5E00",linewidth=1)
plt.plot(x, y3, label='Homing carrier frequency', color="#2B9F78",linewidth=1, linestyle='--')
plt.plot(x, y4, label='Homing allele frequency', color="#2B9F78",linewidth=1)

plt.xlim(0, 20)
plt.xticks([0,5,10,15,20])

plt.ylim(0, 1.05)
plt.yticks([i / 10.0 for i in range(0, 11, 2)])

plt.xlabel('Generation')
plt.ylabel('Frequency')
plt.title('TARE success')
plt.legend()

plt.axhline(0, color='black', linewidth=1.5)
plt.axvline(0, color='black', linewidth=1.5)

plt.savefig("pan_TAREdropratio0.15_HOMSdropratio0.05_1.svg", dpi=300, format='svg', bbox_inches="tight", transparent=True)

plt.show()
