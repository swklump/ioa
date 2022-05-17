# Imports
import time
from glob import glob
from sys import argv, exit
import xlrd
from PyQt5.QtGui import QPixmap, QIntValidator, QDesktopServices
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QLabel, QProgressBar
from PyQt5.uic import loadUi
from pandas import read_excel

from Application_helperfunctions import window_defaults
from ExportData._mainscript import export_data
from BatchEval.batcheval_interchanges import batcheval_int
from BatchEval.batcheval_segments import batcheval_seg
from ImportData.import_arterial import import_arterial
from ImportData.import_freeway import import_freeway
from ImportData.import_interchange import import_interchange
from ImportData.import_ramp import import_ramp
from ParseHTML._mainscript import parse_html
from SegmentAnalysis.segmentanalysis_fs import segmentanalysis_fs
from SegmentAnalysis.segmentanalysis_ramp import segmentanalysis_ramp
from SegmentAnalysis.segmentanalysis_art import segmentanalysis_art

# Global variables
inputfilepath = ''
project_folder = ''
savelocation = ''
html_loc = ''
segmentfile = ''
crash_file_path = ''

appname = 'IHSDM Optimization App'
icon_path = 'UI Files\icon.ico'

if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class Master():
    def backto_mainmenu(self):
        self.close()
        HomePage().exec_()

    # Function for the hyperlink
    def link(self, linkStr):
        QDesktopServices.openUrl(QUrl(linkStr))

    # Set up progress bar
    def setup_prog_bar(self):
        # Progress bar
        self.progress = QProgressBar(self)
        self.progress.setGeometry(500, 10, 250, 20)
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)

    # Run progress bar
    def run_prog_bar(self):
        seconds = 3
        self.completed = 0
        self.progress.setFormat('0%')
        self.progress.setValue(self.completed)
        while self.completed < 100:
            self.progress.setFormat(str(self.completed) + '%')
            self.progress.setValue(self.completed)
            self.completed += 50

            time.sleep(1)
            if seconds == 2:
                self.progress.setFormat('Program running!')
                self.progress.setValue(self.completed)
            else:
                self.progress.setFormat(str(self.completed) + '%')
                self.progress.setValue(self.completed)

            seconds -= 1

    def reset_prog_bar(self):
        # Reset progress bar
        self.completed = 0
        self.progress.setValue(self.completed)
        self.progress.setFormat('0%')


# Homepage
class HomePage(QDialog):
    def __init__(self):
        super(HomePage, self).__init__()
        loadUi('UI Files\HomePage.ui', self)

        # Apply defaults
        window_defaults(self, appname, icon_path)

        # HDR logo
        label = QLabel(self)
        pixmap = QPixmap('UI Files\HDRlogo.png')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        label.move(400, 240)

        # Run functions buttons when clicked
        self.overview_button.clicked.connect(self.ApplicationOverview)
        self.exportdata_button.clicked.connect(self.ExportData)
        self.importdata_button.clicked.connect(self.ImportData)
        self.batch_button.clicked.connect(self.BatchEval)
        self.parsehtml_button.clicked.connect(self.ParseHTML)
        self.segment_analysis_but.clicked.connect(self.SegmentAnalysis)

    # Six buttons on homepage
    def ApplicationOverview(self):
        self.close()
        ApplicationOverview().exec_()

    def ImportData(self):
        self.close()
        ImportData().exec_()

    def ExportData(self):
        self.close()
        ExportData().exec_()

    def BatchEval(self):
        self.close()
        BatchEval().exec_()

    def ParseHTML(self):
        self.close()
        ParseHTML().exec_()

    def SegmentAnalysis(self):
        self.close()
        SegmentAnalysis().exec_()


