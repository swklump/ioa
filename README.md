Explanation of files

The app uses PyQT, QT Designer for the GUI, pandas for data manipulation/analysis, Beautiful soup for HTML parsing, Elemetree for xml manipulation, and PyAutoGui for gui automation.
The app is turned into an exe with "pyinstaller --onefile --windowed --icon=icon.ico Application.spec" run in command line.

1. "Application.py"
	This file is the main script to run the app. To run, in CMD type "python Application.py".
	Each class in the script is for running modules seen from the home page. When first running the app, the HomePage class is activated (line 772-775). From the homepage, you can see 
buttons for "Application Overview and Links", "Import Data", "Export Data", etc. When each of these buttons is clicked, the corresponding class runs (lines 104-109).
	The "Master" class is for passing functions to each module class.

2. "Application_helperfunctions.py" is one function for implementing GUI defaults, like adding the icon in the top left of each window and adding the minimize window button.

3. "Application.spec" specifies how to package the app. 

4. "UI_files" folder has the QT Designer UI files. With QT Designer, UIs are edited with drag and drop.

5. "PNG_files" has the icon that are shown in the UI.

6. "dist" folder is where the exe goes after you run the command to convert to and exe.

7. The folders "ImportData", "ExportData", "BatchEval", "ParseHTML", and "SegmentAnalysis" have the code for running each of the corresponding modules in the app.