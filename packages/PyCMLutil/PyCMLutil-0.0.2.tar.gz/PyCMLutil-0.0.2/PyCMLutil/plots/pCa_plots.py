# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 17:20:25 2020

@author: kscamp3
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def y_pCa_plot(pCa, y, draw_fit=False, ax=[], sym='ro'):
    """ Draws y-pCa plot with optional fit """
    
    # Make axes if requried
    if not ax:
        f = plt.figure(constrained_layout=True)
        f.set_size_inches([3,3])
        spec = gridspec.GridSpec(nrows=1, ncols=1, figure=f)
        ax = f.add_subplot(spec[0,0])
    
    ax.plot(pCa, y, sym)
    
    if draw_fit:
        from curve_fitting.curve_fitting import fit_pCa_data
        
        fit_data = fit_pCa_data(pCa, y)
        
        ax.plot(fit_data['x_fit'], fit_data['y_fit'],
                label='pCa$_{50}$ = %.3f\nn$_H$ = %.2f' %
                    (fit_data['pCa_50'], fit_data['n_H']))
        
    # Add labels
    ax.set_xlabel('pCa')
    ax.set_ylabel('Force')
    ax.legend()
    
    # Flip axis
    ax.invert_xaxis()