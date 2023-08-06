data_str = '../data/pymyovent_test.csv'
out_put = '../examples/vent_test.gif'

from ..PyCMLutil.animation.pymyovent_ventricle import animate_ventricle as av
import pandas as pd
import numpy as np

pandas_data = pd.read_csv(data_str)
pandas_data['internal_radius'] = \
    1e3*np.power((3.0 * 0.001 * pandas_data['volume_ventricle']) / \
    (2.0 * np.pi), (1.0/3.0))
pandas_data['external_radius'] = pandas_data['internal_radius'] + \
    1e3*pandas_data['ventricle_wall_thickness']
#print(pandas_data['internal_radius'])
#print(pandas_data['external_radius'])

av(pandas_data = pandas_data,
    r1_name = 'internal_radius',
    r2_name = 'external_radius',
    output_image_file_string = out_put)
