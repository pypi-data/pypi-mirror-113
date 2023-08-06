# -*- coding: utf-8 -*-
"""
Created on Sat April 16 2021

@author: Hossein_Sharifi
"""

import json
import pandas as pd
import numpy as np
import os

from scipy.signal import find_peaks

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
from matplotlib import patches as pat
from matplotlib.patches import Patch
from matplotlib.patches import Rectangle
import seaborn as sns


def default_formatting():
    """
    Sets default formatting (fontname, axis linewidth, ...)

    Returns
    -------
    formatting : dict
        dictionnary containing the default formatting.

    """
    formatting = dict()
    formatting['data_linewidth'] = 1.5
    formatting['fontname'] = 'Arial'
    formatting['axis_linewidth'] = 1.5
    formatting['x_label_fontsize'] = 12
    formatting['x_label_pad'] = 0
    formatting['y_label_rotation'] = 0
    formatting['y_label_fontsize'] = 12
    formatting['y_label_pad'] = 30
    formatting['legend_location'] = 'upper left'
    formatting['legend_bbox_to_anchor'] = [1.05, 1]
    formatting['legend_fontsize'] = 9
    formatting['legend_handlelength'] = 1
    formatting['tick_fontsize'] = 11
    formatting['patch_alpha'] = 0.3
    formatting['max_rows_per_legend'] = 4
    formatting['palette'] = None

    return formatting

def default_layout():
    """
    Sets default layout (figure size, margin size, grid space)

    Returns
    -------
    layout : dict
        dictionnary containing the default layout.

    """
    layout = dict()
    layout['fig_width'] = 5
    layout['fig_height'] = 5
    layout['panel_height'] = 1
    layout['top_margin'] = 0.1
    layout['bottom_margin'] = 0.1
    layout['left_margin'] = 0.1
    layout['right_margin'] = 0.1
    layout['grid_wspace'] = 0.1
    layout['grid_hspace'] = 0.1

    return layout

def default_processing():
    processing = dict()
    processing['envelope_n'] = 300

    return processing

