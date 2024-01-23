import pandas as pd
import StationList 

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
    one_station.fill_station_data()


    #create the csv file 
    one_station_path = "path" #enter the path here with the station name
    station_temp_df.to_csv(one_station_path, index=False)
    print("station Name created") #enter the station name here


