## @file cluster_centre.py
#
#  CLUSTER CENTERING FUNCTIONS 
#
#  Functions for determining
#  cluster centre.
#  
#  @author Samuel Farrens
#  @version 1.0
#  @date 2015
#

import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

##
#  Function that finds cluster
#  centre using a Gaussian
#  kernel density estimator.
#
#  @param[in] data: Cluster DataFrame.
#
def kde_centre(data):
    
    kde = gaussian_kde(np.vstack([data.x, data.y]),
                       bw_method = 'silverman')

    x_limit = max(abs(data.x.min()), data.x.max())
    y_limit = max(abs(data.y.min()), data.y.max())
    
    xedges = np.linspace(-x_limit, x_limit, 100)
    yedges = np.linspace(-y_limit, y_limit, 100)
    
    xx, yy = np.meshgrid(xedges, yedges)
    gridpoints = np.array([xx.ravel(), yy.ravel()])

    zz = np.reshape(kde(gridpoints), xx.shape)
    index = np.unravel_index(zz.argmax(), zz.shape)
    
    centre = (xedges[index[1]], yedges[index[0]])
    kde_data = (xedges, yedges, zz)
    
    return centre, kde_data