# Application Overview
class ApplicationOverview(QDialog, Master):

    def __init__(self):
        super(ApplicationOverview, self).__init__()
        loadUi('UI Files\ApplicationOverview.ui', self)

        # Apply defaults
        window_defaults(self, appname, icon_path)

        # User manual link
        self.label.linkActivated.connect(self.link)
        self.label.setText(
            '<a href="https://hdrinc.sharepoint.com/:f:/r/teams/TrafficSafetyPracticeGroup/Shared%20Documents/5.%20Tools%20%26%20Spreadsheets/IHSDM%20Optimization%20App?csf=1&web=1&e=Zht3Ax">here.</a>')

        # Set "enter" button
        self.mainmenu.setAutoDefault(True)

        # Main Menu
        self.mainmenu.clicked.connect(self.backto_mainmenu)


# Input Data Module
class ImportData(QDialog, Master):
    def __init__(self):
        super(ImportData, self).__init__()
        loadUi('UI Files\\import_data.ui', self)

        # Apply defaults
        window_defaults(self, appname, icon_path)

        # File ID A-1, A-2, and A-3 link (Step 1)
        self.label_step1.linkActivated.connect(self.link)
        self.label_step1.setText(
            '<a href="https://hdrinc.sharepoint.com/:f:/r/teams/TrafficSafetyPracticeGroup/Shared%20Documents/5.%20Tools%20%26%20Spreadsheets/IHSDM%20Optimization%20App/DCT%20Spreadsheets?csf=1&web=1&e=ldJyej">here.)</a>')

        # Make boxes read only
        read_only_boxes = [self.messagebox, self.filenamebox, self.pfolder_form]
        for r in read_only_boxes:
            r.setReadOnly(True)

        # Restrict entries to integers
        self.angle_form.setValidator(QIntValidator())

        # Set default values
        self.angle_form.setText("0")

        # Attaching functions to the push buttons
        self.mainmenu.clicked.connect(self.backto_mainmenu)
        self.inputfile_button.clicked.connect(self.selectinputfile)
        self.folder_button.clicked.connect(self.selectpfolder)
        self.runapp_but.clicked.connect(self.runapp)

        # Set up progress bar
        self.setup_prog_bar()

    # User uploads file ID A-1, A-2, A-3, or A-4 (Step 1)
    def selectinputfile(self):
        global inputfilepath
        self.messagebox.setText('')
        filename = QFileDialog.getOpenFileName(None, 'Select a file:')
        inputfilepath = filename[0]
        self.filenamebox.setText(inputfilepath)

    # User selects IHSDM project folder location (Step 3)
    def selectpfolder(self):
        global project_folder
        self.messagebox.setText('')
        project_folder = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)
        self.pfolder_form.setText(project_folder)

    # Run app
    def runapp(self):
        global inputfilepath
        global project_folder

        self.messagebox.setText('')

        # Get prefix and angle (Steps 4 and 5)
        prefix = self.prefix_form.text()
        angle = int(self.angle_form.text())
        import_all_attrs = self.eval_all_el_button.currentText()

        # Check if file path for Step 1 is empty.
        if inputfilepath == '' or project_folder == '':
            self.messagebox.setText('Please upload a completed file ID A-1, A-2, A-3 or A-4. (Step 1) '
                                    'and/or select a project folder (Step 3).')
            self.messagebox.setStyleSheet("color: red;")
            return

        # Check to see that project folder starts with a "p"
        slash_index = project_folder.rfind('/')
        pfold = project_folder[slash_index + 1:]
        if pfold[0] != 'p':
            self.messagebox.setText(
                'The project folder selected (Step 3) is not an IHSDM project folder. '
                'Please select an IHSDM project folder.')
            self.messagebox.setStyleSheet("color: red;")
            return

        # Run progress bar
        self.run_prog_bar()

        # Check the format of file ID A-1, A-2, or A-3 (Step 1).
        try:
            df_book = read_excel(inputfilepath, sheet_name=None)
            element_type = list(df_book['Directory'])[1].lower()
        except Exception:
            self.messagebox.setText(
                'The uploaded file ID A-1, A-2, A-3, or A-4 (Step 1) is not in the correct format.'
                'Use the link to upload the correct file format.')
            self.messagebox.setStyleSheet("color: red;")
            self.progress.setFormat('0%')
            self.progress.setValue(0)
            return
        else:
            pass

        included_elements = [import_all_attrs.lower()]

        # Run module with general error exception.
        try:
            if element_type == 'freeway segment':
                import_freeway(project_folder, prefix, included_elements, angle, df_book)
            elif element_type == 'ramp segment':
                import_ramp(project_folder, prefix, included_elements, angle, df_book)
            elif element_type == 'interchange':
                import_interchange(project_folder, inputfilepath)
            elif element_type == 'arterial':
                import_arterial(project_folder, prefix, included_elements, angle, df_book)
            elif element_type == 'ramp terminal':
                self.messagebox.setText('At this time, ramp terminal data cannot be imported.')
                self.messagebox.setStyleSheet("color: red;")
                self.progress.setFormat('0%')
                self.progress.setValue(0)
                return
            elif element_type == 'arterial intersection':
                self.messagebox.setText('At this time, arterial intersection data cannot be imported.')
                self.messagebox.setStyleSheet("color: red;")
                self.progress.setFormat('0%')
                self.progress.setValue(0)
                return
            else:
                self.messagebox.setText('Cell B1 in the "Directory" tab (file ID A-1, A-2, A-3, or A-4 (Step 1)'
                                        ' must state the element type.')
                self.messagebox.setStyleSheet("color: red;")
                self.progress.setFormat('0%')
                self.progress.setValue(0)
                return
        except Exception:
            self.messagebox.setText(
                'An unknown error occurred. Make sure to use the links to upload files in the correct format.'
                ' If this error persists, please send an email to samuel.klump@hdrinc.com.')
            self.messagebox.setStyleSheet("color: red;")
            return
        else:
            pass

        # Reset progress bar
        self.reset_prog_bar()

        # Print success message
        self.messagebox.setText(element_type.title() + ' data successfully imported to IHSDM!')
        self.messagebox.setStyleSheet("color: green;")


