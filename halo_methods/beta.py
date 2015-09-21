## @file beta.py
#
#  BETA MODEL FUNCTIONS 
#
#  Functions for calculating Beta model parameters.
#
#  REFERENCES:
#
#  @author Samuel Farrens
#  @version 1.0
#  @date 2015
#

import numpy as np
from functools import partial

##
#  Function calculates the beta model 
#  projected surface density.
#
#  @param[in] t: t = R / r_s.
#
def bm_proj_sd(t, alpha):

    return 1.0 / (1.0 + t ** 2) ** alpha
    

##
#  Function calculates the beta model
#  projected mass along a cylinder in
#  units of M(r-2).
#
#  @param[in] t: t = R / r_s.
#
def bm_proj_mass(t, alpha):

    if 1.0 - np.around(alpha, 8) == 0.0:
        mp = np.log(1.0 + t  ** 2)
        
    else:
        mp = (1.0 + t ** 2)  ** (1.0 - alpha) / (1.0 - alpha)

    return mp

##
#  Beta model number density for given 
#  projected radius, scale radius and 
#  background density.
#
#  @param[in] R_proj: Projected radius.
#  @param[in] r_scale: Scale radius.
#  @param[in] bg_density: Background density.
#
def bm_num_density(R_proj, r_scale, bg_density, alpha):

    t_up = max(R_proj) / r_scale
    t_low = min(R_proj) / r_scale

    bm_num = len(R_proj) - np.pi * r_scale ** 2 * (t_up ** 2 - t_low ** 2) * bg_density
    bm_den = np.pi * r_scale ** 2 * (bm_proj_mass(t_up, alpha) - bm_proj_mass(t_low, alpha))

    if bm_num <= 0:
        bm_num = 0.1
    
    return bm_num / bm_den

##
#  Maximum liklihood for projected beta
#  model with background.
#
#  @param[in] r_scale_bg: Scale radius
#  and background density.
#  @param[in] R_proj: Projected radius.
#  @param[in] weights: Optional weights.
#
def bm_proj_maxlik_bg(r_scale_bg, R_proj, alpha, weights = None):
    
    bm_sd = np.array(map(partial(bm_proj_sd, alpha = alpha),
                         R_proj / r_scale_bg[0]))

    bm_nden = bm_num_density(R_proj, r_scale_bg[0], r_scale_bg[1], alpha)
    
    prob = bm_nden * bm_sd + r_scale_bg[1]

    if weights is None:
        return np.sum(-np.log(prob))

    else:
        return np.sum(-np.log(prob) * weights)
