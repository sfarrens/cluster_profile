## @file cluster_profile.py
#
#  CLUSTER PROFILE FUNCTIONS 
#
#  Functions for analysing cluster profile.
#
#  @author Samuel Farrens
#  @version 1.0
#  @date 2015
#

import warnings
import numpy as np
from functools import partial
from scipy.stats import chi2, chisquare, ks_2samp, anderson_ksamp
from scipy.optimize import minimize, brute
from functions.stats import chi2_gof
from halo_methods.nfw import *
from halo_methods.beta import *
from biviano_py.biweight import bwt_ave

warnings.simplefilter('ignore')

##
#  Get number density of points along the 
#  projected radius of the cluster.
#
#  Adapated from profmaxliknfwp.pro IDL script by
#  A. Biviano.
#
#  @param[in] R_proj: Projected radius.
#  @param[in] num_points: Number of points
#  @param[in] weights: Optional weights.
#
#  @return Projected radius, projected density
#  and errors.
#
def get_points(R_proj, num_points, weights):
        
    radial_pt = []
    density_pt = []
    density_pt_err = []

    for i in range(len(R_proj) / num_points - 1): 
        r_biweight = bwt_ave(R_proj[num_points * i:num_points * \
                                    (i + 1)])
        radial_pt.append(r_biweight[0][0])
        if i == 0:
            r1 = 0.
        if i > 0:
            r1 = r2
        r2 = R_proj[num_points * (i + 1)]
        weight = np.sum(weights[num_points * i:num_points * (i + 1)])
        density_pt.append(weight / (np.pi * (r2 ** 2 - r1 ** 2)))
        density_pt_err.append(np.sqrt(num_points) / num_points * weight / \
                   (np.pi * (r2 ** 2 - r1 ** 2)))

    return np.array(radial_pt), np.array(density_pt), np.array(density_pt_err)

##
#  Get confidence limits for best-fit scale 
#  radius.
#
#  @param[in] r_scale: Best scale radius.
#  @param[in] bg_density: Best background density.
#  @param[in] R_proj: Projected radius.
#  @param[in] grid: Number of grid points.
#  @param[in] dof: Degree of freedom.
#
#  @return Lower and upper confidence limits.
#
def confidence(opts, r_scale, bg_density, R_proj, grid, dof):
    
    def get_range(value, grid):
        a = tuple(10.0 ** (np.log10(value) + np.array([-grid / 2, grid / 2]) * 1.4 / grid))
        b = (np.max(a) - np.min(a)) / grid * 2.0
        return a + (b,)

    ranges = (get_range(r_scale, grid), get_range(bg_density, grid))

    if opts.model == 'beta':
        res = brute(bm_proj_maxlik_bg, ranges, args = (R_proj, opts.beta, ), full_output = True)

    else:
        res = brute(nfw_proj_maxlik_bg, ranges, args = (R_proj, ), full_output = True)

    x, y = np.array(res[2]), np.array(res[3]).flatten()
    x = x.reshape(x.shape[0], x.shape[1] * x.shape[2]).T
    
    index = (2.0 * (y - np.min(y)) <= chi2.ppf(0.68, dof))
    limits = x[index, 0]

    return np.min(limits), np.max(limits)

