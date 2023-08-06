
data_str = ['data/pymyovent_test.csv']
time_frames = [(5,6),(10,11),[20,21]]
out_put = 'pv_test.png'

from PyCMLutil.plots.pv_plots import display_pv_loop as pv

pv(data_file_string = data_str,
    time_frames = time_frames,
    pressure_var_name = 'pressure_ventricle',
    volume_var_name = 'volume_ventricle',
    template_data = {'formatting':{'palette':'Set2'}},
    time_var_name = 'time',
    legend_labels = ['pv1','pv2','pv3'],
    output_image_file_string = out_put,
    dpi = 300)
