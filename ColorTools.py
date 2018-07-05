import webcolors
import matplotlib



def bgr2rgb(c):
    """
    reorders bgr to rgb
    """
    return (c[2], c[1], c[0])

def closest_color(requested_color):
    #https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python
    #functions for estimating the name of a color
    min_colors = {}
    for name, key in matplotlib.colors.cnames.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) 
        gd = (g_c - requested_color[1])
        bd = (b_c - requested_color[2])
        min_colors[(rd + gd + bd)**2] = name
    return min_colors[min(min_colors.keys())]

def get_color_name(requested_color):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_color)
    except ValueError:
        closest_name = closest_color(requested_color)
        actual_name = None
    return actual_name, closest_name