##
#  Minimisation of profile with background density.
#
#  Adapated from profmaxliknfwp.pro and 
#  profmaxlikbetamodel.pro IDL scripts by A. Biviano.
#
#  @param[in] opts: List of code options.
#  @param[in] R_proj: Projected radius.
#  @param[in] r_scale_ini: Initial scale radius.
#  @param[in] grid: Number of grid points.
#  @param[in] bg_density_ini: Initial background density.
#  @param[in] fit_bg: Option to fit background.
#  @param[in] fpb: Factor?
#  @param[in] weights: Optional weights.
#
#  @return Best-fit scale radius and background density,
#  projected density points with errors, fit to data and
#  chi-squared test results.
#
def best_fit(opts, R_proj, r_scale_ini, grid, bg_density_ini = 0.0, fit_bg = True,
                   fpb = 1, weights = None):

    if fit_bg:
        print ' Fitting the scale radius and the background for', len(R_proj), 'members.'
    else:
        print ' Fitting the scale radius only for', len(R_proj), 'members.'
    print ' Initial estimates of parameters: ', r_scale_ini, bg_density_ini

    if weights is None:
        weights = np.ones(len(R_proj))

    # Sort data
    R_proj = R_proj[np.argsort(R_proj)]
    weights = weights[np.argsort(R_proj)]

    # Get number density for various points along R_proj 
    num_points = fpb * int(np.sqrt(len(R_proj)))
    if num_points < 5:
        print ' Only ', len(R_proj), 'data - not enough for the profiles'
    rd, dp, edp = get_points(R_proj, num_points, weights)

    # Find best values for scale radius and background density
    if not fit_bg:
        bg_bounds = (bg_density_ini, bg_density_ini)
    else:
        bg_bounds = (0.001, None)

    # Get fit to profile      
    x_fit = np.arange(0.001, 5.0, 0.005)

    if opts.model == 'beta':

        print ' Using beta model. [Beta = ' + str(opts.beta) + ']'
        
        r_scale_best, bg_density_best = minimize(bm_proj_maxlik_bg, [r_scale_ini, bg_density_ini],
                                                 args = (R_proj, opts.beta, ), method = 'SLSQP',
                                                 options={'disp': False},
                                                 bounds = ((0.001, None), bg_bounds)).x
    
        y_fit = bm_num_density(R_proj, r_scale_best, bg_density_best, opts.beta) * \
          np.array(map(partial(bm_proj_sd, alpha = opts.beta), (x_fit / r_scale_best))) + \
          bg_density_best * np.sum(weights) / len(R_proj)

    else:

        print ' Using NFW profile.'
          
        r_scale_best, bg_density_best = minimize(nfw_proj_maxlik_bg, [r_scale_ini, bg_density_ini],
                                                 args = (R_proj, ), method = 'SLSQP',
                                                 options={'disp': False},
                                                 bounds = ((0.001, None), bg_bounds)).x

        y_fit = nfw_num_density(R_proj, r_scale_best, bg_density_best) * \
          np.array(map(nfw_proj_sd, (x_fit / r_scale_best))) + \
          bg_density_best * np.sum(weights) / len(R_proj)

    # Evaluate chi^2
    if fit_bg:
        npfree = 2
    else:
        npfree = 1
        
    chi2_param = chi2_gof(np.interp(rd, x_fit, y_fit), dp, edp, npfree)

    # Evaluate K-S test
    ks_param = ks_2samp(np.interp(rd, x_fit, y_fit), dp)

    # Evaluate A-D test
    ad_param = anderson_ksamp([np.interp(rd, x_fit, y_fit), dp])

    if opts.confidence:
        # Evaluate confidence intervals for r_s
        cf_limits = confidence(opts, r_scale_best, bg_density_best, R_proj, grid, npfree)

    # Print results 
    print ''
    print ' Best-fit r_s:', r_scale_best
    if opts.confidence:
        print ' 1-sigma interval: ', cf_limits[0], cf_limits[1]
    print ' Best-fit background density:', bg_density_best, 'gals/Mpc^2'
    print ''
    print ' Chi^2 of the fit is', chi2_param[0], 'for', len(edp) - npfree, 'd.o.f.'
    print ' Probability of the fit is', chi2_param[1], '[rejected if > 0.99]'
    print ''
    print ' KS test resuls:', ks_param[0], ks_param[1]
    print ' AD test results:', ad_param[0], ad_param[2]

    return [r_scale_best, bg_density_best], [rd, dp, edp], [x_fit, y_fit], chi2_param
