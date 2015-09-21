## @file cluster_io.py
#
#  CLUSTER IO FUNCTIONS 
#
#  Functions for managing
#  input and output
#  operations.
#  
#  @author Samuel Farrens
#  @version 1.0
#  @date 2015
#

import numpy as np
import pandas as pd
from time import strftime

##
#  Read ascii file and return pandas
#  DataFrame of cluster members.
#
#  @param[in] opts: List of arguments.
#
#  @return DataFrame of members.
#
def read_ascii(opts):

    # If no column numbers have been specified in radial mode
    # then redefine the default columns to [1 2].
    if opts.radial and np.all(opts.cols == np.arange(1, 5)):
        opts.cols = np.arange(1, 3)

    # If a cluster ID is specified then add the appropriate column
    # number.
    if opts.cluster_id:
        if opts.cluster_id_col > 0:
            opts.cols = np.hstack([opts.cluster_id_col, opts.cols])
        else:
            opts.cols = np.hstack([opts.cols, [max(opts.cols) + 1]])

    # Read the only the specified columns from the input file.
    data = np.genfromtxt(opts.input_file, unpack = True,
                         dtype = 'S', usecols = (np.array(opts.cols) - 1))

    # If a cluster ID is specified then save only the corresponding
    # cluster members.
    if opts.cluster_id:
        print ' * Cluster ID = ', opts.cluster_id
        data = data[1::, (data[0] == opts.cluster_id)]

    print ' Successfully read:', opts.input_file, '(%i members)' % data.shape[1]

    if opts.radial:
        return pd.DataFrame({'id' : data[0],
                            'new_r' : np.array(data[1], dtype = 'float64')})
    
    else:
        return pd.DataFrame({'id' : data[0],
                            'ra' : np.array(data[1], dtype = 'float64'),
                            'dec' : np.array(data[2], dtype = 'float64'),
                            'z' : np.array(data[3], dtype = 'float64')})

##
#  Write ascii file with profile data.
#
#  @param[in] opts: List of code options.
#  @param[in] p_data: Profile data.
#
def write_p_data(opts, p_data):

    output_file = opts.input_file + '.log_data'

    header = 'Log output file for cluster.py: ' + strftime('%c') + '\n' + \
      'Input File: ' + opts.input_file + '\n' + \
      'Model: ' + opts.model + '\n' + \
      'Initial Scale Radius [Mpc]: ' + str(opts.rs) + '\n' + \
      'Initial Background [Mpc^-2]: ' + str(opts.bg) + '\n' + \
      'Cluster Size [Mpc]: ' + str(opts.size) + '\n' + \
      'Best fit parameter values. [Scale Radius, Background]'

    np.savetxt(output_file, np.array([p_data[0],]), header = header)

    f_handle = file(output_file, 'a')

    np.savetxt(f_handle, np.array([p_data[3],]),
               header = 'Chi-Squared value. [Goodness of fit, Probability]')
    np.savetxt(f_handle, np.array(p_data[1]).T,
               header = 'Density points. [Radius, Density, Density Error]')
    np.savetxt(f_handle, np.array(p_data[2]).T,
               header = 'Profile fit. [Radius, Density]')

    f_handle.close()

    print ' Outputting log data to: ' + output_file
