#txt to csv
Frequency = True
Number = True
Smooth = True
v1="HOMSembryocut"
v2="HOMSconversionrate"
a1="e"
a2="c"
color_list = ['#17AD65', '#EE5F00', '#286BEE', '#9B72AA']
mode=1
#embryo cut rate=[0,1]-21-0.05
low_p1=0.0
p1_interval=0.05

#if it uses allele frequency, allele will be 1, if it uses carrier frequency, allele will be 0
#allele=1

import pandas as pd
import ast
import cv2
import os
import glob
import re
import shutil
import numpy as np
from pathlib import Path
import csv
from matplotlib.lines import Line2D  
import matplotlib.pyplot as plt
import ast  
from PIL import Image


def calculate_duration(ranges):
    if not isinstance(ranges, str):
        return []

    range_list = ranges.split(", ")
    durations = []
    for r in range_list:
        if r:  
            start, end = map(int, r.split('-'))
            durations.append(end - start + 1)
    return durations


def find_continuous_blocks(df, column):
    continuous_blocks = []
    start = None
    for i, value in enumerate(df[column]):
        if value and start is None:
            start = i  
        elif not value and start is not None:
            continuous_blocks.append((start, i - 1))
            start = None 
    if start is not None: 
        continuous_blocks.append((start, len(df) - 1))
    return continuous_blocks

def process(file_path):
    df = pd.read_csv(file_path)
    continuous_left = find_continuous_blocks(df, 'continuous_left')
    continuous_right = find_continuous_blocks(df, 'continuous_right')
    continuous_left_H = find_continuous_blocks(df, 'continuous_left_H')
    continuous_right_H = find_continuous_blocks(df, 'continuous_right_H')
    return continuous_left, continuous_right, continuous_left_H, continuous_right_H

def main(folder_path, output_csv, v1, v2, p1, p2, a1, a2, scope, j):
    base_number = int(round(20 * ((p1-low_p1)/p1_interval)))
    if p1 == low_p1:
        file_name = f"{j:04d}.part"
    else:
        file_name = f"{base_number:04d}+{j}.part"
    part_files = [f"{folder_path}/{file_name}"]
    part_number = j
    with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:
            writer.writerow(['Part Filename', 'HOMSembryocut', 'HOMSconversionrate', 'Lowdensitygrowthrate',\
             'Averagedistance', 'suppressed', 'gen_suppressed', 'TAREprediction', 'HOMSprediction', 'HOMSdropgen', \
             'confined_chased', 'confined_gen_chase_started', 'confined_gen_chase_ended', 'confined_duration_of_chasing', \
             'confined_gc_average', 'confined_gc_variance', 'confined_avg_pop_during_chase', 'confined_var_pop_during_chase', \
             'confined_avg_carrier_frequency_during_chase', 'confined_drive_success', 'gen_confined_drive_success', 'confined_drive_lost', \
             'gen_confined_drive_lost', 'r1_resistance', 'gen_r1_resistance', 'suppression_chased', 'suppression_gen_chase_started', \
             'suppression_gen_chase_ended', 'suppression_duration_of_chasing', 'suppression_gc_average', 'suppression_gc_variance', \
             'suppression_avg_pop_during_chase', 'suppression_var_pop_during_chase', 'suppression_avg_carrier_frequency_during_chase', \
             'suppression_drive_lost', 'gen_suppression_drive_lost', 'hr1_resistance', 'gen_hr1_resistance', 'avg_female_fertile', 'stopped_1000', \
             'rate_at_stop', 'hrate_at_stop', 'confined_drive_avg_frequency_in_last_100_generations', 'suppression_drive_avg_frequency_in_last_100_generations', \
             'continuous_left', 'continuous_right', 'continuous_left_H', 'continuous_right_H', 'TARE_penetration', 'TARE_penetration_duration', \
             'Homing_penetration', 'Homing_penetration_duration', 'Picture Link', 'Video Link'])

        for part_file in part_files:
            with open(part_file, 'r') as file:
                if part_number == 0 and p1 == low_p1:
                    next(file) 
                part_content = file.read().strip().strip('()') 
                part_data = part_content.split(',')  
            

            csv_file = f"{d}/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{part_number}_p_non.csv"
            continuous_left, continuous_right, continuous_left_H, continuous_right_H= process(csv_file)
            
            continuous_left = ', '.join([f"{start}-{end}" for start, end in continuous_left])
            continuous_right = ', '.join([f"{start}-{end}" for start, end in continuous_right])


            continuous_left_H = ', '.join([f"{start}-{end}" for start, end in continuous_left_H])
            continuous_right_H = ', '.join([f"{start}-{end}" for start, end in continuous_right_H])


            TARE_penetration = 1 if continuous_left or continuous_right else 0
            Homing_penetration = 1 if continuous_left_H or continuous_right_H else 0

            TARE_penetration_duration = calculate_duration(continuous_left) + calculate_duration(continuous_right)
            Homing_penetration_duration = calculate_duration(continuous_left_H) + calculate_duration(continuous_right_H)

            picture_link = f"./Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{part_number}_s_{scope}_P.png"
            video_link = f"./Tethered_1D_{v1}{p1}_{v2}{p2}/Double/{a1}{p1}_{a2}{p2}_{j}.mp4"

            picture_hyperlink = f'=HYPERLINK("{picture_link}", "Picture Link")'

            if os.path.exists(video_link):
                video_hyperlink = f'=HYPERLINK("{video_link}", "Video Link")'
            else:
                video_hyperlink = 'None'

            writer.writerow([part_file] + part_data + [continuous_left, continuous_right, continuous_left_H, continuous_right_H, TARE_penetration, TARE_penetration_duration, Homing_penetration, Homing_penetration_duration, picture_hyperlink, video_hyperlink])



def natural_sort_key(s):

    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]


