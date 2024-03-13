import os
import sys
import logging
import pandas as pd
import PySimpleGUI as sg
from Template import Template
from StationList import StationList 
import WMO as WMO
import zlib
import oracledb

folder_path_in = os.path.abspath("Input/")
folder_path_out = os.path.abspath("Output/")
driver = 'oracle'
ARKEON_host = 'ARC-CLUSTER.CMC.EC.GC.CA'
ARKEON_port = '1521'
ARKEON_service = 'archive.cmc.ec.gc.ca'
connection = None
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='WMO.log', # Log file name
                    filemode='w')

def connect(usern, passw):
    """
    Connect to database

    Parameters:
    usern: Username that the user entered
    passw: Password that the user entered

    Returns:
    src_conn: The connection to the database
    """
    try:
        src_conn = oracledb.connect(
            user = usern,
            password = passw,
            host = ARKEON_host,
            port = ARKEON_port,
            service_name = ARKEON_service
        )
        return src_conn, True
    except oracledb.DatabaseError as err:
        error, = err.args
        logging.error('Unable to establish connection, due to: %s', error.message)
        sg.popup_error("Invalid username and password")
        return None, False


def get_dataframe():
    """
    Turn the SQL query into a DataFrame

    Parameters:
    None

    Returns:
    pd.DataFrame(rows, columns = column_headers): A DataFrame of the normals query
    """
    
    query =\
    '''
    SELECT
        *
    FROM
        NORMALS_WMO_9120.normals_data       
    '''

    cursor = connection.cursor()

    if cursor is not None:
        logging.info('Executing query...')
        logging.info(query)
        try:
            cursor.execute(query)
        except Exception as err:
            msg = 'Unable to execute query, due to: %s' % str(err)
            logging.error(msg)
        logging.info('Query execution complete.')
    else:
        logging.error('Unable to execute query, due to: no cursor.')
    
    column_headers = [desc[0] for desc in cursor.description]
    rows = []
    for row in cursor:
       rows.append(row)
        
    cursor.close()
    logging.info('Cursor closed.')

    return pd.DataFrame(rows, columns = column_headers)

def check(name_of_file, head):
    """
    Checks that all the Input files are named correctly, have data, and are in the right location.

    Parameters:
    name_of_file: Name of the file that is being checked.
    head: What row the header of the file is at.

    Returns:
    Array (DataFrame, str): If everything is correct, the method will return the csv converted into a DataFrame and no message. Else, it will return None and the error message.

    Example:
    >>> check("1991-2020_WMO_Normals_Data.csv", 0)
             STN_ID  NORMAL_ID  ... DATE_CALCULATED  NORMAL_PERIOD_ID
    27229  66000000          1  ...       1/12/2024                 4
    27230  66000000          1  ...       1/12/2024                 4
    27231  66000000          1  ...       1/12/2024                 4
    27232  66000000          1  ...       1/12/2024                 4
    27233  66000000          1  ...       1/12/2024                 4
    ...
    """
    try:
        path = os.path.join(folder_path_in, name_of_file)
        df = pd.read_csv(path, header = head)
        return df, None  
    
    except FileNotFoundError:
        logging.error(name_of_file + " not named correctly or not in the right location.")
        return None, "Make sure " + name_of_file + " is named correctly and is in the right location. Then rerun the program."
    except pd.errors.EmptyDataError:
        logging.error(name_of_file + " is empty.")
        return None, "Make sure " + name_of_file + " has data stored in it. Please fix and rerun the program."
    except Exception as e:
        logging.error("An error occured: ", e)
        return None, f"An error occurred: {str(e)}"

