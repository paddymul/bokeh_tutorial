import numpy as np
from numpy import pi, cos, sin, linspace, zeros, linspace, \
        short, fromstring, hstack, transpose
from scipy import fft
import time
from bokeh.plotting import *

NUM_SAMPLES = 1024
SAMPLING_RATE = 44100
MAX_FREQ = SAMPLING_RATE / 8
FREQ_SAMPLES = NUM_SAMPLES / 8
SPECTROGRAM_LENGTH = 400

_stream = None
def read_mic():
    import pyaudio
    global _stream
    if _stream is None:
        pa = pyaudio.PyAudio()
        _stream = pa.open(format=pyaudio.paInt16, channels=1, rate=SAMPLING_RATE,
                     input=True, frames_per_buffer=NUM_SAMPLES)
    try:
        audio_data  = fromstring(_stream.read(NUM_SAMPLES), dtype=short)
        normalized_data = audio_data / 32768.0
        return (abs(fft(normalized_data))[:NUM_SAMPLES/2], normalized_data)
    except:
        return None

def get_audio_data(interval=0.05):
    time.sleep(interval)
    starttime = time.time()
    while time.time() - starttime < interval:
        data = read_mic()
        if data is not None:
            return data
    return None

output_server("spectrogram")

# Create the base plot
N = 36
theta = linspace(0, 2*pi, N+1)
rmin = 10
rmax = 20 * np.ones(N)
cx = cy = np.ones(N)
annular_wedge(cx, cy, rmin, rmax, theta[:-1], theta[1:],
        inner_radius_units = "data",
        outer_radius_units = "data",
        color = "#A6CEE3", line_color="black", 
        tools="pan,zoom,resize")
show()

from bokeh.objects import GlyphRenderer
renderer = [r for r in curplot().renderers if isinstance(r, GlyphRenderer)][0]
ds = renderer.data_source
while True:
    data = get_audio_data()
    if data is None:
        continue
    else:
        data = data[0]
    # Zoom in to a frequency range:
    data = data[:len(data)/2]
    histdata = (np.histogram(data, N, density=True)[0] * 5) + rmin
    ds.data["outer_radius"] = histdata
    ds._dirty = True
    session().store_obj(ds)
