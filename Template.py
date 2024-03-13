import pandas as pd

from StationList import StationList


class Template:

    @staticmethod
    def create_template(df, normals_parameter):
        """
        A static method that creates an empty template that conforms to the WMO standards.

        Parameters:
        df: An empty DataFrame that is to be used for the template.
        normals_parameters: The DataFrame of the Normals ID to Parameters ID to be iterated so that each parameter has a table in the template.

        Returns:
        DataFrame: An empty WMO template.

        Example:
        >>> create_template(pd.DataFrame(), wmo_parameters)
        0   World Meteorological Organization Climate Normals for 1991-2020  NaN  NaN  NaN  NaN  ...  NaN  NaN  NaN  NaN  NaN
        0    Single Station Data Sheet For All Climatologic...               NaN  NaN  NaN  NaN  ...  NaN  NaN  NaN  NaN  NaN
        1                                                                    NaN  NaN  NaN  NaN  ...  NaN  NaN  NaN  NaN  NaN
        2                                Station Header Record               NaN  NaN  NaN  NaN  ...  NaN  NaN  NaN  NaN  NaN
        3                                                                    NaN  NaN  NaN  NaN  ...  NaN  NaN  NaN  NaN  NaN
        4                                         Country_Name               NaN  NaN  NaN  NaN  ...  NaN  NaN  NaN  NaN  NaN
        ..                                                 ...               ...  ...  ...  ...  ...  ...  ...  ...  ...  ...
        """
        df.at[0,0] = "World Meteorological Organization Climate Normals for 1991-2020"
        df.at[1, 0] = "Single Station Data Sheet For All Climatological Surface Parameters"
        df.at[2, 0] = ""
        df.at[3, 0] = "Station Header Record"
        df.at[4, 0] = ""
        df.at[5, 0] = "Country_Name"
        df.at[6, 0] = "Station_Name"
        df.at[7, 0] = ""
        df.at[8, 0] = "WMO_Number"
        df.at[8, 1] = "Latitude"
        df.at[8, 2] = "Longitude"
        df.at[8, 3] = "Station_Height"
        df.at[9, 0] = ""
        df.at[10, 0] = ""
        df.at[11, 0] = "WMO Integrated Global Observing System (WIGOS) Station Identifier (if available)"
        df.at[12, 0] = ""
        df.at[13, 0] = ""
        df.at[14, 0] = ""
        df.at[15, 0] = "Principal Climatological Surface Parameters"
        df.at[16, 0] = ""
        df.at[17, 0] = ""

        row_index = 18
        for index, row in normals_parameter.iterrows():
            if index in [9, 10, 11, 12, 13]:
                continue
            df.at[row_index, 0] = "Parameter_Code"
            df.at[row_index, 1] = "Parameter_Name"
            df.at[row_index, 2] = "Units"

            df.at[(row_index + 1), 0] = row["Parameter Code"]
            translation_table = str.maketrans({"≥": ">=", "≤": "<="})
            df.at[(row_index + 1), 1] = row["Parameter Name"].translate(translation_table)
            df.at[(row_index + 1), 2] = row ["Units"]

            df.at[(row_index + 2), 0] = ""

            df.at[(row_index + 3), 0] = "WMO_Number"
            df.at[(row_index + 3), 1] = "Parameter_Code"
            df.at[(row_index + 3), 2] = "Calculation_Name"
            df.at[(row_index + 3), 3] = "Calculation_Code"
            df.at[(row_index + 3), 4] = "January"
            df.at[(row_index + 3), 5] = "February"
            df.at[(row_index + 3), 6] = "March"
            df.at[(row_index + 3), 7] = "April"
            df.at[(row_index + 3), 8] = "May"
            df.at[(row_index + 3), 9] = "June"
            df.at[(row_index + 3), 10] = "July"
            df.at[(row_index + 3), 11] = "August"
            df.at[(row_index + 3), 12] = "September"
            df.at[(row_index + 3), 13] = "October"
            df.at[(row_index + 3), 14] = "November"
            df.at[(row_index + 3), 15] = "December"
            df.at[(row_index + 3), 16] = "Annual"

            df.at[(row_index + 4), 0] = ""
            df.at[(row_index + 5), 0] = ""
            df.at[(row_index + 6), 0] = ""
            df.at[(row_index + 7), 0] = ""
            df.at[(row_index + 8), 0] = ""

            row_index += 9
            if (row["Parameter Code"] == 11):
                df.at[(row_index + 1), 0] = ""
                df.at[(row_index + 2), 0] = ""
                df.at[(row_index + 3), 0] = ""
                row_index += 4

            if (row["Parameter Code"] == 7):
                df.at[(row_index + 1), 0] = ""
                df.at[(row_index + 2), 0] = "Secondary and Other Climatological Surface Parameters (add as needed)"
                df.at[(row_index + 3), 0] = ""
                df.at[(row_index + 4), 0] = ""
                row_index += 5

        df.columns = df.iloc[0]
        return df[1:].reset_index(drop = True)

    @staticmethod
    def modify_template(template_df, station_parameter_name, template_parameter_name, row, col):
        """
        A static method that adds an element to the template if there is nothing in that cell and it does not go out of the DataFrame's boundry.

        Parameters:
        template_df: The current empty template that conforms to the WMO standards.
        station_parameter_name: The name of the new element recorded in the StationList csv file.
        template_parameter_name: The name of the new element to be displayed in the template.
        row: The row in which the new element will be inserted.
        col: The column in which the new element will be inserted.

        Returns:
        Array: An array with the either the DataFrame and a pass message or a None value with a message to why the insertion is not valid.

        Example:
        >>> modify_template(template_df, station_parameter_name, template_parameter_name, 7, 4)
        [template_df, 'pass']
        >>> modify_template(template_df, station_parameter_name, template_parameter_name, 7, 2)
        [None, 'Value already here']
        >>> modify_template(template_df, station_parameter_name, template_parameter_name, 100, 100)
        [None, 'Out of Bounds']
        """
        if int(row) < len(template_df) and int(col) < len(template_df.columns):
            if template_df.iloc[int(row), int(col)] is None or pd.isna(template_df.iloc[int(row), int(col)]):
                template_df.iloc[int(row), int(col)] = template_parameter_name
                StationList.name_key[template_parameter_name] = [station_parameter_name]
                return [template_df, 'pass']
            return [None, 'Value already here']
        return [None, 'Out of Bounds']


            




