# The plot server must be running
# Go to http://localhost:5006/bokeh to view this plot

import numpy as np
from numpy import pi, cos, sin, linspace
from bokeh.plotting import *

colors = ("#A6CEE3", "#1F78B4", "#B2DF8A")
N = 36
r_base = 8
theta = linspace(0, 2*pi, N)
r_x = linspace(0, 6*pi, N-1)
rmin = r_base - cos(r_x) - 1
rmax = r_base + sin(r_x) + 1

output_server("wedge animate")

cx = cy = np.ones_like(rmin)
annular_wedge(cx, cy, 
        rmin, rmax, theta[:-1], theta[1:],
        inner_radius_units="data",
        outer_radius_units="data",
        color = colors[0], 
        line_color="black", tools="pan,zoom,resize")
#show()

import time
from bokeh.objects import GlyphRenderer
renderer = [r for r in curplot().renderers if isinstance(r, GlyphRenderer)][0]
ds = renderer.data_source
while True:
    for i in np.linspace(-2*np.pi, 2*np.pi, 50):
        rmin = ds.data["inner_radius"]
        rmin = np.roll(rmin, 1)
        ds.data["inner_radius"] = rmin
        rmax = ds.data["outer_radius"]
        rmax = np.roll(rmax, -1)
        ds.data["outer_radius"] = rmax
        ds._dirty = True
        session().store_obj(ds)
        time.sleep(.25)
