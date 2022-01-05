"""
Adding here color schemes
"""

def color_scales(choice,levels):
    if choice == "danra_prec":
        colors = ['aqua','dodgerblue','blue','m','magenta','darkorange','red']
        if len(levels) != len(colors):
            print(f"Number of levels {len(levels)} does not match number of colors {len(colors)}!")
    else:
         print(f"Scale {choice} unknown")
         colors = None

    return colors


