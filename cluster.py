#! /Users/Rowen/Documents/Library/anaconda/bin/python

## @file cluster.py
#
#  CLUSTER
#
#  Script for analysing cluster
#  properties.
#  
#  @author Samuel Farrens
#  @version 1.0
#  @date 2015
#

import numpy as np
from cluster_methods import *
from functions.interface import h_line

##
#  Code Main.
def main():

    # Get code arguments
    opts = cluster_opts.get_opts()

    # Read input file
    h_line()
    data = cluster_io.read_ascii(opts)

    if not opts.radial:
        
        # Add X Y data
        data = cluster_props.xy_centre(data, H0 = opts.H0)

        # Get global properties
        cluster = cluster_props.Global(data)
    
        # Assign centre
        if len(opts.centre) == 1:
            if opts.centre[0] == 'kde':
                centre, kde_data = cluster_centre.kde_centre(data)
            elif opts.centre[0] == 'median':
                centre = np.zeros(2)
        else:
            pos = np.array(opts.centre, dtype = 'float')
            centre = cluster_props.xy_pos(pos, cluster.m_centre)
        
        # Add updated R
        data = cluster_props.new_r(data, centre)

    # Get index of mebers within cluster radius
    if not opts.size:
        cluster.get_size_r(data.new_r)
        opts.size = cluster.size_mpc
    index = data.new_r <= float(opts.size)
    print '', sum(index), 'members within R =', opts.size, 'Mpc.'

    # Assign background from S/N
    if opts.sn:
        opts.bg = (sum(index) / opts.sn) ** 2 / cluster.area_mpc

    # Get cluster profile data
    h_line()
    
    if opts.bg:
        bg_fit = False
    else:
        opts.bg = 10.0
        bg_fit = True
        
    p_data = cluster_profile.best_fit(opts, np.array(data.new_r.loc[index]), opts.rs,
                                      100, opts.bg, bg_fit)

    h_line()
    
    if opts.log:
        cluster_io.write_p_data(opts, p_data)

    # Make plots
    if 'zhist' in opts.plot:
        cluster_plot.plot_zhist(opts, data)
    if 'radec' in opts.plot:
        cluster_plot.plot_radec(opts, data)
    if 'xy' in opts.plot:
        cluster_plot.plot_xy(opts, data, centre)
    if 'kde' in opts.plot and opts.centre[0] == 'kde':
        cluster_plot.plot_kde(opts, kde_data, centre)
    if 'profile' in opts.plot:
        cluster_plot.plot_profile(opts, p_data)
    h_line()
        
if __name__ == "__main__":
    main()
