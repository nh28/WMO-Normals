import os
import pandas as pd
from Elements import Elements
from StationList import StationList

def main():
    wmo_data_set_path = input("Please enter the path to the WMO Data Set: ").replace('"', '')
    wmo_data_set_df = pd.read_csv(wmo_data_set_path)

    template_path = input("Please enter the path to the WMO template: ").replace('"', '')
    template_df = pd.read_csv(template_path)

    station_list_path = input("Please enter the Station List: ").replace('"', '')
    station_list_df = pd.read_csv(station_list_path)
    dim_row = 13
    
    """ UNCOMMENT IF WANT THIS FEATURE
    gen_station = StationList(template_df, station_list_df, "")
    bool = ""
    while (bool != "quit"):
        station_key = input("Please enter any other information you need to input for a station (NOT Name, Country, WMO-ID, WIGOS-ID, Lat, Long, Elevation)" + 
                            "\nEnter it in the format template_name:station_list_name:column_on_station_list" + 
                            "\nTo exit, enter quit\n")
        if (station_key.lower() == "quit"):
            bool = station_key.lower()
        else:
            gen_station.add_names_key(station_key)
            dim_row = input("Please indicate what row the station header ends: ")
            gen_station.change_dim_row(dim_row)
            dim_col = input("Please indicate what col the station header ends: ")
            gen_station.change_dim_col(dim_col)
        
    """

    normal_parameters_path = input("Please enter the path to the Normal ID to WMO Parameter ID: ").replace('"', '')
    normals_parameters_df = pd.read_csv(normal_parameters_path)

    path = input("Enter the path you want all the files to output to: ").replace('"', '')

    all_stations = wmo_data_set_df.groupby('ENG_STN_NAME')

    for station_name, station_df in all_stations:
        # fill the information about the station
        station_temp_df = template_df.copy()
        one_station = StationList(station_temp_df, station_list_df, station_name)
        wmo_id = one_station.fill_station_data() #might need to return the data frame insteadquitqui

        el = Elements(station_temp_df, normals_parameters_df)
        all_elements = station_df.groupby("NORMAL_ID")
        quintile_count = 0
        for id, element_station_df in all_elements:
            row = el.find_element_row(id)
            wmo_name = normals_parameters_df.iloc[row, 3]
            wmo_parameter = normals_parameters_df.iloc[row, 2]
            row_template = el.find_wmo_name(wmo_name, dim_row) + 3
            if (id in [185, 186, 187, 188, 189, 190]):
                row_template += quintile_count
                quintile_count+=1
            i = 5
            while (i < len(normals_parameters_df.iloc[0, :]) and normals_parameters_df.iloc[row, i] != None 
                   and not pd.isna(normals_parameters_df.iloc[row, i])):
                calculation = normals_parameters_df.iloc[row, i] 
                i+=1
                el.fill_elements(wmo_id, wmo_parameter, row_template, calculation, element_station_df)
                row_template+=1
        
        #create the csv file 
        one_station_path = os.path.join(path, station_name + ".csv")
        station_temp_df.to_csv(one_station_path, index=False)
        print(station_name + " created") 


if __name__ == "__main__":
    main()
