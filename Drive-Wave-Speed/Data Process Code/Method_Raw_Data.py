# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 12:46:29 2022

@author: Mingzuyu Pan
"""
import csv
generation = ['generation']
SLICE3 =['SLICE3']
SLICE8 = ['SLICE8']
Before_Start_Generation = ['Before_Start_Generation']
Before_Start = ['Before_Start']
Start_Generation = ['Start_Generation']
Start = ['Start']
Actual_Start_Generation = ['Actual_Start_Generation']
Before_Stop_Generation = ['Before_Stop_Generation']
Before_Stop = ['Before_Stop']
Stop_Generation = ['Stop_Generation']
Stop = ['Stop']
Actual_Stop_Generation = ['Actual_Stop_Generation']
Actual_Timed_Gens = ['Actual_Timed_Gens']
Embryo = ['FITNESS']
Germline = ['GROWTH']
Number = ['Number']
Timed_Gens_Tester = ['Timed_Gens_Tester']
Calculate = 'NULL'
MAX = 500
Choose = True
if(Choose == True):
    Address = '\Drive-Embryo'
else:
    Address = '\Fitness-Density'
    
for i in range(20):
    for x in range(11):
        m = x/20 + 0.5
        m_bigger = 100*m
        m_bigger = round(m_bigger)
        f_path = r'C:\Users\dell\Desktop\Wolbachia\T'+str(i)+'\py_data_Wolbachia_csv_'+str(m)+'\large_array_with_python'+str(m_bigger)+'.txt'
        with open(f_path) as f:
            lines = f.readlines()
            slice3_helper = 0
            slice8_helper = 0
            actual_start = 'NULL'
            actual_stop = 'NULL'
        for line in lines:
            if line.startswith("generation"):
                gene = line.split(':')[1]
                gene_0 = gene.split('\n')[0]
                
            if line.startswith("SLICE3"):
                SLICE3_0 = line.split(':')[1]
                SLICE3_1 = SLICE3_0.split('\n')[0]
                if(SLICE3_1 == 'N/A'):
                    SLICE3_1 = '10'
                float_SLICE3_1 = float(SLICE3_1)
                SLICE3.append(float_SLICE3_1)
                if (float_SLICE3_1 < 0.5) & (slice3_helper!= "NULL"):
                    slice3_helper = SLICE3_1
                if (slice3_helper!= "NULL") & (float_SLICE3_1 >= 0.5):
                    Before_Start.append(slice3_helper)
                    Before_Start_Generation.append(float(gene_0)-1)
                    Start.append(float_SLICE3_1)
                    Start_Generation.append(float(gene_0))
                    actual_start = float(gene_0)-1 + (0.5 - float(slice3_helper))/(float_SLICE3_1 - float(slice3_helper))
                    Actual_Start_Generation.append(actual_start)
                    slice3_helper = "NULL" 
                    
                    
            if line.startswith("SLICE8"):
                SLICE8_0 = line.split(':')[1]
                SLICE8_1 = SLICE8_0.split('\n')[0]
                float_SLICE8_1 = float(SLICE8_1)
                SLICE8.append(SLICE8_1)
                if (float_SLICE8_1 < 0.5) & (slice8_helper!= "NULL"):
                    slice8_helper = SLICE8_1
                if (slice8_helper!= "NULL") & (float_SLICE8_1 >= 0.5):
                    Before_Stop.append(slice8_helper)
                    Before_Stop_Generation.append(float(gene_0)-1)
                    Stop.append(float_SLICE8_1)
                    Stop_Generation.append(float(gene_0))
                    actual_stop = float(gene_0)-1 + (0.5 - float(slice8_helper))/(-float(slice8_helper) + float_SLICE8_1)
                    Actual_Stop_Generation.append(actual_stop)
                    slice8_helper = "NULL" 
                    
            if line.startswith("FITNESS"):
                Embryo_0 = line.split(':')[1]
                Embryo_1 = Embryo_0.split('\n')[0]
                Embryo.append(Embryo_1)
            if line.startswith("GROWTH"):
                Germline_0 = line.split(':')[1]
                Germline_1 = Germline_0.split('\n')[0]
                Germline.append(Germline_1)
                Number.append(str(i)) 
            if line.startswith("TIMED"):
                Timed_Gens_Tester_0 = line.split(':')[1]
                Timed_Gens_Tester_1 = Timed_Gens_Tester_0.split('\n')[0]
                Timed_Gens_Tester.append(Timed_Gens_Tester_1)
          
                if((actual_start != 'NULL') & (actual_stop != 'NULL')):
                        actual_timed = actual_stop-actual_start
                        Actual_Timed_Gens.append(actual_timed)                
            
                if((actual_stop == 'NULL') & (actual_start == 'NULL')):
                        Before_Start_Generation.append('0')
                        Before_Start.append('0')
                        Start_Generation.append('0')
                        Start.append('0')
                        Before_Stop_Generation.append('0')
                        Before_Stop.append('0')
                        Stop_Generation.append('0')
                        Stop.append('0')
                        Actual_Start_Generation.append(MAX)
                        Actual_Stop_Generation.append(MAX)
                        Actual_Timed_Gens.append(MAX)
    
                if((actual_stop == 'NULL') & (actual_start != 'NULL')):
                        Before_Stop_Generation.append('0')
                        Before_Stop.append('0')
                        Stop_Generation.append('0')
                        Stop.append('0')
                        Actual_Stop_Generation.append(MAX)
                        Actual_Timed_Gens.append(MAX)
    
                if((actual_stop != 'NULL') & (actual_start == 'NULL')):
                        Before_Start_Generation.append('0')
                        Before_Start.append('0')
                        Start_Generation.append('0')
                        Start.append('0')
                        Actual_Start_Generation.append(MAX)
                        Actual_Timed_Gens.append(MAX)
                slice3_helper = 0
                slice8_helper = 0
                actual_start = 'NULL'
                actual_stop = 'NULL'      




  
rows = zip (Number,Germline,Embryo,Before_Start_Generation,Before_Start,Start_Generation,Start,Actual_Start_Generation,Before_Stop_Generation,Before_Stop,Stop_Generation,Stop,Actual_Stop_Generation,Timed_Gens_Tester,Actual_Timed_Gens)
filePath = r'C:\Users\dell\Desktop\Wolbachia\Wolbachia2_Raw_Data.csv'
with open(filePath, "w", newline='') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)