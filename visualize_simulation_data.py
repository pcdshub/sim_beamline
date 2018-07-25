#  get graph for simulation data
# usage:
# python plot_simulation_data -d "datafile.txt"
import argparse
import matplotlib
matplotlib.use("Agg")  # so that matplotlib doesnot look for display environment
import matplotlib.pyplot as plt
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__))+'/radiosoft-srw_python')
from data_file_handler import extract_simulation_data

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data_file', type = str, help ='simulation data file', required = True)
    args = parser.parse_args()
    data_file_arg = args.data_file
    return data_file_arg

def plot_simulation_data(data_file):
    # the input is a dictionary that comes from above extract simulation data
    data_dict = extract_simulation_data(data_file)
    img = data_dict['data']
    # return tuple (row,column)
    max_index = np.where(img == np.amax(img))
    horizontal = img[max_index[0] , :][0]
    vertical = img[: , max_index[1]]
    f = plt.figure()
    import matplotlib.gridspec as gridspec
    gs = gridspec.GridSpec(2, 2, width_ratios=[2, 1], height_ratios=[2, 1])
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    ax3 = plt.subplot(gs[2])
    ax4 = plt.subplot(gs[3])

    ax1.imshow(img, aspect = 'auto')
    ax1.tick_params(labelbottom = False, labelleft = False)
    yh = list(range(0,len(vertical)))
    ax2.plot(vertical[::-1], yh)
    ax2.tick_params(labelleft=False)
    ax3.plot(horizontal)
    ax3.tick_params(labelbottom=False)
    ax4.text(0, 0.6, "Horizontal range (%.3f, %.3f) um\nVertical range (%.3f, %.3f) um" %(data_dict['horizontal_range'][0]*10**6, data_dict['horizontal_range'][1]*10**6,\
        data_dict['vertical_range'][0]*10**6, data_dict['vertical_range'][1]*10**6), fontsize = 6)
    ax4.tick_params(labelbottom = False, labelleft = False)
    ax4.set_axis_off()

    plt.savefig("image.png")

data_file = get_args()
plot_simulation_data(data_file)
