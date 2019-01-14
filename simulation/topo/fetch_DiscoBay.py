"""
Fetch 1/3" topo around Discovery Bay
"""

from __future__ import print_function
from pylab import *
import sys
from clawpack.geoclaw import topotools
import matplotlib.pyplot as plt


path = 'puget_sound'  # read from 1/3" Puget Sound DEM
extent = [-122.96, -122.82, 47.97, 48.14]

topo = topotools.read_netcdf(path, extent=extent, coarsen=1, verbose=True)

print('x,shape, y.shape: %s, %s' % (topo.x.shape,topo.y.shape))


fname = 'DiscoveryBay_1_3s_center'
fname_asc = fname + '.asc'
topo.write(fname_asc, topo_type=3, header_style='asc',
           grid_registration='llcenter')

topo.plot(limits=(-40,40))
plt.title(fname_asc)
fname_png = fname + '.png'
plt.savefig(fname_png)

print("Created %s and %s" % (fname_asc,fname_png))
