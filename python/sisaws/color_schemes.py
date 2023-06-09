"""
Adding here color schemes
"""

import numpy as np
import matplotlib
from matplotlib import cm

def color_scales(choice,levels) -> list:
    """
    Define colors for specific levels
    Color length and levels must coincide
    """

    if choice == "danra_prec":
        colors = ['aqua','dodgerblue','blue','m','magenta','darkorange','red']
    else:
        print(f"Color scale {choice} unknown")
        sys.exit(1)
    if len(levels) != len(colors):
        print(f"Number of levels {len(levels)} does not match number of colors {len(colors)}!")
        print("Exiting...")
        sys.exit(1)

def color_maps(choice):
    """
    Define a color map
    """
    from matplotlib.colors import ListedColormap
    if choice == "kpnprec":
        #Color scale defined by Kristian
        viridis = cm.get_cmap('viridis', 256)
        kpnprec = viridis(np.linspace(0, 1, 255))
        black   = np.array([0, 0, 0, 1])
        blue    = np.array([0, 0, 1, 1])
        cyan    = np.array([0, 1, 1, 1])
        green   = np.array([0, 1, 0, 1])
        magenta = np.array([1, 0, 1, 1])
        orange  = np.array([1, 0.5, 0, 1])
        red     = np.array([1, 0, 0, 1])
        white   = np.array([1, 1, 1, 1])
        yellow  = np.array([1, 1, 0, 1])
        for x in range (0, 31):
           ctmp = white*(1-x/32)+black*x/32
           kpnprec[x,:]=ctmp
        for x in range (0, 31):
           ctmp = cyan*(1-x/32)+black*x/32
           kpnprec[x+32,:]=ctmp
        for x in range (0, 31):
           ctmp = blue*(1-x/32)+black*x/32
           kpnprec[x+64,:]=ctmp
        for x in range (0, 31):
           ctmp = green*(1-x/32)+black*x/32
           kpnprec[x+96,:]=ctmp
        for x in range (0, 31):
           ctmp = yellow*(1-x/32)+black*x/32
           kpnprec[x+128,:]=ctmp
        for x in range (0, 31):
           ctmp = orange*(1-x/32)+black*x/32
           kpnprec[x+160,:]=ctmp
        for x in range (0, 31):
           ctmp = red*(1-x/32)+black*x/32
           kpnprec[x+192,:]=ctmp
        for x in range (0, 31):
           ctmp = magenta*(1-x/32)+black*x/32
           kpnprec[x+224,:]=ctmp
        color_map=ListedColormap(kpnprec)
    else:
        print(f"Color map {choice} unknown")
        sys.exit(1)


    return color_map


