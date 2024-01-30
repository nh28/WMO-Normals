import os
import pandas as pd
from Elements import Elements
from StationList import StationList
from Template import Template

@staticmethod
def convert(wmo_data_set_df, template_df, station_list_df, normals_parameters_df, folder_path_out):
    gen_station = StationList(template_df, station_list_df)
    gen_station.fill_key()
    
    all_stations = wmo_data_set_df.groupby('STN_ID')
    for station_id, station_df in all_stations:
        
        this_station_template_df = template_df.copy()
        single_station = StationList(this_station_template_df, station_list_df, station_id)
        name_wmo = single_station.fill_station_data() 

        elements_parameters = Elements(this_station_template_df, normals_parameters_df)

        all_elements = station_df.groupby("NORMAL_ID")
        quintile_count = 0
        for id, element_df in all_elements:
            row_in_normals_parameters = elements_parameters.find_element_row(id) 
            wmo_element_name = normals_parameters_df.iloc[row_in_normals_parameters]["Parameter Name"]
            wmo_parameter = normals_parameters_df.iloc[row_in_normals_parameters]["Parameter Code"]
            row_in_station_template = elements_parameters.find_wmo_name(wmo_element_name) + 3

            if (id in [185, 186, 187, 188, 189, 190]):
                row_in_station_template += quintile_count
                quintile_count+=1

            #Warning: assumes that there are a max of two calculations possible
            col_in_parameter = normals_parameters_df.columns.get_loc("Calculation Name")
            limit = col_in_parameter + 2
            while (col_in_parameter < limit and normals_parameters_df.iloc[row_in_normals_parameters, col_in_parameter] != None 
                   and not pd.isna(normals_parameters_df.iloc[row_in_normals_parameters, col_in_parameter])):
                calculation = normals_parameters_df.iloc[row_in_normals_parameters, col_in_parameter] 
                col_in_parameter+=1
                elements_parameters.fill_elements(name_wmo[1], wmo_parameter, row_in_station_template, calculation, element_df)
                row_in_station_template+=1

        one_station_path = os.path.join(folder_path_out, "1991-2020_Normals_Canada_" + name_wmo[0] + ".csv")
        os.makedirs(os.path.dirname(one_station_path), exist_ok=True)
        this_station_template_df.to_csv(one_station_path, index=False)


