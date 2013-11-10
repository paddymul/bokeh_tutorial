
from numpy import pi, arange, sin, cos
import numpy as np
import os.path

from bokeh.objects import (Plot, DataRange1d, 
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
ydr = DataRange1d(sources=[source.columns("y")])

line_glyph = Line(x="x", y="y", line_color="blue")

renderer = GlyphRenderer(data_source = source,  xdata_range = xdr,
        ydata_range = ydr, glyph = line_glyph)

plot = Plot(x_range=xdr, y_range=ydr, data_sources=[source], 
        border=50)

plot.renderers.append(renderer)

renderer2 = GlyphRenderer(data_source = source, xdata_range = xdr,
        ydata_range = ydr, glyph = line_glyph)

plot2 = Plot(x_range=xdr, y_range=ydr, data_sources=[source], 
        border=50)
pantool2 = PanTool(dataranges = [xdr, ydr], dimensions=["width","height"])
zoomtool2 = ZoomTool(dataranges=[xdr,ydr], dimensions=("width","height"))

plot2.renderers.append(renderer2)
plot2.tools = [pantool2, zoomtool2]

sess = session.HTMLFileSession("line_linked.html")
sess.add(plot, renderer, source, xdr, ydr)
sess.plotcontext.children.append(plot)

sess.add(plot2, renderer2, pantool2, zoomtool2)
sess.plotcontext.children.append(plot2)

sess.save(js="relative", css="relative", rootdir=os.path.abspath("."))
print "Wrote line_linked.html"

try:
    import webbrowser
    webbrowser.open("file://" + os.path.abspath("line_linked.html"))
except:
    pass