def display_pv_loop(
        data_file_string = [],
        excel_sheet = 'Sheet1',
        pandas_data = [],
        time_frames = [],
        template_file_string=[],
        template_data=dict(),
        pressure_var_name = "",
        volume_var_name = "",
        time_var_name = "",
        legend_labels = [],
        x_tick = 'min_max',
        y_tick = 'min_max',
        x_label = 'Volume (liters)',
        y_label = 'Pressure (mm Hg)',
        output_image_file_string = [],
        dpi = 300):
    """
    Plot a pressure-volume loop

    Parameters
    ----------
    data_file_string : str, optional
        Path to the data file. The default is [].
    excel_sheet : str, optional
        Excel sheet where the data are stored. The default is 'Sheet1'.
    pandas_data : DataFrame, optional
        DataFrame containing the data. The default is [].
    time_frames: Array of tuples, [(),(),..,()]
    template_file_string : str, optional
        Path to the .json structure file. The default is [].
    template_data : Dictionary , optional
        It contains the formatting and layout variables
    pressure_var_name: str, required
        Variable name for "Pressure" in the data frame
    volume_var_name: str, required
        Variable name for "Volume" in the data frame
    time_var_name : str, optional
        Variable name for "Time" in the data frame
    legend_labels: array of str, optional
    x_tick: str, optional
        Assigned mode for calculating ticks for X axis
    y_tick: str, optional
        Assigned mode for calculating ticks for Y axis
    x_label: str, optional
        X axis label
    y_label: str, optional
        Y axis label
    output_image_file_string : str, optional
        Path where the output plot is saved. The default is [].
    dpi : int, optional
        Image resolution. The default is 300.

    Returns
    -------
    fig : figure
        Handle to the produced pyplot figure.
    ax : axes
        Handle to an array of the pyplot axes.

    """


    # Pull default formatting, then overwite any values from the template
    formatting = default_formatting()
    if ('formatting' in template_data):
        for entry in template_data['formatting']:
            formatting[entry] = template_data['formatting'][entry]

    # Pull default layout, then overwite any values from the template
    layout = default_layout()
    if 'layout' in template_data:
        for entry in template_data['layout']:
            layout[entry] = template_data['layout'][entry]

    # Check time_frames
    if not(time_frames == []):
        if time_var_name == "":
            print('"time_var_name" is not defined!')
            return
        time = time_var_name

    # Work out data before plotting
    pv_dict = dict()
    if (not data_file_string==[]):
        for ds in data_file_string:
            file_type = ds.split('.')[-1]
            if file_type == 'xlsx':
                pandas_data.append(pd.read_excel(ds,sheet_name=excel_sheet))
            if file_type == 'csv':
                pandas_data.append(pd.read_csv(ds))

    # Create pv_dict before plotting
    if len(pandas_data) == 1:
        df = pandas_data[0]
        if time_frames:
            for i,t in enumerate(time_frames):
                sliced_data = df.loc[df[time].between(t[0],t[-1])]

                pv_dict['pv'+str(i)] = \
                    {'pressure' : sliced_data[pressure_var_name].to_numpy(),
                     'volume' : sliced_data[volume_var_name].to_numpy()}
        else:
            pv_dict['pv'] = \
                {'pressure' : df[pressure_var_name].to_numpy(),
                  'volume' : df[volume_var_name].to_numpy()}
    else:
        for i,df in enumerate(pandas_data):

            if len(time_frames) > 0 and i <= len(time_frames):
                sliced_data = df.loc[df[time].between(time_frames[i][0],time_frames[i][-1])]

                pv_dict['pv'+str(i)] = \
                    {'pressure' : sliced_data[pressure_var_name].to_numpy(),
                     'volume' : sliced_data[volume_var_name].to_numpy()}

            else:
                pv_dict['pv'+str(i)] = \
                    {'pressure' : df[pressure_var_name].to_numpy(),
                     'volume' : df[volume_var_name].to_numpy()}

    # Now create figure
    fig = plt.figure(constrained_layout=False)
    fig.set_size_inches([layout['fig_width'], layout['fig_height']])
    spec = gridspec.GridSpec(nrows = 1,
                             ncols = 1,
                             figure = fig,
                             wspace = layout['grid_wspace'],
                             hspace = layout['grid_hspace'])

    legend_symbols = []
    legend_strings = legend_labels

    colors = sns.color_palette(formatting['palette'])

    ax = fig.add_subplot(spec[0,0])
    print('hi')
    for i,pv in enumerate(pv_dict.keys()):

        x = pv_dict[pv]['volume']
        y = pv_dict[pv]['pressure']

        if 'x_scale_factor' in formatting:
            x = formatting['x_scale_factor'] * x
        if 'y_scale_factor' in formatting:
            y = formatting['y_scale_factor'] * y

        if i == 0:
            min_x = 0
            max_x = x[-1]
            min_y = y[0]
            max_y = y[-1]
        min_x = np.amin([min_x, np.amin(x)])
        max_x = np.amax([max_x, np.amax(x)])
        min_y = np.amin([min_y, np.amin(y)])
        max_y = np.amax([max_y, np.amax(y)])

        ax.plot(x,y,
                linewidth = formatting['data_linewidth'],
                color = colors[i],
                clip_on = True)

        if not(legend_labels == []):
            legend_symbols.append(Line2D([0],[0],
                                  color = ax.lines[-1].get_color(),
                                  lw = formatting['data_linewidth']))
    # handle X_axis
    xlim = (min_x, 1.1*max_x)
    xlim = deduce_axis_limits(xlim,'autoscaled')
    if x_tick == 'min_max':
        ax.set_xlim(xlim)
        ax.set_xticks(xlim)

    ax.set_xlabel(x_label,
                  labelpad = formatting['x_label_pad'],
                  fontfamily = formatting['fontname'],
                  fontsize = formatting['x_label_fontsize'])
    # handle Y_axis
    ylim = (min_y, 1.1*max_y)
    print(ylim)
    ylim = deduce_axis_limits(ylim)
    if y_tick == 'min_max':
        ax.set_ylim(ylim)
        ax.set_yticks(ylim)

    ax.set_ylabel(y_label,
                  loc='center',
                  verticalalignment='center',
                  labelpad = formatting['y_label_pad'],
                  fontfamily = formatting['fontname'],
                  fontsize = formatting['y_label_fontsize'],
                  rotation = formatting['y_label_rotation'])
    # handle ax frames
    for a in ['left','bottom']:
        ax.spines[a].set_linewidth(formatting['axis_linewidth'])
        if a == 'left':
            position = min_x - 0.05 * (xlim[-1]-xlim[0])
        elif a == 'bottom':
            position = min_y - 0.05 * (ylim[-1]-ylim[0])
        ax.spines[a].set_position(('data',position))

    ax.tick_params('both',
                    width = formatting['axis_linewidth'])
    for tick_label in ax.get_xticklabels():
        tick_label.set_fontname(formatting['fontname'])
        tick_label.set_fontsize(formatting['tick_fontsize'])
    for tick_label in ax.get_yticklabels():
        tick_label.set_fontname(formatting['fontname'])
        tick_label.set_fontsize(formatting['tick_fontsize'])

    # Remove top and right-hand size of box
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    leg = ax.legend(legend_symbols, legend_strings,
                    loc = formatting['legend_location'],
                    handlelength = formatting['legend_handlelength'],
                    bbox_to_anchor=(formatting['legend_bbox_to_anchor'][0],
                                    formatting['legend_bbox_to_anchor'][1]),
                    prop={'family': formatting['fontname'],
                          'size': formatting['legend_fontsize']})

    leg.get_frame().set_linewidth(formatting['axis_linewidth'])
    leg.get_frame().set_edgecolor("black")

    # Tidy overall figure
    # Move plots inside margins
    lhs = layout['left_margin']/layout['fig_width']
    bot = layout['bottom_margin']/layout['fig_height']
    wid = (layout['fig_width']-layout['left_margin']-layout['right_margin'])/layout['fig_width']
    hei = (layout['fig_height']-layout['bottom_margin']-layout['top_margin'])/layout['fig_height']
    r = [lhs, bot, wid, hei]
    spec.tight_layout(fig, rect=r)

    fig.align_labels()

    # Save if required
    if output_image_file_string:
        print('Saving figure to %s' % output_image_file_string)
        output_dir = os.path.dirname(output_image_file_string)
        if not os.path.isdir(output_dir):
            print('Making output dir')
            os.makedirs(output_dir)
        fig.savefig(output_image_file_string, dpi=dpi)

    return (fig,ax)


