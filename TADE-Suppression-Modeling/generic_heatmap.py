# Author: Sam Champer

from argparse import ArgumentParser
from PIL import Image
from numpy import linspace
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.font_manager as font_manager

# I keep some fonts in a folder other than my standard windows fonts
#  If you want to use custom fonts, point the next line to a folder with your fonts.
font_dirs = [r"E:\plex-master\IBM-Plex-Sans\fonts\complete\ttf"]
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
for ff in font_files:
    font_manager.fontManager.addfont(ff)
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 30,
                     'font.family': "sans-serif",
                     'font.sans-serif': "IBM Plex Sans",       # This is my prefered font. It's open source and available on github if you'd like to use it too.
                     "figure.titlesize": 36,
                     "axes.titlesize": 32,
                     "axes.labelsize": 30,
                     "savefig.pad_inches": 0,
                     "legend.fontsize": 16,
                     "axes.labelpad": 0.5,
                     "text.color": "black",
                     "axes.labelcolor": "black",
                     "xtick.color": "black",
                     "ytick.color": "black",
                     "legend.framealpha": 0.9,
                     "figure.dpi": 400,
                     "savefig.dpi": 400,
                     "patch.facecolor": "white"})


def save_and_display(fig, image_name):
    # Save and display a figure.
    fig.savefig(image_name)
    im = Image.open(image_name)
    im.show()


def transform_range(val, prev_min, prev_max, new_min, new_max):
    # Transform a value from one range to another.
    return (((val - prev_min) * (new_max - new_min)) / (prev_max - prev_min)) + new_min


def heatmap(src, xcol, ycol, zcol, xlabel, ylabel, title, cbarlabel, colormap, barname):
    """
    Plots a heatmap.
    """
    with open(src, 'r') as f:
        data = f.readlines()
    data = data[1:]  # This trims off the header.
    #print(data)
    for i in range(len(data)):
        data[i] = data[i].split(",") # Might need to change between "," and "\t".
        #print(data[i])
    efficacy = "Normal Drive"
    all_x = [float(entry[xcol]) for entry in data]
    #print(all_x)
    all_y = [float(entry[ycol]) for entry in data]
    all_z = [float(entry[zcol]) for entry in data]
    x_dim = len(set(all_x))
    x_min = min(all_x)
    #print(x_min)
    x_max = max(all_x)
    #print(x_max)
    y_dim = len(set(all_y))
    y_min = min(all_y)
    y_max = max(all_y)
    z_min = min(all_z)
    z_max = max(all_z)

    plot_data = [[all_z for i in range(x_dim)] for i in range(y_dim)]

    for entry in data:
        x = float(entry[xcol])
        y = float(entry[ycol])
        z = float(entry[zcol])
        x_coord = int(transform_range(x, x_min, x_max, 0, x_dim - 1) + 0.5)
        # print(x_coord)
        y_coord = int(transform_range(y, y_min, y_max, 0, y_dim - 1) + 0.5)
        #print(y_coord)
        #z is the final output
        plot_data[y_coord][x_coord] = z
        #print(plot_data)

    fig = plt.figure(figsize=(8.6, 8))  # Confure the desired figure size.
    spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
    ax = fig.add_subplot(spec[0, 0])

    # Adjust the next line if the figure or legends are not well aligned with the edge of the image.
    fig.set_tight_layout({"pad":0.2, "w_pad":0.0, "h_pad":0.0})
    ax.set_title(f"{title}     ")
    ax.set_xlabel(f"{xlabel}")
    ax.set_ylabel(f"{ylabel}")
    ax.set_xticks([i+0.5 for i in linspace(0, x_dim-1, 6)])  # This line creates 21 ticks on the x axis which are centered on the column they correspond to.
    ax.set_yticks([i+0.5 for i in linspace(0, y_dim-1, 6)])  # This line creates 22 ticks on the y axis which are centered on the row they correspond to.
    ax.set_xticklabels([f"{i:.0f}" for i in linspace(x_min, x_max, 6)])
    ax.set_yticklabels([f"{i:.2f}" for i in linspace(y_min, y_max, 6)])
    ax.set_aspect('equal')

    # You might want to change z_min and z_max to the actual min and max values for your data.
    # E.g. if your most extreme possible values are [0, 1], but your dataset only has values in [0.02, 0.95],
    # then you should probably override the next line to explicitly set vmin and vmax to 0 and 1.
    hm = ax.pcolormesh(plot_data, cmap=colormap, rasterized=True, vmin=0, vmax=1)

    # The next block of code is for creating the colorbar for the heatmap.
    cbfig = plt.figure(figsize=(6, 1.2))
    cbfig.set_tight_layout({"pad":0.0, "w_pad":0.0, "h_pad":0.0})
    cbspec = gridspec.GridSpec(ncols=1, nrows=1, figure=cbfig)
    cbax = cbfig.add_subplot(cbspec[0, 0])
    colorbar = cbfig.colorbar(hm, cax=cbax, orientation='horizontal')
    colorbar.set_label(f"{cbarlabel}")

    save_and_display(fig, f"{xlabel} {efficacy}.png")
    save_and_display(cbfig, barname + ".png")


def main():
    # Get args from arg parser:
    parser = ArgumentParser()
    parser.add_argument('-src', '--source', default="Suppressed_without_chase.csv", type=str, help="CSV file to make heatmap from.")
    parser.add_argument('-x','--X_COL', default=1, type=int, help="The column of the entries in X.")
    parser.add_argument('-y','--Y_COL', default=0, type=int, help="The column of the entries in Y.")
    parser.add_argument('-z','--Z_COL', default=22, type=int, help="The column of the entries in Z [i.e. the color].")
    parser.add_argument('-x_label', '--X_LABEL', default="Low density growth rate", type=str, help="Label for the x axis.")
    parser.add_argument('-y_label', '--Y_LABEL', default="Migration rate", type=str, help="Label for the Y axis.")
    parser.add_argument('-title', '--TITLE', default="Suppressed without chasing", type=str, help="Title of the graph.")
    parser.add_argument('-cbar', '--CBARLABEL', default="Outcome fraction", type=str, help="Label for the colorbar.")
    parser.add_argument('-nbar', '--BARNAME', default="Outcome fraction", type=str, help="Name of the label picture.")
    arg = vars(parser.parse_args())

    # Here are some nice color schemes to choose from:
    seismic = plt.get_cmap("seismic")
    magma = plt.get_cmap("magma")
    reds = plt.get_cmap('Reds')
    greens = plt.get_cmap('Greens')
    purples = plt.get_cmap("Purples")

    # Choose a color scheme by specifying it on the next line:
    color_range = seismic(linspace(0.5, 1, 2048))

    # A color scheme can also be an explicit list of hex codes for each color:
    # color_range = ["#ca0020", "#f4a582", "#C4C4C4", "#92c5de", "#0060b0"]

    colormap = ListedColormap(color_range)
    heatmap(arg["source"], arg["X_COL"], arg["Y_COL"], arg["Z_COL"], arg["X_LABEL"], arg["Y_LABEL"], arg["TITLE"], arg["CBARLABEL"], colormap, arg["BARNAME"])


if __name__ == "__main__":
    main()
