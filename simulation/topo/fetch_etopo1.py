
from pylab import *
from clawpack.geoclaw import topotools

extent = [-137,-122,38,54]
topo = topotools.read_netcdf('etopo1', extent=extent, verbose=True)

fname = 'etopo1_-137_-122_38_54_1min_nc.asc'
topo.write(fname, topo_type=3, Z_format='%.0f')
print('Created %s' % fname)


    
