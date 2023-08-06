# -*- coding: utf-8 -*-
"""
Demos.md
"""

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from plots import pCa_plots as p
# plots import pCa_plots as p
# import PyCMLutilities.plots.fv_plots as fv
# import PyCMLutilities.curve_fitting.curve_fitting as cf

def demos(demo_group):
    """
    Parameters
    ----------
    demo_group : string
        ken: runs a tension-pCa plot and adds a Hill curve fitting
        plots_multi_panel: runs a multi-panel plot

    Returns
    -------
    None.

    """    
    
    
    if (demo_group == 'ken'):
        pCa = np.array([9, 6, 5.5, 5, 4])
        f = np.array([1, 2, 5, 8, 10])
        p.y_pCa_plot(pCa, f, draw_fit=True)
        
    if (demo_group == "plots_multi_panel"):
        from .demos_plots.demos_multi_panel import demos_multi_panel_code as dmp
        dmp.run_demos()
        
        
        
    # f = np.array([100, 500, 1000, 2000, 5000, 8000])
    # v = np.array([2, 1.5, 1, 0.5, 0.1, 0.01])
    # fv.fv_plot(f, v, draw_fit=True)
    
    # fv_power = f*v
    # fv.power_plot(f, fv_power, draw_fit=True)
    
    # n = 500
    # t = np.linspace(0,1,n)
    # noise = 0.3*np.random.normal(0,1,n)
    # y = noise + 0.5 + 3.0 * (1 - np.exp(-4*t))
    # print(t)
    # print(y)
    
    # fit_data = cf.fit_exponential_recovery(t,y)
    
    # fig = plt.figure(constrained_layout=True)
    # fig.set_size_inches([3,3])
    # spec = gridspec.GridSpec(nrows=1, ncols=1, figure=fig)
    # ax = fig.add_subplot(spec[0,0])
    
    # ax.plot(t, y, 'b-')
    # ax.plot(fit_data['x_fit'], fit_data['y_fit'], 'y-',
    #         label='offset = %g\namp = %g\nrate = %g' %
    #         (fit_data['offset'], fit_data['amp'], fit_data['k']))
    # ax.set_xlabel('x')
    # ax.set_ylabel('y')
    # ax.legend()
    
if __name__ == "__main__":
    demos()  
    
    
    
    

    
    
    
