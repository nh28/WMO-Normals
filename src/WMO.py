import pandas as pd
import Elements
import StationList 

def main():
    wmo_data_set_path = input("Please enter the path to the WMO Data Set: ")
    # "C:\Users\nhars\WMO-Normals\resources\WMO.csv"
    wmo_data_set_df = pd.read_csv(wmo_data_set_path)

    template_path = input("Please enter the path to the WMO template")
    template_df = pd.read_csv(template_path)
    dim_row = input("Please indicate what row the station header ends")
    dim_col = input("Please indicate what col the station header ends")

    station_list_path = input("Please enter the Station List")
    station_list_df = pd.read_csv(station_list_path)

    normal_parameters_path = input("Please enter the path to the Normal ID to WMO Parameter ID")
    normals_parameters_df = pd.read_csv(normal_parameters_path)

    gen_station = StationList(template_df, station_list_df)
    gen_station.fill_station_indices(dim_row, dim_col)

    all_stations = wmo_data_set_df.groupby('ENG_STN_NAME')

    for station_name, station_df in all_stations:
        # fill the information about the station
        station_temp_df = template_df.copy()
        one_station = StationList(station_temp_df, station_list_df, station_name)
        wmo_id = one_station.fill_station_data() #might need to return the data frame instead

        el = Elements(station_temp_df, normals_parameters_df)
        all_elements = station_df.groupby("NORMAL_ID")
        for id, element_station_df in all_elements:
            row = el.find_element_row(id)
            wmo_name = normals_parameters_df.loc[row, 3]
            wmo_parameter = normals_parameters_df.loc[row, 2]
            row_index = el.find_wmo_name(wmo_name, dim_col)
            i = 5
            while (normals_parameters_df.loc[row, i] != None):
                calculation = normals_parameters_df.loc[row, i]
                el.fill_elements(wmo_id, wmo_parameter, row_index, calculation, element_station_df)
                row_index+=1

        #create the csv file 
        one_station_path = "path" #enter the path here with the station name
        station_temp_df.to_csv(one_station_path, index=False)
        print("station Name created") #enter the station name here


if __name__ == "__main__":
    main()