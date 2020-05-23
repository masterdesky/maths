import sys
import numpy as np
import pandas as pd
from numba import jit

import matplotlib.pyplot as plt

from colorcet import palette
import datashader as ds
import datashader.colors as dc
import datashader.utils as utils
from datashader import transfer_functions as tf

from datetime import datetime

def sign_choose():
    return -1 if np.random.random() < 0.5 else 1

@jit(nopython=True)
def Clifford(x, y, a, b, c, d, *o):

    return np.sin(a * y) + c * np.cos(a * x), \
           np.sin(b * x) + d * np.cos(b * y)

@jit(nopython=True)
def Johnny_Svensson(x, y, a, b, c, d, *o):
    """
    x and y both start at 0.1
    Variables a, b, c and d are floating point values between -3 and +3
    """

    return d * np.sin(x * a) - np.sin(y * b), \
           c * np.cos(x * a) + np.cos(y * b)

@jit(nopython=True)
def Symmetric_Icon(x, y, a, b, g, om, l, d, *o):
    zzbar = x*x + y*y
    p = a*zzbar + l
    zreal, zimag = x, y
    
    for i in range(1, d-1):
        za, zb = zreal * x - zimag * y, zimag * x + zreal * y
        zreal, zimag = za, zb
    
    zn = x*zreal - y*zimag
    p += b*zn
    
    return p*x + g*zreal - om*y, \
           p*y - g*zimag + om*x

@jit(nopython=True)
def Ikeda(x, y, u, *o):
    
    t = 0.4 - 6/(1 + x*x + y*y)
    
    return 1 + u * (x * np.cos(t) - y * np.sin(t)), \
           u * (x * np.sin(t) + y * np.cos(t))

@jit(nopython=True)
def Fractal_Dream(x, y, a, b, c, d, *o):
    """
    x and y both should start at 0.1
    Variables a and b are floating point values bewteen -3 and +3
    Variables c and d are floating point values between -0.5 and +1.5
    """
    return np.sin(y * b) + c * np.sin(x * b), \
           np.sin(x * a) + d * np.sin(y * a)

@jit(nopython=True)
def trajectory_coords(att, x0, y0, a, b=0, c=0, d=0, e=0, f=0, n=1e07):
    x = np.zeros(n)
    x[0] = x0
    
    y = np.zeros(n)
    y[0] = y0

    for i in np.arange(n-1):
        x[i+1], y[i+1] = att(x[i], y[i], a, b, c, d, e, f)

    return x, y

def trajectory(att, x0, y0, a, b=0, c=0, d=0, e=0, f=0, n=1e07):
    
    x, y = trajectory_coords(att, x0, y0, a, b, c, d, e, f, n)
    
    return pd.DataFrame(dict(x=x, y=y))

def plot(att, x0, y0, a, b=0, c=0, d=0, e=0, f=0, n=1e07, figscale=2e03, cmap=dc.viridis):
    # Create attractor
    df = trajectory(att, x0, y0, a, b, c, d, e, f, n=int(n))

    cvs = ds.Canvas(plot_width=int(figscale), plot_height=int(figscale))
    agg = cvs.points(df, 'x', 'y')
    ds.transfer_functions.Image.border=0
    img = tf.set_background(tf.shade(agg, cmap=cmap), bg_color)
    utils.export_image(img=img, filename=('./out/{0}_{1}_{2}_{3}_{4}_{5}_{6}_{7}'.format(att.__name__, a, b, c, d, e, f, n)))

    return img

start = datetime.now()
bg_color = 'gainsboro'
cmap = palette.bmy

att = Fractal_Dream
# Fractal_Dream: x0=0.1, y0=0.1, a=-0.966918, b=2.879879, c=0.765145, d=0.744728, e=0, f=0
for i in range(int(sys.argv[1])):
    if att is Johnny_Svensson:
        a = np.random.random()*3*sign_choose()
        b = np.random.random()*3*sign_choose()
        c = np.random.random()*3*sign_choose()
        d = np.random.random()*3*sign_choose()
    elif att is Fractal_Dream:
        a = np.random.random()*3*sign_choose()
        b = np.random.random()*3*sign_choose()
        c = np.random.random()*sign_choose() + 0.5
        d = np.random.random()*sign_choose() + 0.5
   
    print('{0}. plotting started...'.format(i+1))
    plot(att=att, x0=0.1, y0=0.1, a=a, b=b, c=c, d=d, e=0, f=0,
        n=8e07, figscale=2e03, cmap=cmap)
    print(datetime.now() - start)

