import pandas as pd


class Template:

    @staticmethod
    def create_template(df, normals_parameter):
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
            df.at[(row_index + 1), 1] = row["Parameter Name"]
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
                df.at[(row_index + 1), 0] = "Secondary and Other Climatological Surface Parameters (add as needed)"
                df.at[(row_index + 2), 0] = ""
                df.at[(row_index + 3), 0] = ""
                row_index += 4

        df.columns = df.iloc[0]
        return df[1:].reset_index(drop = True)

    """ IN PROGRESS
    @staticmethod
    def modify_template(template_df, user):
        info = user.split(':')
        if info[3] == "insert":
            df1 = template_df.iloc[:int(info[1])]
            df2 = template_df.iloc[int(info[1]):]
            df2 = df2.append(pd.DataFrame({"", ""}), ignore_index = True)
            template_df = pd.concat([df1, df2], ignore_index=True)
            template_df.at[info[1], info[2]] = info[0]
        else:
            template_df.at[info[1], info[2]] = info[0]
    """


            