# Extract Curvature Module
class ExportData(QDialog, Master):
    def __init__(self):
        super(ExportData, self).__init__()
        loadUi('UI Files\\export_data.ui', self)

        # Apply defaults
        window_defaults(self, appname, icon_path)

        # Make boxes read only
        read_only_boxes = [self.messagebox, self.pfolder_form]
        for r in read_only_boxes:
            r.setReadOnly(True)

        # Attaching functions to the push buttons
        self.mainmenu.clicked.connect(self.backto_mainmenu)
        self.folder_button.clicked.connect(self.selectpfolder)
        self.savepathbox.clicked.connect(self.selectsavelocation)
        self.runapp_but.clicked.connect(self.runapp)

        # Set up progress bar
        self.setup_prog_bar()

    # User selects IHSDM project folder location (Step 3)
    def selectpfolder(self):
        global project_folder
        self.messagebox.setText('')
        project_folder = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)
        self.pfolder_form.setText(project_folder)

    # User selects save location for html files (Step 3)
    def selectsavelocation(self):
        global savelocation
        self.messagebox.setText('')
        savelocation = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)
        self.save_name_box.setText(savelocation)

    # Run app
    def runapp(self):
        global inputfilepath
        global included_elements_path
        global project_folder

        self.messagebox.setText('')
        # Get prefix and angle (Steps 4 and 5)
        prefix = self.prefix_form.text()

        # Check to see if the folder path for Step 3 is empty.
        if project_folder == '' or savelocation == '':
            self.messagebox.setText('Please select a project folder (Step 2) and/or save location (Step 3).')
            self.messagebox.setStyleSheet("color: red;")
            return

        # Check to see that project folder starts with a "p"
        slash_index = project_folder.rfind('/')
        pfold = project_folder[slash_index + 1:]
        if pfold[0] != 'p':
            self.messagebox.setText(
                'The project folder selected (Step 2) is not an IHSDM project folder. '
                'Please select an IHSDM project folder.')
            self.messagebox.setStyleSheet("color: red;")
            return

        # Run progress bar
        self.run_prog_bar()

        # Run module with general error exception.
        try:
            export_data(project_folder, prefix, savelocation)
        except Exception:
            self.messagebox.setText(
                'An unknown error occurred. Make sure to use the links to upload files in the correct format.'
                ' If this error persists, please send an email to samuel.klump@hdrinc.com.')
            self.messagebox.setStyleSheet("color: red;")
            return
        else:
            pass

        # Reset progress bar
        self.reset_prog_bar()

        # Print success message
        self.messagebox.setText('Data successfully exported from IHSDM!')
        self.messagebox.setStyleSheet("color: green;")


