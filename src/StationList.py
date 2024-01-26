class StationList:
    name_key = {"Station_Name": ["Station Name"], "Country_Name": ["Province"], "WMO_Number": ["WMO-ID"] , "Latitude": ["Latitude"], "Longitude": ["Longitude"], "Station_Height": ["Elevation (m)"],
                "WMO Integrated Global Observing System (WIGOS) Station Identifier (if available)": ["WIGOS-ID"]}

    def __init__(self, template, station_list, station_id=None):
        self.template = template
        self.station_list = station_list
        self.station_id = station_id if station_id is not None else ""

    def add_names_key(self, list):
        split_list = list.split(':')
        self.names_key[split_list[0]] = [split_list[1], split_list[2]]

    def find_in_temp(self, key):
        dim_row = 0
        while self.template.iloc[dim_row, 0] != "Principal Climatological Surface Parameters":
            dim_row+=1

        for r in range(dim_row):
            for c in range(len(self.template.columns)):
                if self.template.iloc[r, c] == key:
                    return [r, c]

    def fill_key(self):
        for key, value in self.name_key.items():
            for column_name in self.station_list.columns:
                if column_name == value[0]:
                    self.name_key[key].append(self.station_list.columns.get_loc(column_name))

    
    def find_station_row(self):
        virtual_station_id_col = self.station_list["VIRTUAL_STN_ID"]
        for index, value in virtual_station_id_col.items():
            if value == self.station_id:
                return index
        return -1
    
    def fill_station_data(self):
        name_wmo = ["",""]
        row = self.find_station_row()
        for key, value in self.name_key.items():
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
             
                    

