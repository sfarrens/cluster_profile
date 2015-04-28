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

##
#  Read ascii file and return pandas
#  DataFrame of cluster members.
#
#  @param[in] opts: List of arguments.
#
#  @return DataFrame of members.
#
def read_ascii(opts):

    data = np.genfromtxt(opts.input_file, unpack = True,
                         dtype = 'S')[np.array(opts.cols) - 1]

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