# Batch Evaluation Module
class BatchEval(QDialog, Master):
    def __init__(self):
        super(BatchEval, self).__init__()
        loadUi('UI Files\\batcheval.ui', self)

        # Apply defaults
        window_defaults(self, appname, icon_path)

        # Make boxes read only
        read_only_boxes = [self.messagebox, self.filenamebox]
        for r in read_only_boxes:
            r.setReadOnly(True)

        # Restrict entries to integers
        restrict_int = [self.first_index_form, self.number_form, self.firstyear_form, self.endyear_form]
        for i in restrict_int:
            i.setValidator(QIntValidator())

        # Set default values
        self.first_index_form.setText("1")
        self.firstyear_form.setText("2020")
        self.endyear_form.setText("2020")

        # Attaching functions to the push buttons
        self.mainmenu.clicked.connect(self.backto_mainmenu)
        self.savepathbox.clicked.connect(self.selectsavelocation)
        self.runapp_but.clicked.connect(self.runapp)

        # Set up progress bar
        self.setup_prog_bar()

    # User selects save location for html files (Step 3)
    def selectsavelocation(self):
        global savelocation
        self.messagebox.setText('')
        savelocation = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)
        self.filenamebox.setText(savelocation)

    # Run app
    def runapp(self):
        global savelocation

        self.messagebox.setText('')

        number = self.number_form.text()

        # Check that save location is selected (Step 3).
        if savelocation == '':
            self.messagebox.setText('Please select a folder to save the HTML files in (Step 3).')
            self.messagebox.setStyleSheet("color: red;")
            return

        # Check that Steps 4-7 are complete.
        try:
            start_index = int(self.first_index_form.text())
            start_year = int(self.firstyear_form.text())
            end_year = int(self.endyear_form.text())
        except Exception:
            self.messagebox.setText('No indices or years entered! Please enter the indices and years (Steps 4-7).')
            self.messagebox.setStyleSheet("color: red;")
            return
        else:
            pass

        # Check that the start index (Step 4) and number of evaluated elements (Step 5) are not less that one.
        if start_index < 1:
            self.messagebox.setText('The start index (Step 5) and number of evaluated elements (Step 6) '
                                    'must be greater than zero.')
            self.messagebox.setStyleSheet("color: red;")
            return

        # Check that the start year of evaluation (Step 6) is not less than 2000.
        if start_year < 2000:
            self.messagebox.setText('The start year must be greater than 1999 (Step 7).')
            self.messagebox.setStyleSheet("color: red;")
            return

        # Check that the end year is not less than the start year (Steps 6 and 7).
        if end_year < start_year:
            self.messagebox.setText('The end year (Step 8) must be greater than or equal to the start year (Step 7).')
            self.messagebox.setStyleSheet("color: red;")
            return

        # Get evaluation type, output type, and prefix (Step 1, Step 2, and Step 8).
        eval_type = self.eval_type_button.currentText()
        del_eval_choice = self.del_eval_form.currentText()
        output_type = self.output_type_button.currentText()
        eval_all_elements = self.eval_all_el_button.currentText()

        if eval_all_elements == 'No':
            try:
                number = int(number)
            except Exception:
                self.messagebox.setText("In Step 6, 'No' is selected in the drop-down. Please enter a number of "
                                        "elements to evaluate.")
                self.messagebox.setStyleSheet("color: red;")
                return
            else:
                if number < 1:
                    self.messagebox.setText("In Step 6, 'No' is selected in the drop-down. Please enter a number of "
                                            "elements to evaluate.")
                    self.messagebox.setStyleSheet("color: red;")
                    return

        prefix = self.prefix_form.text()

        # Progress bar
        seconds = 5
        self.completed = 0
        while self.completed < 100:
            if seconds == 1:
                self.progress.setFormat(str(seconds - 1) + ' second until program starts!')
            else:
                self.progress.setFormat(str(seconds - 1) + ' seconds until program starts!')
            self.completed += 20
            time.sleep(1)
            seconds -= 1
            if seconds == 0:
                self.progress.setFormat('Program running!')
            self.progress.setValue(self.completed)

        # Run module with general error exception.
        try:
            if eval_type == 'Segments (Freeways and Arterials)':
                batcheval_seg(output_type, start_year, end_year, savelocation, start_index, number, prefix,
                              del_eval_choice, eval_all_elements)
            elif eval_type == 'Interchanges (Ramps and Ramp Terminals)':
                batcheval_int(output_type, start_year, end_year, savelocation, start_index, number, prefix,
                              del_eval_choice, eval_all_elements)
        except Exception:
            self.messagebox.setText(
                "An error occurred or you have used the failsafe to stop the program. "
                "If stopping the program was not intentional, please send an email to samuel.klump@hdrinc.com.")
            self.messagebox.setStyleSheet("color: red;")
            self.completed = 0
            self.progress.setFormat('')
            self.progress.setValue(0)
            return

        # Reset progress bar.
        self.completed = 0
        self.progress.setValue(self.completed)
        self.progress.setFormat('')

        # Print success message.
        self.messagebox.setText('Elements evaluated! '
                                'Check the save location for the HTML output files.')
        self.messagebox.setStyleSheet("color: green;")


