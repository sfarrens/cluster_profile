## @file cluster_props.py
#
#  CLUSTER PROPERTY FUNCTIONS 
#
#  Functions for determining
#  cluster properties.
#  
#  @author Samuel Farrens
#  @version 1.0
#  @date 2015
#

import numpy as np
import pandas as pd
from functions import astro, cosmo2
from library import const

def print_basic(data):

    print 'Mean:'
    print data.mean(0)
    print ''
    print 'Standard Deviation:'
    print data.std(0)

##
#  Class for storing global
#  cluster properties.
class Global():

    ##
    #  Initialisation method.
    #
    #  @param[in] data: Cluster DataFrame.
    #
    def __init__(self, data):

        self.mem = data
        self.m_centre = (data.ra.median(), data.dec.median(),
                         data.z.median())
        self.get_size()

    ##
    #  Get cluster size in arcminutes.
    #
    #  @param[in] centre: Centre coordinates in RA/Dec.
    #
    def get_size(self, centre = None):

        if centre is None:
            centre = self.m_centre
        
        d_ang = np.mean(astro.ang_sep((self.mem.ra, self.mem.dec),
                                      (centre[0], centre[1])))

        self.size_arcm = d_ang * 60.0
        self.area_arcm = np.pi * self.size_arcm ** 2

        self.size_mpc = np.mean(self.mem.r)
        self.area_mpc = np.pi * self.size_mpc ** 2

    ##
    #  Get cluster size in Mpc.
    #
    #  @param[in] r: Member distances from X/Y centre.
    #
    def get_size_r(self, r):
        
        self.size_mpc = np.mean(r)
        self.area_mpc = np.pi * self.size_mpc ** 2
        
##
#  Function that adds the member
#  positions relative to the cluster
#  centre in Mpc/h.
#
#  @param[in] data: Cluster DataFrame.
#  @param[in] centre: Centre Coordinates.
#  @param[in] H0: Hubble constant.
#  Default (H0 = 100.0).
#
#  @return Updated cluster DataFrame.
#
def xy_centre(data, centre = None,  H0 = 100.0):

    if not centre:
        centre = (data.ra.median(), data.dec.median(),
                  data.z.median())

    da = cosmo2.d_angdi(centre[2], *const.BASE) * \
      cosmo2.d_H(H0)
      
    x = da *astro.deg2rad((centre[0] - data.ra) * \
                           np.cos(astro.deg2rad(data.dec)))
    y = da * astro.deg2rad(data.dec - centre[1])
    r = np.sqrt(x ** 2 + y ** 2)
    
    return data.join(pd.DataFrame({'x' : x, 'y' : y, 'r' : r}))

##
#  Function that adds the distances
#  of the cluster memebers from a
#  given centre in Mpc/h.
#
#  @param[in] data: Cluster DataFrame.
#  @param[in] centre: Centre Coordinates.
#  @param[in] name: Name of new r value.
#
#  @return Updated cluster DataFrame.
#
def new_r(data, centre, name = None):

    r = np.sqrt((data.x - centre[0]) ** 2 +
                (data.y - centre[1]) ** 2)

    if not name:
        name = 'new_'
    
    return data.join(pd.DataFrame({name + 'r' : r}))

##
#  Function assigns the appropriate 
#  values of X and Y to a position
#  in RA in Dec for given a centre.
#
#  @param[in] pos: Position in degrees.
#  @param[in] centre: Centre Coordinates
#  in degrees.
#  @param[in] H0: Hubble constant.
#  Default (H0 = 100.0).
#
#  @return Updated cluster DataFrame.
#
def xy_pos(pos, centre, H0 = 100.0):

    da = cosmo2.d_angdi(centre[2], *const.BASE) * \
      cosmo2.d_H(H0)
      
    x = da *astro.deg2rad((centre[0] - pos[0]) * \
                           np.cos(astro.deg2rad(pos[1])))
    y = da * astro.deg2rad(pos[1] - centre[1])
    
    return x, y
