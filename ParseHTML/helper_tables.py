# This function puts data from the html page to the excel sheet
from decimal import Decimal
import numpy as np

def data_to_excel(outsheet, col_headers, data_dict, excluded_items=''):

    outsheet.write(0, 0, 'Highway Name')
    for c in range(len(col_headers)):
        outsheet.write(0, c + 1, col_headers[c][0])

    row = 1
    # Loop through the number of html files
    for k, v in data_dict.items():

        # Loop through the number of rows in the html table
        for m in range(len(v)):
            if excluded_items:
                if v[excluded_items[0]][m] in excluded_items[1]:
                    pass
                else:
                    outsheet.write(row, 0, k)

                    # Loop through the number of columns, assign based on specified data type
                    for c in range(len(col_headers)):
                        try:
                            test_var = v[col_headers[c][0]][m]
                        except KeyError:
                            pass
                        else:
                            if col_headers[c][1] == 'str':
                                outsheet.write(row, c + 1, v[col_headers[c][0]][m])
                            elif col_headers[c][1] == 'int':
                                # Check in NaN
                                if v[col_headers[c][0]][m] != v[col_headers[c][0]][m]:
                                    outsheet.write(row, c + 1, '')
                                else:
                                    try:
                                        outsheet.write(row, c + 1, int(v[col_headers[c][0]][m]))
                                    except ValueError:
                                        outsheet.write(row, c + 1, v[col_headers[c][0]][m])
                            elif col_headers[c][1] == 'decimal':
                                if v[col_headers[c][0]][m] != v[col_headers[c][0]][m]:
                                    outsheet.write(row, c + 1, '')
                                else:
                                    outsheet.write(row, c + 1, Decimal(v[col_headers[c][0]][m]))
                            elif col_headers[c][1] == 'sta':
                                # Check in NaN
                                if v[col_headers[c][0]][m] != v[col_headers[c][0]][m]:
                                    outsheet.write(row, c + 1, '')
                                else:
                                    try:
                                        if v[col_headers[c][0]][m].find('(') > 0:
                                            ind = v[col_headers[c][0]][m].find('(')
                                            value = v[col_headers[c][0]][m][:ind]
                                            outsheet.write(row, c + 1, Decimal(value.replace('+', '')))
                                        else:
                                            outsheet.write(row, c + 1, Decimal(v[col_headers[c][0]][m].replace('+', '')))
                                    except AttributeError:
                                        outsheet.write(row, c + 1, Decimal(v[col_headers[c][0]][m]))
                    row += 1
            else:
                outsheet.write(row, 0, k)
                # Loop through the number of columns, assign based on specified data type
                for c in range(len(col_headers)):
                    try:
                        test_var = v[col_headers[c][0]][m]
                    except KeyError:
                        pass
                    else:
                        # Check in NaN
                        if v[col_headers[c][0]][m] != v[col_headers[c][0]][m]:
                            outsheet.write(row, c + 1, '')
                        elif col_headers[c][1] == 'str':
                            outsheet.write(row, c + 1, v[col_headers[c][0]][m])
                        elif col_headers[c][1] == 'int':
                            try:
                                outsheet.write(row, c + 1, int(v[col_headers[c][0]][m]))
                            except ValueError:
                                outsheet.write(row, c + 1, v[col_headers[c][0]][m])
                        elif col_headers[c][1] == 'decimal':
                            outsheet.write(row, c + 1, Decimal(v[col_headers[c][0]][m]))
                        elif col_headers[c][1] == 'sta':
                            try:
                                if v[col_headers[c][0]][m].find('(') > 0:
                                    ind = v[col_headers[c][0]][m].find('(')
                                    value = v[col_headers[c][0]][m][:ind]
                                    outsheet.write(row, c + 1, Decimal(value.replace('+', '')))
                                else:
                                    outsheet.write(row, c + 1, Decimal(v[col_headers[c][0]][m].replace('+', '')))
                            except AttributeError:
                                outsheet.write(row, c + 1, Decimal(v[col_headers[c][0]][m]))
                row += 1

