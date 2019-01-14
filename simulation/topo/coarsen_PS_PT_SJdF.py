"""
Coarsen PS and PT 1/3 arcsecond DEMs to 2 seconds.
"""

from __future__ import print_function
from pylab import *
import sys
from clawpack.geoclaw import topotools
import matplotlib.pyplot as plt


cases = [('puget_sound', 'PS'),
         ('port_townsend', 'PT'),
         ('strait_of_juan_de_fuca', 'SJdF')]

#cases = [('strait_of_juan_de_fuca', 'SJdF')]

for path,floc in cases:

    print('Processing %s ' % path)

    topo = topotools.read_netcdf(path, coarsen=6, verbose=True)

    print('x,shape, y.shape: %s, %s' % (topo.x.shape,topo.y.shape))


    fname_asc = '%s_2sec_center.asc' % floc
    topo.write(fname_asc, topo_type=3, header_style='asc',
               grid_registration='llcenter')

    topo.plot(limits=(-40,40))
    plt.title(fname_asc)
    fname_png = '%s_2sec_center.png' % floc
    plt.savefig(fname_png)

    print("Created %s and %s" % (fname_asc,fname_png))
