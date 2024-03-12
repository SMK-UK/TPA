'''
Sean Keenan, PhD Physics
Quantum Memories Group, Heriot-Watt University, Edinburgh
2023

Functions designed to perform mathematical operations on data
'''

import numpy as np
from scipy.fftpack import fft, fftfreq
from scipy.integrate import simpson

def average_arrays(list_of_arrays):
    '''
    Calculate the average for a list of numpy arrays
    excluding any arrays that contain inf or nan values
    
    '''
    temp = np.zeros_like(list_of_arrays[0])
    count = 0
    for array in list_of_arrays:
        if not np.isinf(np.sum(array)) and not np.isnan(np.sum(array)):
            temp += array
            count += 1

    return temp/count

def bin_data(data, N: int = 10, edge: bool = False):
    """
    Bin the data and return mean
    
    Parameters
    ----------

    data : list of data to average
    bins : number of bins to group data into
    edge : choose to include right or left edge of bin.

    Returns
    -------

    mean : value of data
    """
    minimum = min(data)
    maximum = max(data)
    bins = np.linspace(minimum, maximum, N+1) 
    binned = np.digitize(data, bins, right=edge)

    return data[binned == np.bincount(binned).argmax()].mean()

def find_longest(data_list):
    """
    Find longest list and length within a lst
    
    Parameters
    ----------

    data_list : list of data

    Returns
    -------

    longest : longest list
    length : length of longest list
    """
    longest = max(data_list, key = lambda i: len(i))
    length = max(map(len, data_list))

    return longest, length

def calc_fft(time, amplitude):
    """
    Perform FFT calculation for amplitude component and generate the frequency
    from times.

    Parameters
    ----------
    time : 1D data array / list to use as reference
    amplitude : 1D data array / list of transmission data

    Returns
    -------
    frequencies : list of frequency values from input time data
    ffts : list of fft calculated from input amplitude data

    """
    N = len(time)
    T = time[1] - time[0]
    fftd = fft(amplitude)
    frequencies = fftfreq(N, T)

    return frequencies, fftd

def normalise(dataset_1, reference, dataset_2=0):
    """
    Normalise a set of data by subtracting a control set and dividing by
    a reference (optional).

    Parameters
    ----------
    dataset_1 : data array to normalise
    reference : reference data to divide by
    dataset_2 : control data to subtract
    
    Returns
    -------
    normalised dataset

    """

    return np.divide(np.subtract(dataset_1, dataset_2), reference)

def OD_calc(ref_data, trans_data, c_factor: float=1):
    """
    Perform OD calculation for transmission data and adjust the reference
    using the correction factor if neccesary

    Parameters
    ----------
    reference : data array to use as reference
    transmission : data array of transmission data
    correction : correction factor for the reference data

    Returns
    -------
    calculated optical depth

    """
    return np.log((ref_data * c_factor)/trans_data)

def ODset_calc(reference_sets, transmitted_sets, c_factor: float=1):

    OD_sets = []
    for index in range(len(reference_sets)):
        OD_temp = []
        for reference in reference_sets[index]:
            for transmission in transmitted_sets[index]:
                OD_temp.append(OD_calc(reference, transmission, c_factor))
            OD_sets.append(OD_temp)

    return OD_sets

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
    start = np.argmin(abs(data - bounds[0]))
    stop = np.argmin(abs(data - bounds[1]))

    return start, stop

def normalise_pulse_area(data, indexes:list[int]):
    '''
    Calculate the normalised pulse area (area_trans / area_ref)
    
    <data>:
        excel file for the data to normalise
    <indexes>:
        list of indexes for the corresponding column data
        
    [0] trans:
        index for the transmitted data
    [1] ref:
        index for the reference data
    [2] time:
        index for the time data

    '''
    # calculate trans pulse area
    area_pulse = simpson(y=data[:,indexes[0]], x=data[:,indexes[2]])
    # calculate ref pulse area
    area_ref = simpson(y=data[:,indexes[1]], x=data[:,indexes[2]])
    #calculate normalised area
    norm = normalise(area_pulse, area_ref)

    return norm

def corrected_pulse_area(dataset_1, dataset_2, indexes:list[int]):
    '''
    Calculate the corrected and normalised pulse area
    
    <dataset_1>:
        excel file for the transmitted and reference pulses
    <dataset_2>:
        excel file for the correction pulse data
    <indexes>:
        list of indexes for the corresponding column data
        
    [0] trans:
        index for the transmitted data
    [1] ref:
        index for the reference data
    [2] time:
        index for the time data

    '''
    area_1 = simpson(y=dataset_1[:,indexes[0]], x=dataset_1[:,indexes[2]])
    area_2 = simpson(y=dataset_1[:,indexes[1]], x=dataset_1[:,indexes[2]])
    control = simpson(y=dataset_2[:,indexes[0]], x=dataset_2[:,indexes[2]])
        
    return normalise(dataset_1=area_1, reference=area_2, dataset_2=control)
