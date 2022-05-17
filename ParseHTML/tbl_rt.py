def rt_tables(rampterminal_files, rampterminal_highwaynames, savelocation):
    from pandas import read_html
    from xlsxwriter import Workbook
    from decimal import Decimal
    from bs4 import BeautifulSoup as bs
    from .helper_tables import data_to_excel, crash_type_table, message_table

    # Dictionaries for each arterial table. Keys are highway name, values are tables
    obs_crashes = {}
    rt_site = {}
    cr_rt_site = {}
    summ = {}
    cr_seg = {}
    exp_cr_seg = {}
    cr_year = {}
    exp_cr_year = {}
    pred_exp_cr = {}
    cr_sev = {}
    type = {}
    eval_message = {}

    # Add html tables to lists for arterials
    for h in range(len(rampterminal_files)):
        tbl = bs(open(rampterminal_files[h]), 'html.parser').find_all('table', {'class': 'Base'})
        tables = read_html(rampterminal_files[h])
        place = 0
        for t in range(len(tables)):
            if list(tables[t])[0] in ['Seg. No.', 'Inter. No.', 'Site No.', 'Year']:
                if place == 0:
                    place = t
        del tables[0:place]
        for t in range(len(tbl)):

            table_title = tbl[t].find('span', {'class': 'TableCaption'}).text
            for r in (('\n', ''), (' ', '')):
                table_title = table_title.replace(*r)

            # Observed Crashes
            if 'ObservedCrashesUsedintheEvaluation' in table_title:
                obs_crashes[rampterminal_highwaynames[h]] = tables[t]

            # Evaluation Ramp Terminal Site
            elif 'EvaluationRampTerminal-Site' in table_title:
                rt_site[rampterminal_highwaynames[h]] = tables[t]
            # Crash Highway Ramp Terminal - Site
            elif 'CrashHighwayRampTerminal-Site' in table_title:
                cr_rt_site[rampterminal_highwaynames[h]] = tables[t]

            # Crash Summary
            elif 'PredictedRampTerminalCrashRatesandFrequenciesSummary' in table_title or \
                    'ExpectedRampTerminalCrashRatesandFrequenciesSummary' in table_title:
                summ[rampterminal_highwaynames[h]] = tables[t]

            # Crashes by Segments
            elif 'PredictedCrashFrequenciesandRatesbyRampTerminal' in table_title:
                cr_seg[rampterminal_highwaynames[h]] = tables[t]
            # Crashes by Segments, Expected
            elif 'ExpectedCrashFrequenciesandRatesbyRampTerminal' in table_title:
                exp_cr_seg[rampterminal_highwaynames[h]] = tables[t]

            # Crashes by Year
            elif 'PredictedCrashFrequenciesbyYear' in table_title:
                cr_year[rampterminal_highwaynames[h]] = tables[t]
            # Crashes by Year, Expected
            elif 'ExpectedCrashFrequenciesbyYear' in table_title:
                exp_cr_year[rampterminal_highwaynames[h]] = tables[t]

            # Comparing Predicted and Expected Crashes
            elif 'ComparingPredictedandExpectedCrashesfortheEvaluationPeriod' in table_title:
                pred_exp_cr[rampterminal_highwaynames[h]] = tables[t]

            # Crashes by Severity
            elif 'PredictedCrashSeveritybyRampTerminal' in table_title or \
                    'ExpectedCrashSeveritybyRampTerminal' in table_title:
                cr_sev[rampterminal_highwaynames[h]] = tables[t]

            # Crashes by Type - Ramp Terminals
            elif 'PredictedRampTerminalCrashTypeDistribution' in table_title or \
                    'ExpectedRampTerminalCrashTypeDistribution' in table_title:
                type[rampterminal_highwaynames[h]] = tables[t]

            # Evaluation Messages
            elif 'EvaluationMessage' in table_title:
                eval_message[rampterminal_highwaynames[h]] = tables[t]

    if len(summ) > 0:
        outbook = Workbook(savelocation + '/' + 'parsed_rampterminal.xlsx')

        # Write columns for Observed Crashes
        if len(obs_crashes) > 0:
            outsheet = outbook.add_worksheet("RT_ObservedCrashes")
            col_headers = [['Year', 'int'],
                           ['Observed Crashes', 'int'],
                           ['Total Crashes Used', 'int'],
                           ['FI Crashes', 'int'],
                           ['FI no/C Crashes', 'int'],
                           ['PDO Crashes', 'int']]
            excluded_items = ['Year', ['All Years']]
            data_to_excel(outsheet, col_headers, obs_crashes, excluded_items)

        # Write columns for Sites
        if len(rt_site) > 0:
            outsheet = outbook.add_worksheet("RT_Sites")
            col_headers = [['Inter. No.', 'int'],
                           ['Title', 'str'],
                           ['Ramp Terminal Type', 'str'],
                           ['Area Type', 'str'],
                           ['Legs', 'int'],
                           ['Location (Sta. ft)', 'sta'],
                           ['Traffic Control', 'str'],
                           ['AADT', 'str'], ]
            data_to_excel(outsheet, col_headers, rt_site)

        # Write columns for Sites, Expected
        if len(cr_rt_site) > 0:
            outsheet = outbook.add_worksheet("RT_Exp_Sites")
            col_headers = [['Inter. No.', 'int'],
                           ['Title', 'str'],
                           ['Ramp Terminal Type', 'str'],
                           ['Area Type', 'str'],
                           ['Legs', 'int'],
                           ['Location (Sta. ft)', 'sta'],
                           ['Traffic Control', 'str'],
                           ['AADT', 'str'], ]
            data_to_excel(outsheet, col_headers, cr_rt_site)

        # Write columns for  Predicted Ramp Terminal Crash Rates and Frequencies Summary
        if len(summ) > 0:
            outsheet = outbook.add_worksheet("RT_Crash_Summary")
            col_headers = ['First Year of Analysis', 'Last Year of Analysis', 'Evaluated Length (mi)',
                           'Average Future Road AADT (vpd)', 'Total Crashes', 'Fatal and Injury Crashes',
                           'Property-Damage-Only Crashes', 'Percent Fatal and Injury Crashes (%)',
                           'Percent Property-Damage-Only Crashes (%)']
            outsheet.write(0, 0, 'Highway Name')
            for c in range(len(col_headers)):
                outsheet.write(0, c + 1, col_headers[c])

            n = 0
            for k, v in summ.items():
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
                n += 1

        # Write columns for Crash Frequencies and Rates by Ramp Terminal
        if len(cr_seg) > 0:
            outsheet = outbook.add_worksheet("RT_Crash_Segment")
            col_headers = [['Segment Number/Intersection Name/Cross Road', 'str'],
                           ['Location (Sta. ft)', 'sta'],
                           ['Total Predicted Crashes for Evaluation Period', 'decimal'],
                           ['Predicted Total Crash Frequency (crashes/yr)', 'decimal'],
                           ['Predicted FI Crash Frequency (crashes/yr)', 'decimal'],
                           ['Predicted PDO Crash Frequency (crashes/yr)', 'decimal'],
                           ['Predicted Travel Crash Rate (crashes/million veh)', 'decimal'], ]
            excluded_items = ['Segment Number/Intersection Name/Cross Road', ['Total']]
            data_to_excel(outsheet, col_headers, cr_seg, excluded_items)

        # Write columns for Crash Frequencies and Rates by Ramp Terminal, Expected
        if len(exp_cr_seg) > 0:
            outsheet = outbook.add_worksheet("RT_Exp_Crash_Segment")
            col_headers = [['Segment Number/Intersection Name/Cross Road', 'str'],
                           ['Location (Sta. ft)', 'sta'],
                           ['Total Expected Crashes for Evaluation Period', 'decimal'],
                           ['Total Predicted Crashes for Evaluation Period', 'decimal'],

                           ['Expected Total Crash Frequency (crashes/yr)', 'decimal'],
                           ['Expected FI Crash Frequency (crashes/yr)', 'decimal'],
                           ['Expected PDO Crash Frequency (crashes/yr)', 'decimal'],

                           ['Predicted Total Crash Frequency (crashes/yr)', 'decimal'],
                           ['Predicted FI Crash Frequency (crashes/yr)', 'decimal'],
                           ['Predicted PDO Crash Frequency (crashes/yr)', 'decimal'],

                           ['(Expected - Predicted) Total Crash Frequency (crashes/yr)', 'decimal'],
                           ['(Expected - Predicted) FI Crash Frequency (crashes/yr)', 'decimal'],
                           ['(Expected - Predicted) PDO Crash Frequency (crashes/yr)', 'decimal'],

                           ['Expected Travel Crash Rate (crashes/million veh)', 'decimal'], ]
            excluded_items = ['Segment Number/Intersection Name/Cross Road', ['Total']]
            data_to_excel(outsheet, col_headers, exp_cr_seg, excluded_items)

        # Write columns for Crash Frequencies by Year
        if len(cr_year) > 0:
            outsheet = outbook.add_worksheet("RT_Crash_Year")
            col_headers = [['Year', 'int'],
                           ['Total Crashes', 'decimal'],
                           ['FI Crashes', 'decimal'],
                           ['Percent FI (%)', 'decimal'],
                           ['PDO Crashes', 'decimal'],
                           ['Percent PDO (%)', 'decimal']]
            excluded_items = ['Year', ['Total', 'Average']]
            data_to_excel(outsheet, col_headers, cr_year, excluded_items)

        # Write columns for Crash Frequencies by Year, Expected
        if len(exp_cr_year) > 0:
            outsheet = outbook.add_worksheet("RT_Exp_Crash_Year")
            col_headers = [['Year', 'int'],
                           ['Total Crashes', 'decimal'],
                           ['FI Crashes', 'decimal'],
                           ['Percent FI (%)', 'decimal'],
                           ['PDO Crashes', 'decimal'],
                           ['Percent PDO (%)', 'decimal']]
            excluded_items = ['Year', ['Total', 'Average']]
            data_to_excel(outsheet, col_headers, exp_cr_year, excluded_items)

        # Write columns for Comparing Predicted and Expected Crashes
        if len(pred_exp_cr) > 0:
            outsheet = outbook.add_worksheet("RT_Pred_Exp_Crashes")
            col_headers = [['Scope', 'str'],
                           ['Total Crashes', 'decimal'],
                           ['FI Crashes', 'decimal'],
                           ['Percent FI (%)', 'decimal'],
                           ['PDO Crashes', 'decimal'],
                           ['Percent PDO (%)', 'decimal']]
            excluded_items = ['Scope', ['Expected - Predicted', 'Percent Difference']]
            data_to_excel(outsheet, col_headers, pred_exp_cr, excluded_items)

        # Write columns for Severity
        if len(cr_sev) > 0:
            outsheet = outbook.add_worksheet("RT_Crash_Sev")
            col_headers = [['Seg. No.', 'int'],
                           ['Fatal (K) Crashes (crashes)', 'decimal'],
                           ['Incapacitating Injury (A) Crashes (crashes)', 'decimal'],
                           ['Non-Incapacitating Injury (B) Crashes (crashes)', 'decimal'],
                           ['Possible Injury (C) Crashes (crashes)', 'decimal'],
                           ['No Injury (O) Crashes (crashes)', 'decimal']]
            excluded_items = ['Seg. No.', ['Total']]
            data_to_excel(outsheet, col_headers, cr_sev, excluded_items)

            col_list = ['Fatal (K) Crashes', 'Incapacitating Injury (A) Crashes',
                        'Non-Incapacitating Injury (B) Crashes', 'Possible Injury (C) Crashes', 'No Injury (O) Crashes']
            for s in range(len(col_list)):
                outsheet.write(0, s + 2, col_list[s])

        # Write columns for Ramp Terminal Crash Type
        if len(type) > 0:
            outsheet = outbook.add_worksheet("RT_Crash_Type")
            excluded_items = ['Total Single Vehicle Crashes', 'Total Multiple Vehicle Crashes',
                              'Total Ramp Terminal Crashes', 'Total Crashes']
            crash_type_table(outsheet, type, excluded_items)

        # Write columns for Evaluation Messages
        if len(eval_message) > 0:
            outsheet = outbook.add_worksheet("RT_Evaluation_Message")
            message_table(outsheet, eval_message)

        outbook.close()

    else:
        pass


