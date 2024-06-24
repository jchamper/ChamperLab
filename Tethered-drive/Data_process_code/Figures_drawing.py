import csv
import pandas as pd
import glob
import os
import re
from argparse import ArgumentParser
from PIL import Image
from numpy import linspace
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.gridspec as gridspec
import matplotlib.font_manager as font_manager
import matplotlib as mpl


d0="D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_10_m1_a1"
d="D:/pku/gene drive/tethered drive/newest code/one-dimensional model/embryo-germline/1D/Peak-find/test/Scope_10_m1_a1/Tethered_1D_e_c"
a="Tethered_1DHOMSembryocut_HOMSconversionrate"

if not os.path.exists(d):
    os.mkdir(d)

#split tuple
def process_csv(input_name, output_name):
    df = pd.read_csv(input_name)
    new_cols = df.iloc[:, 0].str.split(",", expand=True)
    new_cols.columns = ["col_1", "col_2"]
    df = df.drop(df.columns[0], axis=1)
    df = pd.concat([new_cols, df], axis=1)
    df["col_1"] = df["col_1"].str.replace("\(", "", regex=True)
    df["col_2"] = df["col_2"].str.replace("\)", "", regex=True)
    df.insert(0, 'Row_Number', range(1, 1 + len(df)))
    df.to_csv(output_name, index=False, header=False)

# data merge
merge_output=f'{d}/{a}.csv'
base_path =f"{d0}"
pattern = 'Tethered_1D_*_*/e*_c*.csv'

files = glob.glob(os.path.join(base_path, pattern))
all_data = pd.DataFrame()
for file in files:
    df = pd.read_csv(file)
    all_data = pd.concat([all_data, df], ignore_index=True)
all_data_sorted = all_data.sort_values(by=['HOMSconversionrate', 'HOMSembryocut'])
all_data_sorted.to_csv(merge_output, index=False)

# data average
average_input=merge_output
average_output=f'{d}/{a}_a.csv'
with open(average_input, 'r') as f:
    reader = csv.reader(f)
    next(reader) 
    data = [row for row in reader]

new_data = {}
for row in data:
    key = (row[1], row[2]) 
    if key in new_data:
        new_data[key].append(float(row[5]))  
    else:
        new_data[key] = [float(row[5])]

with open(average_output, 'w', newline='') as f:
    writer = csv.writer(f)
    #writer.writerow(['Index', 'Column2', 'Column3', 'Mean'])  
    index = 1
    for key, values in new_data.items():
        writer.writerow([index, key[0], key[1], sum(values) / len(values)])  
        index += 1


# data extract
extract_input=merge_output
extract_output=f'{d}/{a}_ex.csv'
df = pd.read_csv(extract_input)
columns = df.iloc[:, [1, 2, 5, 6, 21, 22, 34, 35, 39, 48, 50, 49, 51]]
columns.to_csv(extract_output, index=False)



# permutation
permutation_input=extract_output
elimination_output=f'{d}/{a}_e.csv' 
elimination_output_process=f'{d}/{a}_e_p.csv'
drive_lost_output=f'{d}/{a}_drive_lost.csv'
drive_lost_output_process=f'{d}/{a}_drive_lost_p.csv'


df0 = pd.read_csv(permutation_input)
df0["key"] = list(zip(df0.iloc[:, 0], df0.iloc[:, 1]))
results0 = {}
for key in df0["key"].unique():
    rows = df0[df0["key"] == key]
    rows_1 = rows[rows.iloc[:, 10] == 1]
    sum_1 = rows_1.iloc[:, 2].sum()
    value_1 = sum_1 / 20
    rows_0 = rows[rows.iloc[:, 10] == 0]
    sum_0 = rows_0.iloc[:, 2].sum()
    value_0 = sum_0 / 20
    results0[key] = (value_1, value_0)


df = pd.read_csv(permutation_input)
df["key"] = list(zip(df.iloc[:, 0], df.iloc[:, 1]))
results = {}
#columns_to_convert = [10] 
#for column in columns_to_convert:
    #df.iloc[:, column] = df.iloc[:, column].astype(int)


