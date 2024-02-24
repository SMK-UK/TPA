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
from fitting_functions import exp_decay

mp.style.use('signature.mplstyle')

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

def plot_scope(time, channel_data, titles=[], multi: bool=False):

    labels = []
    if titles:
        for title in titles:
            labels.append(title)
    if not titles or len(titles) < len(channel_data):
        for index in range(len(titles), len(channel_data), 1):
            labels.append(f'Channel {index+1}')

    if multi:
        num = len(channel_data)

        fig, ax = mp.subplots(nrows=num, ncols=1, sharex='all')
        # shared labels
        fig.tight_layout(w_pad=2, rect=[0.05, 0.05, 1, 1])
        fig.supxlabel('Time ($\mu$s)')
        fig.supylabel('Voltage (V)')

        for index, axis in enumerate(ax):
            axis.set_title(labels[index])
            axis.plot(time, channel_data[index], color=custom_cmap(index))
            
    else:
        fig, ax = mp.subplots()
        for index, data in enumerate(channel_data):
            ax.plot(time, data, color=custom_cmap(index), label=labels[index])
            ax.legend()
        ax.set(xlabel='Time ($\mu$s)', ylabel='Voltage (V)')
    
    return fig, ax

def plot_T1_trigger(time_data, channel_data:list, i:dict=None):
    '''
    Plot T1 data where trigger has been selected.
    Used to check the trigger location

    <time_data>:
        time channel data goes here
    <channel_data>:
        channel data goes here as list
    <i>:
        trigger and channel indexes goes here as dictionary

    '''
    # default to plot all
    if not i:
        i = {'ref': 0,
            'trans':1,
            'trig':0,
            'r_off':-1,
            'off':-1,
            'ramp':-1}

    fig, ax = mp.subplots(ncols=2, nrows=2, sharex=True)
    # tight layout and shared labels
    fig.tight_layout(w_pad=2, rect=[0, 0.05, 1, 1])
    fig.supxlabel('Time ($\mu$s)')

    # plot linear reference data
    ax[0][0].set_title('Reference')
    ax[0][0].plot(time_data[i['trig']:i['ramp']], channel_data[i['ref']][i['trig']:i['ramp']], label='raw', alpha=0.8)
    ax[0][0].plot(time_data[i['trig']+i['r_off']:i['ramp']], channel_data[i['ref']][i['trig']+i['r_off']:i['ramp']], label='cut', alpha=0.8)
    ax[0][0].set(ylabel='Voltage (V)')
    # plot logarithmic reference data
    ax[1][0].set_title('Reference')
    ax[1][0].plot(time_data[i['trig']:i['ramp']], channel_data[i['ref']][i['trig']:i['ramp']], label='raw', alpha=0.8)
    ax[1][0].plot(time_data[i['trig']+i['r_off']:i['ramp']], channel_data[i['ref']][i['trig']+i['r_off']:i['ramp']], label='cut', alpha=0.8)
    ax[1][0].set(ylabel='log scale (a.u.)')
    ax[1][0].set_yscale('log')
    # plot linear transmitted data
    ax[0][1].set_title('Transmitted')
    ax[0][1].plot(time_data[i['trig']:i['ramp']], channel_data[i['trans']][i['trig']:i['ramp']], label='raw', alpha=0.8)
    ax[0][1].plot(time_data[i['trig']+i['off']:i['ramp']], channel_data[i['trans']][i['trig']+i['off']:i['ramp']], label='cut', alpha=0.8)
    ax[0][1].set(ylabel='Voltage (V)')
    ax[0][1].legend()
    # plot logarithmic transmitted data
    ax[1][1].set_title('Transmitted')
    ax[1][1].plot(time_data[i['trig']:i['ramp']], channel_data[i['trans']][i['trig']:i['ramp']], label='raw', alpha=0.8)
    ax[1][1].plot(time_data[i['trig']+i['off']:i['ramp']], channel_data[i['trans']][i['trig']+i['off']:i['ramp']], label='cut', alpha=0.8)
    ax[1][1].set(ylabel='log scale (a.u.)')
    ax[1][1].set_yscale('log')

    return fig, ax

def plot_T1_fit(time, data, fit):
    '''
    Plot T1 fitted data on top of experimental data
    
    '''
    fig, ax = mp.subplots(nrows=1, ncols=2)
    
    ax[0].set_title('Reference Fit')
    ax[0].plot(time, data, color='blue', alpha=0.5, label='Exp. Data')
    ax[0].plot(time, exp_decay((time), *fit), color='orange', linestyle='--', alpha=1, label='Fit')
    ax[0].ticklabel_format(axis='both', style='sci', scilimits=(0,0), useMathText = True)
    ax[0].legend()

    ax[1].set_title('Log Scale Fit')
    ax[1].plot(time,data, color='blue', alpha=0.5, label='Exp. Data')
    ax[1].plot(time, exp_decay((time), *fit), color='orange', linestyle='--', alpha=1, label='Fit')
    ax[1].set_yscale('log')
    ax[1].legend()
   
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