# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 17:20:25 2020

@author: kscamp3
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def fv_plot(f, v, draw_fit=False, ax=[], sym='ro'):
    """ Draws fv_plot with optional fit """
    
    # Make axes if requried
    if not ax:
        fig = plt.figure(constrained_layout=True)
        fig.set_size_inches([3,3])
        spec = gridspec.GridSpec(nrows=1, ncols=1, figure=fig)
        ax = fig.add_subplot(spec[0,0])
    
    ax.plot(f, v, sym)
    
    if draw_fit:
        from ..curve_fitting.curve_fitting import fit_hyperbola
        
        fit_data = fit_hyperbola(f, v)
        
        ax.plot(fit_data['x_fit'], fit_data['y_fit'],
                label='x$_0$ = %g\na = %g\nb = %g' %
                    (fit_data['x_0'], fit_data['a'], fit_data['b']))
        
    # Add labels
    ax.set_xlabel('Force')
    ax.set_ylabel('Velocity')
    ax.legend()
    
def power_plot(f, fv_power, draw_fit=False, ax=[], sym='ro'):
    """ Draws force_power_plot with optional fit """
    
    # Make axes if requried
    if not ax:
        fig = plt.figure(constrained_layout=True)
        fig.set_size_inches([3,3])
        spec = gridspec.GridSpec(nrows=1, ncols=1, figure=fig)
        ax = fig.add_subplot(spec[0,0])
    
    ax.plot(f, fv_power, sym)
    
    if draw_fit:
        from ..curve_fitting.curve_fitting import fit_power_curve
        
        fit_data = fit_power_curve(f, fv_power)
        
        ax.plot(fit_data['x_fit'], fit_data['y_fit'],
                label='x$_0$ = %g\na = %g\nb = %g' %
                    (fit_data['x_0'], fit_data['a'], fit_data['b']))
        
    # Add labels
    ax.set_xlabel('Force')
    ax.set_ylabel('Power')
    ax.legend()
    