for key in df["key"].unique():
    rows = df[df["key"] == key]
    rows_1 = rows[(rows.iloc[:, 2] == 0) & (rows.iloc[:, 6] == 0) & (rows.iloc[:, 10] == 1)]
    rows_1_1 = rows_1[rows_1.iloc[:, 6] == 0] 
    rows_1_1_1= rows_1_1[rows_1_1.iloc[:, 6] == 0]
    sum_1 = rows_1.iloc[:,4].sum() #TARE drive lost with chasing 
    value_1 = sum_1 / 20
    rows_0 = rows[(rows.iloc[:, 2] == 0) & (rows.iloc[:, 4] == 0) & (rows.iloc[:, 10] == 1)]
    rows_0_0 = rows_0[rows_0.iloc[:, 4] == 0]
    rows_0_0_0= rows_0_0[rows_0_0.iloc[:, 9] == 1]
    sum_0 = rows_0.iloc[:, 6].sum() #HOMS drive lost with chasing 
    value_0 = sum_0 / 20    
    rows_2 = rows[(rows.iloc[:, 2] == 0) & (rows.iloc[:, 6] == 0) & (rows.iloc[:, 10] == 0)]
    sum_2 = rows_2.iloc[:,4].sum() #TARE drive lost without chasing 
    value_2 = sum_2 / 20
    rows_3 = rows[(rows.iloc[:, 2] == 0)&(rows.iloc[:, 6] == 0)]
    sum_3 = rows_3.iloc[:, 8].sum() #low equilibrium
    value_3 = sum_3 / 20
    rows_4 = rows[(rows.iloc[:, 2] == 0) & (rows.iloc[:, 4] == 0) & (rows.iloc[:, 10] == 0)]
    sum_4 = rows_4.iloc[:, 6].sum() #HOMS drive lost with chasing  
    value_4 = sum_4 / 20
    results[key] = (value_1, value_0, value_2, value_3, value_4)


count_1 = df[(df.iloc[:, 2] == 0) & (df.iloc[:, 4] == 0) & (df.iloc[:, 10] == 0) & (df.iloc[:, 6] == 0)].shape[0]
count_2 = df[(df.iloc[:, 2] == 0) & (df.iloc[:, 4] == 0) & (df.iloc[:, 10] == 1) & (df.iloc[:, 6] == 0)].shape[0]
count_3 = df[(df.iloc[:, 2] == 0) & (df.iloc[:, 4] == 1) & (df.iloc[:, 10] == 0) & (df.iloc[:, 6] == 0)].shape[0]
count_4 = df[(df.iloc[:, 2] == 0) & (df.iloc[:, 4] == 1) & (df.iloc[:, 10] == 1) & (df.iloc[:, 6] == 0)].shape[0]
count_5 = df[(df.iloc[:, 2] == 0) & (df.iloc[:, 4] == 0) & (df.iloc[:, 10] == 0) & (df.iloc[:, 6] == 1)].shape[0]
count_6 = df[(df.iloc[:, 2] == 0) & (df.iloc[:, 4] == 0) & (df.iloc[:, 10] == 1) & (df.iloc[:, 6] == 1)].shape[0]
count_7 = df[(df.iloc[:, 2] == 0) & (df.iloc[:, 4] == 1) & (df.iloc[:, 10] == 0) & (df.iloc[:, 6] == 1)].shape[0]
count_8 = df[(df.iloc[:, 2] == 0) & (df.iloc[:, 4] == 1) & (df.iloc[:, 10] == 1) & (df.iloc[:, 6] == 1)].shape[0]
count_9 = df[(df.iloc[:, 2] == 1) & (df.iloc[:, 10] == 0)].shape[0]
count_10 = df[(df.iloc[:, 2] == 1) & (df.iloc[:, 10] == 1)].shape[0]


total = df.shape[0]

print(f"total{total}")

ratio_1 = count_1/total
ratio_2 = count_2/total
ratio_3 = count_3/total
ratio_4 = count_4/total
ratio_5 = count_5/total
ratio_6 = count_6/total
ratio_7 = count_7/total
ratio_8 = count_8/total
ratio_9 = count_9/total
ratio_10 = count_10/total


