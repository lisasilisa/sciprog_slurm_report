import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap



def set_plot_config():
    plot_config = {}

    c_map = plt.get_cmap('Blues')  
    truncated_c_map = truncate_colormap(c_map, 0.2, 0.8)

    plot_config['c_map'] = truncated_c_map
    plot_config['leg_loc'] = 'lower right'
    plot_config['label_font_size'] = 14
    plot_config['label_pad'] = 15
    plot_config['tick_font_size'] = 14
    plot_config['leg_font_size'] = 8
    plot_config['bar_width'] = 0.35
    plot_config['dpi'] = 300

    return plot_config