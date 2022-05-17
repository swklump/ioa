# Wait til internet explorer pops up
import pyautogui as pg
from os import rename, remove
from bs4 import BeautifulSoup as bs
from shutil import rmtree
import PyPDF2


def process_evals(timegap, output_type, savelocation, prefix, del_eval_choice):
    # Wait til internet explorer pops up
    r = None
    while r is None:
        r = pg.locateOnScreen('PNG Files\\internet.png')
    pg.sleep(timegap)

    # Save html
    if output_type in ['HTML Only', 'HTML and PDF']:
        pg.hotkey('ctrl', 's')
        pg.sleep(timegap)

        # enter file names
        pg.write(str(savelocation) + '\\' + str(0))
        pg.sleep(timegap)
        pg.press('enter')
        pg.sleep(timegap)

    # Close html page
    pg.hotkey('altleft', 'f4')
    pg.sleep(timegap)

    # Close IHSDM window
    pg.hotkey('altleft', 'c')
    pg.sleep(timegap)

    if output_type in ['PDF Only', 'HTML and PDF']:

        # Right-click evaluation
        r = None
        while r is None:
            r = pg.locateOnScreen('PNG Files\\deleval.png')
        pg.click('PNG Files\\deleval.png', button='right')
        pg.sleep(timegap)

        # "Show Report"
        r = None
        while r is None:
            r = pg.locateOnScreen('PNG Files\\show_report.png')
        pg.click('PNG Files\\show_report.png')
        pg.sleep(timegap)

        # "Show Report - PDF"
        r = None
        while r is None:
            r = pg.locateOnScreen('PNG Files\\show_pdf.png')
        pg.click('PNG Files\\show_pdf.png')
        pg.sleep(timegap)

        # Open up pdf
        r = None
        while r is None:
            r = pg.locateOnScreen('PNG Files\\open_pdf.png')
        pg.click('PNG Files\\open_pdf.png')
        pg.sleep(7)

        # Save pdf
        pg.hotkey('ctrl', 'shift', 's')
        pg.sleep(timegap)
        pg.write(str(savelocation) + '\\' + str(0))
        pg.sleep(timegap)
        pg.press('enter')
        pg.sleep(timegap)

        # Close pdf viewer
        pg.hotkey('altleft', 'f4')
        pg.sleep(timegap)

    if del_eval_choice == 'Delete evaluations out of IHSDM':
        # Delete evaluation
        r = None
        while r is None:
            r = pg.locateOnScreen('PNG Files\\deleval.png')
        pg.click('PNG Files\\deleval.png', button='right')
        pg.sleep(timegap)

        # Confirm deletion
        pg.hotkey('altleft', 'l')
        pg.sleep(timegap)
        r = None
        while r is None:
            r = pg.locateOnScreen('PNG Files\\ok.png')
        pg.click('PNG Files\\ok.png')
        pg.sleep(timegap)

    # Rename the html page based on the element name in IHSDM
    if output_type in ['HTML Only', 'HTML and PDF']:
        number_fname = savelocation + '\\' + str(0) + '.htm'
        number_fname = number_fname.replace('/', '\\')

        file = bs(open(number_fname), 'html.parser').find_all('font')
        for f in file:
            if 'Highway Title' in f.text or 'Intersection Title' in f.text:
                index = f.text.find(':')
                filename = f.text[index + 2:].replace('\n', '')
                if prefix in filename:
                    filename = filename.replace(prefix, '').strip()
                filename = savelocation + '\\' + filename + '.htm'
                filename = filename.replace('/', '\\')
                # if loop goes out of wack
                if 'Highway Title' in f.text:
                    try:
                        rename(number_fname, filename)
                        rmtree(number_fname[:-4] + '_files' + '\\')
                    except FileExistsError:
                        remove(filename)
                        rename(number_fname, filename)
                        rmtree(number_fname[:-4] + '_files' + '\\')
                elif 'Intersection Title' in f.text:
                    try:
                        rename(number_fname, filename)
                    except FileExistsError:
                        remove(filename)
                        rename(number_fname, filename)

    # Rename the PDF page based on the element name in IHSDM
    if output_type in ['PDF Only', 'HTML and PDF']:
        number_fname = savelocation + '\\' + str(0) + '.pdf'
        number_fname = number_fname.replace('/', '\\')

        pdf_fileobject = open(str(savelocation) + '\\' + str(0) + '.pdf', 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_fileobject)
        page_text = pdf_reader.getPage(4).extractText()
        for line in page_text.splitlines():
            # Get alignment name
            if 'Highway Title:' in line:
                text_index1 = line.find('Highway Title:')
                text_index2 = line.find('Highway Comment:')
                filename = line[text_index1 + 15:text_index2]
            if prefix in filename:
                filename = filename.replace(prefix, '').strip()
            filename = savelocation + '\\' + filename + '.pdf'
            filename = filename.replace('/', '\\')
            pdf_fileobject.close()
            # if loop goes out of wack
            try:
                rename(number_fname, filename)
            except FileExistsError:
                remove(filename)
                rename(number_fname, filename)
