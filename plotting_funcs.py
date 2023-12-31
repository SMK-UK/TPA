'''
Sean Keenan, PhD Physics
Quantum Memories Group, Heriot-Watt University, Edinburgh
2023

Functions designed to plot data

V.0.1
'''

from numpy import argmin, linspace, min, vstack
import matplotlib.pyplot as mp
from matplotlib.colors import ListedColormap, LinearSegmentedColormap, to_rgba
import numpy as np
import os

scope_colours = ['gold', 'limegreen', 'orange', 'royalblue']
scope_rgba = [to_rgba(colour) for colour in scope_colours]
og_cmap = mp.cm.get_cmap('tab10')

# Get the colors from the existing colormap
og_colors = og_cmap(np.linspace(0, 1, og_cmap.N))
# Combine existing colors with predefined colors
combined_colors = np.vstack([scope_rgba, og_colors])
# Create a new colormap from the combined colors
custom_cmap = ListedColormap(combined_colors)

def plot_spectra(x_data, y_data, data_indexes = [], keys = list[str], shifter: int or float=0,
            axis_lbls = None, sec_axis = True, save = False, 
            data_labels = [], lims: tuple = (), woi: list = [], res = 80):
    """
    zoom in on a particular area of interest in a dataset

    Parameters
    ----------

    data : list / array - data to perform zoom
    bounds : tuple - lower and upper bounds of the region of interest

    Returns
    -------

    start, stop : start and stop index for the zoomed data
    """

    data_lbl = None

    for m, key in enumerate(keys):
        fig, ax = mp.subplots()
        ax.grid(True, color='silver', linewidth=0.5)
        if axis_lbls:
            ax.set_title('Halfwave Plate: ' + key)
            ax.set(xlabel=axis_lbls[0], ylabel=axis_lbls[1])
        if sec_axis:
            sec_ax = ax.secondary_xaxis('top', functions=
                                        (lambda x: 1e7/x, lambda x: 1e7/x))
            sec_ax.set_xlabel('Wavelength (nm)')
        if woi:
            for woi_set in woi:
                for vline in woi_set[0]:
                    ax.axvline(x=vline, linestyle=woi_set[1], 
                               color=woi_set[2], linewidth='1')
        shift = 0
        for o, x in enumerate(x_data[m]):
            
            plot_colour = mp.cm.winter(linspace(0, 1, len(x_data[m])))
            if lims:
                lower, upper = zoom(x, lims)
                x = x[lower:upper]
                y = y_data[m][o][lower:upper]
            else:
                y = y_data[m][o]
            y -= (min(y) - shift)
            if data_labels:
                data_lbl = os.path.split(data_labels[o])[1]
            ax.plot(x, y, color=plot_colour[o],
                    linestyle='-', alpha=0.8, label=data_lbl)
            if data_indexes:
                ax.plot(x[data_indexes[m][o]], y[data_indexes[m][o]], 
                        color='red',
                   marker='x', linestyle='None', alpha=1, 
                   label='_nolegend_')     
            shift += shifter

        ax.legend(bbox_to_anchor=(1.01, 1), loc='best', fontsize=8)
        fig.tight_layout()

        if save:
            folder = os.path.split(data_labels[0])[0]
            region = str(round(x[lower])) + '_' + str(round(x[upper])) + '_' + key
            name = os.path.join(folder, region + '.png')

            fig.savefig(fname=name, dpi=res, format='png', bbox_inches='tight')

def plot_scope(time, channel_data, multi: bool=False):

    if multi:
        num = len(channel_data)

        fig, ax = mp.subplots(nrows=num, ncols=1, sharex='all')
        # shared labels
        fig.tight_layout(w_pad=2, rect=[0.05, 0.05, 1, 1])
        fig.supxlabel('Time ($\mu$s)')
        fig.supylabel('Voltage (V)')

        for index, axis in enumerate(ax):
            axis.set_title(f'Channel {index+1}')
            axis.plot(time, channel_data(index), color=custom_cmap[num])
            
    else:
        fig, ax = mp.subplots()
        for index, data in enumerate(channel_data):
            ax.plot(time, data, color=custom_cmap(index), label=f'Channel {index+1}')
            ax.legend()
        ax.set(xlabel='Time ($\mu$s)', ylabel='Voltage (V)')

def zoom(data, bounds:tuple=()):
    """
    zoom in on a particular area of interest in a dataset

    Parameters
    ----------
    data : list / array - data to perform zoom
    bounds : tuple - lower and upper bounds of the region of interest

    Returns
    -------
    start, stop : start and stop index for the zoomed data

    """
    start = argmin(abs(data - bounds[0]))
    stop = argmin(abs(data - bounds[1]))

    return start, stop