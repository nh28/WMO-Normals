class StationList:
    station_indices_dict = {}

    def __init__(self, template, station_list, station_name=None):
        self.template = template
        self.station_list = station_list
        self.station_name = station_name if station_name is not None else ""

    def fill_station_indices(self, dim_row, dim_col):
        self.station_list
        # make this a key: [parameterName, value: [col index in station list, row, col] or [] if not
        #hard to do since the station list headers do not match the template names
        #create another file? extend to a previous file?

    def find_station_row(self):
        for num in range(1,self.station_list.value_counts()):
            if self.station_name == self.station_list.loc[num, 1]:
                return num   
        return -1
    
    def fill_station_data(self):
        self.template.at[5, 1] = "CANADA"
        self.template.at[6, 1] = self.station_name

        row = self.find_station_row()
        for key, value in StationList.station_indices_dict.items():
            if value.size() != 0: #later add if the station does not exist
                value = self.station_list.loc[row, StationList.station_indices_dict[key][0]]
                if (key == "Latitude" or key == "Longitude"):
                    translation_table = str.maketrans({"'": "|", '"': "|", "°": "|"})
                    value = value.translate(translation_table)

                self.template.loc[StationList.station_indices_dict[key][1], 
                                  StationList.station_indices_dict[key][2]] = value
                    

