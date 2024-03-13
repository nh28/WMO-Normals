class StationList:
    name_key = {"Station_Name": ["Station Name"], "Country_Name": ["Province"], "WMO_Number": ["WMO-ID"] , "Latitude": ["Latitude"], "Longitude": ["Longitude"], "Station_Height": ["Elevation (m)"],
                "WMO Integrated Global Observing System (WIGOS) Station Identifier (if available)": ["WIGOS-ID"]}

    """
    This class represents the fuctions related to the StationList.

    Attributes:
    name_key: This is a dictionary of all the header information that is contained in the StationList csv that will be filled into the template.
    template: This is the DataFrame of template for the station.
    station_list: This is the DataFrame that holds the StationList csv.
    station_id: This is the current station's id.
    """

    def __init__(self, template, station_list, station_id=None):
        """
        Initialize a new instance of StationList.

        Parameters:
        template: This is the DataFrame of template for the station.
        station_list: This is the DataFrame that holds the StationList csv.
        station_id: This is the current station's id.
        """
        self.template = template
        self.station_list = station_list
        self.station_id = station_id if station_id is not None else ""

    def find_in_temp(self, key):
        """
        Finds the location of a key in the header information in the template.

        Parameters:
        key: The value to find in the template.

        Returns:
        Array (int): This contains the row and columns that represents the location of the key in the template. Returns an array with None, otherwise.

        Example:
        >>> find_in_temp('Station_Name')
        [5, 0]
        >>> find_in_temp('random value')
        [None, None]
        """
        dim_row = 0
        while self.template.iloc[dim_row, 0] != "Principal Climatological Surface Parameters":
            dim_row+=1

        for r in range(dim_row):
            for c in range(len(self.template.columns)):
                if self.template.iloc[r, c] == key:
                    return [r, c]
        return [None, None]

    def fill_key(self):
        """
        Parses through the dictionary and appends the column location of each value in the StationList DataFrame.

        Parameters:
        None

        Returns:
        None

        Example:
        >>> print(names_key)
        name_key = {"Station_Name": ["Station Name"], "Country_Name": ["Province"], "WMO_Number": ["WMO-ID"] , "Latitude": ["Latitude"], "Longitude": ["Longitude"], "Station_Height": ["Elevation (m)"],
                "WMO Integrated Global Observing System (WIGOS) Station Identifier (if available)": ["WIGOS-ID"]}
        >>> fill_key()
        >>> print(names_key)
        {'Station_Name': ['Station Name', 17], 'Country_Name': ['Province', 8], 'WMO_Number': ['WMO-ID', 4], 'Latitude': ['Latitude', 18], 'Longitude': ['Longitude', 10], 'Station_Height': ['Elevation (m)', 11],
                'WMO Integrated Global Observing System (WIGOS) Station Identifier (if available)': ['WIGOS-ID', 5]}
        """
        for key, value in self.name_key.items():
            if len(self.name_key[key]) == 1:
                found = False
                for column_name in self.station_list.columns:
                    if column_name == value[0]:
                        found = True
                        self.name_key[key].append(self.station_list.columns.get_loc(column_name))
                        
                if not found:
                    self.name_key[key].append(-1)

    
    def find_station_row(self):
        """
        Finds the row that contain all the information for the station in the StationList dataframe.

        Parameters:
        None

        Returns:
        int: The index of where the station information is in the StationList, and returns -1 otherwise.

        Example:
        >>> print(station_id)
        38000000
        >>> find_station_row()
        23
        """
        virtual_station_id_col = self.station_list["VIRTUAL_STN_ID"]
        for index, value in virtual_station_id_col.items():
            if value == self.station_id:
                return index
        return -1
    
    def fill_station_data(self):
        """
        Fills all the station data for the given station.

        Parameters:
        None

        Returns:
        Array (str): name_wmo is returned and contains the station name and the wmo number.

        Example:
        >>> fill_station_data()
        ['ALERT CLIMATE', '71355']
        """
        name_wmo = ["",""]
        row = self.find_station_row()
        for key, value in self.name_key.items():
            if (value[1] != -1):
                location = self.find_in_temp(key)            
                data = str(self.station_list.iloc[row, value[1]])

                #rounding
                index = data.find(".")
                if (index != -1):
                    if int(data[(index + 1):]) >= 5:
                        data = int(data[:index]) + 1
                    else:
                        data = data[:index] 
                    
                if (key == "Latitude" or key == "Longitude"):
                    translation_table = str.maketrans({"'": "|", '"': "|", "°": "|"})
                    data = data.translate(translation_table)    
                if (key == "WMO_Number"):
                    name_wmo[1] = data
                if (key == "Station_Name"):
                    name_wmo[0] = data

                if (key == "Station_Name" or key == "Country_Name"):
                    self.template.iloc[location[0], location[1] + 1] = data   
                else:
                    self.template.iloc[location[0] + 1, location[1]] = data        
        return name_wmo
             
                    