col_0 = df.columns[0]
col_1 = df.columns[1]
col_2 = df.columns[2]
col_3 = df.columns[3]
col_4 = df.columns[4]
col_5 = df.columns[5]
col_6 = df.columns[6]
col_7 = df.columns[7]
col_8 = df.columns[8]
col_9 = df.columns[9]
col_10 = df.columns[10]
col_11 = df.columns[11]

print(f"two drives remain without chasing({col_2}=0 AND{col_4}=0 AND{col_10}=0 AND{col_6}=0 ): {count_1} rows {ratio_1} ratio")
print(f"two drives remain with chasing({col_2}=0 AND{col_4}=0 AND{col_10}=1 AND{col_6}=0 ): {count_2} rows {ratio_2} ratio")
print(f"TARE drive lost without chasing({col_2}=0 AND{col_4}=1 AND{col_10}=0 AND{col_6}=0 ): {count_3} rows {ratio_3} ratio")
print(f"TARE drive lost with chasing({col_2}=0 AND{col_4}=1 AND{col_10}=1 AND{col_6}=0 ): {count_4} rows {ratio_4} ratio")
print(f"HOMS drive lost without chasing({col_2}=0 AND{col_4}=0 AND{col_10}=0 AND{col_6}=1 ): {count_5} rows {ratio_5} ratio")
print(f"HOMS drive lost with chasing({col_2}=0 AND{col_4}=0 AND{col_10}=1 AND{col_6}=1 ): {count_6} rows {ratio_6} ratio")
print(f"two drives lost without chasing({col_2}=0 AND{col_4}=1 AND{col_10}=0 AND{col_6}=1 ): {count_7} rows {ratio_7} ratio")
print(f"two drives lost with chasing({col_2}=0 AND{col_4}=1 AND{col_10}=1 AND{col_6}=1 ): {count_8} rows {ratio_8} ratio")
print(f"elimination without chasing({col_2}=1 AND{col_10}=0 ): {count_9} rows {ratio_9} ratio")
print(f"elimination with chasing({col_2}=1 AND{col_10}=1 ): {count_10} rows {ratio_10} ratio")

output = pd.DataFrame.from_dict(results, orient="index", columns=["value_1", "value_0", "value_2", "value_3", "value_4"])
output.to_csv(drive_lost_output)
process_csv(drive_lost_output, drive_lost_output_process)

output0 = pd.DataFrame.from_dict(results0, orient="index", columns=["value_1", "value_0"])
output0.to_csv(elimination_output)
process_csv(elimination_output, elimination_output_process)


# generation suppressed
gen_input=extract_output
gen_output=f'{d}/{a}_gen.csv'
gen_output_process=f'{d}/{a}_gen_p.csv'
df1 = pd.read_csv(gen_input)
df1["key"] = list(zip(df1.iloc[:,0], df1.iloc[:,1]))
df1_filtered = df1[(df1.iloc[:,2] == 1)].copy()  # Use .copy() to avoid SettingWithCopyWarning
df1_filtered["avg"] = df1_filtered.groupby("key")[df1.columns[3]].transform("mean")
df1_filtered["count"] = df1_filtered.groupby("key")["key"].transform("count")
df1_merged = df1.merge(df1_filtered[["key", "avg", "count"]], on="key", how="left")
df1_merged["avg"] = df1_merged["avg"].fillna(10000)
df1_merged["count"] = df1_merged["count"].fillna(0)
df1_merged[["key", "avg", "count"]].drop_duplicates().to_csv(gen_output, index=False)
process_csv(gen_output, gen_output_process)


# heatmap
plt.rcParams['svg.fonttype'] = 'none'
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 32,
                     'font.family': "Arial",
                     "axes.titlesize": 32,     
                     "axes.labelsize": 32,
                     "savefig.pad_inches": 0,
                     "legend.fontsize": 2,
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
                     "legend.framealpha": 0.2,
                     "patch.facecolor": "white"})