wmo_station, error_message2 = check("StationList.csv", 0)
wmo_parameters, error_message3 = check("NormalID_to_WMOParameterID.csv", 1)
wmo_data = None
template_df = None
if (wmo_station is not None) and (wmo_parameters is not None):
    all_stations = WMO.list_all_stations(wmo_station)
    template_df = Template.create_template(pd.DataFrame(), wmo_parameters)
    gen_station = StationList(template_df, wmo_station)
    gen_station.fill_key()

    logging.info("Program Started")
    sg.theme('Light Green 1') 
    layout = [[sg.Text('WMO Normals Reformatter', justification='center', size=(20, 1), font=('Arial', 12, 'bold'), enable_events=True)],
                [sg.Text("")],
                [sg.Text("Please enter your ARKEON access before proceeding:")],
                [sg.Text("Username: "), sg.Input(key = "-user-")],
                [sg.Text("Password: "), sg.InputText(key = "-pw-", password_char='*')],
                [sg.Button("Login")],
                [sg.Text("")],
                [sg.Text("Please enter any other information you need to input for a station (NOT Name, Country, WMO-ID, WIGOS-ID, Lat, Long, Elevation)")],
                [sg.Text("Station Parameter Name: "), sg.Input(key = '-IN1-')],
                [sg.Text("Template Parameter Name: "), sg.Input(key = "-IN2-")],
                [sg.Text("Row in Template: "), sg.Input(key = "-IN3-")],
                [sg.Text("Column in Template: "), sg.Input(key = "-IN4-")],
                [sg.Button("Add to Template")],
                [sg.Text("")],
                [sg.Text("Download One Station:"), sg.Combo(values=all_stations, key="-STATION-", enable_events= True), sg.Button("Download This Station")],
                [sg.Text("Download All Stations:"), sg.Button("Download All Files")],
                [sg.Text("")],
                [sg.Exit()],]

    window = sg.Window("WMO Normals Reformatter", layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        
        if (event == "Login"):
            if wmo_data is None:
                username = values['-user-']
                password = values['-pw-']
                connection, success = connect(username, password)
                if success:
                    wmo_data = get_dataframe()
                    sg.popup("Login Successful")
            else:
                sg.popup_error("Already logged in")

        if wmo_data is not None:
            if(event == "Add to Template"):
                station_parameter_name = values['-IN1-'].strip()
                template_parameter_name = values['-IN2-'].strip()
                row = values['-IN3-'].strip()
                col = values['-IN4-'].strip()

                if station_parameter_name and template_parameter_name and row and col:
                    mod = Template.modify_template(template_df, station_parameter_name, template_parameter_name, row, col)
                    if mod[1] == 'pass':
                        template_df = mod[0]
                        gen_station.fill_key()
                        sg.popup("Successfully added to template.")
                        window["-IN1-"].update("")
                        window["-IN2-"].update("")
                        window["-IN3-"].update("")
                        window["-IN4-"].update("")
                    else:
                        sg.popup_error(mod[1])
                else:
                    sg.popup_error("Please enter values in all the fields.")

            if event == "Download This Station":
                if values["-STATION-"]:
                    station_data_df = WMO.only_one_station(wmo_data, wmo_station, values["-STATION-"])
                    if station_data_df.empty:
                        logging.error("Cannot find station in wmo data.")
                        sg.popup_error("Cannot find station.")
                    else:
                        window.disable()
                        sg.popup("Download starting...You will not be able to close the main window until the download is complete.")
                        WMO.convert(station_data_df, template_df, wmo_station, wmo_parameters, folder_path_out)
                        sg.popup("Complete. You can find the file at " + folder_path_out)
                        window.enable()
                else:
                    sg.popup_error("Please select a station to download.")

            if(event == "Download All Files"):
                window.disable()           
                sg.popup("Download starting...You will not be able to close the main window until the download is complete." +
                        "The program might say it is not reponding, but please check the output folder to confirm if nothing is happening. The estimated waiting time is 2 minutes.")
                WMO.convert(wmo_data, template_df, wmo_station, wmo_parameters, folder_path_out)
                sg.popup("Complete. You can find the files in " + folder_path_out)
                window.enable()
        else:
            sg.popup_error("Please log in")

    window.close()
    logging.info("Program ended")
    
else:  
    if (error_message2 is not None):
        logging.error(error_message2)
        sg.popup_error(error_message2)
    if (error_message3 is not None):
        logging.error(error_message3)
        sg.popup_error(error_message3)
