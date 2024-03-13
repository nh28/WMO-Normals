import os
import pandas as pd
from Elements import Elements
from StationList import StationList
from Template import Template

@staticmethod
def list_all_stations(station_list_df):
    """
    A static method creates an array that contains the names of all the stations that have data in the data set.

    Parameters:
    station_list_df: The StationList DataFrame that contains a list of all the stations, and whether or not they have a virtual id.

    Returns:
    Array (str): An array that contains all the station names.

    Example:
    >>> list_all_stations(station_list_df)
    ['ALERT CLIMATE', 'ARVIAT CLIMATE', 'ATIKOKAN (AUT)', 'BAGOTVILLE A', 'BAKER LAKE CLIMATE', 'BANCROFT AUTO', 'BANFF CS', 'BIG TROUT LAKE', 'BUFFALO NARROWS (AUT)', ...]
    """
    all_s = []
    all_stations = station_list_df.groupby("Station Name")
    for name, station_df in all_stations:
        if not pd.isna(station_df["VIRTUAL_STN_ID"].iloc[0]):
            all_s.append(name)
    return all_s

@staticmethod
def only_one_station(wmo_data_set_df, station_list_df, station):
    """
    A static method returns the DataFrame for only one station out of all the stations.

    Parameters:
    wmo_data_set_df: The DataFrame that contains the information of all the stations.
    station_list_df: The StationList DataFrame.
    station: The name of the station we want to get the DataFrame for.

    Returns:
    DataFrame: Returns the portion of the collective DataFrame for the specific station, and if the station doesn't exist it returns a blank DataFrame.

    Example:
    >>> only_one_station(wmo_data_set_df, station_list_df, 'BAGOTVILLE A')
            STN_ID  NORMAL_ID  ... DATE_CALCULATED  NORMAL_PERIOD_ID
    22455  54000000          1  ...       1/12/2024                 4
    22456  54000000          1  ...       1/12/2024                 4
    22457  54000000          1  ...       1/12/2024                 4
    22458  54000000          1  ...       1/12/2024                 4
    22459  54000000          1  ...       1/12/2024                 4
    ...         ...        ...  ...             ...               ...
    23003  54000000        192  ...       1/12/2024                 4
    23004  54000000        192  ...       1/12/2024                 4
    23005  54000000        192  ...       1/12/2024                 4
    23006  54000000        192  ...       1/12/2024                 4
    23007  54000000        192  ...       1/12/2024                 4
    """
    station_id = ""
    all_stations = station_list_df.groupby("Station Name")
    for name, station_df in all_stations:
        if name == station:
            station_id = station_df["VIRTUAL_STN_ID"].iloc[0]

    all_station_data = wmo_data_set_df.groupby("STN_ID")
    for id, station_data_df in all_station_data:
        if(id == station_id):
            return station_data_df
    return pd.DataFrame()

@staticmethod
def convert(wmo_data_set_df, template_df, station_list_df, normals_parameters_df, folder_path_out):
    """
    A static method fills all the information into the template(s) and then converts them to csv.

    Parameters:
    wmo_data_set_df: The DataFrame with the station(s) data.
    template_df: The empty template that will be used for each station.
    station_list_df: The StationList DataFrame that contains the header information for all the stations.
    normals_parameters_df: The Normal ID to Parameter ID DataFrame.
    folder_path_out: The location of the Output folder that all the csv files will be placed into.

    Returns:
    None
    """
    all_stations = wmo_data_set_df.groupby('STN_ID')
    for station_id, station_df in all_stations:
        
        this_station_template_df = template_df.copy()
        single_station = StationList(this_station_template_df, station_list_df, station_id)
        name_wmo = single_station.fill_station_data() 

        elements_parameters = Elements(this_station_template_df, normals_parameters_df)
        elements_parameters.fill_element_headers(name_wmo[1])

        all_elements = station_df.groupby("NORMAL_ID")
        quintile_count = 0
        for id, element_df in all_elements:
            row_in_normals_parameters = elements_parameters.find_element_row(id) 
            translation_table = str.maketrans({"≥": ">=", "≤": "<="})
            wmo_element_name = normals_parameters_df.iloc[row_in_normals_parameters]["Parameter Name"].translate(translation_table)
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
                elements_parameters.fill_elements(row_in_station_template, calculation, element_df)
                row_in_station_template+=1

        one_station_path = os.path.join(folder_path_out, "1991-2020_Normals_Canada_" + name_wmo[0].replace("/", "_") + ".csv")
        os.makedirs(os.path.dirname(one_station_path), exist_ok=True)
        this_station_template_df.to_csv(one_station_path, index=False)


