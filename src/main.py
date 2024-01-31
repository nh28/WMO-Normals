import os
import time
import pandas as pd
import PySimpleGUI as sg
from Template import Template 
import WMO as WMO

folder_path_in = os.path.abspath("Input/")
folder_path_out = os.path.abspath("Output/")

def check_data():
    try:
        wmo_data_set_path = os.path.join(folder_path_in, "goose.csv")
        wmo_data_set_df = pd.read_csv(wmo_data_set_path)
        return wmo_data_set_df, None  
    
    except FileNotFoundError:
        return None, "Make sure 1991-2020_WMO_Normals_Data.csv is named correctly and is in the right location."
    except pd.errors.EmptyDataError:
        return None, "Make sure 1991-2020_WMO_Normals_Data.csv has data stored in it."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

def check_station():
    try:
        station_list_path = os.path.join(folder_path_in, "StationList.csv")
        station_list_df = pd.read_csv(station_list_path)
        return station_list_df, None  
    
    except FileNotFoundError:
        return None, "Make sure StationList.csv is named correctly and is in the right location."
    except pd.errors.EmptyDataError:
        return None, "Make sure StationList.csv has data stored in it."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

def check_parameters():
    try:
        normal_parameters_path = os.path.join(folder_path_in, "NormalID_to_WMOParameterID.csv")
        normals_parameters_df = pd.read_csv(normal_parameters_path, header = 1)
        return normals_parameters_df, None  
    
    except FileNotFoundError:
        return None, "Make sure NormalID_to_WMOParameterID.csv is named correctly and is in the right location."
    except pd.errors.EmptyDataError:
        return None, "Make sure NormalID_to_WMOParameterID.csv has data stored in it."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

def show_progress(wmo_data, template_df, wmo_station, wmo_parameters, folder_path_out):
    layout = [
        [sg.Text("Download starting...You will not be able to close this window until the download is complete.")],
        [sg.Text('Progress:')],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS-')]
    ]

    window = sg.Window('Progress', layout, finalize=True)
    progress_bar = window['-PROGRESS-']
    window.disable()

    for i in range(101):
        WMO.convert(wmo_data, template_df, wmo_station, wmo_parameters, folder_path_out)
        progress_bar.update_bar(i)
    
    window.close()

sg.theme('Light Green 1') 
layout = [[sg.Text('WMO Normals Reformatter', justification='center', size=(20, 1), font=('Arial', 12, 'bold'), enable_events=True)],
            [sg.Text("Please enter any other information you need to input for a station (NOT Name, Country, WMO-ID, WIGOS-ID, Lat, Long, Elevation)" + 
                            "\nEnter it in the format station_parameter_name:template_parameter_name:row:col")],
            [sg.Text("Station Parameter Name: "), sg.Input(key = '-IN1-')],
            [sg.Text("Template Parameter Name: "), sg.Input(key = "-IN2-")],
            [sg.Text("Row in Template: "), sg.Input(key = "-IN3-")],
            [sg.Text("Column in Template: "), sg.Input(key = "-IN4-")],
            [sg.Button("Add to Template")],
            [sg.Button("Download Files"), sg.Exit()],]

window = sg.Window("WMO Normals Reformatter", layout)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break

    wmo_data, error_message1 = check_data()
    wmo_station, error_message2 = check_station()
    wmo_parameters, error_message3 = check_parameters()
    if (wmo_data is not None) and (wmo_station is not None) and (wmo_parameters is not None):
        template_df = Template.create_template(pd.DataFrame(), wmo_parameters)
        if(event == "Add to Template"):
            station_parameter_name = values['-IN1-'].strip()
            template_parameter_name = values['-IN2-'].strip()
            row = values['-IN3-'].strip()
            col = values['-IN4-'].strip()

            if station_parameter_name and template_parameter_name and row and col:
                mod = Template.modify_template(template_df, station_parameter_name, template_parameter_name, row, col)
                if mod == 'pass':
                    sg.popup("Successfully added to template.")
                    window["-IN1-"].update("")
                    window["-IN2-"].update("")
                    window["-IN3-"].update("")
                    window["-IN4-"].update("")
                else:
                    sg.popup_error(mod)
            else:
                sg.popup_error("Please enter values in all the fields.")

        if(event == "Download Files"):
            window.disable()
            show_progress(wmo_data, template_df, wmo_station, wmo_parameters, folder_path_out)
            sg.popup("Complete. You can find the files in " + folder_path_out)
            window.enable()
           
    else:
        if (error_message1 is not None):
            sg.popup_error(error_message1)
        if (error_message2 is not None):
            sg.popup_error(error_message2)
        if (error_message3 is not None):
            sg.popup_error(error_message3)
        

window.close()