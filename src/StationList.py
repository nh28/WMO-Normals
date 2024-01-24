class StationList:
    name_key = {"WMO_Number": ["WMO-ID", 5] , "Latitude": ["Latitude", 11], "Longitude": ["Longitude", 12], "Station_Height": ["Elevation (m)", 13],
                "WMO Integrated Global Observing System (WIGOS) Station Identifier (if available)": ["WIGOS-ID", 6]}
    dim_row = 13
    dim_col = 3

    def __init__(self, template, station_list, station_name=None):
        self.template = template
        self.station_list = station_list
        self.station_name = station_name if station_name is not None else ""

    def add_names_key(self, list):
        split_list = list.split(':')
        self.names_key[split_list[0]] = [split_list[1], split_list[2]]

    def change_dim_row(self, row):
        self.dim_row = row
    
    def change_dim_col(self, col):
        self.dim_col = col

    def find_in_temp(self, key):
        for r in range(self.dim_row + 1):
            for c in range(self.dim_col + 1):
                if self.template.iloc[r, c] == key:
                    return [r, c]
        

    def find_station_row(self):
        num = 0;
        while (self.station_list.iloc[num, 1] is not None):
            if self.station_name == self.station_list.iloc[num, 1]:
                return num   
            num+=1
        return -1
    
    def fill_station_data(self):
        self.template.iloc[4, 1] = "CANADA"
        self.template.iloc[5, 1] = self.station_name
        
        wmo = ""
        row = self.find_station_row()
        for key, value in self.name_key.items():
            loca = self.find_in_temp(key)            
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
            self.template.iloc[loca[0] + 1, loca[1]] = data       
            if (key == "WMO_Number"):
                wmo = data
        return wmo
             
                    