# Parse HTML Module
class ParseHTML(QDialog, Master):
    def __init__(self):
        super(ParseHTML, self).__init__()
        loadUi('UI Files\\parse_html.ui', self)

        # Apply defaults
        window_defaults(self, appname, icon_path)

        # Set boxes to read only
        read_only_boxes = [self.messagebox, self.filenamebox]
        for r in read_only_boxes:
            r.setReadOnly(True)

        # Attaching functions to the push buttons
        self.mainmenu.clicked.connect(self.backto_mainmenu)
        self.html_path_box.clicked.connect(self.select_html_loc)
        self.runapp_but.clicked.connect(self.runapp)

        # Set up progress bar
        self.setup_prog_bar()

    # User selects location of HTML files
    def select_html_loc(self):
        global html_loc
        self.messagebox.setText('')
        html_loc = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)
        self.filenamebox.setText(html_loc)

    # Run app
    def runapp(self):
        global html_loc

        self.messagebox.setText('')

        # Check that html location is selected
        if html_loc == '':
            self.messagebox.setText('Please select a folder location to save the HTML outputs in (Step 1).')
            self.messagebox.setStyleSheet("color: red;")
            return

        # Check that there are html or htm files in selected location.
        htmlfiles = glob(html_loc + '/' + '*.htm')
        if len(htmlfiles) == 0:
            htmlfiles = glob(html_loc + '/' + '*.html')
        if len(htmlfiles) == 0:
            self.messagebox.setText(
                'There were no HTML files found in the selected folder! Please select a folder with HTML outputs.')
            self.messagebox.setStyleSheet("color: red;")
            return

        # Run progress bar
        self.run_prog_bar()

        # Run module with general error exception.
        try:
            parse_html(html_loc)
        except Exception:
            self.messagebox.setText(
                'An error occurred. If this error persists, please send and email to samuel.klump@hdrinc.com.')
            self.messagebox.setStyleSheet("color: red;")
            self.progress.setValue(self.completed)
            self.progress.setFormat('0%')
            return

        # Reset progress bar
        self.reset_prog_bar()

        # Print success message
        if len(htmlfiles) == 1:
            self.messagebox.setText(str(len(htmlfiles)) + ' HTML file parsed!')
        else:
            self.messagebox.setText(str(len(htmlfiles)) + ' HTML files parsed!')
        self.messagebox.setStyleSheet("color: green;")


