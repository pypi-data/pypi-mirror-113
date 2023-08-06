# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 23:40:08 2020

@author: ken
"""
import os
import numpy as np
import matplotlib.pyplot as plt

from plots import multi_panel as mp

def run_demos():
    """
    Calls pymyovent_example to run a demo plot

    Returns
    -------
    None.

    """
    
    # annotate_plot()
    
    # cycle_plots()
    pymyovent_example()
    
def pymyovent_example():
    """
    Runs a multi-panel plot from PyMyoVent data

    Returns
    -------
    None.

    """
    
    data_file_string = 'data/pymyovent_test.csv'
    template_file_string = 'json/pymyovent.json'
    image_file_string = 'temp/pymyovent.png'
    
    # Adjust input files for current path
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    data_file_string = os.path.join(
            current_dir,data_file_string)
    template_file_string = os.path.join(
            current_dir, template_file_string)
    image_file_string = os.path.join(
            current_dir, image_file_string)

    # Make a figure
    fig, ax = mp.multi_panel_from_flat_data(
            data_file_string=data_file_string,
            template_file_string=template_file_string,
            output_image_file_string=image_file_string)

    # Close
    plt.close(fig)    

    
def single_run():

    data_file_string = 'c:/temp/pymyovent_test.csv'
    template_file_string = 'json/pymyovent.json'
    image_file_string = 'temp/pymyovent.png'

    # Adjust input files for current path
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    data_file_string = os.path.join(
            current_dir,data_file_string)
    template_file_string = os.path.join(
            current_dir, template_file_string)
    image_file_string = os.path.join(
            current_dir, image_file_string)

    # Make a figure
    fig, ax = mp.multi_panel_from_flat_data(
            data_file_string=data_file_string,
            template_file_string=template_file_string,
            output_image_file_string=image_file_string)

    # Close
    plt.close(fig)    
        
def annotate_plot():
    """
    Add annotations to a plot 

    Returns
    -------
    None.

    """
    
    data_file_string = 'data/test_data.xlsx'
    template_file_string = 'json/2_2.json'
    image_file_string = 'temp/2_2_annotation.png'

    # Adjust input files for current path
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    data_file_string = os.path.join(
            current_dir,data_file_string)
    template_file_string = os.path.join(
            current_dir, template_file_string)
    image_file_string = os.path.join(
            current_dir, image_file_string)
    
    # Make a figure
    fig, ax = mp.multi_panel_from_flat_data(
            data_file_string=data_file_string,
            template_file_string=template_file_string)

    # Add annotations
    ax[0].text(10,2,'Demo text',fontname='Arial')
    ax[1].plot([0,15],[3,3],'r--')
    
    for a in ax:
        yy = np.asarray(a.get_ylim())
        a.plot([5,5],yy,'--',color='#FF45FF')
    
    # Save if required
    if image_file_string:
        print('Saving figure to %s' % image_file_string)
        fig.savefig(image_file_string)
    
    plt.close(fig)

def cycle_plots():
    """
    Plots a series of figures with differents .json structure files

    Returns
    -------
    None.

    """
    
    data_file_string = 'data/test_data.xlsx'
    image_dir = 'temp'
    json_dir = 'json'
   
    # Get files in json dir
    current_dir = os.path.dirname(os.path.realpath(__file__))
    json_dir = os.path.join(current_dir, json_dir)
    json_files = [f for f in os.listdir(json_dir) 
                  if os.path.isfile(os.path.join(json_dir,f))]
    json_files.append('')
    json_files.remove('pymyovent.json')
    
    data_file_string = os.path.join(
            current_dir,data_file_string)
    
    for js in json_files:
        if (js == ''):
            image_name = 'blank_json'
            json_file_string = ''
        else:
            image_name = js.split('.')[0]
            json_file_string = os.path.join(
                current_dir, json_dir, js)
            
        print(json_file_string)
        # continue
        
        image_file_string = os.path.join(
                current_dir,image_dir,('%s.png' % image_name))
                
        fig, ax = mp.multi_panel_from_flat_data(
            data_file_string=data_file_string,
            template_file_string=json_file_string,
            output_image_file_string=image_file_string)
    
        plt.close(fig)
