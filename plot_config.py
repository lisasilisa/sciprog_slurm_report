import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx




def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    """
    Extract subset of colormap (to only get colors in a specific range)
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Arguments:
    cmap: matplotlib.colors.Colormap; colormap
    minval: float; new min value, default is old min value
    maxval: float; new max value, default is old max value
    n: int; number of sampled points from the old colormap

    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Returns: new_cmap: matplotlib.colors.Colormap
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    """
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap



def set_plot_config():
    """
    Set default values for visualization
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    Returns: plot_config: dict
    """
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