def save_and_dispaly(fig, image_name):
    fig.savefig(image_name)
    im = Image.open(image_name)
    im.show()


def transform_range(val, prev_min, prev_max, new_min, new_max):
    return (((val - prev_min) * (new_max - new_min)) / (prev_max - prev_min)) + new_min


def heatmap_g(outcome, src, xcol, ycol, zcol, xlabel, ylabel, title, cbarlabel):
    name = {
    0: "Suppressed successfully",
    1: "Suppressed with chasing",
    2: "Suppressed without chasing",
    3: "TARE drive lost with chasing",
    4: "Homing drive lost with chasing",
    5: "Suppressed generation",
    6: "TARE drive lost without chasing",
    7: "low equilibrium",
    8: "Homing drive lost without chasing"}[outcome]
    pic=f"{a}{name}"

    with open(src, 'r') as f:
        data = f.readlines()
    data = data[0:] 
    for i in range(len(data)):
        data[i] = data[i].split(',')
    drivename = data[0][0]
    all_x = [float(entry[xcol]) for entry in data]
    all_y = [float(entry[ycol]) for entry in data]
    all_z = [float(entry[zcol]) for entry in data]
    x_dim = len(set(all_x))
    x_min = min(all_x)
    x_max = max(all_x)
    y_dim = len(set(all_y))
    y_min = min(all_y)
    y_max = max(all_y)
    z_min = min(all_z)
    z_max = max(all_z)
    plot_data = [[0.0 for i in range(x_dim)] for i in range(y_dim)]

    for entry in data:
        x = float(entry[xcol])
        y = float(entry[ycol])
        z = float(entry[zcol])
        x_coord = int(transform_range(x, x_min, x_max, 0, x_dim - 1)+0.5)
        y_coord = int(transform_range(y, y_min, y_max, 0, y_dim - 1)+0.5)
        plot_data[y_coord][x_coord] = z

    fig = plt.figure(figsize=(20,8.5)) 
    spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
    ax = fig.add_subplot(spec[0, 0])

   
    fig.set_tight_layout({"pad":0.0, "w_pad":0.0, "h_pad":0.0})
    ax.set_title(f"{title}")  
    ax.set_xlabel(f"{xlabel}")
    ax.set_ylabel(f"{ylabel}")
    #ax.set_xticks([0.1,0.2,0.3,0.4,0.5,0.6]])
    #ax.set_yticks(np.arrange(data.shape[]))
    #ax.set_xticks([i+0.5 for i in linspace(0, x_dim-1, 21)])  
    #ax.set_yticks([i+0.5 for i in linspace(0, y_dim-1, 21)])
    ax.set_xticks([i+0.5 for i in linspace(0, x_dim-1, 6)])  
    ax.set_yticks([i+0.5 for i in linspace(0, y_dim-1, 6)])
    ax.set_xticklabels([0.00,0.20,0.40,0.60,0.80,1.00])
    ax.set_yticklabels([0.80,0.84,0.88,0.92,0.96,1.00])
    #ax.set_xticklabels([0.00,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00])
    #ax.set_yticklabels([0.80,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.90,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,1.00])
    ax.set_aspect('equal')  
    cmap=plt.cm.Blues
    #cmap=plt.cm.ocean_r
    cmap.set_over("Black")
    hm = ax.pcolormesh(plot_data, cmap = cmap, rasterized=False, vmin=51, vmax=371) #51 371
    """
    用于创建具有非规则矩形网格的伪彩色图即热图
    包含2D数组中的值为color-mapped的值。
    cmap:此参数是颜色图实例或注册的颜色图名称。rainbow\BuGn\RdYlGn\RdYlBu\Blues\Spectral_r\viridis_r\gist_earth\RdGy_r\RdBu
    \\
    norm:此参数是Normalize实例，将数据值缩放到规范的颜色图范围[0，1]以映射到颜色
    rasterized: 是否矢量
    vmin, vmax:这些参数本质上是可选的，它们是颜色栏范围
    """

    cbfig = plt.figure(figsize=(300,0.3))
    cbfig.subplots_adjust(right=0.15)
    cbfig.set_tight_layout({"pad":0.4, "w_pad":0.0, "h_pad":0.0})
    cbspec = gridspec.GridSpec(ncols=1, nrows=1, figure=cbfig)
    cbax = cbfig.add_subplot(cbspec[0, 0])
    colorbar = cbfig.colorbar(hm,label='Suppressed generation', cax=cbax, orientation='horizontal')

    #save_and_dispaly(cbfig, f"colorbar_glf.png")
    cbfig.savefig(f"{d}/{pic}_colorbar_glf.svg", dpi=150, format='svg', bbox_inches="tight")
    fig.savefig(f"{d}/{pic}.svg", dpi=300, format='svg', bbox_inches="tight")
    #plt.show()


