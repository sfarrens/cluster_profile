## @file fits.py
#
#  FITTING FUNCTIONS 
#
#  Functions for finding best
#  fit to data.
#  
#  @author Samuel Farrens
#  @version 1.0
#  @date 2015
#

from scipy.odr import *

##
#  Equation of a line: y = mx + b
#
#  @param[in] B: Slope (m) and intercept (b).
#  @param[in] x: Data.
#
#  @return Value of y.
#
def linear_fit(B, x):
    
    return B[0] * x + B[1]

##
#  Orthogonal distance regression fit.
#
#  @param[in] x: x data.
#  @param[in] y: y data.
#  @param[in] xerr: x data errors.
#  @param[in] yerr: y data errors.
#  @param[in] fit: Function for fit.
#
#  @return Best fit parameters.
#
def fit_odr(x, y, xerr, yerr, fit):
    
    model = Model(fit)
    r_data = RealData(x, y, sx = xerr, sy = yerr)
    odr = ODR(r_data, model, beta0 = [1.0, 2.0])
    odr_out = odr.run()
    
    return odr_out.beta