def handle_annotations(template_data, ax, panel_index, formatting):
    if not ('annotations' in template_data):
        return
    annotation_data = template_data['annotations']
    for an in annotation_data:
        if ((an['panel'] == 'all') or (an['panel'] == panel_index)):
            # check for vertical lines
            if (an['type'] == 'v_line'):
                # define default formats for v_line,
                # if they are not alrady defined
                if not('linestyle' in an):
                    an['linestyle'] = '--'
                if not('linewidth' in an):
                    an['linewidth'] = formatting['data_linewidth']
                if not('color' in an):
                    an['color'] = 'black'
                # now draw the v_line
                ax.axvline(x = an['x_value'],
                            linestyle = an['linestyle'],
                            linewidth = an['linewidth'],
                            color = an['color'])

            # check for horizontal lines
            elif (an['type'] == 'h_line'):
                # define default formats for v_line,
                # if they are not alrady defined
                if not('linestyle' in an):
                    an['linestyle'] = '--'
                if not('linewidth' in an):
                    an['linewidth'] = formatting['data_linewidth']
                if not('color' in an):
                    an['color'] = 'black'
                # now draw the v_line
                ax.axhline(y = an['y_value'],
                            linestyle = an['linestyle'],
                            linewidth = an['linewidth'],
                            color = an['color'])

            elif (an['type'] == 'box'):
                # drawing box
                x_start = an['x_coord']
                y_lim = ax.get_ylim()
                y_start = y_lim[0] + \
                        (y_lim[1]-y_lim[0]) * an['y_rel_coord']
                h_box = (y_lim[1]-y_lim[0]) * an['rel_height']
                xy_start = [x_start,y_start]
                if not('linestyle' in an):
                    an['linestyle'] = '-'
                if not('linewidth' in an):
                    an['linewidth'] = formatting['data_linewidth']
                if not('face_color' in an):
                    an['face_color'] = 'none'
                if not('edge_color' in an):
                    an['edge_color'] = 'black'
                box = Rectangle(xy = xy_start,
                            width = an['width'],
                            height = h_box,
                            facecolor = an['face_color'],
                            edgecolor = an['edge_color'],
                            linestyle = an['linestyle'],
                            linewidth = an['linewidth'],
                            clip_on = False)
                ax.add_patch(box)

            elif (an['type'] == 'text'):
                # writing text
                y_lim = ax.get_ylim()
                if not('label_fontsize' in an):
                    an['label_fontsize'] = formatting['y_label_fontsize']
                if not('label_color' in an):
                    an['label_color'] = 'black'
                ax.text(x = an['x_coord'],
                        y = y_lim[0] + (y_lim[1]-y_lim[0]) * an['y_rel_coord'],
                        s = an['label'],
                        fontsize = an['label_fontsize'],
                        fontfamily = formatting['fontname'],
                        horizontalalignment='center',
                        verticalalignment='center',
                        color = an['label_color'])

def deduce_axis_limits(lim, mode_string=[]):
    """
    Sets the x limits

    Parameters
    ----------
    lim : tuple
        tuple containing the first and last x-value from the data.
    mode_string : str, optional
        If set to "close_fit", the x limits are the closest to the lim input. The default is [].

    Returns
    -------
    Tuple containing the x limits

    """

    # Start simply
    lim = np.asarray(lim)
    lim[0] = multiple_less_than(lim[0])
    lim[1] = multiple_greater_than(lim[1])

    if (mode_string != 'close_fit'):
        if (lim[0]>0):
            lim[0]=0
        else:
            if (lim[1]<0):
                lim[1]=0

    return ((lim[0],lim[1]))

def multiple_greater_than(v, multiple=0.2):
    if (v>0):
        n = np.floor(np.log10(v))
        m = multiple*np.power(10,n)
        v = m*np.ceil(v/m)
    if (v<0):
        n = np.floor(np.log10(-v))
        m = multiple*np.power(10,n)
        v = m*np.ceil(v/m)

    return v

def multiple_less_than(v, multiple=0.2):
    if (v>0):
        n = np.floor(np.log10(v))
        m = multiple*np.power(10,n)
        v = m*np.floor(v/m)
    if (v<0):
        n = np.floor(np.log10(-v))
        m = multiple*np.power(10,n)
        v = m*np.floor(v/m)

    return v

if __name__ == "__main__":
    (fig,ax) = multi_panel_from_flat_data()
    plt.close(fig)
