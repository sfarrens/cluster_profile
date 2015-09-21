Cluster Profile Code
==================

@authors Samuel Farrens, Andrea Biviano

Contents
------------
1. [Introduction](#intro_anchor)
2. [Dependenies](#depend_anchor)
3. [Execution](#exe_anchor)

<a name="intro_anchor"></a>
Introduction
------------
The code cluster.py is written in Python and can fit a projected
density profile (at present NFW or Beta Model) to the members
of a cluster of galaxies.

<a name="depend_anchor"></a>
Dependencies
------------

The code requires the following packages:

* <a href="http://www.numpy.org/" target="_blank">Numpy</a>

* <a href="http://www.scipy.org/" target="_blank">SciPy</a> 

* <a href="http://pandas.pydata.org/" target="_blank">Pandas</a>

* <a href="http://matplotlib.org/" target="_blank">Matplotlib</a> 

<a name="exe_anchor"></a>
Execution
------------

**Input Format**

The expected input is an ASCII with any of the following formats. Note
that the column numbers for each of the properties can be specified
using the option `--cols`.

* `Default Format`:
  1. Galaxy ID
  2. Galaxy Right Ascension
  3. Galaxy Declination
  4. Galaxy Redshift

* `Default Format + Cluster ID`:
  1. Cluster ID
  2. Galaxy ID
  3. Galaxy Right Ascension
  4. Galaxy Declination
  5. Galaxy Redshift

* `Radial Format`:
  1. Galaxy ID
  2. Galaxy Distance from Centre

* `Radial Format + Cluster ID`:
  1. Cluster ID
  2. Galaxy ID
  3. Galaxy Distance from Centre

**Run**

The code can be run as an executable by changing the file permissions
and specifying the path to Python (this is first line of the
cluster.py file and the default is /usr/bin/python) e.g.:

> \>\> chmod +x cluster.py

Otherwise to run the code symply run Python e.g:

> \>\> python cluster.py

Help and a list of arguments are provided with the `--help` option e.g:

> \>\> python cluster.py --help

A discription of all of the code options is provided below.

**Example**

To obtain a plot of the best fit NFW profile to a cluster of size 1.5
Mpc/h where the input file is formatted as the default described above:

> \>\> python cluster.py -i INPUT_FILE -s 1.5 --plot profile

To obtain a plot of the Beta Model fit (beta = 0.5) to a cluster with ID = 27 where
the cluster ID, and galaxy ID and positions (RA, DEC and z) are in
columns 4, 7, 8, 9 and 10 respectively:

> \>\> python cluster.py -i INPUT_FILE -s 1.5 -c 4 7 8 9 10 --plot
> profile --model beta --beta 0.5

**Code Options**

* ` -h [ --help ]`: This option produces the help message with all the
  code options and exits.

* ` -i [ --input_file ]`: This option specifies the input file name.

* ` -r [--radial]`: This option specifies that input file should be
  read in radial mode.

* `-c [--cols]`: This option specifies the column numbers of the
  cluster galaxy member properties. If unused this option defaults to
  the default mode described above.

* `--id`: This option specifies the cluster ID. This option should
  be used if the input file contains more than one cluster. Note that
  the input file must have a column with the unique identifier of each
  cluster.
  
* `--id_col`: This option specifies column number of the cluster ID.
  If unsued it defaults to the first column in the file.

* `--centre`: This option specifies the cluster centre.  The
options permitted are kde (kernel density estimator), median or
manually inputted coordinates. The default option is kde.

* `-s [--size]`: This option specifies the cluster size in Mpc. Only
  member galaxies within this radius will be taken into account.

* `--rs`: This option specifies an intial estimate of the scale radius
  in Mpc. The default is 0.3.
  
*  `--sn`: This option specifies the cluster signal-to-noise
   ratio. This is used to derive a fixed background density.
   
*  `--bg`:  This option specifies a fixed background density in Mpc^-2.
   
*  `--cl`: This option specifies the that the cofindence limits of the
   chi-squared are to be calculated.

*  `--log`: This option specifies that the code output is to be saved to a log file.

*  `--model`: This option specifies the projected density model. The
   options permitted are nfw (Navarro-Frenk-White) or beta (Beta
   Model). The default option is nfw.

*  `--beta`: This option specifies the value of the coefficient for
   the beta model. The default value is 1.0.

*  `--plot`: This option specifies the plots that are to be
   produced. The options permitted are radec (the galaxy member
   positions), xy (the real-space galaxy member positions), kde (the
   results of the kernel density estimator), profile (the cluster
   profile) and all (all of the plots).

*  `--H0`: This option specifies the value of the Hubble parameter in
   km/s/Mpc. The default value is 100.0. Note that the deafult
   corresponds to Mpc/h.