def heatmap(outcome, src, xcol, ycol, zcol, xlabel, ylabel, title, cbarlabel):
    name = {
    0: "Suppressed successfully",
    1: "Suppressed with chasing",
    2: "Suppressed without chasing",
    3: "TARE drive lost with chasing",
    4: "Homing drive lost with chasing",
    5: "Suppressed generation",
    6: "TARE drive lost without chasing",
    7: "low equilibrium",
    8: "Homing drive lost without chasing"}[outcome]
    pic=f"{a}{name}"

    with open(src, 'r') as f:
        data = f.readlines()
    data = data[0:] 
    for i in range(len(data)):
        data[i] = data[i].split(',')
    drivename = data[0][0]
    all_x = [float(entry[xcol]) for entry in data]
    all_y = [float(entry[ycol]) for entry in data]
    all_z = [float(entry[zcol]) for entry in data]
    x_dim = len(set(all_x))
    x_min = min(all_x)
    x_max = max(all_x)
    y_dim = len(set(all_y))
    y_min = min(all_y)
    y_max = max(all_y)
    z_min = min(all_z)
    z_max = max(all_z)
    plot_data = [[0.0 for i in range(x_dim)] for i in range(y_dim)]

    for entry in data:
        x = float(entry[xcol])
        y = float(entry[ycol])
        z = float(entry[zcol])
        x_coord = int(transform_range(x, x_min, x_max, 0, x_dim - 1)+0.5)
        y_coord = int(transform_range(y, y_min, y_max, 0, y_dim - 1)+0.5)
        plot_data[y_coord][x_coord] = z

    fig = plt.figure(figsize=(20,8.5)) 
    spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig) 
    ax = fig.add_subplot(spec[0, 0])

    fig.set_tight_layout({"pad":0.0, "w_pad":0.0, "h_pad":0.0})
    ax.set_title(f"{title}")  
    ax.set_xlabel(f"{xlabel}")
    ax.set_ylabel(f"{ylabel}")
    #ax.set_xticks([0.1,0.2,0.3,0.4,0.5,0.6]])
    #ax.set_yticks(np.arrange(data.shape[]))
    #ax.set_xticks([i+0.5 for i in linspace(0, x_dim-1, 21)])  
    #ax.set_yticks([i+0.5 for i in linspace(0, y_dim-1, 21)])
    ax.set_xticks([i+0.5 for i in linspace(0, x_dim-1, 6)])  
    ax.set_yticks([i+0.5 for i in linspace(0, y_dim-1, 6)])
    ax.set_xticklabels([0.00,0.20,0.40,0.60,0.80,1.00])
    ax.set_yticklabels([0.80,0.84,0.88,0.92,0.96,1.00])
    #ax.set_xticklabels([0.00,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00])
    #ax.set_yticklabels([0.80,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.90,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,1.00])
    ax.set_aspect('equal')  
    hm = ax.pcolormesh(plot_data, cmap = "Reds", rasterized=False, vmin=0.00, vmax=1.00)
    """
    用于创建具有非规则矩形网格的伪彩色图即热图
    包含2D数组中的值为color-mapped的值。
    cmap:此参数是颜色图实例或注册的颜色图名称。rainbow\BuGn\RdYlGn\RdYlBu\Blues\Spectral_r\viridis_r\gist_earth\RdGy_r\RdBu
    \\
    norm:此参数是Normalize实例，将数据值缩放到规范的颜色图范围[0，1]以映射到颜色
    rasterized: 是否矢量
    vmin, vmax:这些参数本质上是可选的，它们是颜色栏范围
    """

    cbfig = plt.figure(figsize=(300,0.3))
    cbfig.subplots_adjust(right=0.15)
    cbfig.set_tight_layout({"pad":0.4, "w_pad":0.0, "h_pad":0.0})
    cbspec = gridspec.GridSpec(ncols=1, nrows=1, figure=cbfig)
    cbax = cbfig.add_subplot(cbspec[0, 0])
    colorbar = cbfig.colorbar(hm,label='Frequency of outcome', cax=cbax, orientation='horizontal')

    #save_and_dispaly(cbfig, f"colorbar_glf.png")
    cbfig.savefig(f"{d}/{pic}_colorbar_glf.svg", dpi=150, format='svg', bbox_inches="tight")
    fig.savefig(f"{d}/{pic}.svg", dpi=300, format='svg', bbox_inches="tight")
    #plt.show()

