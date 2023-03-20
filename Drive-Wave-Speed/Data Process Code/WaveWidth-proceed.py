# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 14:11:57 2023

@author: Mingzuyu Pan
"""
import pandas as pd
import csv
number = ['set_number']
B_number = ['original_number']
frequency_9_1 = ['frequency_0.9_x1']
position_9_1 = ['position_0.9_x1']
frequency_9_2 = ['frequency_0.9_x2']
position_9_2 = ['position_0.9_x2']
frequency_1_1 = ['frequency_0.1_x1']
position_1_1 = ['position_0.1_x1']
frequency_1_2 = ['frequency_0.1_x2']
position_1_2 = ['position_0.1_x2']
right = ['accurate_right']
left = ['accurate_left']
distance = ['distance']
calculate = 0
for m in range(20):
    source = r"T"+str(m+1)+"\\count.txt"
    with open(source,'r') as f:
        for line in f.readlines():
            n = line
    # print(n)
    n = int(n)
    calculate = calculate + n
    for i in range(n):
        filepath =source = r"T"+str(m+1)+"\\result_"+str(i+1)+".txt"
        position = []
        drive_carrier_frequency = []
        with open(filepath,'r') as f:
            for line in f.readlines():
                if (line.startswith("generation") != True):
                    p = float(line.split(":",3)[1])
                    if ((line.split(":",3)[3]).split("\n",1)[0] == "NULL"):
                        f = float(10000)
                    else:
                        f = float((line.split(":",3)[3]).split("\n",1)[0])
                    position.append(p)
                    drive_carrier_frequency.append(f)
        df=pd.DataFrame([position,drive_carrier_frequency],index=['position','drive_carrier_frequency'])
        df = df.T
        # print(df)
        if len((df[(df['drive_carrier_frequency']<=0.9)].index.tolist())) ==0 or len((df[(df['drive_carrier_frequency']<=0.1)].index.tolist())) == 0:
            B_number.append(m+1)
            number.append(i)
            right.append("NAN")
            left.append("NAN")
            frequency_9_1.append("NAN")
            position_9_1.append("NAN")
            frequency_9_2.append("NAN")
            position_9_2.append("NAN")
            frequency_1_1.append("NAN")
            position_1_1.append("NAN")
            frequency_1_2.append("NAN")
            position_1_2.append("NAN")
            distance.append('NAN')
        else:
            #for 0.9 accuarte position
            index_9 = (df[(df['drive_carrier_frequency']<=0.9)].index.tolist())[0]
            freq_9_1 = df.iloc[index_9,1]
            posi_9_1 = df.iloc[index_9,0]
            freq_9_2 = df.iloc[(index_9-1),1]
            posi_9_2 = df.iloc[(index_9-1),0]
            frequency_9_1.append(freq_9_1)
            position_9_1.append(posi_9_1)
            frequency_9_2.append(freq_9_2)
            position_9_2.append(posi_9_2)
            # print(index_9)
            # print(freq_9_1)
            # print(posi_9_1)
            # print(freq_9_2)
            # print(posi_9_2)
            index_1 = (df[(df['drive_carrier_frequency']<=0.1)].index.tolist())[0]
            freq_1_1 = df.iloc[index_1,1]
            posi_1_1 = df.iloc[index_1,0]
            freq_1_2 = df.iloc[(index_1-1),1]
            posi_1_2 = df.iloc[(index_1-1),0]
            frequency_1_1.append(freq_1_1)
            position_1_1.append(posi_1_1)
            frequency_1_2.append(freq_1_2)
            position_1_2.append(posi_1_2)
            # print(index_1)
            # print(freq_1_1)
            # print(posi_1_1)
            # print(freq_1_2)
            # print(posi_1_2)
            accurate_1 = posi_1_2 + (freq_1_2-0.1)/(freq_1_2-freq_1_1)*0.02
            # print(accurate_1)
            accurate_9 = posi_9_2 + (freq_9_2-0.9)/(freq_9_2-freq_9_1)*0.02
            # print(accurate_9)
            distance_now = accurate_1 - accurate_9
            if (posi_9_1 == 0.01):
                distance_now = "NAN"
            if (freq_9_2 == 10000):
                distance_now = "NAN"
            if (freq_9_2 == 1.0 or freq_9_2 == 0.0):
                distance_now = "NAN"
            if (freq_1_2-freq_1_1 == 0):
                accurate_1 = 'NAN'
            if (freq_9_2-freq_9_1==0):
                accurate_9 = 'NAN'
            number.append(i+1)
            B_number.append(m+1)
            right.append(accurate_1)
            left.append(accurate_9)
            distance.append(distance_now)
            
    # print(number)
    # print(right)
    # print(left)
    rows = zip (B_number,number,position_9_2,frequency_9_2,position_9_1,frequency_9_1,position_1_2,frequency_1_2,position_1_1,frequency_1_1,left,right,distance)
    filePath = r'Z-linkedW-shredder_Raw_Data.csv'
    with open(filePath, "w", newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)
print(calculate)