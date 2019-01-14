"""
Create fgmax_grid.txt input files 

"""

from __future__ import print_function

from clawpack.geoclaw import fgmax_tools

# this is called from setrun.py
def make_fgmax_grid_1(min_level_check):
    dx_fine = 2/3. * 1./3600.  # grid resolution desired

    fg = fgmax_tools.FGmaxGrid()
    fg.point_style = 2       # will specify a 2d grid of points
    fg.x1 = -122.9 + dx_fine/2.
    fg.x2 = -122.83 - dx_fine/2.
    fg.y1 = 47.98 + dx_fine/2.
    fg.y2 = 48.02 - dx_fine/2.
    fg.dx = dx_fine
    fg.tstart_max =  1.5*3600.     # when to start monitoring max values
    fg.tend_max = 1.e10       # when to stop monitoring max values
    fg.dt_check = 10.         # target time (sec) increment between updating 
                               # max values
    fg.min_level_check = min_level_check    # which levels to monitor max on
    fg.arrival_tol = 1.e-2    # tolerance for flagging arrival

    fg.input_file_name = 'fgmax_grid_1.txt'
    fg.write_input_data()

# if __name__=="__main__":
#     make_fgmax_grid_1(5)
#     print('make_fgmax_grid_1 is called from setrun.py')
