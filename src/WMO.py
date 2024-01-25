import os
import pandas as pd
from Elements import Elements
from StationList import StationList
from Template import Template

def main():
    while True:
        try:
            wmo_data_set_path = input("Please enter the path to the WMO Data Set: ").replace('"', '')
            wmo_data_set_df = pd.read_csv(wmo_data_set_path)
            break
        except FileNotFoundError:
            print("File not found. Please enter a valid path.")
        except pd.errors.EmptyDataError:
            print("The file is empty. Please enter a valid path.")
        except Exception as e:
            print("An error occurred:", e)
    
    while True:
        try:
            station_list_path = input("Please enter the path to the Station List: ").replace('"', '')
            station_list_df = pd.read_csv(station_list_path)
            break
        except FileNotFoundError:
            print("File not found. Please enter a valid path.")
        except pd.errors.EmptyDataError:
            print("The file is empty. Please enter a valid path.")
        except Exception as e:
            print("An error occurred:", e)
        
    
    while True:
        try:
            normal_parameters_path = input("Please enter the path to the Normal ID to WMO Parameter ID: ").replace('"', '')
            normals_parameters_df = pd.read_csv(normal_parameters_path, header = 1)
            break
        except FileNotFoundError:
            print("File not found. Please enter a valid path.")
        except pd.errors.EmptyDataError:
            print("The file is empty. Please enter a valid path.")
        except Exception as e:
            print("An error occurred:", e)
    
    path = input("Enter the path you want all the files to output to: ").replace('"', '')

    template_df = Template.create_template(pd.DataFrame(), normals_parameters_df)

    bool = ""
    while (bool != "quit"):
        modification = input("\nPlease enter any other information you need to input for a station (NOT Name, Country, WMO-ID, WIGOS-ID, Lat, Long, Elevation)" + 
                            "\nEnter it in the format parameter_name:row:col" + 
                            "\nTo exit, enter quit\n")
        if (modification.lower() == "quit"):
            bool = modification.lower()
        else:
            Template.modify_template(template_df, modification)
    
    all_stations = wmo_data_set_df.groupby('ENG_STN_NAME')
    for station_name, station_df in all_stations:
        
        this_station_template_df = template_df.copy()
        single_station = StationList(this_station_template_df, station_list_df, station_name)
        wmo_id = single_station.fill_station_data() 

        elements_parameters = Elements(this_station_template_df, normals_parameters_df)

        all_elements = station_df.groupby("NORMAL_ID")
        quintile_count = 0
        for id, element_df in all_elements:
            row_in_normals_parameters = elements_parameters.find_element_row(id) 
            wmo_name = normals_parameters_df.iloc[row_in_normals_parameters, 3]
            wmo_parameter = normals_parameters_df.iloc[row_in_normals_parameters, 2]
            row_in_station_template = elements_parameters.find_wmo_name(wmo_name, 13) + 3

            if (id in [185, 186, 187, 188, 189, 190]):
                row_in_station_template += quintile_count
                quintile_count+=1

            col_in_station_temp = 5
            while (col_in_station_temp < len(normals_parameters_df.iloc[0, :]) and normals_parameters_df.iloc[row_in_normals_parameters, col_in_station_temp] != None 
                   and not pd.isna(normals_parameters_df.iloc[row_in_normals_parameters, col_in_station_temp])):
                calculation = normals_parameters_df.iloc[row_in_normals_parameters, col_in_station_temp] 
                col_in_station_temp+=1
                elements_parameters.fill_elements(wmo_id, wmo_parameter, row_in_station_template, calculation, element_df)
                row_in_station_template+=1
         
        while True:
            try:
                one_station_path = os.path.join(path, station_name + ".csv")
                this_station_template_df.to_csv(one_station_path, index=False)
                print(station_name + " created") 
                break
            except Exception as e:
                path = input("An error occurred while constructing the file path, please paste a valid path")


if __name__ == "__main__":
    main()
