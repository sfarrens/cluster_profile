#Python implementation of bwtav.pro IDL script by Andrea Biviano

import numpy as np
from scipy.stats import t, chi2

def iter_bwt(x, x_median, x_mad):
    
    u1 = (x - x_median) / (6.0 * x_mad)
    u2 = (x - x_median) / (9.0 * x_mad)
    
    st1 = np.sum((((x - x_median) ** 2) * (1.0 - (u2 ** 2)) ** 4) * (np.abs(u2) < 1.0))
    st2 = np.sum((1.0 - (u2 ** 2)) * (1.0 - (5.0 * u2 ** 2)) * (np.abs(u2) < 1.0))
    st3 = np.sum(((x - x_median) * (1.0 - u1 * u1) ** 2) * (np.abs(u1) < 1.0))
    st4 = np.sum(((1.0 - u1 ** 2) ** 2) * (abs(u1) < 1.0))

    bwt_ave = x_median + st3 / st4
    bwt_std = float(len(x)) * np.sqrt(st1 / (float(len(x)) - 1.0)) / np.abs(st2)
    
    return bwt_ave, bwt_std

def bwt_ave(x):

    x_median = np.median(x)
    x_mad = np.median(np.abs(x - np.median(x)))

    bwt_ave = 0.0
    while np.around(np.abs(bwt_ave - x_median), 8) > 0:
        bwt_ave, bwt_std = iter_bwt(x, x_median, x_mad)
        x_median = bwt_ave
        
    chi2_68_left = chi2.ppf(0.32 / 2.0, len(x) - 1)
    chi2_68_right = chi2.isf(0.32 / 2.0, len(x) - 1)
    t_68 = t.isf(0.32 / 2.0, long(0.7 * (len(x) - 1)))
        
    bwt_ave_low = bwt_ave + t_68 * bwt_std / np.sqrt(len(x))
    bwt_ave_up = bwt_ave - t_68 * bwt_std / np.sqrt(len(x))
    bwt_std_low = (np.sqrt((len(x) - 1) / chi2_68_left) - 1.) * bwt_std
    bwt_std_up = (np.sqrt((len(x) - 1) / chi2_68_right) - 1.) * bwt_std
        
    return (bwt_ave, bwt_ave_low, bwt_ave_up), (bwt_std, bwt_std_low, bwt_std_up)
