class Elements:
    
    def __init__(self, template, normals_parameters):
        self.template = template
        self.normals_parameters = normals_parameters

    def find_element_row(self, id):
        num = 1;
        while (num < len(self.normals_parameters)):
            if str(id) == self.normals_parameters.iloc[num, 0]:
                return num   
            num+=1
        return -1
    
    def find_wmo_name(self, wmo_name, dim_row):
        num = dim_row;
        while (num < len(self.template)):
            if wmo_name == self.template.iloc[num, 1]:
                return num   
            num+=1
        return -1
            
    def fill_elements(self, wmo_id, wmo_parameter, row_index, calculation, element_station_df):
        col_in_data_set = 0
        if calculation in ["Sum", "Count", "Mean", "Max", "Min", "Q0", "Q1", "Q2", "Q3", "Q4", "Q5"]:
            col_in_data_set = 5
        if calculation in ["MinDate", "MaxDate"]:
            col_in_data_set = 6
        if calculation == "NOY":
            col_in_data_set = 10
        
        col_in_temp = 4
        self.template.iloc[row_index, (col_in_temp - 4)] = wmo_id
        self.template.iloc[row_index, (col_in_temp - 3)] = wmo_parameter
        self.template.iloc[row_index, (col_in_temp - 2)] = calculation
        self.template.iloc[row_index, (col_in_temp - 1)] = self.get_calculation_num(calculation);
        for index, value in element_station_df.iloc[:, col_in_data_set].items():
            self.template.iloc[row_index, col_in_temp] = value
            col_in_temp+=1


    def get_calculation_num(self, calculation):
        if calculation == "Mean":
            return 1
        if calculation == "Max":
            return 2
        if calculation == "Min":
            return 3
        if calculation == "Sum":
            return 4
        if calculation == "Count":
            return 5
        if calculation == "Q0":
            return 6
        if calculation == "Q1":
            return 7
        if calculation == "Q2":
            return 8
        if calculation == "Q3":
            return 9
        if calculation == "Q4":
            return 10
        if calculation == "Q5":
            return 11
        if calculation == "Median":
            return 12
        if calculation == "SDMean":
            return 13
        if calculation == "SDMeanD":
            return 14
        if calculation == "MaxDate":
            return 15
        if calculation == "MinDate":
            return 16
        if calculation == "MinMon":
            return 17
        if calculation == "DMinMon":
            return 18
        if calculation == "MaxMon":
            return 19
        if calculation == "DMaxMon":
            return 20
        if calculation == "NOY":
            return 98
        if calculation == "Custom":
            return 99



            