def crash_type_table(outsheet, data_dict, excluded_items):

    col_headers = ['Element Type', 'Crash Type', 'Fatal and Injury Crashes', 'Fatal and Injury Crashes (%)',
                   'Property Damage Only Crashes', 'Property Damage Only Crashes (%)', 'Total Crashes',
                   'Total Crashes (%)']
    outsheet.write(0, 0, 'Highway Name')
    for c in range(len(col_headers)):
        outsheet.write(0, c + 1, col_headers[c])

    row = 1
    for k, v in data_dict.items():
        for m in range(len(v)):
            if v.iloc[:, 1][m] in excluded_items:
                pass
            else:
                outsheet.write(row, 0, k)
                for t in np.arange(2):
                    if v.iloc[:, t][m] != v.iloc[:, t][m]:
                        outsheet.write(row, t + 1, '')
                    else:
                        outsheet.write(row, t + 1, v.iloc[:, t][m])
                for t in np.arange(6):
                    if v.iloc[:, t + 2][m] != v.iloc[:, t + 2][m]:
                        outsheet.write(row, t + 3, '')
                    else:
                        outsheet.write(row, t + 3, Decimal(v.iloc[:, t + 2][m]))
                row += 1

def crash_summ_table(outsheet, data_dict):

    col_headers = ['First Year of Analysis', 'Last Year of Analysis', 'Evaluated Length (mi)',
                   'Average Future Road AADT (vpd)', 'Total Crashes', 'Fatal and Injury Crashes',
                   'Property-Damage-Only Crashes', 'Percent Fatal and Injury Crashes (%)',
                   'Percent Property-Damage-Only Crashes (%)', 'Crash Rate (crashes/mi/yr)',
                   'FI Crash Rate (crashes/mi/yr)', 'PDO Crash Rate (crashes/mi/yr)',
                   'Total Travel (million veh-mi)', 'Travel Crash Rate (crashes/million veh-mi)',
                   'Travel FI Crash Rate (crashes/million veh-mi)', 'Travel PDO Crash Rate (crashes/million veh-mi)']
    outsheet.write(0, 0, 'Highway Name')
    for c in range(len(col_headers)):
        outsheet.write(0, c + 1, col_headers[c])

    n = 0
    for k, v in data_dict.items():
        outsheet.write(n + 1, 0, k)
        outsheet.write(n + 1, 1, int(v[1][0]))
        outsheet.write(n + 1, 2, int(v[1][1]))
        outsheet.write(n + 1, 3, Decimal(v[1][2]))
        outsheet.write(n + 1, 4, int(v[1][3]))
        outsheet.write(n + 1, 5, Decimal(v[1][5]))
        outsheet.write(n + 1, 6, Decimal(v[1][6]))
        outsheet.write(n + 1, 7, Decimal(v[1][7]))
        outsheet.write(n + 1, 8, int(v[1][9]))
        outsheet.write(n + 1, 9, int(v[1][10]))
        outsheet.write(n + 1, 10, Decimal(v[1][12]))
        outsheet.write(n + 1, 11, Decimal(v[1][13]))
        outsheet.write(n + 1, 12, Decimal(v[1][14]))
        outsheet.write(n + 1, 13, Decimal(v[1][16]))
        outsheet.write(n + 1, 14, Decimal(v[1][17]))
        outsheet.write(n + 1, 15, Decimal(v[1][18]))
        outsheet.write(n + 1, 16, Decimal(v[1][19]))
        n += 1

def message_table(outsheet, data_dict):

    col_headers = [['Start Location (Sta. ft)', 'sta'],
                   ['End Location (Sta. ft)', 'sta'],
                   ['Message', 'str']]

    outsheet.write(0, 0, 'Highway Name')
    for c in range(len(col_headers)):
        outsheet.write(0, c + 1, col_headers[c][0])

    outsheet.write(0, 4, 'Data Problem?')

    row = 1
    # Loop through the number of html files
    for k, v in data_dict.items():

        # Loop through the number of rows in the html table
        for m in range(len(v)):
            outsheet.write(row, 0, k)
            # Loop through the number of columns, assign based on specified data type
            for c in range(len(col_headers)):
                if col_headers[c][1] == 'str':
                    outsheet.write(row, c + 1, v[col_headers[c][0]][m])
                    if 'This indicates there is problem with the input data.' in v[col_headers[c][0]][m]:
                        outsheet.write(row, 4, 'Yes')
                    else:
                        outsheet.write(row, 4, 'No')
                elif col_headers[c][1] == 'sta':
                    # Check in NaN
                    if v[col_headers[c][0]][m] != v[col_headers[c][0]][m]:
                        outsheet.write(row, c + 1, '')
                    else:
                        try:
                            if v[col_headers[c][0]][m].find('(') > 0:
                                ind = v[col_headers[c][0]][m].find('(')
                                value = v[col_headers[c][0]][m][:ind]
                                outsheet.write(row, c + 1, Decimal(value.replace('+', '')))
                            else:
                                outsheet.write(row, c + 1, Decimal(v[col_headers[c][0]][m].replace('+', '')))
                        except AttributeError:
                            outsheet.write(row, c + 1, Decimal(v[col_headers[c][0]][m]))
            row += 1