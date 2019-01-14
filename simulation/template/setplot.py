
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

from __future__ import print_function

import pylab
import glob, os
from numpy import loadtxt
from matplotlib import image


# --------------------------
def setplot(plotdata=None):
# --------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of clawpack.visclaw.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 


    from clawpack.visclaw import colormaps, geoplot

    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()

    plotdata.clearfigures()  # clear any old figures,axes,items dat
    plotdata.format = "binary"

    try:
        tsudata = open(plotdata.outdir+'/geoclaw.data').readlines()
        for line in tsudata:
            if 'sea_level' in line:
                sea_level = float(line.split()[0])
                print("sea_level = ",sea_level)
    except:
        print("Could not read sea_level, setting to 0.")
        sea_level = 0.

    clim_ocean = 1.0
    clim_coast = 1.0

    cmax_ocean = clim_ocean + sea_level
    cmin_ocean = -clim_ocean + sea_level
    cmax_coast = clim_coast + sea_level
    cmin_coast = -clim_coast + sea_level

    my_land_colors = colormaps.make_colormap({0:[.8,1,.8], 1:[.4,0.8,.4]})
    #my_land_colors = colormaps.make_colormap({0:[.08,.4,.08], 1:[.08,.4,.08]})
    #my_land_colors = colormaps.make_colormap({0:[.2,.7,.2], 1:[.2,.7,.2]})
    #my_land_colors = colormaps.make_colormap({0:[.4,1,.4], 0.98:[.2,.7,.2], 1:[.9,.8,.2]})

    #my_land_colors = colormaps.make_colormap({0:[0.8,1.0,0.5], 1:[0.4,0.8,0.4]})

    # To plot gauge locations on pcolor or contour plot, use this as
    # an afteraxis function:

    def addgauges(current_data):
        from clawpack.visclaw import gaugetools
        gaugetools.plot_gauge_locations(current_data.plotdata, \
             # gaugenos=[46404,46407,46419], format_string='ko', add_labels=True)
             format_string='ko', add_labels=True)

    def timeformat(t):
        from numpy import mod
        hours = int(t/3600.)
        tmin = mod(t,3600.)
        min = int(tmin/60.)
        sec = int(mod(tmin,60.))
        timestr = '%s:%s:%s' % (hours,str(min).zfill(2),str(sec).zfill(2))
        return timestr
        
    def title_hours(current_data):
        from pylab import title
        t = current_data.t
        timestr = timeformat(t)
        title('%s after initiation' % timestr)

    def aframe(current_data):
        from pylab import figure, savefig

        if 1:
            tminutes = int(current_data.t / 60.)

            figure(0)
            fname = 'Pacific%s.png' % tminutes
            savefig(fname)
            print("Saved ",fname)
    
            figure(11)
            fname = 'GraysHarbor%s.png' % tminutes
            savefig(fname)
            print("Saved ",fname)

            figure(12)
            fname = 'Westport%s.png' % tminutes
            savefig(fname)
            print("Saved ",fname)
    
            figure(13)
            fname = 'Ocosta%s.png' % tminutes
            savefig(fname)
            print("Saved ",fname)
    
    #plotdata.afterframe = aframe

    #-----------------------------------------
    # Figure for big area
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Pacific', figno=0)
    plotfigure.kwargs = {'figsize': (5,6)}
    #plotfigure.show = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    #plotaxes.cmd = 'subplot(121)'
    plotaxes.title = 'Pacific'
    plotaxes.scaled = False
    # modified for debug:
    plotaxes.xlimits = [-132,-122]
    plotaxes.ylimits = [40,50]
    #plotaxes.xlimits = [231.5,236.5] 
    #plotaxes.ylimits = [45,49]

    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi, savefig
        title_hours(current_data)
        ticklabel_format(format='plain',useOffset=False)
        xticks(rotation=20)
        a = gca()
        a.set_aspect(1./cos(46.86*pi/180.))
        addgauges(current_data)
    plotaxes.afteraxes = aa

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.surface_or_depth
    my_cmap = colormaps.make_colormap({-1.0: [0.0,0.0,1.0], \
                                     -0.5: [0.5,0.5,1.0], \
                                      0.0: [1.0,1.0,1.0], \
                                      0.5: [1.0,0.5,0.5], \
                                      1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = cmin_ocean
    plotitem.imshow_cmax = cmax_ocean
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0]

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    #plotitem.show = False
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = my_land_colors  #geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0]

    # Add contour lines for shoreline
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    #plotitem.show = False
    plotitem.plot_var = geoplot.topo
    from numpy import arange, linspace
    plotitem.contour_levels = [0.]
    plotitem.amr_contour_colors = ['g']  # color on each level
    plotitem.kwargs = {'linestyles':'solid', 'linewidths':0.5}
    plotitem.amr_contour_show = [0,0,1,0]  # show contours only on one level
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0

 

    #-----------------------------------------
    # Figure for zoom
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='WA', figno=1)
    plotfigure.kwargs = {'figsize': (5,6)}
    #plotfigure.show = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    #plotaxes.cmd = 'subplot(121)'
    plotaxes.title = 'Pacific'
    plotaxes.scaled = False
    # modified for debug:
    #plotaxes.xlimits = [-126,-122]
    #plotaxes.ylimits = [46,50]
    plotaxes.xlimits = [-125.3,-122]
    plotaxes.ylimits = [46,48.8]

    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi, savefig
        title_hours(current_data)
        ticklabel_format(format='plain',useOffset=False)
        xticks(rotation=20)
        a = gca()
        a.set_aspect(1./cos(46.86*pi/180.))
        addgauges(current_data)
    plotaxes.afteraxes = aa

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.surface_or_depth
    my_cmap = colormaps.make_colormap({-1.0: [0.0,0.0,1.0], \
                                     -0.5: [0.5,0.5,1.0], \
                                      0.0: [1.0,1.0,1.0], \
                                      0.5: [1.0,0.5,0.5], \
                                      1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = cmin_ocean
    plotitem.imshow_cmax = cmax_ocean
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0]

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    #plotitem.show = False
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = my_land_colors  #geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0]

    # Add contour lines for shoreline
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    #plotitem.show = False
    plotitem.plot_var = geoplot.topo
    from numpy import arange, linspace
    plotitem.contour_levels = [0.]
    plotitem.amr_contour_colors = ['g']  # color on each level
    plotitem.kwargs = {'linestyles':'solid', 'linewidths':0.5}
    plotitem.amr_contour_show = [0,0,0,1,0,0]  # only on level 4
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0


 
    #-----------------------------------------
    # Figure for zoom2
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name="Sequim / Discovery Bay", figno=11)
    #plotfigure.show = False
    plotfigure.kwargs = {'figsize': (9,5)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    #plotaxes.cmd = 'subplot(122)'
    plotaxes.title = "Sequim and Discovery Bays"
    plotaxes.scaled = False

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.surface_or_depth
    my_cmap = colormaps.make_colormap({-1.0: [0.0,0.0,1.0], \
                                      -0.5: [0.5,0.5,1.0], \
                                       0.0: [1.0,1.0,1.0], \
                                       0.5: [1.0,0.5,0.5], \
                                       1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap
    plotitem.imshow_cmin = cmin_coast
    plotitem.imshow_cmax = cmax_coast
    plotitem.add_colorbar = True
    # plotitem.colorbar_shrink = 0.4
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0]

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.land
    land_cmap = colormaps.make_colormap({0: [0.08,.4,0.08], \
                                       1.0: [0.08,.4,0.08]})
    plotitem.imshow_cmap = land_cmap  #geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0]
    plotaxes.xlimits = [-123.12, -122.82]
    plotaxes.ylimits = [47.965,   48.15]
    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi, savefig
        addgauges(current_data)
        title_hours(current_data)
        ticklabel_format(format='plain',useOffset=False)
        xticks(rotation=20)
        a = gca()
        a.set_aspect(1./cos(46.86*pi/180.))
    plotaxes.afteraxes = aa

    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi, imshow, savefig
        from clawpack.visclaw.plottools import plotbox
        addgauges(current_data)
        title_hours(current_data)
        ticklabel_format(format='plain',useOffset=False)
        xticks(rotation=20)
        a = gca()
        a.set_aspect(1./cos(46.86*pi/180.))
        if current_data.t > 40*60.:
            extent = (235.8756, 235.9116, 46.854, 46.8756)
            plotbox(extent)
    plotaxes.afteraxes = aa

    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = [0.]
    plotitem.amr_contour_colors = ['g']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':1}
    plotitem.amr_contour_show = [0,0,0,0,1,0]
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0

 

    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------

    def save_gauge(current_data):
        from pylab import plot, legend, xticks, floor,\
            yticks,xlabel,savefig,xlim,ylim,xlabel,ylabel
        t = current_data.t
        gaugeno = current_data.gaugeno
        xticks(linspace(0,1,7),[str(i) for i in range(0,70,10)])
        xlabel('time (minutes) after quake',fontsize=15)
        ylabel('meters',fontsize=15)
        ylim(-1,10)
        fname = "Gauge%s.png" % gaugeno
        savefig(fname)
        print("Saved ",fname)

    def fix_gauge(current_data):
        from pylab import plot, legend, xticks, floor, yticks,\
            xlabel,savefig,xlim,where,nan,ones
        t = current_data.t
        gaugeno = current_data.gaugeno
        q = current_data.q

        h = q[0,:]
        h0 = q[0,0] * ones(h.shape)
        level = current_data.gaugesoln.level
        #B = current_data.gaugesoln.aux[0,:]
        dh_refine = 0.
        for j in range(1,len(h0)):
            if level[j] != level[j-1]:
                dh_refine = dh_refine + h[j] - h[j-1]  #B[j-1]-B[j] 
            h0[j] = h0[j] + dh_refine

        ddepth = q[0,:] - h0[:]
        plot(t, ddepth, 'b-')

        n = int(floor(t.max()/1800.) + 2)
        xticks([1800*i for i in range(n)],[str(i/2.) for i in range(n)],\
          fontsize=15)
        yticks(fontsize=15)
        xlabel("Hours", fontsize=15)
        #save_gauge(current_data)

    plotfigure = plotdata.new_plotfigure(name='depth plots', figno=301, \
                    type='each_gauge')
    #plotfigure.clf_each_gauge = False
    plotfigure.kwargs = {'figsize':(12,4)}


    # Set up for axes in this figure:
    if 0:
        plotaxes = plotfigure.new_plotaxes()
        #plotaxes.ylimits = [-1,10]
        plotaxes.title = 'Surface elevation (red) and change in depth (blue)'

        # plot eta as red curve:
        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        plotitem.plot_var = 3
        plotitem.plotstyle = 'r-'
        plotaxes.afteraxes = fix_gauge

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Depth'
    # plot depth as red curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 0
    plotitem.plotstyle = 'r-'
    #plotaxes.afteraxes = fix_gauge

    plotfigure = plotdata.new_plotfigure(name='surface elevation plots', figno=302, \
                    type='each_gauge')
    #plotfigure.clf_each_gauge = False
    plotfigure.kwargs = {'figsize':(12,4)}

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Surface elevation'
    # plot depth as red curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'b-'

    # to compare with gauges from a different run:
    # plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    # plotitem.show = False
    # plotitem.outdir = '_output_3levels'
    # plotitem.plot_var = 0
    # plotitem.plotstyle = 'b-'

    #-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via clawpack.visclaw.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True

    return plotdata

    
