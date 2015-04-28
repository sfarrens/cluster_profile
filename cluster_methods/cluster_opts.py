## @file cluster_opts.py
#
#  CLUSTER OPTION FUNCTIONS 
#
#  Functions for retreiving
#  code arguments.
#  
#  @author Samuel Farrens
#  @version 1.0
#  @date 2015
#

import argparse

##
#  Function to read in code arguments.
#
#  @return List of arguments.
#
def get_opts():

    col_help = ('Set column numbers for member properties: ID, RA, DEC, Z' + \
                '[Default 3 4 5 6]')

    plot_help = ('Produce plots. Available options:' +
                 '\n radec -- plot RA/Dec distribution of cluster members' +
                 '\n xy -- plopt X/Y distribution of clusyter members' +
                 '\n kde -- plot centre found by Kernel Density Estimation' +
                 '\n profile -- plot density profile of cluster members' +
                 '\n all -- plot everything.')

    parser = argparse.ArgumentParser('CLUSTER OPTIONS:',
                                     formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument('-i', '--input_file', dest = 'input_file',
                        help = 'Input file name.')

    parser.add_argument('-r', '--radial', action = 'store_true',
                        dest = 'radial', help = 'Input file coordinates are radial.')
    
    parser.add_argument('-c', '--cols', dest = 'cols', default = range(4, 8),
                        nargs = '+', type = int, help = col_help)

    parser.add_argument('--id', dest = 'cluster_id', help = 'Cluster ID.')

    parser.add_argument('--centre', dest = 'centre', default = ['kde'], nargs = '+',
                        help = 'Cluster centre. Default (centre = \'kde\')')

    parser.add_argument('-s', '--size', dest = 'size', default = '1.5', type = float,
                        help = 'Cluster radius in Mpc.')

    parser.add_argument('--rs', dest = 'rs', default = 0.3, type = float,
                        help = 'Initial estimate of scale radius. Default (rs = 0.3) [Mpc]')

    parser.add_argument('--sn', dest = 'sn', type = float,
                        help = 'Cluster signa-to-noise ratio.')

    parser.add_argument('--bg', dest = 'bg', type = float,
                        help = 'Fixed number of background objects per Mpc.')

    parser.add_argument('--cl', action = 'store_true', dest = 'confidence',
                        help = 'Show results with confidence limits.')
    
    parser.add_argument('--plot', default = ['profile'], nargs = '+', 
                        dest = 'plot', help = plot_help)

    parser.add_argument('--H0', dest = 'H0', default = 100.0, type = float,
                        help = 'Hubble constant. Default (H0 = 100.0) [km/s/Mpc]')
    
    opts = check_opts(parser)
    
    return opts

##
#  Function to read in code arguments.
#
#  @param[in] parser: List of arguments.
#
def check_opts(parser):

    opts = parser.parse_args()
    
    if not opts.input_file:
        parser.error('argument --input_file: file name not provided.')

    if len(opts.centre) > 2:
        parser.error('argument --centre: takes a maximum of two values.')        
        
    if 'all' in opts.plot:
        opts.plot.extend(['radec', 'xy', 'kde', 'profile'])

    return opts
