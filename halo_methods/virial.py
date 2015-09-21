## @file virial.py
#
#  VIRIAL METHODS
#
#  Functions related to the
#  virial theorem.
#  
#  @author Samuel Farrens
#  @version 1.0
#  @date 2015
#

import sys
sys.path.append("/Users/Rowen/Documents/Codes/Python")

import numpy as np
from functions.cosmo2 import rho_crit
from library import const

##
#  This function calculates R_200 from M_200
#  for a given cosmology.
#
#  @param[in] lm200: log_10(M_200).
#  @param[in] H0: Hubble constant [km/s/Mpc].
#  @param[in] z: Redshift.
#  @param[in] Omega_M: Matter density parameter.
#  @param[in] Omega_L: Dark energy density parameter.
#
#  @return R_200 in Mpc
# 
def r200(lm200, H0, z, Omega_M, Omega_L):

    R_C = rho_crit(H0, z, Omega_M, Omega_L)
    
    R  = (3.0 * 10.0 ** lm200 * const.M_SUN) / \
      (4.0 * np.pi * 200.0 * R_C)

    return (R ** (1.0 / 3.0)) / (const.MPC * 1000.0)
