from PyCMLutil.plots.multi_panel_cat import multi_panel_cat_from_flat_data as mplc
import pandas as pd
if __name__ == "__main__":


    data_file_string = "data/valvular_disease.xlsx"

    temp_file_string = "json/valvular.json"
    fig_file_string = "valves.png"
    temp_list = ['json/1X1_strip_valvular.json',
                'json/1X1_strip_hue_valvular.json',
                'json/1X1_point_valvular.json',
                'json/1X1_point_strip_valvular.json',
                'json/1X1_point_hue_valvular.json',
                'json/1X1_box_valvular.json',
                'json/1X1_box_strip_valvular.json',
                'json/1X1_box_hue_valvular.json',
                'json/4X4_multiple_valvular.json']
    temp_list = ['json/1X1_point_valvular.json']
    for i,t in enumerate(temp_list):
        print(i)
        output_image_str = 'examples/'+t.split('.')[0].split('/')[-1]+'.png'


        mplc(data_file_string = data_file_string,
            template_file_string = t,
            output_image_file_string = output_image_str,dpi=100)
    """print(out_dict['ax'][0].figure)
                out_dict_2 = mplc(data_file_string = data_file_string,
                    template_file_string = "json/test_cat_2.json",
                    output_image_file_string = "test_cat2.png",
                    predef = out_dict)
                print(out_dict_2['rows_per_column'])"""
    test = 0
    if test:
        import matplotlib.pyplot as plt
        import matplotlib.gridspec as gridspec

        new_fig = plt.figure()
        spec = gridspec.GridSpec(1,2)

        ax = out_dict['ax'][0]
        
