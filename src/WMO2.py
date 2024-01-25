import os
import pandas as pd
from Elements import Elements
from StationList import StationList
from Template import Template

def main():
    wmo_data_set_path = r"C:\Users\harschn\Documents\PortableGit\WMO-Normals\resources\goose.csv" #input("Please enter the path to the WMO Data Set: ").replace('"', '')
    wmo_data_set_df = pd.read_csv(wmo_data_set_path)

    station_list_path = r"C:\Users\harschn\Documents\PortableGit\WMO-Normals\resources\StationList.csv" #input("Please enter the Station List: ").replace('"', '')
    station_list_df = pd.read_csv(station_list_path)
    
    normal_parameters_path = r"C:\Users\harschn\Documents\PortableGit\WMO-Normals\resources\NormalID_to_WMOParameterID.csv" #input("Please enter the path to the Normal ID to WMO Parameter ID: ").replace('"', '')
    normals_parameters_df = pd.read_csv(normal_parameters_path, header = 1)

    path = r"C:\Users\harschn\Documents\PortableGit\WMO-Normals\resources" #input("Enter the path you want all the files to output to: ").replace('"', '')

    template_df = Template.create_template(pd.DataFrame(), normals_parameters_df)

    """ IN PROGRESS
    bool = ""
    while (bool != "quit"):
        modification = input("Please enter any other information you need to input for a station (NOT Name, Country, WMO-ID, WIGOS-ID, Lat, Long, Elevation)" + 
                            "\nEnter it in the format parameter_name:row:col:insert or append" + 
                            "\nTo exit, enter quit\n")
        if (modification.lower() == "quit"):
            bool = modification.lower()
        else:
            Template.modify_template(template_df, modification)

    """
    
    all_stations = wmo_data_set_df.groupby('ENG_STN_NAME')

    for station_name, station_df in all_stations:
        # fill the information about the station
        station_temp_df = template_df.copy()
        one_station = StationList(station_temp_df, station_list_df, station_name)
        wmo_id = one_station.fill_station_data() 

        el = Elements(station_temp_df, normals_parameters_df)
        all_elements = station_df.groupby("NORMAL_ID")
        quintile_count = 0
        for id, element_station_df in all_elements:
            row = el.find_element_row(id) 
            wmo_name = normals_parameters_df.iloc[row, 3]
            wmo_parameter = normals_parameters_df.iloc[row, 2]
            row_template = el.find_wmo_name(wmo_name, 13) + 3
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
