## @file cluster_plot.py
#
#  CLUSTER PLOTTING FUNCTIONS 
#
#  Functions for plotting
#  cluster properties.
#  
#  @author Samuel Farrens
#  @version 1.0
#  @date 2015
#

import numpy as np
import matplotlib.pyplot as plt

##
#  Function that plots ra and dec
#  distribution of cluster members.
#
#  @param[in] opts: List of arguments.
#  @param[in] data: Cluster DataFrame.
#
def plot_radec(opts, data):

    plt.figure()

    plt.xlim(data.ra.min(), data.ra.max())
    plt.ylim(data.dec.min(), data.dec.max())

    plt.scatter(data.ra, data.dec,
                marker = '+', color = 'k',
                label = 'Members')
    
    plt.plot(np.ones(2) * data.ra.median(), (plt.ylim()),
              '--', color = 'gray',
              label = 'Median Centre')
    plt.plot((plt.xlim()), np.ones(2) * data.dec.median(),
              '--', color = 'gray')

    plt.xlabel('RA')
    plt.ylabel('Dec')
    plt.title('Cluster Member Positions')
    plt.legend(scatterpoints = 1, fontsize = 10)

    output_file = opts.input_file + '.radec.pdf'
    plt.savefig(output_file)
    print ' RA/Dec plot saved to:', output_file  

    plt.close()

##
#  Function that plots cluster members
#  with respect to the cluster median
#  centre.
#
#  @param[in] opts: List of arguments.
#  @param[in] data: Cluster DataFrame.
#  @param[in] centre: Centre coordinates.
#
def plot_xy(opts, data, centre = None):

    plt.figure()

    x_limit = max(abs(data.x.min()), data.x.max())
    y_limit = max(abs(data.y.min()), data.y.max())
    
    plt.xlim(-x_limit, x_limit)
    plt.ylim(-y_limit, y_limit)

    plt.scatter(data.x, data.y,
                marker = '+', color = 'k',
                label = 'Members')
    
    plt.plot(np.zeros(2), (plt.ylim()), '--',
             color = 'gray', label = 'Median Centre')
    plt.plot((plt.xlim()), np.zeros(2), '--',
             color = 'gray')

    if centre is not None:
        plt.plot(np.ones(2) * centre[0], (plt.ylim()), 'r:',
                label = 'New Centre')
        plt.plot((plt.xlim()), np.ones(2) * centre[1], 'r:')

    if opts.H0 == 100.0:
        plt.xlabel(r'X [Mpc h$^{-1}$]')
        plt.ylabel(r'Y [Mpc h$^{-1}$]')
    else:
        plt.xlabel('X [Mpc]')
        plt.ylabel('Y [Mpc]')
        
    plt.title('Cluster Member Positions')
    plt.legend(scatterpoints = 1, fontsize = 10)

    output_file = opts.input_file + '.xy.pdf'
    plt.savefig(output_file)
    print ' X/Y plot saved to:', output_file  

    plt.close()

##
#  Function that plots kde contours.
#
#  @param[in] opts: List of arguments.
#  @param[in] kde_data: KDE results.
#  @param[in] centre: KDE centre coordinates.
#
def plot_kde(opts, kde_data, centre = None):

    plt.figure()

    plt.contourf(kde_data[0], kde_data[1],
                 kde_data[2], 30)

    if centre:
        plt.plot(np.ones(2) * centre[0], (plt.ylim()), 'w:',
                label = 'KDE Centre')
        plt.plot((plt.xlim()), np.ones(2) * centre[1], 'w:')
    
    if opts.H0 == 100.0:
        plt.xlabel(r'X [Mpc h$^{-1}$]')
        plt.ylabel(r'Y [Mpc h$^{-1}$]')
    else:
        plt.xlabel('X [Mpc]')
        plt.ylabel('Y [Mpc]')
        
    plt.legend()
    plt.colorbar()

    output_file = opts.input_file + '.kde.pdf'
    plt.savefig(output_file)
    print ' KDE plot saved to:', output_file  
    
    plt.close()

##
#  Function that plots cluster profile.
#
#  @param[in] opts: List of arguments.
#  @param[in] p_data: Profile data.
#
def plot_profile(opts, p_data):
    
    plt.figure()
    
    plt.plot(p_data[1][0], p_data[1][1] ,'bx')
    plt.errorbar(p_data[1][0], p_data[1][1], yerr = p_data[1][2],
                 linestyle = 'None')

    plt.plot(*(p_data[2] + ['r-']))

    plt.xlim(np.min(p_data[1][0]) / 3., 1.5 * np.max(p_data[1][0]))
    plt.ylim(np.min(p_data[1][1]) / 2., np.max(p_data[1][1]) * 2.)
    plt.xscale('log')
    plt.yscale('log')

    if opts.H0 == 100.0:
        plt.xlabel(r'R [Mpc h$^{-1}$]')
        plt.ylabel(r'Number Density [Mpc$^{-2}$ h$^2$]')
        rs = r'$r_s =$ %.3f Mpc h$^{-1}$'
        rho = r'$\rho_{BG} =$ %.3f Mpc$^{-2}$ h$^2$'
    else:
        plt.xlabel('R [Mpc]')
        plt.ylabel(r'Number Density [Mpc$^{-2}$]')
        rs = r'$r_s =$ %.3f Mpc'
        rho = r'$\rho_{BG} =$ %.3f Mpc$^{-2}$'
    
    plt.text(0.25 * plt.xlim()[1], 0.8 * plt.ylim()[1],
             rs % p_data[0][0])
    plt.text(0.25 * plt.xlim()[1], 0.7 * plt.ylim()[1],
             rho % p_data[0][1])
    plt.text(0.25 * plt.xlim()[1], 0.6 * plt.ylim()[1],
             r'$\chi^2 =$ %.3f' % p_data[3][0])
        
    plt.title('Projected NFW Best-Fit')

    output_file = opts.input_file + '.profile.pdf'
    plt.savefig(output_file)
    print ' Profile plot saved to:', output_file  
    
    plt.close()
