## @file np_adjust.py
#
#  NUMPY ADJUSTMENT FUNCTIONS 
#
#  Functions for making some
#  minor adjustments to the
#  standard output of Numpy
#  functions.
#  
#  @author Samuel Farrens
#  @version 1.0
#  @date 2015
#

##
#  Function corrects the x-range output
#  from np.histogram for plotting.
#
#  @param[in] vals: x-range from np.histogram
#
#  @return Corrected x-range.
#
def x_bins(vals):

    return (vals[:-1] + vals[1:]) / 2.0

##
#  Function corrects the x-range output
#  from np.histogram for plotting step.
#
#  @param[in] vals: x-range from np.histogram
#
#  @return Corrected x-range step.
#
def x_bins_step(vals):

    return x_bins(vals) + (vals[1] - vals[0]) / 2.0