def main(outcome,heatmap_input,column,h):
    name = {
    0: "Suppressed successfully",
    1: "Suppressed with chasing",
    2: "Suppressed without chasing",
    3: "TARE drive lost with chasing",
    4: "Homing drive lost with chasing",
    5: "Suppressed generation",
    6: "TARE drive lost without chasing",
    7: "low equilibrium",
    8: "Homing drive lost without chasing"}[outcome]

    parser = ArgumentParser()
    parser.add_argument('-src', '--source', \
                        default=f"{heatmap_input}",type=str, help="CSV file to make heatmap from.")
    parser.add_argument('-x','--X_COL', default=1, type=int, help="The column of the entries in X.")
    parser.add_argument('-y','--Y_COL', default=2, type=int, help="The column of the entries in Y.")
    parser.add_argument('-z','--Z_COL', default=column, type=int, help="The column of the entries in Z [i.e. the color].")
    parser.add_argument('-x_label', '--X_LABEL', default="Embryo cut rate", type=str, help="Label for the x axis.")
    parser.add_argument('-y_label', '--Y_LABEL', default="Drive conversion efficiency", type=str, help="Label for the Y axis.")
    parser.add_argument('-title', '--TITLE', default=name, type=str, help="Title of the graph.")
    parser.add_argument('-cbar', '--CBARLABEL', default="Frequency of outcome", type=str, help="Label for the colorbar.")
    arg = vars(parser.parse_args())

    seismic = plt.get_cmap("seismic")
    magma = plt.get_cmap("magma")
    Reds = plt.get_cmap('Reds')
    greens = plt.get_cmap('Greens')
    Purples = plt.get_cmap('Purples')
    copper = plt.get_cmap("copper")
    RdGy = plt.get_cmap("RdGy")
    Accent = plt.get_cmap("Accent")
    if h=="0":
        heatmap(outcome, arg["source"], arg["X_COL"], arg["Y_COL"], arg["Z_COL"], arg["X_LABEL"], arg["Y_LABEL"], arg["TITLE"], arg["CBARLABEL"])
    if h=="1":
        heatmap_g(outcome, arg["source"], arg["X_COL"], arg["Y_COL"], arg["Z_COL"], arg["X_LABEL"], arg["Y_LABEL"], arg["TITLE"], arg["CBARLABEL"])
        
# main heatmap
if __name__ == "__main__":
    main(0,average_output,3,"0")



# elimination heatmap
if __name__ == "__main__":
    main(1, elimination_output_process, 3,"0")
    main(2, elimination_output_process, 4,"0")



# drive lost heatmap
    main(3, drive_lost_output_process, 3,"0")
    main(4, drive_lost_output_process, 4,"0")
    main(6, drive_lost_output_process, 5,"0")
    main(7, drive_lost_output_process, 6,"0")
    main(8, drive_lost_output_process, 7,"0")


# generation heatmap 
    main(5, gen_output_process, 3,"1")