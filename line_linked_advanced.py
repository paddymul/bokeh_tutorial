
from numpy import pi, arange, sin, cos
import numpy as np
import os.path

from bokeh.objects import (Plot, DataRange1d, GridPlot,
        ColumnDataSource, GlyphRenderer, PanTool, ZoomTool)

from bokeh.glyphs import Line
from bokeh import session

x = np.linspace(-2*pi, 2*pi, 1000)
y = sin(x)
z = cos(x)
widths = np.ones_like(x) * 0.02
heights = np.ones_like(x) * 0.2

source = ColumnDataSource(data=dict(x=x,y=y,z=z,widths=widths,
            heights=heights))

xdr = DataRange1d(sources=[source.columns("x")])
xdr2 = DataRange1d(sources=[source.columns("x")])
ydr = DataRange1d(sources=[source.columns("y")])
ydr2 = DataRange1d(sources=[source.columns("y")])

line_glyph = Line(x="x", y="y", line_color="blue")

renderer = GlyphRenderer(data_source = source,  xdata_range = xdr,
        ydata_range = ydr, glyph = line_glyph)
pantool = PanTool(dataranges = [xdr, ydr], dimensions=["width","height"])
zoomtool = ZoomTool(dataranges=[xdr,ydr], dimensions=("width","height"))

plot = Plot(x_range=xdr, y_range=ydr, data_sources=[source], 
        border=50)
plot.tools = [pantool, zoomtool]
plot.renderers.append(renderer)

#notice that these two have a differen y data range
renderer2 = GlyphRenderer(data_source = source, xdata_range = xdr,
        ydata_range = ydr2, glyph = line_glyph)

plot2 = Plot(x_range=xdr, y_range=ydr2, data_sources=[source], 
        border=50)

plot2.renderers.append(renderer2)

#notice that these two have a differen y data range
renderer3 = GlyphRenderer(data_source = source, xdata_range = xdr2,
        ydata_range = ydr, glyph = line_glyph)

plot3 = Plot(x_range=xdr2, y_range=ydr, data_sources=[source], 
        border=50)

plot3.renderers.append(renderer3)

#this is a dummy plot with no renderers
plot4 = Plot(x_range=xdr2, y_range=ydr, data_sources=[source], 
        border=50)


sess = session.HTMLFileSession("line_linked_advanced.html")
sess.add(plot, renderer, source, xdr, ydr, pantool, zoomtool)

sess.add(plot2, renderer2, ydr2, xdr2, renderer3, plot3, plot4)
grid = GridPlot(children=[[plot, plot2], [plot3, plot4 ]], name="linked_advanced")

sess.add(grid)
sess.plotcontext.children.append(grid)


sess.save(js="relative", css="relative", rootdir=os.path.abspath("."))
print "Wrote line_linked_advanced.html"

try:
    import webbrowser
    webbrowser.open("file://" + os.path.abspath("line_linked_advanced.html"))
except:
    pass

