# Author: Sam Champer

from argparse import ArgumentParser
from PIL import Image
from numpy import linspace
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.gridspec as gridspec
import matplotlib.font_manager as font_manager
import matplotlib as mpl

plt.style.use('ggplot')
plt.rcParams.update({'font.size': 32,
                     'font.family': "Times New Roman",
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
    # Save and display a figure.
    fig.savefig(image_name)
    im = Image.open(image_name)
    im.show()


def transform_range(val, prev_min, prev_max, new_min, new_max):
    # Transform a value from one range to another.
    return (((val - prev_min) * (new_max - new_min)) / (prev_max - prev_min)) + new_min


def heatmap(src, xcol, ycol, zcol, xlabel, ylabel, title, cbarlabel, colormap):
    """
    Plots a heatmap.
    """
    with open(src, 'r') as f:
        data = f.readlines()
    data = data[1:] 
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
        x_coord = int(transform_range(x, x_min, x_max, 0, x_dim - 1) + 0.5)
        y_coord = int(transform_range(y, y_min, y_max, 0, y_dim - 1) + 0.5)
        plot_data[y_coord][x_coord] = z

    fig = plt.figure(figsize=(8,8.5))  # Confure the desired figure size.
    spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig) #place
    ax = fig.add_subplot(spec[0, 0])

    # Adjust the next line if the figure or legends are not well aligned with the edge of the image.
    fig.set_tight_layout({"pad":0.0, "w_pad":0.0, "h_pad":0.0})
    ax.set_title(f"{title}")  
    ax.set_xlabel(f"{xlabel}")
    ax.set_ylabel(f"{ylabel}")
    #ax.set_xticks([0.1,0.2,0.3,0.4,0.5,0.6]])
    #ax.set_yticks(np.arrange(data.shape[]))
    ax.set_xticks([i+0.5 for i in linspace(0, x_dim-1, 6)])  
    ax.set_yticks([i+0.5 for i in linspace(0, y_dim-1, 6)])  
    ax.set_xticklabels([0,0.2,0.4,0.6,0.8,1.0])
    ax.set_yticklabels([0,1.0,2.0,3.0,4.0,5.0])
    ax.set_aspect('equal')  
    hm = ax.pcolormesh(plot_data, cmap = 'Reds', rasterized=False, vmin=0, vmax=1)

    # The next block of code is for creating the colorbar for the heatmap.
    cbfig = plt.figure(figsize=(1.5,8.5))
    cbfig.subplots_adjust(right=0.15)
    cbfig.set_tight_layout({"pad":0.4, "w_pad":0.0, "h_pad":0.0})
    cbspec = gridspec.GridSpec(ncols=1, nrows=1, figure=cbfig)
    cbax = cbfig.add_subplot(cbspec[0, 0])
    colorbar = cbfig.colorbar(hm, cax=cbax, orientation='vertical')

    save_and_dispaly(cbfig, f"colorbar_glf.png")
    plt.show()

def main():
    # Get args from arg parser:
    parser = ArgumentParser()
    parser.add_argument('-src', '--source', default="data.csv", type=str, help="CSV file to make heatmap from.")
    parser.add_argument('-x','--X_COL', default=1, type=int, help="The column of the entries in X.")
    parser.add_argument('-y','--Y_COL', default=2, type=int, help="The column of the entries in Y.")
    parser.add_argument('-z','--Z_COL', default=3, type=int, help="The column of the entries in Z [i.e. the color].")
    parser.add_argument('-x_label', '--X_LABEL', default="x_label", type=str, help="Label for the x axis.")
    parser.add_argument('-y_label', '--Y_LABEL', default="y_label", type=str, help="Label for the Y axis.")
    parser.add_argument('-title', '--TITLE', default="Title", type=str, help="Title of the graph.")
    parser.add_argument('-cbar', '--CBARLABEL', default="COLOR BAR LABEL", type=str, help="Label for the colorbar.")
    arg = vars(parser.parse_args())

    # Here are some nice color schemes to choose from:
    seismic = plt.get_cmap("seismic")
    magma = plt.get_cmap("magma")
    Reds = plt.get_cmap('Reds')
    greens = plt.get_cmap('Greens')
    Purples = plt.get_cmap('Purples')
    copper = plt.get_cmap("copper")
    RdGy = plt.get_cmap("RdGy")
    Accent = plt.get_cmap("Accent")
    # Choose a color scheme by specifying it on the next line:
    color_range = Reds(linspace(0, 1, 100))
    colormap = ListedColormap(color_range)
    print(colormap)
    heatmap(arg["source"], arg["X_COL"], arg["Y_COL"], arg["Z_COL"], arg["X_LABEL"], arg["Y_LABEL"], arg["TITLE"], arg["CBARLABEL"], colormap)


if __name__ == "__main__":
    main()