# Analyze Inputs Module
class SegmentAnalysis(QDialog, Master):
    def __init__(self):
        super(SegmentAnalysis, self).__init__()
        loadUi('UI Files\\segment_analysis.ui', self)

        # Apply defaults
        window_defaults(self, appname, icon_path)

        # Data import files link (Step 1)
        self.label_step1.linkActivated.connect(self.link)
        self.label_step1.setText(
            '<a href="https://hdrinc.sharepoint.com/:f:/r/teams/TrafficSafetyPracticeGroup/Shared%20Documents/5.%20Tools%20%26%20Spreadsheets/IHSDM%20Optimization%20App/DCT%20Spreadsheets?csf=1&web=1&e=CU7Hgx">here.)</a>')

        # Example crash output file link (Step 2)
        self.label_step2.linkActivated.connect(self.link)
        self.label_step2.setText(
            '<a href="https://hdrinc.sharepoint.com/:f:/r/teams/TrafficSafetyPracticeGroup/Shared%20Documents/5.%20Tools%20%26%20Spreadsheets/IHSDM%20Optimization%20App/IOA_Module5_Segment%20Analysis%20for%20Freeways,%20Ramps,%20and%20Arterials_Files?csf=1&web=1&e=AxS0Su">here.)</a>')

        # Segment file (Step 3)
        self.label_step3.linkActivated.connect(self.link)
        self.label_step3.setText(
            '<a href="https://hdrinc.sharepoint.com/:f:/r/teams/TrafficSafetyPracticeGroup/Shared%20Documents/5.%20Tools%20%26%20Spreadsheets/IHSDM%20Optimization%20App/IOA_Module5_Segment%20Analysis%20for%20Freeways,%20Ramps,%20and%20Arterials_Files?csf=1&web=1&e=AxS0Su">here.)</a>')

        # Set boxes as read only
        read_only_boxes = [self.messagebox, self.filenamebox, self.filenamebox_2, self.filenamebox_3,
                           self.filenamebox_4]
        for r in read_only_boxes:
            r.setReadOnly(True)

        self.seg_dist_form.setInputMask('00.00')

        # Attaching functions to the push buttons
        self.mainmenu.clicked.connect(self.backto_mainmenu)
        self.inputfile_button.clicked.connect(self.selectinputfile)
        self.inputfile_button_2.clicked.connect(self.select_crash_file)
        self.inputfile_button_3.clicked.connect(self.selectsegmentfile)
        self.savepathbox.clicked.connect(self.selectsavelocation)
        self.runapp_but.clicked.connect(self.runapp)

        # Set up progress bar
        self.setup_prog_bar()

    # User selects completed file ID A-1, A-2, or A-3
    def selectinputfile(self):
        global inputfilepath
        self.messagebox.setText('')
        filename = QFileDialog.getOpenFileName(None, 'Select a file:')
        inputfilepath = filename[0]
        self.filenamebox.setText(inputfilepath)

    # User selects crash output file
    def select_crash_file(self):
        global crash_file_path
        self.messagebox.setText('')
        filename = QFileDialog.getOpenFileName(None, 'Select a file:')
        crash_file_path = filename[0]
        self.filenamebox_2.setText(crash_file_path)

    # User selects file ID C-1
    def selectsegmentfile(self):
        global segmentfile
        self.messagebox.setText('')
        filename = QFileDialog.getOpenFileName(None, 'Select a file:')
        segmentfile = filename[0]
        self.filenamebox_3.setText(segmentfile)

    # User selects save location for file
    def selectsavelocation(self):
        global savelocation
        self.messagebox.setText('')
        savelocation = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)
        self.filenamebox_4.setText(savelocation)

    # Run app
    def runapp(self):
        global inputfilepath
        global crash_file_path
        global segmentfile
        global savelocation

        self.messagebox.setText('')
        seg_dist = self.seg_dist_form.text()

        # Check file path for Step 1 selected.
        if inputfilepath == '' or crash_file_path == '' or savelocation == '':
            self.messagebox.setText('Please upload a completed file ID A-1, A-2, or A-3 (Step 1), upload a crash '
                                    'output file (Step 2), and/or select a save location (Step 4).')
            self.messagebox.setStyleSheet("color: red;")
            return

        # Check file path for Step 3 selected.
        if seg_dist == '.' and segmentfile == '':
            self.messagebox.setText('Please enter a segment distance or upload a completed file ID C-1 (Step 3).')
            self.messagebox.setStyleSheet("color: red;")
            return
        elif seg_dist != '.' and segmentfile != '':
            self.messagebox.setText('You cannot enter a segmentation distance and upload a file ID C-1. Please either'
                                    ' enter a segmentation distance OR upload a file ID C-1 (Step 3).')
            self.messagebox.setStyleSheet("color: red;")
            return
        elif seg_dist != '.' and segmentfile == '':
            seg_dist = float(seg_dist.strip(' "'))

        # Run progress bar
        self.run_prog_bar()

        # Check format of file ID A-1, A-2, or A-3 (Step 1)
        try:
            book = xlrd.open_workbook(inputfilepath)
            direct_sheet = book.sheet_by_name('Directory')
        except Exception:
            self.messagebox.setText(
                'The uploaded file ID A-1, A-2, or A-3 (Step 1) is not in the correct format.'
                'Use the link to upload the correct file format.')
            self.messagebox.setStyleSheet("color: red;")
            return
        else:
            pass
        # Run module with general error exception.
        try:
            if direct_sheet.cell_value(0, 1).lower() == 'freeway segment':
                segmentanalysis_fs(inputfilepath, crash_file_path, seg_dist, segmentfile, savelocation)
            elif direct_sheet.cell_value(0, 1).lower() == 'ramp segment':
                segmentanalysis_ramp(inputfilepath, crash_file_path, seg_dist, segmentfile, savelocation)
            elif direct_sheet.cell_value(0, 1).lower() == 'arterial':
                segmentanalysis_art(inputfilepath, crash_file_path, seg_dist, segmentfile, savelocation)
            elif direct_sheet.cell_value(0, 1).lower() == 'ramp terminal':
                self.messagebox.setText('Ramp terminal data cannot be segmented.')
                self.messagebox.setStyleSheet("color: red;")
                self.progress.setFormat('0%')
                self.progress.setValue(0)
                return
            elif direct_sheet.cell_value(0, 1).lower() == 'arterial intersection':
                self.messagebox.setText('Arterial intersection data cannot be segmented.')
                self.messagebox.setStyleSheet("color: red;")
                self.progress.setFormat('0%')
                self.progress.setValue(0)
                return
        except Exception:
            self.messagebox.setText(
                "An unknown error occurred. Make sure the standard data template is uploaded. "
                "If this error persists, please send an email to samuel.klump@hdrinc.com.")
            self.messagebox.setStyleSheet("color: red;")
            return
        else:
            pass

        # Reset progress bar
        self.reset_prog_bar()

        # Print success message
        self.messagebox.setText('Data successfully analyzed!')
        self.messagebox.setStyleSheet("color: green;")


app = QApplication(argv)
widget = HomePage()
widget.show()
exit(app.exec_())
