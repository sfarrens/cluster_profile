## @file astro.py
#
#  STATISTICS FUNCTIONS 
#
#  Basic statistics functions.
#  
#  @author Samuel Farrens
#  @version 1.0
#  @date 2015
#

import numpy as np
import scipy.stats as ss

##
#  Function that tests the chi^2 goodness
#  of fit.
#
#  @param[in] data_obs: Observed data.
#  @param[in] data_exp: Expected data.
#  @param[in] sigma: Expected data error.
#  @param[in] ddof: Delta degrees of freedom.
#  Default (ddof = 1).
#
#  @return Chi-squared value and probability.
#
#  Degrees of freedom = len(data_obs) - ddof
#
#  @exception ValueError for invalid RA.
#
def chi2_gof(data_obs, data_exp, sigma, ddof = 1):

    chi2 = np.sum(((data_obs - data_exp) / sigma) ** 2)
    p_val = ss.chi2.cdf(chi2, len(data_obs) - ddof)

    return chi2, p_val
