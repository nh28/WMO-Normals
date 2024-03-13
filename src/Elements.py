import re
class Elements:
    """
    This class represents the different elements that need to be filled into the template.

    Attributes:
    template (DataFrame): This is the template that should only have the station header filled in. 
    normals_parameters: This is the file containing the different elements' names, ids, and calculations that will need to be filled into the template.
    """

    def __init__(self, template, normals_parameters):
        """
        Initialize a new instance of Elements.

        Parameters:
        template (DataFrame): This is the template that should only have the station header filled in. 
        normals_parameters: This is the file containing the different elements' names, ids, and calculations that will need to be filled into the template.
        """
        self.template = template
        self.normals_parameters = normals_parameters

    def find_element_row(self, id):
        """
        Finds the row of the Normals ID to Parameters ID csv files that the element is in.

        Parameters:
        id: The Normal ID of the element.

        Returns:
        int: The row of the element if found. If not found, then returns -1.

        Example:
        >>> find_element_row(115)
        7
        >>> find_element_row(200)
        -1
        """
        num = 0;
        while (num < len(self.normals_parameters)):
            if id == self.normals_parameters.iloc[num]["Normal ID"]:
                return num   
            num+=1
        return -1
    
    def find_wmo_name(self, wmo_name):
        """
        Finds element's WMO name in the template.

        Parameters:
        wmo_name: The WMO name that the element goes by that would be shown in the template.

        Returns:
        int: The row of the element if found. If not found, then returns -1.

        Example:
        >>> find_wmo_name('Precipitation_Total')
        18
        >>> find_wmo_name('Another Element')
        -1
        """
        num = 0;
        while (num < len(self.template)):
            if wmo_name == self.template.iloc[num, 1]:
                return num   
            num+=1
        return -1
            
    def fill_elements(self, row_index, calculation, element_station_df):
        """
        Finds element's WMO name in the template.

        Parameters:
        wmo_id: The station's WMO id.
        wmo_parameter: The parameter code of the element being filled in.
        row_index: The location of the element in the template that we are trying to fill in.
        calculation: The name of the type of calculation we are filling in.
        element_station_df: The Dataframe of the current station with just the element we are trying to fill in. 

        Returns:
        void

        Example:
        >>> print(this_station_template_df.iloc[17:23,:5])
        0  World Meteorological Organization Climate Normals for 1991-2020                  NaN  ...       NaN     NaN
        17                                     Parameter_Code                    Parameter_Name  ...       NaN     NaN
        18                                                  1               Precipitation_Total  ...       NaN     NaN
        19                                                                                  NaN  ...       NaN     NaN
        20                                         WMO_Number                    Parameter_Code  ...  December  Annual
        21                                                                                  NaN  ...       NaN     NaN
        22                                                                                  NaN  ...       NaN     NaN
        >>> elements_parameters.fill_elements(name_wmo[1], wmo_parameter, row_in_station_template, calculation, element_df)
        >>> print(this_station_template_df.iloc[17:23,:5])
        0  World Meteorological Organization Climate Normals for 1991-2020                  NaN  ...       NaN     NaN
        17                                     Parameter_Code                    Parameter_Name  ...       NaN     NaN
        18                                                  1               Precipitation_Total  ...       NaN     NaN
        19                                                                                  NaN  ...       NaN     NaN
        20                                         WMO_Number                    Parameter_Code  ...  December  Annual
        21                                              71356                                 1  ...      11.7     NaN
        22                                              71356                                 1  ...      24.0     NaN
        """
        col_in_data_set = ""
        date = False
        if calculation in ["Sum", "Count", "Mean", "Max", "Min", "Q0", "Q1", "Q2", "Q3", "Q4", "Q5"]:
            col_in_data_set = "VALUE"
        if calculation in ["MinDate", "MaxDate"]:
            col_in_data_set = "FIRST_OCCURRENCE_DATE"
            date = True
        if calculation == "NOY":
            col_in_data_set = "YEAR_COUNT_NORMAL_PERIOD"
        
        col_in_temp = 3
        months = element_station_df.groupby("MONTH")
        for month, month_df in months:
            value = month_df[col_in_data_set].iloc[0]
            if date:
                yyyy_mm_dd_t = re.split(r'[- ]', str(value))
                if month == 13:
                    value = yyyy_mm_dd_t[0] + "/" + yyyy_mm_dd_t[1] + "/" + yyyy_mm_dd_t[2]
                else:
                    value = yyyy_mm_dd_t[0] + "/" + yyyy_mm_dd_t[2]
            col = col_in_temp + int(month)
            self.template.iloc[row_index, col] = value
        

    def fill_element_headers(self, wmo_id):
        """
        Fills the WMO ID, parameter name, calculation, and calculation code for each of the elements in the station, regardless if they are empty.

        Parameters:
        wmo_id: The station's WMO ID.

        Returns:
        None
        """
        elements = self.normals_parameters.groupby("Parameter Name")

        for element, element_df in elements:
            translation_table = str.maketrans({"≥": ">=", "≤": "<="})
            element = element.translate(translation_table)
            element_row = self.find_wmo_name(element)
            wmo_parameter = self.template.iloc[element_row, 0]

            calculations_1 = element_df.groupby("Calculation Name")
            template_row = element_row + 3
            for calculation, calculations_1_df in calculations_1:
                self.template.iloc[template_row, 0] = wmo_id
                self.template.iloc[template_row, 1] = wmo_parameter
                self.template.iloc[template_row, 2] = calculation
                self.template.iloc[template_row, 3] = self.get_calculation_num(calculation)
                template_row+=1
            
            NOY_or_Date = self.normals_parameters.columns.get_loc("Calculation Name") + 1
            calculations_2 = element_df.groupby(element_df.columns[NOY_or_Date])
            for calculation, calculations_2_df in calculations_2:
                self.template.iloc[template_row, 0] = wmo_id
                self.template.iloc[template_row, 1] = wmo_parameter
                self.template.iloc[template_row, 2] = calculation
                self.template.iloc[template_row, 3] = self.get_calculation_num(calculation)
                template_row+=1
            

    def get_calculation_num(self, calculation):
        """
        Returns the corresponding calculation number based on the calculation name.

        Parameters:
        calculation: The name of the calculation.

        Returns:
        int: Returns the corresponding calculation number.

        Example:
        >>> get_calculation_num('Mean')
        1
        """
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



            

