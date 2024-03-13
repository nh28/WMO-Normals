# WMO-Normals



## Requirements

- [ ] In requirements.txt
    - [ ] altgraph==0.17.4
    - [ ] cffi==1.16.0
    - [ ] cryptography==42.0.4
    - [ ] numpy==1.26.3
    - [ ] oracledb==2.0.1
    - [ ] packaging==23.2
    - [ ] pandas==2.2.0
    - [ ] pefile==2023.2.7
    - [ ] pycparser==2.21
    - [ ] pyinstaller==6.3.0
    - [ ] pyinstaller-hooks-contrib==2024.0
    - [ ] PySimpleGUI==4.60.5
    - [ ] python-dateutil==2.8.2
    - [ ] pytz==2023.4
    - [ ] pywin32-ctypes==0.2.2
    - [ ] setuptools==69.0.3
    - [ ] six==1.16.0
    - [ ] tzdata==2023.4
- [ ] Other
    - [ ] PortableGit or Git installed
    - [ ] MUST be on VPN

## Clone and Configure (using Git)

```
>>> git clone https://gccode.ssc-spc.gc.ca/harschnena/wmo-normals
```

## Set Up

create a virtual environment and download the necessary libraries
Note: if you are using PortableGit, in order to be able to pip install you need to open the command prompt git-cmd.exe

```
>>> cd wmo-normals
>>> py -3 -m venv .venv
>>> cd .venv
>>> cd Scripts
>>> activate.bat
>>> # install all the libraries from requirements.txt
>>> pip install -r requirements.txt

```

## Confirming Installation
You can make use of pip freeze to see what libraries you have installed in your virtual environment
If using PortableGit, in order to be able to pip you need to open the command prompt git-cmd.exe

```
>>> cd wmo-normals
>>> cd .venv
>>> cd Scripts
>>> activate.bat
>>> py pip freeze > requirements.txt
>>> cat requirements.txt
```


## Name Requirements
- [ ] src
    - [ ] contains the Python code
    - [ ] contains the input folder
	- [ ] contains the output folder
- [ ] Input
    - [ ] NormalID_to_WMOParameterID.csv
	- [ ] StationList.csv
- [ ] Output 
    - [ ] 1991-2020_Normals_Canada_STN_NAME.csv

## How to Run
- [ ] With Python
```
>>> cd wmo-normals
>>> cd src
>>> cd .venv
>>> cd Scripts
>>> activate.bat
>>> # You can verify that the virtual environment is running by seeing (.venv) in front of your command line
>>> cd ..
>>> cd ..
>>> py main.py
>>> # Once done, deactivate the venv. You can verify that the virtual environment is not running by not seeing (.venv) in front of your command line
>>> cd .venv
>>> cd Scripts
>>> deactivate.bat
```
- [ ] With exe
    - [ ] IMPORTANT: MAKE SURE main.exe, _internal, py files, Input, and Output folders are all in the SAME PLACE
    - [ ] User can just run the main.exe file

## Making Modifications
- [ ] Template
    - [ ] If changes are necessary to the template, you can use the feature included to add a element
    - [ ] If bigger changes are necessary that involves the reformatting of the whole template, edit in Template.py and recompile everything
- [ ] Column Names
    - [ ] The code does not depend on the ordering of the columns in these files
    - [ ] Please make sure that you have the necessary columns present and names correctly:
        - [ ] 1991-2020_WMO_Normals_Data: 'STN_ID', 'NORMAL_ID', 'ENG_ELEMENTNAME',	'MONTH', 'VALUE', 'FIRST_OCCURRENCE_DATE','YEAR_COUNT_NORMAL_PERIOD', 'ENG_STN_NAME'
        - [ ] StationList: 'VIRTUAL_STN_ID', 'Station Name', 'Province', 'WMO-ID', 'WIGOS-ID', 'Latitude', 'Longitude', 'Elevation (m)'
        - [ ] NormalID_to_WMOParameterID: 'Normal Name', 'Parameter Code', 'Parameter Name', 'Units', 'Calculation Name' (Note: accounts for a max of two calculations per normal name), 'Normal ID'
            - [ ] NOTE: this file has a title row before the table
- [ ] Recompiling the exe file    
        
```
>>> cd wmo-normals
>>> cd src
>>> cd .venv
>>> cd Scripts
>>> activate.bat
>>> # You can verify that the virtual environment is running by seeing (.venv) in front of your command line
>>> cd ..
>>> cd ..
>>> pyinstaller --hidden-import=cryptography.hazmat.primitives.kdf.pbkdf2 main.py
>>> IMPORTANT: once you have the dist folder, take the main.exe and the _internal files out of the folder in the same place as all your py files, Input, and Output folders
```

## Errors
After each run, there will be a WMO.log that will appear in the same directory as your main.exe file. This contains a written account of if the program started, details about the run, what errors occured, and if the program ended.