def create_video_from_images(folder_path, output_video='output_video.mp4', frame_size=(1920, 1080), fps=30):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video, fourcc, fps, frame_size)


    images = glob.glob(os.path.join(folder_path, 'output_*.png'))
    images.sort(key=natural_sort_key)  

    for image in images:
        img = cv2.imread(image)
        img = cv2.resize(img, frame_size)
        filename = os.path.basename(image).split('.')[0]
        cv2.putText(img, filename, (700, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        video.write(img)


    blank_frame = np.zeros((frame_size[1], frame_size[0], 3), dtype=np.uint8)
    for _ in range(int(fps * 0.5)):  
        video.write(blank_frame)

    video.release()


def mark_continuous_true(series):
    continuous = series.astype(int).groupby(series.ne(series.shift()).cumsum()).transform('count') * series
    return continuous >= 3

def process_row(row,drive,wt,empty):
    def parse_values(value):
        return [float(x.strip()) for x in str(value).split(',') if x.strip().replace('.', '', 1).isdigit()]

    def add_or_replace(values_list, new_tuple):

        for i, existing_tuple in enumerate(values_list):
            if len(existing_tuple) == 3 and len(new_tuple) == 3:
                outer, _, inner = existing_tuple
                if new_tuple[0] == outer or new_tuple[2] == inner or set(new_tuple[1]) == set(existing_tuple[1]):
                    if abs(new_tuple[0] - new_tuple[2]) < abs(outer - inner):
                        values_list[i] = new_tuple
                    return
            else:

                print("Incorrect tuple format:", existing_tuple)
        values_list.append(new_tuple)

    col1 = parse_values(row[drive])
    col3 = parse_values(row[wt])
    col5 = parse_values(row[empty])

    left, right = False, False
    left_values, right_values = [], []

    for val1 in col1:
        for val5 in col5:
            if val5 < val1:
                between_values = [x for x in col3 if val5 < x < val1]
                if between_values and not any(x in col1 + col5 for x in range(int(val5)+1, int(val1))):
                    new_tuple = (val5, between_values, val1)
                    left = True
                    add_or_replace(left_values, new_tuple)
            elif val5 > val1:
                between_values = [x for x in col3 if val1 < x < val5]
                if between_values and not any(x in col1 + col5 for x in range(int(val1)+1, int(val5))): 
                    new_tuple = (val5, between_values, val1)
                    right = True
                    add_or_replace(right_values, new_tuple)

    return left, left_values, right, right_values


def combine_images_vertically(img_path1, img_path2, output_path):
    img1 = Image.open(img_path1)
    img2 = Image.open(img_path2)

    width = max(img1.width, img2.width)
    height = img1.height + img2.height

    new_img = Image.new('RGB', (width, height))

    new_img.paste(img1, (0, 0))
    new_img.paste(img2, (0, img1.height))

    new_img.save(output_path)



allele=1
if allele == 0:
    def find_sequences(df,a,b):
        sequences = []
        i = 0
        while i < len(df) - 1:
            if df.iloc[i, a] == True and df.iloc[i + 1, a] == True and df.iloc[i, b] == False:
                start = i
                while i < len(df) and df.iloc[i, a] == True:
                    if df.iloc[i, b] == True:  
                        break
                    i += 1
                end = i

                true_count = 0
                for j in range(end, len(df)):
                    if df.iloc[j, b] == True:
                        true_count += 1
                    else:
                        if true_count >= 2:
                            sequences.append((start, j))  
                        i = j
                        break
                else:
                    if true_count >= 2:
                        sequences.append((start, len(df)))  
                    break
            else:
                i += 1
        return sequences

    def check_condition_H(row):

        col1 = str(row['Homing'])
        col3 = str(row['HWT'])
        col5 = str(row['Empty'])


        col1_values = [float(val) for val in col1.split(",") if val]
        col3_values = [float(val) for val in col3.split(",") if val]
        col5_values = [float(val) for val in col5.split(",") if val]


        for val5 in col5_values:
            for val3 in col3_values:
                for val1 in col1_values:
                    if val5 < val3 < val1:
                        return True, (val1, val3, val5)
        return False, None

    def check_condition_after_H(row):

        col1 = str(row['Homing'])
        col3 = str(row['HWT'])
        col5 = str(row['Empty'])

        col1_values = [float(val) for val in col1.split(",") if val]
        col3_values = [float(val) for val in col3.split(",") if val]
        col5_values = [float(val) for val in col5.split(",") if val]

        for val5 in col5_values:
            for val3 in col3_values:
                for val1 in col1_values:
                    if val3 < val5 < val1:
                        return True, (val1, val3, val5)
        return False, None

    def process_csv_H(input_file, output_file):
        df = pd.read_csv(input_file)

        df['Result_H'], df['Values_H']= zip(*df.apply(check_condition_H, axis=1))
        df['Result_after_H'], df['Values_after_H']= zip(*df.apply(check_condition_after_H, axis=1))

        df.to_csv(output_file, index=False)

    def check_condition(row):
        col1 = str(row['TARE'])
        col3 = str(row['TWT'])
        col5 = str(row['Empty'])

        col1_values = [float(val) for val in col1.split(",") if val]
        col3_values = [float(val) for val in col3.split(",") if val]
        col5_values = [float(val) for val in col5.split(",") if val]

        for val5 in col5_values:
            for val3 in col3_values:
                for val1 in col1_values:
                    if val5 < val3 < val1:
                        return True, (val1, val3, val5)
        return False, None

    def check_condition_after(row):
        col1 = str(row['TARE'])
        col3 = str(row['TWT'])
        col5 = str(row['Empty'])
        col1_values = [float(val) for val in col1.split(",") if val]
        col3_values = [float(val) for val in col3.split(",") if val]
        col5_values = [float(val) for val in col5.split(",") if val]

        for val5 in col5_values:
            for val3 in col3_values:
                for val1 in col1_values:
                    if val3 < val5 < val1:
                        return True, (val1, val3, val5)
        return False, None

    def process_csv(input_file, output_file):
        df = pd.read_csv(input_file)
        df['Result'], df['Values']= zip(*df.apply(check_condition, axis=1))
        df['Result_after'], df['Values_after']= zip(*df.apply(check_condition_after, axis=1))
        df.to_csv(output_file, index=False)


    def smooth_values_with_original_data(df, mode=1, group_size=100):
        original_df = df.copy()

        weights = {
            1: [0.1875, 0.375, 0.75, 1, 0.75, 0.375, 0.1875],
            2: [0.2, 0.4, 0.8, 1, 0.8, 0.4, 0.2],
            3: [0.125, 0.25, 0.5, 1, 0.5, 0.25, 0.125]
        }[mode]

        one_sided_weights = weights[3:]

        for start in range(0, len(df), group_size):
            end = min(start + group_size, len(df))
            for i in range(start, end):
                for col in df.columns[1:]:  
                    if i < start + 3:
                        right_size = i - start + 1
                        window = original_df[col][i:i + right_size]
                        adjusted_weights = one_sided_weights[:right_size]
                    elif i >= end - 3:
                        left_size = end - i
                        window = original_df[col][i - left_size + 1:i + 1]
                        adjusted_weights = one_sided_weights[-left_size:]
                    else:
                        window = original_df[col][i - 3:i + 4]
                        adjusted_weights = weights

                    if len(window) != 0 and len(window) == len(adjusted_weights):
                        weighted_sum = sum(w * x for w, x in zip(adjusted_weights, window))
                        df.at[i, col] = weighted_sum / sum(adjusted_weights)
                    else:
                        df.at[i, col] = original_df.at[i, col]

        return df


    def merge_continuous_zero_y(col):
        col = [(x, y) for x, y in col if x != 0]

        merged = []
        start_index = None
        end_index = None
        current_y = None

        for i, (x, y) in enumerate(col):
            if start_index is None:
                start_index = i
                current_y = y
            end_index = i

            if i + 1 < len(col) and (col[i + 1][1] != current_y or col[i + 1][0] - x > 1):
                avg_x = sum(col[j][0] for j in range(start_index, end_index + 1)) / (end_index - start_index + 1)
                merged.append((avg_x, current_y))
                start_index = None

        if start_index is not None:
            avg_x = sum(col[j][0] for j in range(start_index, end_index + 1)) / (end_index - start_index + 1)
            merged.append((avg_x, current_y))

        return merged

    def merge_non_zero_points(col):
        threshold=3
        if not col:
            return []

        merged = []
        in_small_segment = False

        for i, (x, y) in enumerate(col):
            if y < threshold:
                if not in_small_segment:
                    in_small_segment = True
            else:
                if in_small_segment:
                    in_small_segment = False
                merged.append((x, y))  

        return merged

    def merge_non_zero_points_wt(col):
        merged = [(x, y) for x, y in col if y != 0 and x != 0]
        return merged



    def calculate_average(data):
        try:
            numbers = [float(x) for x in data.split(',')]
            return sum(numbers) / len(numbers)
        except:
            return None

    def check_conditions(row_n, row_n_plus_1):
        cond1 = row_n_plus_1[0] > row_n_plus_1[2] and \
                row_n_plus_1[3] - row_n[3] > 0 and row_n_plus_1[2] - row_n[2] > 0 and \
                row_n_plus_1[3] - row_n[3] > row_n_plus_1[2] - row_n[2] and \
                row_n_plus_1[3] - row_n_plus_1[2] >= -2 and row_n[3] - row_n[2] <= 0

        cond2 = row_n_plus_1[0] < row_n_plus_1[2] and \
                row_n_plus_1[3] - row_n[3] < 0 and row_n_plus_1[2] - row_n[2] < 0 and \
                row_n_plus_1[3] - row_n[3] < row_n_plus_1[2] - row_n[2] and \
                row_n_plus_1[3] - row_n_plus_1[2] <= 2 and row_n[3] - row_n[2] >= 0

        return cond1 or cond2

    for s in range(10,11):
        def find_extreme_value_with_merging(merged_col2, merged_col6, max_distance=50):
            col6_x = [x[0] for x in merged_col6] if merged_col6 else []

            merged_col2 = list(merged_col2) 
            i = 0
            while i < len(merged_col2) - 1:
                if merged_col2[i + 1][0] - merged_col2[i][0] < max_distance:
                    if not any(x > merged_col2[i][0] and x < merged_col2[i + 1][0] for x in col6_x):
                        if merged_col2[i][1] > merged_col2[i + 1][1]:
                            del merged_col2[i + 1]
                        else:
                            del merged_col2[i]
                        continue 
                i += 1

            return merged_col2


        def find_extreme_value(series, extreme='max'):
            extreme_idx = []
            n = s
            for i in range(len(series)):
                is_extreme = True  

                for j in range(1, min(n+1, len(series) - i)):
                    if (extreme == 'max' and float(series.iloc[i]) < float(series.iloc[i + j])) or \
                       (extreme == 'min' and float(series.iloc[i]) > float(series.iloc[i + j])):
                        is_extreme = False
                        break  

                if is_extreme:  
                    for j in range(1, min(n+1, i+1)):
                        if (extreme == 'max' and float(series.iloc[i]) < float(series.iloc[i - j])) or \
                           (extreme == 'min' and float(series.iloc[i]) > float(series.iloc[i - j])):
                            is_extreme = False
                            break  

                if is_extreme:
                    extreme_idx.append(i)  

            return extreme_idx


        for a in range(20,21):
            p1=a/20
            for b in range(80,81):
                p2=b/100

                if not os.path.exists(f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test"):
                    os.mkdir(f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test")
                if not os.path.exists(f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}"):
                    os.mkdir(f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}")
                if not os.path.exists(f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}/Tethered_1D_{v1}_{v2}{p2}"):
                    os.mkdir(f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}/Tethered_1D_{v1}_{v2}{p2}")
                if not os.path.exists(f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}/Tethered_1D_{v1}_{v2}{p2}/Tethered_1D_{v1}{p1}_{v2}{p2}"):
                    os.mkdir(f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}/Tethered_1D_{v1}_{v2}{p2}/Tethered_1D_{v1}{p1}_{v2}{p2}")
                d=f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}/Tethered_1D_{v1}_{v2}{p2}"
                d0=f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Tethered_1D_{v1}_{v2}{p2}"
                if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency"):
                    os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency")
                if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Double"):
                    os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Double")
                if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number"):
                    os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number")
                if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak"):
                    os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak")
                if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Penetration"):
                    os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Penetration")







                if Frequency == True: 

                    for i in range(0, 20):
                        path_output=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/wave_{a1}{p1}_{a2}{p2}_"+str(i)+".csv"
                        csvFile = open(path_output,'w',newline='',encoding='utf-8')
                        writer = csv.writer(csvFile)
                        csvRow = []
                        #,'r',encoding='gb2312'
                        path_input=d0+f"/wave_{v1}{p1}_{v2}{p2}_"+str(i)+".txt"
                        f = open(path_input)
                        header_list = ["slice_in_one_percent", "confined_drive_carrier_frequency_in_one_percent", "confined_drive_allele_frequency_in_one_percent", "suppression_drive_carrier_frequency_in_one_percent", "suppression_drive_allele_frequency_in_one_percent", "confined_drive_wt_frequency_in_one_percent", "confined_drive_wt_allele_frequency_in_one_percent", "suppression_drive_wt_frequency_in_one_percent", "suppression_drive_wt_allele_frequency_in_one_percent", "wt_frequency_in_one_percent", "num_in_one_percent", "num_in_all"]
                        writer.writerow(header_list)
                        for line in f:
                            csvRow = line.split()
                            writer.writerow(csvRow)
                         
                        f.close()
                        csvFile.close()

                        path_input=f"{d}/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/wave_{a1}{p1}_{a2}{p2}_"+str(i)+".csv"
                        path_output=f"{d}/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/wave_{a1}{p1}_{a2}{p2}_"+str(i)+"_n.csv" #name cannot be too long 

                        df = pd.read_csv(path_input)
                        divider = df.iloc[:, 10]

                        for col in [1, 3, 5, 7, 9]:
                            df.iloc[:, col] = df.iloc[:, col].div(divider, axis=0).fillna(0)

                        for col in [2, 4, 6, 8]:
                            df.iloc[:, col] = df.iloc[:, col].div(divider, axis=0).fillna(0)

                        df.to_csv(path_output, index=False)
                        if Smooth == True:
                            df = pd.read_csv(path_output)
                            original_output=f"{d}/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/wave_{a1}{p1}_{a2}{p2}_"+str(i)+"_n_o.csv"
                            smoothed_df = smooth_values_with_original_data(df)
                            Smooth_output=f"{d}/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/wave_{a1}{p1}_{a2}{p2}_"+str(i)+"_n_s.csv"
                            smoothed_df.to_csv(Smooth_output, index=False)

                    for j in range(0, 20):
                        if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_{j}"):
                            os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_{j}")
                        folder=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_{j}"
                        path=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/wave_{a1}{p1}_{a2}{p2}_{j}_n.csv"


                        df = pd.read_csv(path)


                        plt.figure(figsize=(10, 6), dpi=200)

                        for i in range(0, len(df), 100):
                            sub_df = df.iloc[i:i+100]
                            fig, ax = plt.subplots()
                            name=["confined_drive_carrier_frequency_in_one_percent", "suppression_drive_carrier_frequency_in_one_percent", "confined_drive_wt_frequency_in_one_percent", "suppression_drive_wt_frequency_in_one_percent"]
                            sub_df.plot(x="slice_in_one_percent", y=["confined_drive_carrier_frequency_in_one_percent", "suppression_drive_carrier_frequency_in_one_percent", "confined_drive_wt_frequency_in_one_percent", "suppression_drive_wt_frequency_in_one_percent"], ax=ax, color = color_list)
                            sub_df.plot(x="slice_in_one_percent", y="num_in_one_percent", ax=ax, secondary_y=True, kind="area", color="gray", alpha=0.5)
                            ax.set_xlim(1, 100)
                            ax.set_xticks([1 + 10 * i for i in range(10)])

                            ax.set_ylim(0, 1)
                            ax.set_yticks([0.2 * i for i in range(6)])

                            ax.right_ax.set_ylim(0, 140)
                            ax.right_ax.set_yticks([20 * i for i in range(8)])

                            ax.legend(loc='upper center', bbox_to_anchor=(1.5, 0.5), ncol=1)
                            ax.right_ax.legend(loc='upper center', bbox_to_anchor=(1.5, 0.1), ncol=1)
                            fig.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_{j}/output_{i/100}.png", dpi=200, bbox_inches="tight")
                            plt.close('all') 

                    for j in range(0, 20):
                        if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_s_{j}"):
                            os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_s_{j}")
                        folder=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_s_{j}"
                        path=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/wave_{a1}{p1}_{a2}{p2}_{j}_n_s.csv"

                        df = pd.read_csv(path)

                        plt.figure(figsize=(10, 6), dpi=200)

                        for i in range(0, len(df), 100):
                            sub_df = df.iloc[i:i+100]

                            fig, ax = plt.subplots()

                            sub_df.plot(x="slice_in_one_percent", y=["confined_drive_carrier_frequency_in_one_percent", "suppression_drive_carrier_frequency_in_one_percent", "confined_drive_wt_frequency_in_one_percent", "suppression_drive_wt_frequency_in_one_percent"], ax=ax, color = color_list)
                            sub_df.plot(x="slice_in_one_percent", y="num_in_one_percent", ax=ax, secondary_y=True, kind="area", color="gray", alpha=0.5)
                            
                            ax.set_xlim(1, 100)
                            ax.set_xticks([1 + 10 * i for i in range(10)])

                            ax.set_ylim(0, 1)
                            ax.set_yticks([0.2 * i for i in range(6)])

                            ax.right_ax.set_ylim(0, 140)
                            ax.right_ax.set_yticks([20 * i for i in range(8)])

                            ax.legend(loc='upper center', bbox_to_anchor=(1.5, 0.5), ncol=1)
                            ax.right_ax.legend(loc='upper center', bbox_to_anchor=(1.5, 0.1), ncol=1)
                            fig.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_s_{j}/output_s_{i/100}.png", dpi=200, bbox_inches="tight")
                            plt.close('all') 



                if Number == True:
                    import csv
                    import os
                    d=f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}/Tethered_1D_{v1}_{v2}{p2}"
                    if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number"):
                        os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number")
                    for i in range(0, 20):
                        path_output=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/wave_{a1}{p1}_{a2}{p2}_"+str(i)+".csv"
                        csvFile = open(path_output,'w',newline='',encoding='utf-8')
                        writer = csv.writer(csvFile)
                        csvRow = []
                        path_input=d0+f"/wave_{v1}{p1}_{v2}{p2}_"+str(i)+".txt"
                        f = open(path_input)
                        header_list = ["slice_in_one_percent", "confined_drive_carrier_frequency_in_one_percent", "confined_drive_allele_frequency_in_one_percent", "suppression_drive_carrier_frequency_in_one_percent", "suppression_drive_allele_frequency_in_one_percent", "confined_drive_wt_frequency_in_one_percent", "confined_drive_wt_allele_frequency_in_one_percent", "suppression_drive_wt_frequency_in_one_percent", "suppression_drive_wt_allele_frequency_in_one_percent", "wt_frequency_in_one_percent", "num_in_one_percent", "num_in_all"]
                        writer.writerow(header_list)
                        for line in f:
                            csvRow = line.split()
                            writer.writerow(csvRow)
                         
                        f.close()
                        csvFile.close()

                    import pandas as pd
                    for i in range(0, 20):
                        path_input=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/wave_{a1}{p1}_{a2}{p2}_"+str(i)+".csv"
                        path_output=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/wave_{a1}{p1}_{a2}{p2}_"+str(i)+"_n.csv"
                        df = pd.read_csv(path_input)
                        df.to_csv(path_output, index=False)
                        if Smooth == True:
                            df = pd.read_csv(path_input)
                            original_output=f"{d}/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/wave_{a1}{p1}_{a2}{p2}_"+str(i)+"_n_o.csv"
                            smoothed_df = smooth_values_with_original_data(df)
                            Smooth_output=f"{d}/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/wave_{a1}{p1}_{a2}{p2}_"+str(i)+"_n_s.csv"
                            smoothed_df.to_csv(Smooth_output, index=False)



                    for j in range(0, 20):
                        plt.figure(figsize=(10, 6), dpi=200)
                        peak_output=d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak.csv'
                        peak_average=d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_a.csv'
                        peak_average_penetration=d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_a_p.csv'
                        if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_{j}"):
                            os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_{j}")
                        folder=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_{j}"
                        path=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/wave_{a1}{p1}_{a2}{p2}_{j}_n.csv"
                        path1=d0+f"/wave_{v1}{p1}_{v2}{p2}_{j}.txt"
                        df = pd.read_csv(path, header=None,index_col=False)
                        df3 = pd.read_csv(path)
                        df2 = df.iloc[1:]
                        df1 = pd.read_csv(path1, sep=' ', header=None, index_col=False)



                        store=[]
                        for i in range(0, len(df2), 100):
                            group = df2[i:i+100]
                            col2_max_idx = find_extreme_value(group[1], 'max')
                            col2_max_val = group.iloc[col2_max_idx, 1]
                            col2 = [(index%100, float(value)) for index, value in col2_max_val.items()]
                            col2_sorted = sorted(col2, key=lambda x: x[0])
                            old_merged_col2 = merge_non_zero_points(col2_sorted)                

                            col4_max_idx = find_extreme_value(group[3], 'max') 
                            col4_max_val = group.iloc[col4_max_idx, 3]
                            col4 = [(index%100, float(value)) for index, value in col4_max_val.items()]
                            col4_sorted = sorted(col4, key=lambda x: x[0])
                            merged_col4 = merge_non_zero_points(col4_sorted)     

                            col6_max_idx = find_extreme_value(group[5], 'max')
                            col6_max_val = group.iloc[col6_max_idx, 5]
                            col6 = [(index%100, float(value)) for index, value in col6_max_val.items()]
                            col6_sorted = sorted(col6, key=lambda x: x[0])
                            merged_col6 = merge_non_zero_points_wt(col6_sorted)     

                            col8_max_idx = find_extreme_value(group[7], 'max')
                            col8_max_val = group.iloc[col8_max_idx, 7]
                            col8 = [(index%100, float(value)) for index, value in col8_max_val.items()]
                            col8_sorted = sorted(col8, key=lambda x: x[0])
                            merged_col8 = merge_non_zero_points_wt(col8_sorted)     

                            col11_min_idx = find_extreme_value(group[10], 'min')
                            col11_min_val = group.iloc[col11_min_idx, 10]
                            col11_min_val = pd.to_numeric(col11_min_val, errors='coerce')
                            col11_min_val = col11_min_val[col11_min_val < 20]
                            col11 = [(index%100, float(value)) for index, value in col11_min_val.items()]
                            col11_sorted = sorted(col11, key=lambda x: x[0])
                            merged_col11 = merge_continuous_zero_y(col11_sorted)      

                            merged_col2 = find_extreme_value_with_merging(old_merged_col2, merged_col6, max_distance=50)

                            data=[merged_col2,merged_col4,merged_col6,merged_col8,merged_col11]
                            #print(data)
                            values = [','.join(str(item[0]) for item in lst) for lst in data]
                            store.append(values)

                            sub_df = df3.iloc[i:i+100]
                            

                            fig, ax = plt.subplots()
                            sub_df.plot(x="slice_in_one_percent", y=["confined_drive_carrier_frequency_in_one_percent", "suppression_drive_carrier_frequency_in_one_percent", "confined_drive_wt_frequency_in_one_percent", "suppression_drive_wt_frequency_in_one_percent"], ax=ax, color = color_list)

                            sub_df.plot(x="slice_in_one_percent", y="num_in_one_percent", ax=ax, secondary_y=True, kind="area", color="gray", alpha=0.5)

                            ax.set_xlim(1, 100)
                            ax.set_xticks([1 + 10 * i for i in range(10)])


                            ax.set_ylim(0, 140)
                            ax.set_yticks([20 * i for i in range(8)])

                            ax.right_ax.set_ylim(0, 140)
                            ax.right_ax.set_yticks([20 * i for i in range(8)])

                            if not merged_col2:
                                print("No TARE peak")
                            else:
                                for x_2, y_2 in merged_col2:
                                    y_2 = float(y_2)
                                    plt.scatter(x_2, y_2, color='#17AD65', label='', marker='s')

                            if not merged_col4:
                                print("No Homing peak")
                            else:
                                for x_4, y_4 in merged_col4:
                                    y_4 = float(y_4)
                                    plt.scatter(x_4, y_4, color='#EE5F00', label='', marker='s')

                            if not merged_col6:
                                print("No TWT peak")
                            else:
                                for x_6, y_6 in merged_col6:
                                    y_6 = float(y_6)
                                    plt.scatter(x_6, y_6, color='#286BEE', label='', marker='s')    

                            if not merged_col8:
                                print("No HWT peak")
                            else:
                                for x_8, y_8 in merged_col8:
                                    y_8 = float(y_8)
                                    plt.scatter(x_8, y_8, color='#9B72AA', label='', marker='s')    

                            if not merged_col11:
                                print("No empty peak")
                            else:
                                for x_11, y_11 in merged_col11:
                                    y_11 = float(y_11)
                                    plt.scatter(x_11, y_11, color='#606060', label='', marker='s')  


                            ax.legend(loc='upper center', bbox_to_anchor=(1.5, 0.5), ncol=1)
                            ax.right_ax.legend(loc='upper center', bbox_to_anchor=(1.5, 0.1), ncol=1)

                            ax.right_ax.set_ylim(0, 140)
                            ax.right_ax.set_yticks([20 * i for i in range(8)])

                            plt.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_{j}/output_{i/100}.png", dpi=200, bbox_inches="tight") 
                            plt.close("all") 

                        df4 = pd.DataFrame(store,columns=['TARE', 'Homing', 'TWT', 'HWT', 'Empty'])

                        df4.to_csv(peak_output, index=False)

                        df5 = pd.read_csv(peak_output, dtype=str)

                        '''
                        plt.figure(figsize=(10, 6))
                        ax = plt.gca()

                        for index, row in df5.iterrows():
                            ax.set_xticks(range(0, len(df5),5), minor=True)

                            plt.grid(which='minor', axis='x', zorder=2)
                            plt.grid(axis='x', zorder=2)
                            if pd.notna(row[0]):
                                y_values_0 = [float(val_0) for val_0 in row[0].split(',')]
                                plt.scatter([index] * len(y_values_0), y_values_0, color='#17AD65', label='TARE', zorder=3)
                                #if len(y_values_0) > 1:
                                    #plt.plot([index] * len(y_values_0), y_values_0, color='#17AD65', label='TARE')

                            if pd.notna(row[1]):
                                y_values_1 = [float(val_1) for val_1 in row[1].split(',')]
                                plt.scatter([index] * len(y_values_1), y_values_1, color='#EE5F00', label='Homing', zorder=3)
                                #if len(y_values_1) > 1:
                                    #plt.plot([index] * len(y_values_1), y_values_1, color='#EE5F00', label='Homing')

                            if pd.notna(row[2]):
                                y_values_2 = [float(val_2) for val_2 in row[2].split(',')]
                                plt.scatter([index] * len(y_values_2), y_values_2, color='#286BEE', label='TWT', zorder=3)
                                #if len(y_values_2) > 1:
                                    #plt.plot([index] * len(y_values_2), y_values_2, color='#286BEE', label='TWT')

                            if pd.notna(row[3]):
                                y_values_3 = [float(val_3) for val_3 in row[3].split(',')]
                                plt.scatter([index] * len(y_values_3), y_values_3, color='#9B72AA', label='HWT', zorder=3)
                                #if len(y_values_3) > 1:
                                    #plt.plot([index] * len(y_values_3), y_values_3, color='#9B72AA', label='HWT')

                            if pd.notna(row[4]):
                                y_values_4 = [float(val_4) for val_4 in row[4].split(',')]
                                plt.scatter([index] * len(y_values_4), y_values_4, color='gray', label='Empty', zorder=3)
                                #if len(y_values_4) > 1:
                                    #plt.plot([index] * len(y_values_4), y_values_4, color='gray', label='Empty')



                        handles, labels = ax.get_legend_handles_labels()

                        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]

                        ax.legend(*zip(*unique))

                        plt.title('')
                        plt.xlabel('Generation')
                        plt.ylabel('Peak')
                        #plt.grid(axis='x')


                        plt.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_{s}.png", dpi=300, bbox_inches="tight") 
                        #plt.show()
                        plt.close("all")
                        '''


                        df6 = pd.read_csv(peak_output)
                        for column in df6.columns:
                            df6[column] = df6[column].apply(lambda x: calculate_average(x) if isinstance(x, str) else x)
                        df6.to_csv(peak_average, index=False)


                        new_df = pd.read_csv(peak_average)
                        selected_rows = []
                        for i in range(len(new_df) - 1):
                            if check_conditions(new_df.iloc[i], new_df.iloc[i + 1]):
                                selected_rows.append(new_df.iloc[i])

                        selected_df = pd.DataFrame(selected_rows)
                        selected_df.to_csv(peak_average_penetration, index=False)


                        '''
                        plt.scatter(new_df.index, new_df[new_df.columns[0]], color='#17AD65') 
                        plt.plot(new_df.index, new_df[new_df.columns[0]], linestyle='-', linewidth=1, color='#17AD65') 
                        plt.scatter(new_df.index, new_df[new_df.columns[1]], color='#EE5F00') 
                        plt.plot(new_df.index, new_df[new_df.columns[1]], linestyle='-', linewidth=1, color='#EE5F00') 
                        plt.scatter(new_df.index, new_df[new_df.columns[2]], color='#286BEE')  
                        plt.plot(new_df.index, new_df[new_df.columns[2]], linestyle='-', linewidth=1, color='#286BEE')
                        plt.scatter(new_df.index, new_df[new_df.columns[3]], color='#9B72AA')  
                        plt.plot(new_df.index, new_df[new_df.columns[3]], linestyle='-', linewidth=1, color='#9B72AA')
                        plt.scatter(new_df.index, new_df[new_df.columns[4]], color='#606060')  
                        plt.plot(new_df.index, new_df[new_df.columns[4]], linestyle='-', linewidth=1, color='#606060')
                        y_min = plt.ylim()[0] - (plt.ylim()[1] - plt.ylim()[0]) * 0.05

                        for index in selected_df.index:
                            plt.axvline(x=index, color='red', linestyle='--')
                            plt.text(index, y_min, str(index), color='red', verticalalignment='bottom', horizontalalignment='center')

                        plt.xlabel('Index')
                        plt.ylabel(new_df.columns[0])
                        plt.title('Scatter Plot of Data')
                        plt.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_{s}_a.png", dpi=300, bbox_inches="tight") 
                        #plt.show()
                        plt.close("all")
                        '''

                    for j in range(0, 20):
                        plt.figure(figsize=(10, 6), dpi=300)
                        peak_output=d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_s.csv'
                        peak_average=d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_a_s.csv'
                        peak_average_penetration=d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_a_p_s.csv'
                        if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_s_{j}"):
                            os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_s_{j}")
                        folder=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_s_{j}"
                        path=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/wave_{a1}{p1}_{a2}{p2}_{j}_n_s.csv"
                        path1=d0+f"/wave_{v1}{p1}_{v2}{p2}_{j}.txt"
                        df = pd.read_csv(path, header=None,index_col=False)
                        df3 = pd.read_csv(path)
                        df2 = df.iloc[1:]
                        df1 = pd.read_csv(path1, sep=' ', header=None, index_col=False)
                        store=[]
                        for i in range(0, len(df2), 100):
                            group = df2[i:i+100]
                            col2_max_idx = find_extreme_value(group[1], 'max')
                            col2_max_val = group.iloc[col2_max_idx, 1]
                            col2 = [(index%100, float(value)) for index, value in col2_max_val.items()]
                            col2_sorted = sorted(col2, key=lambda x: x[0])
                            old_merged_col2 = merge_non_zero_points(col2_sorted)                

                            col4_max_idx = find_extreme_value(group[3], 'max') 
                            col4_max_val = group.iloc[col4_max_idx, 3]
                            col4 = [(index%100, float(value)) for index, value in col4_max_val.items()]
                            col4_sorted = sorted(col4, key=lambda x: x[0])
                            old_merged_col4 = merge_non_zero_points(col4_sorted)     

                            col6_max_idx = find_extreme_value(group[5], 'max')
                            col6_max_val = group.iloc[col6_max_idx, 5]
                            col6 = [(index%100, float(value)) for index, value in col6_max_val.items()]
                            col6_sorted = sorted(col6, key=lambda x: x[0])
                            merged_col6 = merge_non_zero_points_wt(col6_sorted)     


                            col8_max_idx = find_extreme_value(group[7], 'max')
                            col8_max_val = group.iloc[col8_max_idx, 7]
                            col8 = [(index%100, float(value)) for index, value in col8_max_val.items()]
                            col8_sorted = sorted(col8, key=lambda x: x[0])
                            merged_col8 = merge_non_zero_points_wt(col8_sorted)     


                            col11_min_idx = find_extreme_value(group[10], 'min')
                            col11_min_val = group.iloc[col11_min_idx, 10]
                            col11_min_val = pd.to_numeric(col11_min_val, errors='coerce')
                            col11_min_val = col11_min_val[col11_min_val < 20]
                            col11 = [(index%100, float(value)) for index, value in col11_min_val.items()]
                            col11_sorted = sorted(col11, key=lambda x: x[0])
                            merged_col11 = merge_continuous_zero_y(col11_sorted)      


                            merged_col2 = find_extreme_value_with_merging(old_merged_col2, merged_col6, max_distance=50)
                            merged_col4 = find_extreme_value_with_merging(old_merged_col4, merged_col8, max_distance=50)
                            
                            data=[merged_col2,merged_col4,merged_col6,merged_col8,merged_col11]

                            values = [','.join(str(item[0]) for item in lst) for lst in data]
                            store.append(values)
                            
                            sub_df = df3.iloc[i:i+100]                            
                            fig, ax = plt.subplots()
                            sub_df.plot(x="slice_in_one_percent", y=["confined_drive_carrier_frequency_in_one_percent", "suppression_drive_carrier_frequency_in_one_percent", "confined_drive_wt_frequency_in_one_percent", "suppression_drive_wt_frequency_in_one_percent"], ax=ax, color = color_list)
                            sub_df.plot(x="slice_in_one_percent", y="num_in_one_percent", ax=ax, secondary_y=True, kind="area", color="gray", alpha=0.5)
                            
                            ax.set_xlim(1, 100)
                            ax.set_xticks([1 + 10 * i for i in range(10)])

                            ax.set_ylim(0, 140)
                            ax.set_yticks([20 * i for i in range(8)])

                            ax.right_ax.set_ylim(0, 140)
                            ax.right_ax.set_yticks([20 * i for i in range(8)])

                            if not merged_col2:
                                print("No TARE peak")
                            else:
                                for x_2, y_2 in merged_col2:
                                    y_2 = float(y_2)
                                    plt.scatter(x_2, y_2, color='#17AD65', label='', marker='s')

                            if not merged_col4:
                                print("No Homing peak")
                            else:
                                for x_4, y_4 in merged_col4:
                                    y_4 = float(y_4)
                                    plt.scatter(x_4, y_4, color='#EE5F00', label='', marker='s')

                            if not merged_col6:
                                print("No TWT peak")
                            else:
                                for x_6, y_6 in merged_col6:
                                    y_6 = float(y_6)
                                    plt.scatter(x_6, y_6, color='#286BEE', label='', marker='s')    

                            if not merged_col8:
                                print("No HWT peak")
                            else:
                                for x_8, y_8 in merged_col8:
                                    y_8 = float(y_8)
                                    plt.scatter(x_8, y_8, color='#9B72AA', label='', marker='s')    

                            if not merged_col11:
                                print("No empty peak")
                            else:
                                for x_11, y_11 in merged_col11:
                                    y_11 = float(y_11)
                                    plt.scatter(x_11, y_11, color='#606060', label='', marker='s')  

                            ax.legend(loc='upper center', bbox_to_anchor=(1.5, 0.5), ncol=1)
                            ax.right_ax.legend(loc='upper center', bbox_to_anchor=(1.5, 0.1), ncol=1)
                            ax.right_ax.set_ylim(0, 140)
                            ax.right_ax.set_yticks([20 * i for i in range(8)])
                            plt.ylim(0, 140) 
                            plt.yticks([20 * i for i in range(8)])  

                            plt.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_s_{j}/output_s_{i/100}.png", dpi=200, bbox_inches="tight") 
                            plt.close("all") 

                        df4 = pd.DataFrame(store,columns=['TARE', 'Homing', 'TWT', 'HWT', 'Empty'])
                        df4.to_csv(peak_output, index=False)

                        df5 = pd.read_csv(peak_output, dtype=str)

                        penetration_output = d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_penetration.csv' 
                        penetration_TARE = d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_p_T.csv'
                        penetration_Homing = d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_p_H.csv'
                        process_csv(peak_output, penetration_output)
                        process_csv_H(penetration_output, penetration_output)

                        plt.figure(figsize=(10, 6))
                        ax = plt.gca()

                        for index, row in df5.iterrows():
                            ax.set_xticks(range(0, len(df5),5), minor=True)
                            plt.grid(which='minor', axis='x', zorder=2)
                            plt.grid(axis='x', zorder=2)
                            if pd.notna(row[0]):
                                y_values_0 = [float(val_0) for val_0 in row[0].split(',')]
                                plt.scatter([index] * len(y_values_0), y_values_0, color='#17AD65', label='TARE', zorder=3)

                                #if len(y_values_0) > 1:
                                    #plt.plot([index] * len(y_values_0), y_values_0, color='#17AD65', label='TARE')

                            if pd.notna(row[1]):
                                y_values_1 = [float(val_1) for val_1 in row[1].split(',')]
                                plt.scatter([index] * len(y_values_1), y_values_1, color='#EE5F00', label='Homing', zorder=3)

                                #if len(y_values_1) > 1:
                                    #plt.plot([index] * len(y_values_1), y_values_1, color='#EE5F00', label='Homing')

                            if pd.notna(row[2]):
                                y_values_2 = [float(val_2) for val_2 in row[2].split(',')]
                                plt.scatter([index] * len(y_values_2), y_values_2, color='#286BEE', label='TWT', zorder=3)

                                #if len(y_values_2) > 1:
                                    #plt.plot([index] * len(y_values_2), y_values_2, color='#286BEE', label='TWT')

                            if pd.notna(row[3]):
                                y_values_3 = [float(val_3) for val_3 in row[3].split(',')]
                                plt.scatter([index] * len(y_values_3), y_values_3, color='#9B72AA', label='HWT', zorder=3)

                                #if len(y_values_3) > 1:
                                    #plt.plot([index] * len(y_values_3), y_values_3, color='#9B72AA', label='HWT')

                            if pd.notna(row[4]):
                                y_values_4 = [float(val_4) for val_4 in row[4].split(',')]
                                plt.scatter([index] * len(y_values_4), y_values_4, color='gray', label='Empty', zorder=3)

                                #if len(y_values_4) > 1:
                                    #plt.plot([index] * len(y_values_4), y_values_4, color='gray', label='Empty')


                        handles, labels = ax.get_legend_handles_labels()
                        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
                        ax.legend(*zip(*unique))

                        df7 = pd.read_csv(penetration_output)  

                        for index, row in df7.iterrows():
                            if pd.notna(row['Values']):
                                values = ast.literal_eval(row['Values'])
                                for val in values:
                                    plt.scatter(index, val, marker='*', color='black', s=30, zorder=4)
                                    plt.axvline(x=index, color='r', linestyle='--', zorder=2)
                            if pd.notna(row['Values_after']):
                                values = ast.literal_eval(row['Values_after'])
                                for val in values:
                                    plt.scatter(index, val, marker='s', color='white', s=10, zorder=5)
                                    plt.axvline(x=index, color='g', linestyle=':', zorder=2)

                        sequences = find_sequences(df7,5,7)


                        df7['successful-penetration'] = False
                        for start, end in sequences:
                            df7.loc[start:end-1, 'successful-penetration'] = True

                        y_100 = 100
                        for start, end in sequences:
                            plt.plot([start-0.5, end - 0.5, end - 0.5, start-0.5, start-0.5],
                                     [0, 0, y_100, y_100, 0],
                                     color='green', linestyle='--', linewidth=3)

                        df7.to_csv(penetration_TARE, index=False)

                        plt.title('')
                        plt.xlabel('Generation')
                        plt.ylabel('Peak')

                        plt.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_s_{s}_T.png", dpi=300, bbox_inches="tight") 
                        plt.close("all")
                        plt.figure(figsize=(10, 6))
                        ax = plt.gca()

                        for index, row in df5.iterrows():
                            ax.set_xticks(range(0, len(df5),5), minor=True)
                            plt.grid(which='minor', axis='x', zorder=2)
                            plt.grid(axis='x', zorder=2)
                            if pd.notna(row[0]):
                                y_values_0 = [float(val_0) for val_0 in row[0].split(',')]
                                plt.scatter([index] * len(y_values_0), y_values_0, color='#17AD65', label='TARE', zorder=3)
                                #if len(y_values_0) > 1:
                                    #plt.plot([index] * len(y_values_0), y_values_0, color='#17AD65', label='TARE')

                            if pd.notna(row[1]):
                                y_values_1 = [float(val_1) for val_1 in row[1].split(',')]
                                plt.scatter([index] * len(y_values_1), y_values_1, color='#EE5F00', label='Homing', zorder=3)
                                #if len(y_values_1) > 1:
                                    #plt.plot([index] * len(y_values_1), y_values_1, color='#EE5F00', label='Homing')

                            if pd.notna(row[2]):
                                y_values_2 = [float(val_2) for val_2 in row[2].split(',')]
                                plt.scatter([index] * len(y_values_2), y_values_2, color='#286BEE', label='TWT', zorder=3)
                                #if len(y_values_2) > 1:
                                    #plt.plot([index] * len(y_values_2), y_values_2, color='#286BEE', label='TWT')

                            if pd.notna(row[3]):
                                y_values_3 = [float(val_3) for val_3 in row[3].split(',')]
                                plt.scatter([index] * len(y_values_3), y_values_3, color='#9B72AA', label='HWT', zorder=3)
                                #if len(y_values_3) > 1:
                                    #plt.plot([index] * len(y_values_3), y_values_3, color='#9B72AA', label='HWT')

                            if pd.notna(row[4]):
                                y_values_4 = [float(val_4) for val_4 in row[4].split(',')]
                                plt.scatter([index] * len(y_values_4), y_values_4, color='gray', label='Empty', zorder=3)
                                #if len(y_values_4) > 1:
                                    #plt.plot([index] * len(y_values_4), y_values_4, color='gray', label='Empty')


                        handles, labels = ax.get_legend_handles_labels()
                        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
                        ax.legend(*zip(*unique))

                        df7 = pd.read_csv(penetration_output) 

                        for index, row in df7.iterrows():
                            if pd.notna(row['Values_H']):
                                values = ast.literal_eval(row['Values_H'])
                                for val in values:
                                    plt.scatter(index, val, marker='*', color='black', s=30, zorder=4)
                                    plt.axvline(x=index, color='r', linestyle='--', zorder=2)
                            if pd.notna(row['Values_after_H']):
                                values = ast.literal_eval(row['Values_after_H'])
                                for val in values:
                                    plt.scatter(index, val, marker='s', color='white', s=10, zorder=5)
                                    plt.axvline(x=index, color='g', linestyle=':', zorder=2)

                        sequences_H = find_sequences(df7,9,11)


                        df7['successful-penetration_H'] = False
                        for start, end in sequences_H:
                            df7.loc[start:end-1, 'successful-penetration_H'] = True

                        y_100 = 100

                        for start, end in sequences_H:
                            plt.plot([start-0.5, end - 0.5, end - 0.5, start-0.5, start-0.5],
                                     [0, 0, y_100, y_100, 0],
                                     color='orange', linestyle='--', linewidth=3)

                        df7.to_csv(penetration_TARE, index=False)

                        plt.title('')
                        plt.xlabel('Generation')
                        plt.ylabel('Peak')

                        plt.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_s_{s}_H.png", dpi=300, bbox_inches="tight") 
                        plt.close("all")
                        img_path1 = d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_s_{s}_T.png"
                        img_path2 = d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_s_{s}_H.png"
                        output_path = d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_s_{s}.png"
                        combine_images_vertically(img_path1, img_path2, output_path)

                        df6 = pd.read_csv(peak_output)
                        for column in df6.columns:
                            df6[column] = df6[column].apply(lambda x: calculate_average(x) if isinstance(x, str) else x)

                        df6.to_csv(peak_average, index=False)

                        new_df = pd.read_csv(peak_average)
                        selected_rows = []
                        for i in range(len(new_df) - 1):
                            if check_conditions(new_df.iloc[i], new_df.iloc[i + 1]):
                                selected_rows.append(new_df.iloc[i])

                        selected_df = pd.DataFrame(selected_rows)
                        selected_df.to_csv(peak_average_penetration, index=False)


                        '''
                        plt.scatter(new_df.index, new_df[new_df.columns[0]], color='#17AD65') 
                        plt.plot(new_df.index, new_df[new_df.columns[0]], linestyle='-', linewidth=1, color='#17AD65') 
                        plt.scatter(new_df.index, new_df[new_df.columns[1]], color='#EE5F00') 
                        plt.plot(new_df.index, new_df[new_df.columns[1]], linestyle='-', linewidth=1, color='#EE5F00') 
                        plt.scatter(new_df.index, new_df[new_df.columns[2]], color='#286BEE')  
                        plt.plot(new_df.index, new_df[new_df.columns[2]], linestyle='-', linewidth=1, color='#286BEE')
                        plt.scatter(new_df.index, new_df[new_df.columns[3]], color='#9B72AA')  
                        plt.plot(new_df.index, new_df[new_df.columns[3]], linestyle='-', linewidth=1, color='#9B72AA')
                        plt.scatter(new_df.index, new_df[new_df.columns[4]], color='#606060')  
                        plt.plot(new_df.index, new_df[new_df.columns[4]], linestyle='-', linewidth=1, color='#606060')
                        y_min = plt.ylim()[0] - (plt.ylim()[1] - plt.ylim()[0]) * 0.05

                        for index in selected_df.index:
                            plt.axvline(x=index, color='red', linestyle='--')
                            plt.text(index, y_min, str(index), color='red', verticalalignment='bottom', horizontalalignment='center')
                        plt.xlabel('Index')
                        plt.ylabel(new_df.columns[0])
                        plt.title('Scatter Plot of Data')

                        plt.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_{s}_a_s.png", dpi=300, bbox_inches="tight") 
                        #plt.show()
                        plt.close("all")
                        '''






                from PIL import Image
                import numpy as np
                d=f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}/Tethered_1D_{v1}_{v2}{p2}"
                for j in range(0, 20):
                    import os
                    if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Double/fig_s_{j}"):
                        os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Double/fig_s_{j}")
                    folder_path = (d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_s_{j}") 
                    png_count = 0

                    for filename in os.listdir(folder_path):
                        if filename.endswith(".png"):
                            png_count += 1
                    a=round(float(png_count), 1)

                    for i in np.arange(0,a,1):
                        image1 = Image.open(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_{j}/output_{i}.png")
                        image2 = Image.open(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_{j}/output_{i}.png")
                        image3 = Image.open(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_s_{j}/output_s_{i}.png")
                        image4 = Image.open(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_s_{j}/output_s_{i}.png")  
                        width1, height1 = image1.size
                        width2, height2 = image2.size
                        width3, height3 = image3.size
                        width4, height4 = image4.size
                        new_width = max(width1+width3, width2+width4)
                        new_height = max(height1+height2, height3+height4)

                        combined_image = Image.new('RGB', (new_width, new_height))
                        combined_image.paste(image1, (0, 0))

                        combined_image.paste(image2, (0, height1))
                        combined_image.paste(image3, (width1, 0))
                        combined_image.paste(image4, (width1, height1))
                        combined_image.save(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Double/fig_s_{j}/output_{i}.png")
                        plt.close('all') 


if allele==1:

    def find_sequences(df,a,b):
        sequences = []
        i = 0
        while i < len(df) - 1:
            if df.iloc[i, a] == True and df.iloc[i + 1, a] == True and df.iloc[i, b] == False:
                start = i
                while i < len(df) and df.iloc[i, a] == True:
                    if df.iloc[i, b] == True:  
                        break
                    i += 1
                end = i

                true_count = 0
                for j in range(end, len(df)):
                    if df.iloc[j, b] == True:
                        true_count += 1
                    else:
                        if true_count >= 2:
                            sequences.append((start, j)) 
                        i = j
                        break
                else:
                    if true_count >= 2:
                        sequences.append((start, len(df))) 
                    break
            else:
                i += 1
        return sequences



    def check_condition_H(row):
        col1 = str(row['Homing'])
        col3 = str(row['HWT'])
        col5 = str(row['Empty'])

        col1_values = [float(val) for val in col1.split(",") if val]
        col3_values = [float(val) for val in col3.split(",") if val]
        col5_values = [float(val) for val in col5.split(",") if val]

        for val5 in col5_values:
            for val3 in col3_values:
                for val1 in col1_values:
                    if val5 < val3 < val1:
                        return True, (val1, val3, val5)
        return False, None

    def check_condition_after_H(row):
        col1 = str(row['Homing'])
        col3 = str(row['HWT'])
        col5 = str(row['Empty'])

        col1_values = [float(val) for val in col1.split(",") if val]
        col3_values = [float(val) for val in col3.split(",") if val]
        col5_values = [float(val) for val in col5.split(",") if val]

        for val5 in col5_values:
            for val3 in col3_values:
                for val1 in col1_values:
                    if val3 < val5 < val1:
                        return True, (val1, val3, val5)
        return False, None

    def process_csv_H(input_file, output_file):
        df = pd.read_csv(input_file)
        df['Result_H'], df['Values_H']= zip(*df.apply(check_condition_H, axis=1))
        df['Result_after_H'], df['Values_after_H']= zip(*df.apply(check_condition_after_H, axis=1))
        df.to_csv(output_file, index=False)


    def check_condition(row):
        col1 = str(row['TARE'])
        col3 = str(row['TWT'])
        col5 = str(row['Empty'])

        col1_values = [float(val) for val in col1.split(",") if val]
        col3_values = [float(val) for val in col3.split(",") if val]
        col5_values = [float(val) for val in col5.split(",") if val]

        for val5 in col5_values:
            for val3 in col3_values:
                for val1 in col1_values:
                    if val5 < val3 < val1:
                        return True, (val1, val3, val5)
        return False, None

    def check_condition_after(row):
        col1 = str(row['TARE'])
        col3 = str(row['TWT'])
        col5 = str(row['Empty'])

        col1_values = [float(val) for val in col1.split(",") if val]
        col3_values = [float(val) for val in col3.split(",") if val]
        col5_values = [float(val) for val in col5.split(",") if val]

        for val5 in col5_values:
            for val3 in col3_values:
                for val1 in col1_values:
                    if val3 < val5 < val1:
                        return True, (val1, val3, val5)
        return False, None

    def process_csv(input_file, output_file):
        df = pd.read_csv(input_file)

        df['Result'], df['Values']= zip(*df.apply(check_condition, axis=1))
        df['Result_after'], df['Values_after']= zip(*df.apply(check_condition_after, axis=1))

        df.to_csv(output_file, index=False)


    def smooth_values_with_original_data(df, mode=1, group_size=100):
        original_df = df.copy()

        weights = {
            1: [0.1875, 0.375, 0.75, 1, 0.75, 0.375, 0.1875],
            2: [0.2, 0.4, 0.8, 1, 0.8, 0.4, 0.2],
            3: [0.125, 0.25, 0.5, 1, 0.5, 0.25, 0.125]
        }[mode]

        one_sided_weights = weights[3:]

        for start in range(0, len(df), group_size):
            end = min(start + group_size, len(df))
            for i in range(start, end):
                for col in df.columns[1:]:  
                    if i < start + 3:
                        right_size = i - start + 1
                        window = original_df[col][i:i + right_size]
                        adjusted_weights = one_sided_weights[:right_size]
                    elif i >= end - 3:
                        left_size = end - i
                        window = original_df[col][i - left_size + 1:i + 1]
                        adjusted_weights = one_sided_weights[-left_size:]
                    else:
                        window = original_df[col][i - 3:i + 4]
                        adjusted_weights = weights

                    if len(window) != 0 and len(window) == len(adjusted_weights):
                        weighted_sum = sum(w * x for w, x in zip(adjusted_weights, window))
                        df.at[i, col] = weighted_sum / sum(adjusted_weights)
                    else:
                        df.at[i, col] = original_df.at[i, col]

        return df


    def merge_continuous_zero_y(col):
        col = [(x, y) for x, y in col if x != 0]

        merged = []
        start_index = None
        end_index = None
        current_y = None

        for i, (x, y) in enumerate(col):
            if start_index is None:
                start_index = i
                current_y = y
            end_index = i

            if i + 1 < len(col) and (col[i + 1][1] != current_y or col[i + 1][0] - x > 1):
                avg_x = sum(col[j][0] for j in range(start_index, end_index + 1)) / (end_index - start_index + 1)
                merged.append((avg_x, current_y))
                start_index = None

        if start_index is not None:
            avg_x = sum(col[j][0] for j in range(start_index, end_index + 1)) / (end_index - start_index + 1)
            merged.append((avg_x, current_y))

        return merged

    def merge_non_zero_points(col):
        threshold=3
        if not col:
            return []

        merged = []
        in_small_segment = False

        for i, (x, y) in enumerate(col):
            if y < threshold:
                if not in_small_segment:
                    in_small_segment = True
            else:
                if in_small_segment:
                    in_small_segment = False
                merged.append((x, y)) 
        return merged

    def merge_non_zero_points_wt(col):
        merged = [(x, y) for x, y in col if y != 0 and x != 0]
        return merged




    def calculate_average(data):
        try:
            numbers = [float(x) for x in data.split(',')]
            return sum(numbers) / len(numbers)
        except:
            return None

    def check_conditions(row_n, row_n_plus_1):
        cond1 = row_n_plus_1[0] > row_n_plus_1[2] and \
                row_n_plus_1[3] - row_n[3] > 0 and row_n_plus_1[2] - row_n[2] > 0 and \
                row_n_plus_1[3] - row_n[3] > row_n_plus_1[2] - row_n[2] and \
                row_n_plus_1[3] - row_n_plus_1[2] >= -2 and row_n[3] - row_n[2] <= 0

        cond2 = row_n_plus_1[0] < row_n_plus_1[2] and \
                row_n_plus_1[3] - row_n[3] < 0 and row_n_plus_1[2] - row_n[2] < 0 and \
                row_n_plus_1[3] - row_n[3] < row_n_plus_1[2] - row_n[2] and \
                row_n_plus_1[3] - row_n_plus_1[2] <= 2 and row_n[3] - row_n[2] >= 0

        return cond1 or cond2

    for s in range(10,11):
        def find_extreme_value_with_merging(merged_col2, merged_col6, max_distance=50):
            col6_x = [x[0] for x in merged_col6] if merged_col6 else []

            merged_col2 = list(merged_col2)  
            i = 0
            while i < len(merged_col2) - 1:
                if merged_col2[i + 1][0] - merged_col2[i][0] < max_distance:
                    if not any(x > merged_col2[i][0] and x < merged_col2[i + 1][0] for x in col6_x):
                        if merged_col2[i][1] > merged_col2[i + 1][1]:
                            del merged_col2[i + 1]
                        else:
                            del merged_col2[i]
                        continue  
                i += 1

            return merged_col2


        def find_extreme_value_easy(series, extreme='max'):
            extreme_idx = []
            n = s
            for i in range(len(series)):
                is_extreme = True  

                for j in range(1, min(n+1, len(series) - i)):
                    if (extreme == 'max' and float(series.iloc[i]) < float(series.iloc[i + j])) or \
                       (extreme == 'min' and float(series.iloc[i]) > float(series.iloc[i + j])):
                        is_extreme = False
                        break  

                if is_extreme:  
                    for j in range(1, min(n+1, i+1)):
                        if (extreme == 'max' and float(series.iloc[i]) < float(series.iloc[i - j])) or \
                           (extreme == 'min' and float(series.iloc[i]) > float(series.iloc[i - j])):
                            is_extreme = False
                            break  

                if is_extreme:
                    extreme_idx.append(i)  

            return extreme_idx

        def find_extreme_value(series, extreme='max'):
            extreme_idx = []
            n = s
            for i in range(len(series)):
                is_extreme = True 

                for j in range(1, min(n+1, len(series) - i)):
                    if (extreme == 'max' and float(series.iloc[i]) < float(series.iloc[i + j])) or \
                       (extreme == 'min' and float(series.iloc[i]) > float(series.iloc[i + j])):
                        is_extreme = False
                        break 

                if is_extreme:  
                    for j in range(1, min(n+1, i+1)):
                        if (extreme == 'max' and float(series.iloc[i]) < float(series.iloc[i - j])) or \
                           (extreme == 'min' and float(series.iloc[i]) > float(series.iloc[i - j])):
                            is_extreme = False
                            break 

                if is_extreme:
                    extreme_idx.append(i)  

            return extreme_idx


        for a in range(20,21):
            p1=a/20
            for b in range(80,81):
                p2=b/100

                if not os.path.exists(f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test"):
                    os.mkdir(f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test")
                if not os.path.exists(f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}"):
                    os.mkdir(f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}")
                if not os.path.exists(f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}/Tethered_1D_{v1}_{v2}{p2}"):
                    os.mkdir(f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}/Tethered_1D_{v1}_{v2}{p2}")
                if not os.path.exists(f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}/Tethered_1D_{v1}_{v2}{p2}/Tethered_1D_{v1}{p1}_{v2}{p2}"):
                    os.mkdir(f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}/Tethered_1D_{v1}_{v2}{p2}/Tethered_1D_{v1}{p1}_{v2}{p2}")
                d=f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}/Tethered_1D_{v1}_{v2}{p2}"
                d0=f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Tethered_1D_{v1}_{v2}{p2}"
                if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency"):
                    os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency")
                if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Double"):
                    os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Double")
                if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number"):
                    os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number")
                if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak"):
                    os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak")
                if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Penetration"):
                    os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Penetration")


                if Frequency == True: 
                        
                    for i in range(0, 20):
                        path_output=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/wave_{a1}{p1}_{a2}{p2}_"+str(i)+".csv"
                        csvFile = open(path_output,'w',newline='',encoding='utf-8')
                        writer = csv.writer(csvFile)
                        csvRow = []
                        #,'r',encoding='gb2312'
                        path_input=d0+f"/wave_{v1}{p1}_{v2}{p2}_"+str(i)+".txt"
                        f = open(path_input)
                        header_list = ["slice_in_one_percent", "confined_drive_carrier_frequency_in_one_percent", "confined_drive_allele_frequency_in_one_percent", "suppression_drive_carrier_frequency_in_one_percent", "suppression_drive_allele_frequency_in_one_percent", "confined_drive_wt_frequency_in_one_percent", "confined_drive_wt_allele_frequency_in_one_percent", "suppression_drive_wt_frequency_in_one_percent", "suppression_drive_wt_allele_frequency_in_one_percent", "wt_frequency_in_one_percent", "num_in_one_percent", "num_in_all"]
                        writer.writerow(header_list)
                        for line in f:
                            csvRow = line.split()
                            writer.writerow(csvRow)
                         
                        f.close()
                        csvFile.close()

                        path_input=f"{d}/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/wave_{a1}{p1}_{a2}{p2}_"+str(i)+".csv"
                        path_output=f"{d}/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/wave_{a1}{p1}_{a2}{p2}_"+str(i)+"_n.csv" 
                        df = pd.read_csv(path_input)

                        divider = df.iloc[:, 10]

                        for col in [1, 3, 5, 7, 9]:
                            df.iloc[:, col] = df.iloc[:, col].div(divider, axis=0).fillna(0)

                        for col in [2, 4, 6, 8]:
                            df.iloc[:, col] = df.iloc[:, col].div(divider, axis=0).fillna(0)

                        df.to_csv(path_output, index=False)
                        if Smooth == True:
                            df = pd.read_csv(path_output)
                            original_output=f"{d}/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/wave_{a1}{p1}_{a2}{p2}_"+str(i)+"_n_o.csv"
                            smoothed_df = smooth_values_with_original_data(df)
                            Smooth_output=f"{d}/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/wave_{a1}{p1}_{a2}{p2}_"+str(i)+"_n_s.csv"
                            smoothed_df.to_csv(Smooth_output, index=False)


                    for j in range(0, 20):
                        if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_{j}"):
                            os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_{j}")
                        folder=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_{j}"
                        path=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/wave_{a1}{p1}_{a2}{p2}_{j}_n.csv"


                        df = pd.read_csv(path)
                        '''

                        plt.figure(figsize=(10, 6), dpi=200)

                        for i in range(0, len(df), 100):
                            sub_df = df.iloc[i:i+100]
                            


                            fig, ax = plt.subplots()
                            # allele==1
                            name=["confined_drive_allele_frequency_in_one_percent", "suppression_drive_allele_frequency_in_one_percent", "confined_drive_wt_allele_frequency_in_one_percent", "suppression_drive_wt_allele_frequency_in_one_percent"]
                            #for col in range(0, 20):  
                                #ax.plot(sub_df.iloc[:, 0], sub_df.iloc[:, 2*col+1], label=name[col], color=color_list[col])
                            #sub_df.plot(x="slice_in_one_percent", y=["confined_drive_carrier_frequency_in_one_percent", "confined_drive_allele_frequency_in_one_percent", "suppression_drive_carrier_frequency_in_one_percent", "suppression_drive_allele_frequency_in_one_percent", "confined_drive_wt_frequency_in_one_percent", "confined_drive_wt_allele_frequency_in_one_percent"], ax=ax)
                            sub_df.plot(x="slice_in_one_percent", y=["confined_drive_allele_frequency_in_one_percent", "suppression_drive_allele_frequency_in_one_percent", "confined_drive_wt_allele_frequency_in_one_percent", "suppression_drive_wt_allele_frequency_in_one_percent"], ax=ax, color = color_list)
                            #sub_df.plot(x="slice_in_one_percent", y="num_in_one_percent", ax=ax, secondary_y=True, kind="bar", color="gray", width=1, alpha=0.5)
                            sub_df.plot(x="slice_in_one_percent", y="num_in_one_percent", ax=ax, secondary_y=True, kind="area", color="gray", alpha=0.5)
                            #ax.plot(sub_df.iloc[:, 0], sub_df.iloc[:, 9], label="num_in_one_percent", color="gray")
                      

                            #ax.set_xticks(sub_df["slice_in_one_percent"].values[::len(sub_df) // 10])
                            #ax.set_xticks(sub_df["slice_in_one_percent"].values)
                            ax.set_xlim(1, 100)
                            ax.set_xticks([1 + 10 * i for i in range(10)])
                            ax.set_ylim(0, 1)
                            ax.set_yticks([0.2 * i for i in range(6)])

                            ax.right_ax.set_ylim(0, 140)
                            ax.right_ax.set_yticks([20 * i for i in range(8)])

                            ax.legend(loc='upper center', bbox_to_anchor=(1.5, 0.5), ncol=1)
                            ax.right_ax.legend(loc='upper center', bbox_to_anchor=(1.5, 0.1), ncol=1)
                            fig.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_{j}/output_{i/100}.png", dpi=200, bbox_inches="tight")
                            plt.close('all') 
                            '''


                    for j in range(0, 20):
                        if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_s_{j}"):
                            os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_s_{j}")
                        folder=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_s_{j}"
                        path=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/wave_{a1}{p1}_{a2}{p2}_{j}_n_s.csv"

                        '''

                        df = pd.read_csv(path)
                        plt.figure(figsize=(10, 6), dpi=200)

                        for i in range(0, len(df), 100):
                            sub_df = df.iloc[i:i+100]
                            fig, ax = plt.subplots()

                            #sub_df.plot(x="slice_in_one_percent", y=["confined_drive_carrier_frequency_in_one_percent", "confined_drive_allele_frequency_in_one_percent", "suppression_drive_carrier_frequency_in_one_percent", "suppression_drive_allele_frequency_in_one_percent", "confined_drive_wt_frequency_in_one_percent", "confined_drive_wt_allele_frequency_in_one_percent"], ax=ax)
                            sub_df.plot(x="slice_in_one_percent", y=["confined_drive_allele_frequency_in_one_percent", "suppression_drive_allele_frequency_in_one_percent", "confined_drive_wt_allele_frequency_in_one_percent", "suppression_drive_wt_allele_frequency_in_one_percent"], ax=ax, color = color_list)

                            #sub_df.plot(x="slice_in_one_percent", y="num_in_one_percent", ax=ax, secondary_y=True, kind="bar", color="gray", width=1, alpha=0.5)
                            sub_df.plot(x="slice_in_one_percent", y="num_in_one_percent", ax=ax, secondary_y=True, kind="area", color="gray", alpha=0.5)
                                                  

                            #ax.set_xticks(sub_df["slice_in_one_percent"].values[::len(sub_df) // 10])
                            #ax.set_xticks(sub_df["slice_in_one_percent"].values)

                            ax.set_xlim(1, 100)
                            ax.set_xticks([1 + 10 * i for i in range(10)])


                            ax.set_ylim(0, 1)
                            ax.set_yticks([0.2 * i for i in range(6)])

                            ax.right_ax.set_ylim(0, 140)
                            ax.right_ax.set_yticks([20 * i for i in range(8)])
                            """

                            ax.legend(loc='upper center', bbox_to_anchor=(1.5, 0.5), ncol=1)
                            ax.right_ax.legend(loc='upper center', bbox_to_anchor=(1.5, 0.1), ncol=1)
                            fig.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_s_{j}/output_s_{i/100}.png", dpi=200, bbox_inches="tight")
                            plt.close('all') 

                            #fig.savefig(f"Tethered_wavetest_{v1}_{v2}0.86/fig/output_{i/100}.png")
                            ##print(os.path.join("Tethered_wavetest_{v1}_{v2}0.86/fig","/output_{i/100}.png"))

                        '''

                    '''
                    for i in range(0, len(df), 100):
                        x = df.iloc[i:i+100, 0] 
                        y = df.iloc[i:i+100, 1:9] 
                        plt.plot(x, y)

                    plt.xlabel('x')
                    plt.ylabel('y')

                    plt.title('wave')
                    plt.show()
                    '''

                if Number == True:
                    import csv
                    import os
                    d=f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_{s}_m{mode}_a{allele}/Tethered_1D_{v1}_{v2}{p2}"
                    if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number"):
                        os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number")
                    for i in range(0, 20):
                        path_output=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/wave_{a1}{p1}_{a2}{p2}_"+str(i)+".csv"
                        csvFile = open(path_output,'w',newline='',encoding='utf-8')
                        writer = csv.writer(csvFile)
                        csvRow = []
                        #,'r',encoding='gb2312'
                        path_input=d0+f"/wave_{v1}{p1}_{v2}{p2}_"+str(i)+".txt"
                        f = open(path_input)
                        header_list = ["slice_in_one_percent", "confined_drive_carrier_frequency_in_one_percent", "confined_drive_allele_frequency_in_one_percent", "suppression_drive_carrier_frequency_in_one_percent", "suppression_drive_allele_frequency_in_one_percent", "confined_drive_wt_frequency_in_one_percent", "confined_drive_wt_allele_frequency_in_one_percent", "suppression_drive_wt_frequency_in_one_percent", "suppression_drive_wt_allele_frequency_in_one_percent", "wt_frequency_in_one_percent", "num_in_one_percent", "num_in_all"]
                        writer.writerow(header_list)
                        for line in f:
                            csvRow = line.split()
                            writer.writerow(csvRow)
                         
                        f.close()
                        csvFile.close()

                    #data normalize
                    import pandas as pd
                    for i in range(0, 20):
                        path_input=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/wave_{a1}{p1}_{a2}{p2}_"+str(i)+".csv"
                        path_output=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/wave_{a1}{p1}_{a2}{p2}_"+str(i)+"_n.csv"
                        df = pd.read_csv(path_input)
                        df.to_csv(path_output, index=False)
                        if Smooth == True:
                            df = pd.read_csv(path_input)
                            original_output=f"{d}/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/wave_{a1}{p1}_{a2}{p2}_"+str(i)+"_n_o.csv"
                            smoothed_df = smooth_values_with_original_data(df)
                            Smooth_output=f"{d}/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/wave_{a1}{p1}_{a2}{p2}_"+str(i)+"_n_s.csv"
                            smoothed_df.to_csv(Smooth_output, index=False)

                    for j in range(0, 20):
                        plt.figure(figsize=(10, 6), dpi=200)
                        peak_output=d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak.csv'
                        peak_average=d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_a.csv'
                        peak_average_penetration=d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_a_p.csv'
                        if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_{j}"):
                            os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_{j}")
                        folder=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_{j}"
                        path=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/wave_{a1}{p1}_{a2}{p2}_{j}_n.csv"
                        path1=d0+f"/wave_{v1}{p1}_{v2}{p2}_{j}.txt"
                        df = pd.read_csv(path, header=None,index_col=False)
                        df3 = pd.read_csv(path)
                        df2 = df.iloc[1:]
                        df1 = pd.read_csv(path1, sep=' ', header=None, index_col=False)




                        store=[]
                        for i in range(0, len(df2), 100):
                            group = df2[i:i+100]
                            col2_max_idx = find_extreme_value(group[2], 'max')
                            col2_max_val = group.iloc[col2_max_idx, 2]
                            col2 = [(index%100, float(value)) for index, value in col2_max_val.items()]
                            col2_sorted = sorted(col2, key=lambda x: x[0])
                            old_merged_col2 = merge_non_zero_points(col2_sorted)                

                            col4_max_idx = find_extreme_value(group[4], 'max') 
                            col4_max_val = group.iloc[col4_max_idx, 4]
                            col4 = [(index%100, float(value)) for index, value in col4_max_val.items()]
                            col4_sorted = sorted(col4, key=lambda x: x[0])
                            merged_col4 = merge_non_zero_points(col4_sorted)     

                            col6_max_idx = find_extreme_value(group[6], 'max')
                            col6_max_val = group.iloc[col6_max_idx, 6]
                            ##print(col6_max_val)
                            col6 = [(index%100, float(value)) for index, value in col6_max_val.items()]
                            col6_sorted = sorted(col6, key=lambda x: x[0])
                            merged_col6 = merge_non_zero_points_wt(col6_sorted)     

                            col8_max_idx = find_extreme_value(group[8], 'max')
                            col8_max_val = group.iloc[col8_max_idx, 8]
                            ##print(col6_max_val)
                            col8 = [(index%100, float(value)) for index, value in col8_max_val.items()]
                            col8_sorted = sorted(col8, key=lambda x: x[0])
                            merged_col8 = merge_non_zero_points_wt(col8_sorted)     

                            col11_min_idx = find_extreme_value(group[10], 'min')
                            col11_min_val = group.iloc[col11_min_idx, 10]
                            col11_min_val = pd.to_numeric(col11_min_val, errors='coerce')
                            ##print(col11_min_val)
                            col11_min_val = col11_min_val[col11_min_val < 20]
                            col11 = [(index%100, float(value)) for index, value in col11_min_val.items()]
                            col11_sorted = sorted(col11, key=lambda x: x[0])
                            merged_col11 = merge_continuous_zero_y(col11_sorted)      

                            merged_col2 = find_extreme_value_with_merging(old_merged_col2, merged_col6, max_distance=50)

                            data=[merged_col2,merged_col4,merged_col6,merged_col8,merged_col11]
                            #print(data)
                            values = [','.join(str(item[0]) for item in lst) for lst in data]
                            store.append(values)

                        df4 = pd.DataFrame(store,columns=['TARE', 'Homing', 'TWT', 'HWT', 'Empty'])
                        df4.to_csv(peak_output, index=False)

                        df5 = pd.read_csv(peak_output, dtype=str)                            
                            #df2 = df2.append(pd.Series(values, index=df.columns), ignore_index=True)

                            #print(f'Col 2 max values: {col2_max_val.tolist()}')
                            #print(f'Col 4 max values: {col4_max_val.tolist()}')
                            #print(f'Col 6 max values: {col6_max_val.tolist()}')
                            #print(f'Col 8 max values: {col8_max_val.tolist()}')
                            #print(f'Col 11 min values: {col11_min_val.tolist()}')

                        '''
                            sub_df = df3.iloc[i:i+100]
                            
                            fig, ax = plt.subplots()

                            #sub_df.plot(x="slice_in_one_percent", y=["confined_drive_carrier_frequency_in_one_percent", "confined_drive_allele_frequency_in_one_percent", "suppression_drive_carrier_frequency_in_one_percent", "suppression_drive_allele_frequency_in_one_percent", "confined_drive_wt_frequency_in_one_percent", "confined_drive_wt_allele_frequency_in_one_percent"], ax=ax)
                            sub_df.plot(x="slice_in_one_percent", y=["confined_drive_allele_frequency_in_one_percent", "suppression_drive_allele_frequency_in_one_percent", "confined_drive_wt_allele_frequency_in_one_percent", "suppression_drive_wt_allele_frequency_in_one_percent"], ax=ax, color = color_list)

                            #sub_df.plot(x="slice_in_one_percent", y="num_in_one_percent", ax=ax, secondary_y=True, kind="bar", color="gray", width=1, alpha=0.5)
                            sub_df.plot(x="slice_in_one_percent", y="num_in_one_percent", ax=ax, secondary_y=True, kind="area", color="gray", alpha=0.5)


                            #ax.set_xticks(sub_df["slice_in_one_percent"].values[::len(sub_df) // 10])
                            #ax.set_xticks(sub_df["slice_in_one_percent"].values)

                            ax.set_xlim(1, 100)
                            ax.set_xticks([1 + 10 * i for i in range(10)])

                            ax.set_ylim(0, 140)
                            ax.set_yticks([20 * i for i in range(8)])

                            ax.right_ax.set_ylim(0, 140)
                            ax.right_ax.set_yticks([20 * i for i in range(8)])

                            if not merged_col2:
                                print("No TARE peak")
                            else:
                                for x_2, y_2 in merged_col2:
                                    y_2 = float(y_2)
                                    plt.scatter(x_2, y_2, color='#17AD65', label='', marker='s')

                            #plt.show()

                            if not merged_col4:
                                print("No Homing peak")
                            else:
                                for x_4, y_4 in merged_col4:
                                    y_4 = float(y_4)
                                    plt.scatter(x_4, y_4, color='#EE5F00', label='', marker='s')

                            #plt.show()
                            if not merged_col6:
                                print("No TWT peak")
                            else:
                                for x_6, y_6 in merged_col6:
                                    y_6 = float(y_6)
                                    plt.scatter(x_6, y_6, color='#286BEE', label='', marker='s')    

                            #plt.show()
                            if not merged_col8:
                                print("No HWT peak")
                            else:
                                for x_8, y_8 in merged_col8:
                                    y_8 = float(y_8)
                                    plt.scatter(x_8, y_8, color='#9B72AA', label='', marker='s')    

                            #plt.show()
                            if not merged_col11:
                                print("No empty peak")
                            else:
                                for x_11, y_11 in merged_col11:
                                    y_11 = float(y_11)
                                    plt.scatter(x_11, y_11, color='#606060', label='', marker='s')  

                            #plt.show()


                            ax.legend(loc='upper center', bbox_to_anchor=(1.5, 0.5), ncol=1)
                            ax.right_ax.legend(loc='upper center', bbox_to_anchor=(1.5, 0.1), ncol=1)
                            ax.right_ax.set_ylim(0, 140)
                            ax.right_ax.set_yticks([20 * i for i in range(8)])
                            #fig.savefig(f"Tethered_wavetest_{v1}_{v2}0.86/fig/output_{i/100}.png")
                            ##print(os.path.join("Tethered_wavetest_{v1}_{v2}0.86/fig","/output_{i/100}.png"))
                            plt.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_{j}/output_{i/100}.png", dpi=200, bbox_inches="tight") 
                            plt.close("all") 
                        '''

                        '''
                        plt.figure(figsize=(10, 6))
                        ax = plt.gca()

                        for index, row in df5.iterrows():
                            ax.set_xticks(range(0, len(df5),5), minor=True)
                            plt.grid(which='minor', axis='x', zorder=2)
                            plt.grid(axis='x', zorder=2)
                            if pd.notna(row[0]):
                                y_values_0 = [float(val_0) for val_0 in row[0].split(',')]
                                plt.scatter([index] * len(y_values_0), y_values_0, color='#17AD65', label='TARE', zorder=3)
                                #if len(y_values_0) > 1:
                                    #plt.plot([index] * len(y_values_0), y_values_0, color='#17AD65', label='TARE')

                            if pd.notna(row[1]):
                                y_values_1 = [float(val_1) for val_1 in row[1].split(',')]
                                plt.scatter([index] * len(y_values_1), y_values_1, color='#EE5F00', label='Homing', zorder=3)
                                #if len(y_values_1) > 1:
                                    #plt.plot([index] * len(y_values_1), y_values_1, color='#EE5F00', label='Homing')

                            if pd.notna(row[2]):
                                y_values_2 = [float(val_2) for val_2 in row[2].split(',')]
                                plt.scatter([index] * len(y_values_2), y_values_2, color='#286BEE', label='TWT', zorder=3)
                                #if len(y_values_2) > 1:
                                    #plt.plot([index] * len(y_values_2), y_values_2, color='#286BEE', label='TWT')

                            if pd.notna(row[3]):
                                y_values_3 = [float(val_3) for val_3 in row[3].split(',')]
                                plt.scatter([index] * len(y_values_3), y_values_3, color='#9B72AA', label='HWT', zorder=3)
                                #if len(y_values_3) > 1:
                                    #plt.plot([index] * len(y_values_3), y_values_3, color='#9B72AA', label='HWT')

                            if pd.notna(row[4]):
                                y_values_4 = [float(val_4) for val_4 in row[4].split(',')]
                                plt.scatter([index] * len(y_values_4), y_values_4, color='gray', label='Empty', zorder=3)
                                #if len(y_values_4) > 1:
                                    #plt.plot([index] * len(y_values_4), y_values_4, color='gray', label='Empty')


                        handles, labels = ax.get_legend_handles_labels()
                        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]

                        ax.legend(*zip(*unique))

                        plt.title('')
                        plt.xlabel('Generation')
                        plt.ylabel('Peak')
                        #plt.grid(axis='x')


                        plt.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_{s}.png", dpi=300, bbox_inches="tight") 
                        #plt.show()
                        plt.close("all")

                        '''

                        df6 = pd.read_csv(peak_output)

                        for column in df6.columns:
                            df6[column] = df6[column].apply(lambda x: calculate_average(x) if isinstance(x, str) else x)

                        df6.to_csv(peak_average, index=False)

                        new_df = pd.read_csv(peak_average)
                        selected_rows = []
                        for i in range(len(new_df) - 1):
                            if check_conditions(new_df.iloc[i], new_df.iloc[i + 1]):
                                selected_rows.append(new_df.iloc[i])

                        selected_df = pd.DataFrame(selected_rows)
                        selected_df.to_csv(peak_average_penetration, index=False)


                        '''
                        plt.scatter(new_df.index, new_df[new_df.columns[0]], color='#17AD65') 
                        plt.plot(new_df.index, new_df[new_df.columns[0]], linestyle='-', linewidth=1, color='#17AD65') 
                        plt.scatter(new_df.index, new_df[new_df.columns[1]], color='#EE5F00') 
                        plt.plot(new_df.index, new_df[new_df.columns[1]], linestyle='-', linewidth=1, color='#EE5F00') 
                        plt.scatter(new_df.index, new_df[new_df.columns[2]], color='#286BEE')  
                        plt.plot(new_df.index, new_df[new_df.columns[2]], linestyle='-', linewidth=1, color='#286BEE')
                        plt.scatter(new_df.index, new_df[new_df.columns[3]], color='#9B72AA')  
                        plt.plot(new_df.index, new_df[new_df.columns[3]], linestyle='-', linewidth=1, color='#9B72AA')
                        plt.scatter(new_df.index, new_df[new_df.columns[4]], color='#606060')  
                        plt.plot(new_df.index, new_df[new_df.columns[4]], linestyle='-', linewidth=1, color='#606060')
                        y_min = plt.ylim()[0] - (plt.ylim()[1] - plt.ylim()[0]) * 0.05

                        for index in selected_df.index:
                            plt.axvline(x=index, color='red', linestyle='--')
                            plt.text(index, y_min, str(index), color='red', verticalalignment='bottom', horizontalalignment='center')

                        plt.xlabel('Index')
                        plt.ylabel(new_df.columns[0])
                        plt.title('Scatter Plot of Data')
                        plt.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_{s}_a.png", dpi=300, bbox_inches="tight") 
                        #plt.show()
                        plt.close("all")
                        '''

                    for j in range(0, 20):
                        plt.figure(figsize=(10, 6), dpi=300)
                        peak_output=d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_s.csv'
                        peak_average=d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_a_s.csv'
                        peak_average_penetration=d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_a_p_s.csv'
                        if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_s_{j}"):
                            os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_s_{j}")
                        folder=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_s_{j}"
                        path=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/wave_{a1}{p1}_{a2}{p2}_{j}_n_s.csv"
                        path1=d0+f"/wave_{v1}{p1}_{v2}{p2}_{j}.txt"
                        df = pd.read_csv(path, header=None,index_col=False)
                        df3 = pd.read_csv(path)
                        df2 = df.iloc[1:]
                        df1 = pd.read_csv(path1, sep=' ', header=None, index_col=False)
                        store=[]
                        print(len(df2))
                        for i in range(0, len(df2), 100):
                            group = df2[i:i+100]
                            col2_max_idx = find_extreme_value(group[2], 'max')
                            col2_max_val = group.iloc[col2_max_idx, 2]
                            col2 = [(index%100, float(value)) for index, value in col2_max_val.items()]
                            col2_sorted = sorted(col2, key=lambda x: x[0])
                            old_merged_col2 = merge_non_zero_points(col2_sorted)                
                            col4_max_idx = find_extreme_value(group[4], 'max') 
                            col4_max_val = group.iloc[col4_max_idx, 4]
                            col4 = [(index%100, float(value)) for index, value in col4_max_val.items()]
                            col4_sorted = sorted(col4, key=lambda x: x[0])
                            old_merged_col4 = merge_non_zero_points(col4_sorted)  

                            col6_max_idx = find_extreme_value(group[6], 'max')
                            col6_max_val = group.iloc[col6_max_idx, 6]
                            col6 = [(index%100, float(value)) for index, value in col6_max_val.items()]
                            col6_sorted = sorted(col6, key=lambda x: x[0])
                            merged_col6 = merge_non_zero_points_wt(col6_sorted)  

                            col8_max_idx = find_extreme_value(group[8], 'max')
                            col8_max_val = group.iloc[col8_max_idx, 8]
                            col8 = [(index%100, float(value)) for index, value in col8_max_val.items()]
                            col8_sorted = sorted(col8, key=lambda x: x[0])
                            merged_col8 = merge_non_zero_points_wt(col8_sorted)     

                            col11_min_idx = find_extreme_value(group[10], 'min')
                            col11_min_val = group.iloc[col11_min_idx, 10]
                            col11_min_val = pd.to_numeric(col11_min_val, errors='coerce')
                            col11_min_val = col11_min_val[col11_min_val < 20]
                            col11 = [(index%100, float(value)) for index, value in col11_min_val.items()]
                            col11_sorted = sorted(col11, key=lambda x: x[0])
                            merged_col11 = merge_continuous_zero_y(col11_sorted)


                            merged_col2 = find_extreme_value_with_merging(old_merged_col2, merged_col6, max_distance=50)
                            merged_col4 = find_extreme_value_with_merging(old_merged_col4, merged_col8, max_distance=50)
                            
                            data=[merged_col2,merged_col4,merged_col6,merged_col8,merged_col11]

                            values = [','.join(str(item[0]) for item in lst) for lst in data]
                            store.append(values)
                            
                            #df2 = df2.append(pd.Series(values, index=df.columns), ignore_index=True)

                            #print(f'Col 2 max values: {col2_max_val.tolist()}')
                            #print(f'Col 4 max values: {col4_max_val.tolist()}')
                            #print(f'Col 6 max values: {col6_max_val.tolist()}')
                            #print(f'Col 8 max values: {col8_max_val.tolist()}')
                            #print(f'Col 11 min values: {col11_min_val.tolist()}')

                            '''
                            sub_df = df3.iloc[i:i+100]
                            fig, ax = plt.subplots()

                            #sub_df.plot(x="slice_in_one_percent", y=["confined_drive_carrier_frequency_in_one_percent", "confined_drive_allele_frequency_in_one_percent", "suppression_drive_carrier_frequency_in_one_percent", "suppression_drive_allele_frequency_in_one_percent", "confined_drive_wt_frequency_in_one_percent", "confined_drive_wt_allele_frequency_in_one_percent"], ax=ax)
                            sub_df.plot(x="slice_in_one_percent", y=["confined_drive_allele_frequency_in_one_percent", "suppression_drive_allele_frequency_in_one_percent", "confined_drive_wt_allele_frequency_in_one_percent", "suppression_drive_wt_allele_frequency_in_one_percent"], ax=ax, color = color_list)

                            #sub_df.plot(x="slice_in_one_percent", y="num_in_one_percent", ax=ax, secondary_y=True, kind="bar", color="gray", width=1, alpha=0.5)
                            sub_df.plot(x="slice_in_one_percent", y="num_in_one_percent", ax=ax, secondary_y=True, kind="area", color="gray", alpha=0.5)
                            
                            #ax.set_xticks(sub_df["slice_in_one_percent"].values[::len(sub_df) // 10])
                            #ax.set_xticks(sub_df["slice_in_one_percent"].values)

                            ax.set_xlim(1, 100)
                            ax.set_xticks([1 + 10 * i for i in range(10)])

                            ax.set_ylim(0, 140)
                            ax.set_yticks([20 * i for i in range(8)])

                            ax.right_ax.set_ylim(0, 140)
                            ax.right_ax.set_yticks([20 * i for i in range(8)])

                            if not merged_col2:
                                print("No TARE peak")
                            else:
                                for x_2, y_2 in merged_col2:
                                    y_2 = float(y_2)
                                    plt.scatter(x_2, y_2, color='#17AD65', label='', marker='s')

                            if not merged_col4:
                                print("No Homing peak")
                            else:
                                for x_4, y_4 in merged_col4:
                                    y_4 = float(y_4)
                                    plt.scatter(x_4, y_4, color='#EE5F00', label='', marker='s')

                            if not merged_col6:
                                print("No TWT peak")
                            else:
                                for x_6, y_6 in merged_col6:
                                    y_6 = float(y_6)
                                    plt.scatter(x_6, y_6, color='#286BEE', label='', marker='s')    

                            if not merged_col8:
                                print("No HWT peak")
                            else:
                                for x_8, y_8 in merged_col8:
                                    y_8 = float(y_8)
                                    plt.scatter(x_8, y_8, color='#9B72AA', label='', marker='s')    

                            if not merged_col11:
                                print("No empty peak")
                            else:
                                for x_11, y_11 in merged_col11:
                                    y_11 = float(y_11)
                                    plt.scatter(x_11, y_11, color='#606060', label='', marker='s')  

                            ax.legend(loc='upper center', bbox_to_anchor=(1.5, 0.5), ncol=1)
                            ax.right_ax.legend(loc='upper center', bbox_to_anchor=(1.5, 0.1), ncol=1)

                            ax.right_ax.set_ylim(0, 140)
                            ax.right_ax.set_yticks([20 * i for i in range(8)])
                            plt.ylim(0, 140) 
                            plt.yticks([20 * i for i in range(8)])  


                            #fig.savefig(f"Tethered_wavetest_{v1}_{v2}0.86/fig/output_{i/100}.png")
                            #print(os.path.join("Tethered_wavetest_{v1}_{v2}0.86/fig","/output_{i/100}.png"))
                            plt.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_s_{j}/output_s_{i/100}.png", dpi=200, bbox_inches="tight") 
                            plt.close("all") 
                            '''

                        df4 = pd.DataFrame(store,columns=['TARE', 'Homing', 'TWT', 'HWT', 'Empty'])
                        df4.to_csv(peak_output, index=False)

                        df5 = pd.read_csv(peak_output, dtype=str)

                        penetration_output = d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_penetration.csv'
                        penetration_TARE = d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_p_T.csv'  # 输出文件名
                        process_csv(peak_output, penetration_output)
                        process_csv_H(penetration_output, penetration_output)

                        penetration_nonoverlapping = d+f'/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_p_non.csv'

                        df10 = pd.read_csv(peak_output)

                        df10[['left', 'left_values', 'right', 'right_values']] = df10.apply(process_row, axis=1, result_type='expand', args=("TARE", "TWT", "Empty"))
                        df10[['left_H', 'left_values_H', 'right_H', 'right_values_H']] = df10.apply(process_row, axis=1, result_type='expand', args=("Homing", "HWT", "Empty"))

                        df10['continuous_left'] = mark_continuous_true(df10['left'])
                        df10['continuous_right'] = mark_continuous_true(df10['right'])
                        df10['continuous_left_H'] = mark_continuous_true(df10['left_H'])
                        df10['continuous_right_H'] = mark_continuous_true(df10['right_H'])

                        df10.to_csv(penetration_nonoverlapping, index=False)


                        #old-decide-way   pattern transition
                        '''
                        plt.figure(figsize=(10, 6))
                        ax = plt.gca()
                        for index, row in df5.iterrows():
                            ax.set_xticks(range(0, len(df5),5), minor=True)
                            plt.grid(which='minor', axis='x', zorder=2)
                            plt.grid(axis='x', zorder=2)
                            if pd.notna(row[0]):
                                y_values_0 = [float(val_0) for val_0 in row[0].split(',')]
                                plt.scatter([index] * len(y_values_0), y_values_0, color='#17AD65', label='TARE', zorder=3)
                                #if len(y_values_0) > 1:
                                    #plt.plot([index] * len(y_values_0), y_values_0, color='#17AD65', label='TARE')

                            if pd.notna(row[1]):
                                y_values_1 = [float(val_1) for val_1 in row[1].split(',')]
                                plt.scatter([index] * len(y_values_1), y_values_1, color='#EE5F00', label='Homing', zorder=3)
                                #if len(y_values_1) > 1:
                                    #plt.plot([index] * len(y_values_1), y_values_1, color='#EE5F00', label='Homing')

                            if pd.notna(row[2]):
                                y_values_2 = [float(val_2) for val_2 in row[2].split(',')]
                                plt.scatter([index] * len(y_values_2), y_values_2, color='#286BEE', label='TWT', zorder=3)
                                #if len(y_values_2) > 1:
                                    #plt.plot([index] * len(y_values_2), y_values_2, color='#286BEE', label='TWT')

                            if pd.notna(row[3]):
                                y_values_3 = [float(val_3) for val_3 in row[3].split(',')]
                                plt.scatter([index] * len(y_values_3), y_values_3, color='#9B72AA', label='HWT', zorder=3)
                                #if len(y_values_3) > 1:
                                    #plt.plot([index] * len(y_values_3), y_values_3, color='#9B72AA', label='HWT')

                            if pd.notna(row[4]):
                                y_values_4 = [float(val_4) for val_4 in row[4].split(',')]
                                plt.scatter([index] * len(y_values_4), y_values_4, color='gray', label='Empty', zorder=3)
                                #if len(y_values_4) > 1:
                                    #plt.plot([index] * len(y_values_4), y_values_4, color='gray', label='Empty')


                        handles, labels = ax.get_legend_handles_labels()
                        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]

                        ax.legend(*zip(*unique))
                        df7 = pd.read_csv(penetration_output)

                        for index, row in df7.iterrows():
                            #if row['Result'] == 'TRUE':
                                #plt.axvline(x=index, color='r', linestyle='--')
                            if pd.notna(row['Values']):
                                values = ast.literal_eval(row['Values'])
                                for val in values:
                                    plt.scatter(index, val, marker='*', color='black', s=30, zorder=4)
                                    plt.axvline(x=index, color='r', linestyle='--', zorder=2)
                            if pd.notna(row['Values_after']):
                                values = ast.literal_eval(row['Values_after'])
                                for val in values:
                                    plt.scatter(index, val, marker='s', color='white', s=10, zorder=5)
                                    plt.axvline(x=index, color='g', linestyle=':', zorder=2)
                        sequences = find_sequences(df7,5,7)


                        df7['successful-penetration'] = False
                        for start, end in sequences:
                            df7.loc[start:end-1, 'successful-penetration'] = True

                        y_100 = 100

                        for start, end in sequences:
                            plt.plot([start-0.5, end - 0.5, end - 0.5, start-0.5, start-0.5],
                                     [0, 0, y_100, y_100, 0],
                                     color='green', linestyle='--', linewidth=3)

                        df7.to_csv(penetration_TARE, index=False)
                        plt.title('')
                        plt.xlabel('Generation')
                        plt.ylabel('Peak')
                        #plt.grid(axis='x')

                        plt.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_s_{s}_T.png", dpi=300, bbox_inches="tight") 
                        plt.close("all")

                        plt.figure(figsize=(10, 6))
                        ax = plt.gca()

                        for index, row in df5.iterrows():
                            ax.set_xticks(range(0, len(df5),5), minor=True)

                            plt.grid(which='minor', axis='x', zorder=2)
                            plt.grid(axis='x', zorder=2)
                            if pd.notna(row[0]):
                                y_values_0 = [float(val_0) for val_0 in row[0].split(',')]
                                plt.scatter([index] * len(y_values_0), y_values_0, color='#17AD65', label='TARE', zorder=3)
                                #if len(y_values_0) > 1:
                                    #plt.plot([index] * len(y_values_0), y_values_0, color='#17AD65', label='TARE')

                            if pd.notna(row[1]):
                                y_values_1 = [float(val_1) for val_1 in row[1].split(',')]
                                plt.scatter([index] * len(y_values_1), y_values_1, color='#EE5F00', label='Homing', zorder=3)
                                #if len(y_values_1) > 1:
                                    #plt.plot([index] * len(y_values_1), y_values_1, color='#EE5F00', label='Homing')

                            if pd.notna(row[2]):
                                y_values_2 = [float(val_2) for val_2 in row[2].split(',')]
                                plt.scatter([index] * len(y_values_2), y_values_2, color='#286BEE', label='TWT', zorder=3)
                                #if len(y_values_2) > 1:
                                    #plt.plot([index] * len(y_values_2), y_values_2, color='#286BEE', label='TWT')

                            if pd.notna(row[3]):
                                y_values_3 = [float(val_3) for val_3 in row[3].split(',')]
                                plt.scatter([index] * len(y_values_3), y_values_3, color='#9B72AA', label='HWT', zorder=3)
                                #if len(y_values_3) > 1:
                                    #plt.plot([index] * len(y_values_3), y_values_3, color='#9B72AA', label='HWT')

                            if pd.notna(row[4]):
                                y_values_4 = [float(val_4) for val_4 in row[4].split(',')]
                                plt.scatter([index] * len(y_values_4), y_values_4, color='gray', label='Empty', zorder=3)
                                #if len(y_values_4) > 1:
                                    #plt.plot([index] * len(y_values_4), y_values_4, color='gray', label='Empty')

                        handles, labels = ax.get_legend_handles_labels()
                        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]

                        ax.legend(*zip(*unique))
                        df7 = pd.read_csv(penetration_output) 

                        for index, row in df7.iterrows():
                            #if row['Result'] == 'TRUE':
                                #plt.axvline(x=index, color='r', linestyle='--')
                            if pd.notna(row['Values_H']):
                                values = ast.literal_eval(row['Values_H'])
                                for val in values:
                                    plt.scatter(index, val, marker='*', color='black', s=30, zorder=4)
                                    plt.axvline(x=index, color='r', linestyle='--', zorder=2)
                            if pd.notna(row['Values_after_H']):
                                values = ast.literal_eval(row['Values_after_H'])
                                for val in values:
                                    plt.scatter(index, val, marker='s', color='white', s=10, zorder=5)
                                    plt.axvline(x=index, color='g', linestyle=':', zorder=2)
                        sequences_H = find_sequences(df7,9,11)


                        df7['successful-penetration_H'] = False
                        for start, end in sequences_H:
                            df7.loc[start:end-1, 'successful-penetration_H'] = True
                        y_100 = 100

                        for start, end in sequences_H:
                            plt.plot([start-0.5, end - 0.5, end - 0.5, start-0.5, start-0.5],
                                     [0, 0, y_100, y_100, 0],
                                     color='orange', linestyle='--', linewidth=3)

                        df7.to_csv(penetration_TARE, index=False)

                        plt.title('')
                        plt.xlabel('Generation')
                        plt.ylabel('Peak')
                        #plt.grid(axis='x')

                        plt.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_s_{s}_H.png", dpi=300, bbox_inches="tight") 
                        plt.close("all")
                        img_path1 = d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_s_{s}_T.png"
                        img_path2 = d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_s_{s}_H.png"
                        output_path = d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_s_{s}.png"
                        combine_images_vertically(img_path1, img_path2, output_path)
                        '''

                        df6 = pd.read_csv(peak_output)

                        for column in df6.columns:
                            df6[column] = df6[column].apply(lambda x: calculate_average(x) if isinstance(x, str) else x)

                        df6.to_csv(peak_average, index=False)

                        new_df = pd.read_csv(peak_average)
                        selected_rows = []
                        for i in range(len(new_df) - 1):
                            if check_conditions(new_df.iloc[i], new_df.iloc[i + 1]):
                                selected_rows.append(new_df.iloc[i])

                        selected_df = pd.DataFrame(selected_rows)
                        selected_df.to_csv(peak_average_penetration, index=False)


                        '''
                        plt.scatter(new_df.index, new_df[new_df.columns[0]], color='#17AD65') 
                        plt.plot(new_df.index, new_df[new_df.columns[0]], linestyle='-', linewidth=1, color='#17AD65') 
                        plt.scatter(new_df.index, new_df[new_df.columns[1]], color='#EE5F00') 
                        plt.plot(new_df.index, new_df[new_df.columns[1]], linestyle='-', linewidth=1, color='#EE5F00') 
                        plt.scatter(new_df.index, new_df[new_df.columns[2]], color='#286BEE')  
                        plt.plot(new_df.index, new_df[new_df.columns[2]], linestyle='-', linewidth=1, color='#286BEE')
                        plt.scatter(new_df.index, new_df[new_df.columns[3]], color='#9B72AA')  
                        plt.plot(new_df.index, new_df[new_df.columns[3]], linestyle='-', linewidth=1, color='#9B72AA')
                        plt.scatter(new_df.index, new_df[new_df.columns[4]], color='#606060')  
                        plt.plot(new_df.index, new_df[new_df.columns[4]], linestyle='-', linewidth=1, color='#606060')
                        y_min = plt.ylim()[0] - (plt.ylim()[1] - plt.ylim()[0]) * 0.05
                        for index in selected_df.index:
                            plt.axvline(x=index, color='red', linestyle='--')
                            plt.text(index, y_min, str(index), color='red', verticalalignment='bottom', horizontalalignment='center')
                        plt.xlabel('Index')
                        plt.ylabel(new_df.columns[0])
                        plt.title('Scatter Plot of Data'


                        plt.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_peak_{s}_a_s.png", dpi=300, bbox_inches="tight") 
                        #plt.show()
                        plt.close("all")
                        '''


                        plt.figure(figsize=(10, 6))
                        ax = plt.gca()

                        for index, row in df5.iterrows():
                            ax.set_xticks(range(0, len(df5),5), minor=True)
                            plt.grid(which='minor', axis='x', zorder=2)
                            plt.grid(axis='x', zorder=2)
                            if pd.notna(row[0]):
                                y_values_0 = [float(val_0) for val_0 in row[0].split(',')]
                                plt.scatter([index] * len(y_values_0), y_values_0, color='#17AD65', label='TARE', zorder=3)
                                #if len(y_values_0) > 1:
                                    #plt.plot([index] * len(y_values_0), y_values_0, color='#17AD65', label='TARE')

                            if pd.notna(row[1]):
                                y_values_1 = [float(val_1) for val_1 in row[1].split(',')]
                                plt.scatter([index] * len(y_values_1), y_values_1, color='#EE5F00', label='Homing', zorder=3)
                                #if len(y_values_1) > 1:
                                    #plt.plot([index] * len(y_values_1), y_values_1, color='#EE5F00', label='Homing')

                            if pd.notna(row[2]):
                                y_values_2 = [float(val_2) for val_2 in row[2].split(',')]
                                plt.scatter([index] * len(y_values_2), y_values_2, color='#286BEE', label='TWT', zorder=3)
                                #if len(y_values_2) > 1:
                                    #plt.plot([index] * len(y_values_2), y_values_2, color='#286BEE', label='TWT')

                            if pd.notna(row[3]):
                                y_values_3 = [float(val_3) for val_3 in row[3].split(',')]
                                plt.scatter([index] * len(y_values_3), y_values_3, color='#9B72AA', label='HWT', zorder=3)
                                #if len(y_values_3) > 1:
                                    #plt.plot([index] * len(y_values_3), y_values_3, color='#9B72AA', label='HWT')

                            if pd.notna(row[4]):
                                y_values_4 = [float(val_4) for val_4 in row[4].split(',')]
                                plt.scatter([index] * len(y_values_4), y_values_4, color='gray', label='Empty', zorder=3)
                                #if len(y_values_4) > 1:
                                    #plt.plot([index] * len(y_values_4), y_values_4, color='gray', label='Empty')

                        handles, labels = ax.get_legend_handles_labels()
                        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]

                        ax.legend(*zip(*unique))

                        df9 = pd.read_csv(penetration_nonoverlapping)

                        for col in ['continuous_left', 'continuous_right']:
                            continuous_groups = df9[col].astype(int).groupby(df9[col].ne(df9[col].shift()).cumsum())
                            group_counts = continuous_groups.transform('sum') * df9[col]

                            for _, group in continuous_groups:
                                if group.iloc[0] != 0:
                                    start = group.index[0]
                                    end = group.index[-1]
                                    color = 'red' if col == 'continuous_left' else 'green'
                                    plt.axvspan(start, end, color=color, alpha=0.2, linestyle='--', zorder=1)

                        for i, row in df9.iterrows():
                            if row['left']:
                                plt.axvline(x=i, color='red', linestyle='--', alpha=0.7, zorder=2)
                            if row['right']:
                                plt.axvline(x=i, color='green', linestyle=':', alpha=0.7, zorder=2)

                            if row['left_values'] != '[]':
                                left_values = ast.literal_eval(row['left_values'])
                                for k, group in enumerate(left_values, start=1):
                                    for value in group:
                                        if isinstance(value, list):
                                            for val in value:
                                                plt.text(i, val, str(k), color='black', fontsize=6, ha='center', va='center', zorder=5)
                                        else:
                                            plt.text(i, value, str(k), color='black', fontsize=6, ha='center', va='center', zorder=5)

                            if row['right_values'] != '[]':
                                right_values = ast.literal_eval(row['right_values'])
                                for k, group in enumerate(right_values, start=1):
                                    for value in group:
                                        if isinstance(value, list):
                                            for val in value:
                                                plt.text(i, val, str(k), color='black', fontsize=6, ha='center', va='center', zorder=5)
                                        else:
                                            plt.text(i, value, str(k), color='black', fontsize=6, ha='center', va='center', zorder=5)

                        plt.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_s_{s}_P_T.png", dpi=300, bbox_inches="tight") 
                        plt.close("all")

                        plt.figure(figsize=(10, 6))
                        ax = plt.gca()

                        for index, row in df5.iterrows():
                            ax.set_xticks(range(0, len(df5),5), minor=True)
                            plt.grid(which='minor', axis='x', zorder=2)
                            plt.grid(axis='x', zorder=2)
                            if pd.notna(row[0]):
                                y_values_0 = [float(val_0) for val_0 in row[0].split(',')]
                                plt.scatter([index] * len(y_values_0), y_values_0, color='#17AD65', label='TARE', zorder=3)
                                #if len(y_values_0) > 1:
                                    #plt.plot([index] * len(y_values_0), y_values_0, color='#17AD65', label='TARE')

                            if pd.notna(row[1]):
                                y_values_1 = [float(val_1) for val_1 in row[1].split(',')]
                                plt.scatter([index] * len(y_values_1), y_values_1, color='#EE5F00', label='Homing', zorder=3)
                                #if len(y_values_1) > 1:
                                    #plt.plot([index] * len(y_values_1), y_values_1, color='#EE5F00', label='Homing')

                            if pd.notna(row[2]):
                                y_values_2 = [float(val_2) for val_2 in row[2].split(',')]
                                plt.scatter([index] * len(y_values_2), y_values_2, color='#286BEE', label='TWT', zorder=3)
                                #if len(y_values_2) > 1:
                                    #plt.plot([index] * len(y_values_2), y_values_2, color='#286BEE', label='TWT')

                            if pd.notna(row[3]):
                                y_values_3 = [float(val_3) for val_3 in row[3].split(',')]
                                plt.scatter([index] * len(y_values_3), y_values_3, color='#9B72AA', label='HWT', zorder=3)
                                #if len(y_values_3) > 1:
                                    #plt.plot([index] * len(y_values_3), y_values_3, color='#9B72AA', label='HWT')

                            if pd.notna(row[4]):
                                y_values_4 = [float(val_4) for val_4 in row[4].split(',')]
                                plt.scatter([index] * len(y_values_4), y_values_4, color='gray', label='Empty', zorder=3)
                                #if len(y_values_4) > 1:
                                    #plt.plot([index] * len(y_values_4), y_values_4, color='gray', label='Empty')

                        handles, labels = ax.get_legend_handles_labels()
                        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]

                        ax.legend(*zip(*unique))

                        df11 = pd.read_csv(penetration_nonoverlapping)

                        for col in ['continuous_left_H', 'continuous_right_H']:
                            continuous_groups = df11[col].astype(int).groupby(df11[col].ne(df11[col].shift()).cumsum())
                            group_counts = continuous_groups.transform('sum') * df11[col]

                            for _, group in continuous_groups:
                                if group.iloc[0] != 0:
                                    start = group.index[0]
                                    end = group.index[-1]
                                    color = 'red' if col == 'continuous_left_H' else 'green'
                                    plt.axvspan(start, end, color=color, alpha=0.2, linestyle='--', zorder=1)

                        for i, row in df11.iterrows():
                            if row['left_H']:
                                plt.axvline(x=i, color='red', linestyle='--', alpha=0.7, zorder=2)
                            if row['right_H']:
                                plt.axvline(x=i, color='green', linestyle=':', alpha=0.7, zorder=2)
                            if row['left_values_H'] != '[]':
                                left_values = ast.literal_eval(row['left_values_H'])
                                for k, group in enumerate(left_values, start=1):
                                    for value in group:
                                        if isinstance(value, list):
                                            for val in value:
                                                plt.text(i, val, str(k), color='black', fontsize=6, ha='center', va='center', zorder=5)
                                        else:
                                            plt.text(i, value, str(k), color='black', fontsize=6, ha='center', va='center', zorder=5)

                            if row['right_values_H'] != '[]':
                                right_values = ast.literal_eval(row['right_values_H'])
                                for k, group in enumerate(right_values, start=1):
                                    for value in group:
                                        if isinstance(value, list):
                                            for val in value:
                                                plt.text(i, val, str(k), color='black', fontsize=6, ha='center', va='center', zorder=5)
                                        else:
                                            plt.text(i, value, str(k), color='black', fontsize=6, ha='center', va='center', zorder=5)


                        plt.savefig(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_s_{s}_P_H.png", dpi=300, bbox_inches="tight") 
                        plt.close("all")

                        img_path3 = d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_s_{s}_P_T.png"
                        img_path4 = d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_s_{s}_P_H.png"
                        output_path = d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Peak/wave_{a1}{p1}_{a2}{p2}_{j}_s_{s}_P.png"

                        combine_images_vertically(img_path3, img_path4, output_path)
                        '''

                    for j in range(0, 20):


                        if not os.path.exists(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Double/fig_s_{j}"):
                            os.mkdir(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Double/fig_s_{j}")
                        folder_path = (d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_s_{j}")
                        png_count = 0
                        for filename in os.listdir(folder_path):
                            if filename.endswith(".png"):
                                png_count += 1
                        a=round(float(png_count), 1)
                        #print(a)

                        for i in np.arange(0,a,1):
                            image1 = Image.open(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_{j}/output_{i}.png")
                            image2 = Image.open(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_{j}/output_{i}.png")
                            image3 = Image.open(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_s_{j}/output_s_{i}.png")
                            image4 = Image.open(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_s_{j}/output_s_{i}.png")  
                            width1, height1 = image1.size
                            width2, height2 = image2.size
                            width3, height3 = image3.size
                            width4, height4 = image4.size
                            print(width1, height1)
                            print(width2, height2)
                            print(width3, height3)
                            print(width4, height4)
                            #print(width1, height1, width2, height2)
                            new_width = max(width1+width3, width2+width4)
                            new_height = max(height1+height2, height3+height4)
                            combined_image = Image.new('RGB', (new_width, new_height))
                            combined_image.paste(image1, (0, 0))
                            combined_image.paste(image2, (0, height1))
                            combined_image.paste(image3, (width1, 0))
                            combined_image.paste(image4, (width1, height1))

                            combined_image.save(d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Double/fig_s_{j}/output_{i}.png")
                            #combined_image.show()
                            plt.close('all') 
                            #combined_image.show() 

                        input_folder = d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Double/fig_s_{j}"
                        output_video = d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Double/{a1}{p1}_{a2}{p2}_{j}.mp4"
                        create_video_from_images(input_folder, output_video=output_video, fps=10)
                        '''

                        folder_path=f"D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Tethered_1D_{v1}_{v2}{p2}"
                        all_output_csv=d+f"/{a1}{p1}_{a2}{p2}.csv"

                        if __name__ == '__main__':
                            main(folder_path, all_output_csv, v1, v2, p1, p2, a1, a2, s, j)

                        frequency_path=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_{j}"
                        number_path=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_{j}"


                        frequency_s_path=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Frequency/fig_s_{j}"
                        number_s_path=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Number/fig_s_{j}"
                        double_s_path=d+f"/Tethered_1D_{v1}{p1}_{v2}{p2}/Double/fig_s_{j}"

                        try:
                            shutil.rmtree(frequency_path)
                            print(f"{frequency_path} deleted")
                        except OSError as e:
                            print(f"error: {e}")

                        try:
                            shutil.rmtree(number_path)
                            print(f"{number_path} deleted")
                        except OSError as e:
                            print(f"error: {e}")

                        try:
                            shutil.rmtree(frequency_s_path)
                            print(f"{frequency_s_path} deleted")
                        except OSError as e:
                            print(f"error: {e}")

                        try:
                            shutil.rmtree(number_s_path)
                            print(f"{number_s_path} deleted")
                        except OSError as e:
                            print(f"error: {e}")   

                        try:
                            shutil.rmtree(double_s_path)
                            print(f"{double_s_path} deleted")
                        except OSError as e:
                            print(f"error: {e}")                                                 