# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 01:03:23 2020

@author: ken
"""

import pandas as pd
import numpy as np

def create_test_data():
    
    n = 2000
    d = pd.DataFrame({'time': np.linspace(0,20,n)})
    d['up'] = np.linspace(2,4,n)
    d['down'] = np.linspace(4,1,n)
    d['crossing'] = np.linspace(-1,2,n)
    d['slow_wave'] = 2+np.sin(d['time']*2*np.pi*0.1)
    d['medium_wave'] = np.linspace(4,8,n) + 0.7*np.sin(d['time']*2*np.pi*1)
    d['fast_wave'] = 7+1.5*np.sin(d['time']*2*np.pi*20)
    d['wave_mix'] = 8+3*np.sin(d['time']*0.2*np.pi) + 2*np.sin(d['time']*2*np.pi)
  
    d.to_excel('data/test_data.xlsx', index=False)
    
if __name__ == "__main__":
    create_test_data()
                      