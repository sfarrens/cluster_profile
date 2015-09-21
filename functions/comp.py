## @file comp.py
#
#  COMPUTATIONAL FUNCTIONS 
#
#  Basic indexing functions.
#  
#  @author Samuel Farrens
#  @version 1.0
#  @date 2015
#

import numpy as np
import warnings

##
#  Function that checks if the minimum 
#  value is valid.
#
#  @param[in] min_val: Minimum of bin range.
#
#  @exception ValueError if min_val < 0.0.
#
def check_min(min_val):

    if min_val < 0.0:
        raise ValueError('MIN_VAL must be >= 0.0.')

##
#  Function that checks if the minimum and
#  maximum values are valid.
#
#  @param[in] min_val: Minimum of bin range.
#  @param[in] max_val: Maximum of bin range.
#
#  @exception ValueError if min_val > max_val.
#
def check_minmax(min_val, max_val):

    check_min(min_val)

    if min_val > max_val:
        raise ValueError('MIN_VAL must be < MAX_VAL.')

##
#  Function that finds the bin corresponding
#  to a given value.
#
#  @param[in] value: Input value.
#  @param[in] min_value: Minimum of bin range.
#  @param[in] bin_size: Width of bins.
#
def find_bin(value, min_value, bin_size):

    check_min(min_value)

    return np.floor(np.round((np.array(value) - np.array(min_value)) / \
                              np.array(bin_size), 8)).astype('int')

##
#  Function that finds the number of bins 
#  for a given range and bin size.
#
#  @param[in] min_value: Minimum of bin range.
#  @param[in] max_value: Maximum of bin range.
#  @param[in] bin_size: Width of bins.
#                              
def num_bins(min_value, max_value, bin_size):

    #check_minmax(min_value, max_value)

    return np.floor(np.round((np.array(max_value) - np.array(min_value)) / \
                             np.array(bin_size), 8)).astype('int')

##
#  Function that the x-range values for 
#  bins in a given range.
#
#  @param[in] n_bins: Number of bins.
#  @param[in] min_value: Minimum of bin range.
#  @param[in] bin_size: Width of bins.
# 
def x_vals(n_bins, min_value, bin_size):

    return (np.arange(n_bins) + 0.5) * bin_size + min_value

##
#  Function that the checks if the input value 
#  is within a given range.
#
#  @param[in] value: Input value.
#  @param[in] min_value: Minimum of bin range.
#  @param[in] max_value: Maximum of bin range.
# 
def within(value, min_value, max_value):

    check_minmax(min_value, max_value)

    return ((np.array(value) >= np.array(min_value)) & \
            (np.array(value) < np.array(max_value)))

##
#  Function that sets all NaN values in an  
#  array to 1.
#
#  @param[in] array: Input array.
# 
def nan2one(array):

    new_array = np.copy(array)
    
    new_array[np.isnan(new_array)] = 1.0

    return new_array

##
#  Function that sets all NaN values in an  
#  array to 0.
#
#  @param[in] array: Input array.
# 
def nan2zero(array):

    new_array = np.copy(array)
    
    new_array[np.isnan(new_array)] = 0.0

    return new_array

##
#  Feature scale data. Ignores division by
#  zero. 
#
#  @param[in] data: Input data.
#  @param[in] min_val: Minimum value.
#  @param[in] max_val: Maximum value.
#
#  @exception ValueError if data > max_val.
# 
def scale(data, min_val, max_val):

    warnings.simplefilter('ignore')

    data = np.array(data)

    if np.any(data > max_val):
        raise ValueError('DATA must be <= MAX_VAL.')

    check_minmax(min_val, max_val)
    
    scaled = np.float64(data - min_val) / \
      np.float64(max_val - min_val)

    if isinstance(scaled, float):
        scaled = np.array([scaled])
    
    return nan2zero(scaled)
