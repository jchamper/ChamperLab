# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 10:43:35 2022

@author: Mingzuyu Pan
"""

import csv
DriveEfficieny = ['GROWTH']
Embryo = ['FITNESS']
Average = ['AVERAGE']
MAX = 500
f_path = r'C:\Users\dell\Desktop\Wolbachia\Wolbachia2_Raw_Data.csv'
with open(f_path) as csvfile:
    reader = csv.reader(csvfile)
    count = 0
    total = 0   
    Max_count = 0
    Normal_count = 0
    Normal_sum = 0
    average = 0
    while(total < 231 ):
        m = total*20+1
        total = total + 1
        for i,rows in enumerate(reader):
            if(count<20):
                if(i == m):
                    row = rows
                    drive = float(row[1])
                    embryo =float(row[2])
                    value = float(row[14])
                    if (value == MAX):
                        Max_count = Max_count + 1
                    else:
                        Normal_count = Normal_count + 1
                        Normal_sum = Normal_sum + value
                    m = m + 1
                    count = count + 1
                    
            if(count == 20): 
                count = 0
                if (Normal_count >= 3):
                    average = Normal_sum/Normal_count
                    average = round(average,4)
                    DriveEfficieny.append(drive)
                    Embryo.append(embryo)
                    Average.append(average)
                    Max_count = 0
                    Normal_count = 0
                    Normal_sum = 0
                    average = 0
                else:
                    DriveEfficieny.append(drive)
                    Embryo.append(embryo)
                    Average.append("5000")
                    Max_count = 0
                    Normal_count = 0
                    Normal_sum = 0
                    average = 0
rows = zip (DriveEfficieny,Embryo,Average)
filePath = r'C:\Users\dell\Desktop\Wolbachia2_Data_For_Heatmap.csv'
with open(filePath, "w", newline='') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
    
                
            
    
            