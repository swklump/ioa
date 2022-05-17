def frwy_tables(freeway_files, freeway_highwaynames, savelocation):
    from pandas import read_html
    from xlsxwriter import Workbook
    from bs4 import BeautifulSoup as bs
    from .helper_tables import data_to_excel, crash_type_table, crash_summ_table, message_table

    # Dictionaries for each freeway table. Keys are highway name, values are tables
    obs_crashes = {}
    homog_seg = {}
    homog_seg_scl = {}
    crash_homog_seg = {}
    crash_homog_seg_scl = {}
    summ = {}
    scl_summ = {}
    cr_seg = {}
    cr_seg_scl = {}
    exp_cr_seg = {}
    exp_cr_seg_scl = {}
    cr_horiz = {}
    exp_cr_horiz = {}
    cr_year = {}
    exp_cr_year = {}
    pred_exp_cr = {}
    cr_sev = {}
    cr_sev_scl = {}
    fs_type = {}
    exit_type = {}
    entrance_type = {}
    eval_message = {}

    # Add html tables to lists for freeways
    for h in range(len(freeway_files)):
        tbl = bs(open(freeway_files[h]), 'html.parser').find_all('table', {'class': 'Base'})
        tables = read_html(freeway_files[h])
        place = 0
        for t in range(len(tables)):
            if list(tables[t])[0] in ['Seg. No.', 'Inter. No.', 'Year', 'Name']:
                if place == 0:
                    place = t
        del tables[0:place]
        for t in range(len(tbl)):

            table_title = tbl[t].find('span', {'class': 'TableCaption'}).text
            for r in (('\n', ''), (' ', '')):
                table_title = table_title.replace(*r)

            # Observed Crashes
            if 'ObservedCrashesUsedintheEvaluation' in table_title:
                obs_crashes[freeway_highwaynames[h]] = tables[t]

            # Homogeneous Segments
            elif 'EvaluationFreeway-HomogeneousSegments' in table_title:
                homog_seg[freeway_highwaynames[h]] = tables[t]
            elif 'EvaluationFreeway-SpeedChangeLanes' in table_title:
                homog_seg_scl[freeway_highwaynames[h]] = tables[t]
            # Crash Homogeneous Segments
            elif 'CrashHighwayFreeway-HomogeneousSegments' in table_title:
                crash_homog_seg[freeway_highwaynames[h]] = tables[t]
            elif 'CrashHighwayFreeway-SpeedChangeLanes' in table_title:
                crash_homog_seg_scl[freeway_highwaynames[h]] = tables[t]

            # Crash Summary
            elif 'PredictedFreewayCrashRatesandFrequenciesSummary' in table_title or \
                    'ExpectedFreewayCrashRatesandFrequenciesSummary' in table_title:
                summ[freeway_highwaynames[h]] = tables[t]
            elif 'PredictedFreewaySpeedChangeLaneCrashRatesandFrequenciesSummary' in table_title or \
                    'ExpectedFreewaySpeedChangeLaneCrashRatesandFrequenciesSummary' in table_title:
                scl_summ[freeway_highwaynames[h]] = tables[t]

            # Crashes by Segments
            elif 'PredictedCrashFrequenciesandRatesbyFreewaySegment/Intersection' in table_title:
                cr_seg[freeway_highwaynames[h]] = tables[t]
            elif 'PredictedCrashFrequenciesandRatesbyFreewaySpeedChangeLane' in table_title:
                cr_seg_scl[freeway_highwaynames[h]] = tables[t]
            # Expected Crashes by Segments
            elif 'ExpectedCrashFrequenciesandRatesbyFreewaySegment/Intersection' in table_title:
                exp_cr_seg[freeway_highwaynames[h]] = tables[t]
            elif 'ExpectedCrashFrequenciesandRatesbyFreewaySpeedChangeLane' in table_title:
                exp_cr_seg_scl[freeway_highwaynames[h]] = tables[t]

            # Crashes by Horizontal Design Element
            elif 'PredictedCrashFrequenciesandRatesbyHorizontalDesignElement' in table_title:
                cr_horiz[freeway_highwaynames[h]] = tables[t]
            # Crashes by Horizontal Design Element, Expected
            elif 'ExpectedCrashFrequenciesandRatesbyHorizontalDesignElement' in table_title:
                exp_cr_horiz[freeway_highwaynames[h]] = tables[t]

            # Crashes by Year
            elif 'PredictedCrashFrequenciesbyYear' in table_title:
                cr_year[freeway_highwaynames[h]] = tables[t]
            # Crashes by Year, Expected
            elif 'ExpectedCrashFrequenciesbyYear' in table_title:
                exp_cr_year[freeway_highwaynames[h]] = tables[t]

            # Comparing Predicted and Expected Crashes
            elif 'ComparingPredictedandExpectedCrashesfortheEvaluationPeriod' in table_title:
                pred_exp_cr[freeway_highwaynames[h]] = tables[t]

            # Crashes by Severity
            elif 'PredictedCrashSeveritybyFreewaySegment' in table_title or \
                    'ExpectedCrashSeveritybyFreewaySegment' in table_title:
                cr_sev[freeway_highwaynames[h]] = tables[t]
            elif 'PredictedCrashSeveritybySpeedChangeLane' in table_title or \
                    'ExpectedCrashSeveritybySpeedChangeLane' in table_title:
                cr_sev_scl[freeway_highwaynames[h]] = tables[t]

            # Crashes by Type - Freeway Segments
            elif 'PredictedFreewayCrashTypeDistribution' in table_title or \
                    'ExpectedFreewayCrashTypeDistribution' in table_title:
                fs_type[freeway_highwaynames[h]] = tables[t]
            elif 'PredictedExitSpeedChangeLaneCrashTypeDistribution' in table_title or \
                    'ExpectedExitSpeedChangeLaneCrashTypeDistribution' in table_title:
                exit_type[freeway_highwaynames[h]] = tables[t]
            elif 'PredictedEntranceSpeedChangeLaneCrashTypeDistribution' in table_title or \
                    'ExpectedEntranceSpeedChangeLaneCrashTypeDistribution' in table_title:
                entrance_type[freeway_highwaynames[h]] = tables[t]

            # Evaluation Messages
            elif 'EvaluationMessage' in table_title:
                eval_message[freeway_highwaynames[h]] = tables[t]

    outbook = Workbook(savelocation + '/' + 'parsed_freewaysegment.xlsx')

    # Write columns for Observed Crashes
    if len(obs_crashes) > 0:
        outsheet = outbook.add_worksheet("Frwy_ObservedCrashes")
        col_headers = [['Year', 'int'],
                       ['Observed Crashes', 'int'],
                       ['Total Crashes Used', 'int'],
                       ['FI Crashes', 'int'],
                       ['FI no/C Crashes', 'int'],
                       ['PDO Crashes', 'int']]
        excluded_items = ['Year', ['All Years']]
        data_to_excel(outsheet, col_headers, obs_crashes, excluded_items)

    # Write columns for Homogeneous Segments
    if len(homog_seg) > 0:
        outsheet = outbook.add_worksheet("Frwy_HomogSegments")
        col_headers = [['Seg. No.', 'int'],
                       ['Type', 'str'],
                       ['Area Type', 'str'],
                       ['Start Location (Sta. ft)', 'sta'],
                       ['End Location (Sta. ft)', 'sta'],
                       ['Length (ft)', 'decimal'],
                       ['Length(mi)', 'decimal'],
                       ['AADT', 'str'],
                       ['Median Width (ft)', 'decimal'],
                       ['Effective Median Width (ft)', 'decimal'] ]
        data_to_excel(outsheet, col_headers, homog_seg)

    # Write columns for Homogeneous Segments. Speed Change Lane
    if len(homog_seg_scl) > 0:
        outsheet = outbook.add_worksheet("Frwy_HomogSegments_SCL")
        col_headers = [['Seg. No.', 'int'],
                       ['Type', 'str'],
                       ['Ramp Type', 'str'],
                       ['Start Location (Sta. ft)', 'sta'],
                       ['End Location (Sta. ft)', 'sta'],
                       ['Length (ft)', 'decimal'],
                       ['Length(mi)', 'decimal'],
                       ['AADT', 'str'],
                       ['Median Width (ft)', 'decimal'],
                       ['Effective Median Width (ft)', 'decimal']]
        data_to_excel(outsheet, col_headers, homog_seg_scl)

    # Write columns for Crash Highway Freeway Homogeneous Segments
    if len(crash_homog_seg) > 0:
        outsheet = outbook.add_worksheet("Frwy_CrashHomogSegments")
        col_headers = [['Seg. No.', 'int'],
                       ['Type', 'str'],
                       ['Area Type', 'str'],
                       ['Start Location (Sta. ft)', 'sta'],
                       ['End Location (Sta. ft)', 'sta'],
                       ['Length (ft)', 'decimal'],
                       ['Length(mi)', 'decimal'],
                       ['AADT', 'str'],
                       ['Median Width (ft)', 'decimal'],
                       ['Effective Median Width (ft)', 'decimal']]
        data_to_excel(outsheet, col_headers, crash_homog_seg)

    # Write columns for Crash Highway Freeway Homogeneous Segments, Speed Change Lane
    if len(crash_homog_seg_scl) > 0:
        outsheet = outbook.add_worksheet("Frwy_CrashHomogSegments_SCL")
        col_headers = [['Seg. No.', 'int'],
                       ['Type', 'str'],
                       ['Ramp Type', 'str'],
                       ['Start Location (Sta. ft)', 'sta'],
                       ['End Location (Sta. ft)', 'sta'],
                       ['Length (ft)', 'decimal'],
                       ['Length(mi)', 'decimal'],
                       ['AADT', 'str'],
                       ['Median Width (ft)', 'decimal'],
                       ['Effective Median Width (ft)', 'decimal']]
        data_to_excel(outsheet, col_headers, crash_homog_seg_scl)

    # Write columns for Crash Rates and Frequencies Summary
    if len(summ) > 0:
        outsheet = outbook.add_worksheet("Frwy_Crash_Summary")
        crash_summ_table(outsheet, summ)

    # Write columns for Speed Change Lane Crash Rates and Frequencies Summary
    if len(scl_summ) > 0:
        outsheet = outbook.add_worksheet("Frwy_Crash_Summary_SCL")
        crash_summ_table(outsheet, scl_summ)

    # Write columns for Crash Frequencies and Rates by Segment/Intersection
    if len(cr_seg) > 0:
        outsheet = outbook.add_worksheet("Frwy_Crash_Segment")
        col_headers = [['Segment Number/Intersection Name/Cross Road', 'int'],
                       ['Start Location (Sta. ft)', 'sta'],
                       ['End Location (Sta. ft)', 'sta'],
                       ['Effective Length (mi)', 'decimal'],
                       ['Total Predicted Crashes for Evaluation Period', 'decimal'],
                       ['Predicted Total Crash Frequency (crashes/yr)', 'decimal'],
                       ['Predicted FI Crash Frequency (crashes/yr)', 'decimal'],
                       ['Predicted PDO Crash Frequency (crashes/yr)', 'decimal'],
                       ['Predicted Crash Rate (crashes/mi/yr)', 'decimal'],
                       ['Predicted Travel Crash Rate (crashes/million veh-mi)', 'decimal'], ]
        excluded_items = ['Segment Number/Intersection Name/Cross Road', ['Total']]
        data_to_excel(outsheet, col_headers, cr_seg, excluded_items)

    # Write columns for Crash Frequencies and Rates by Speed Change Lane
    if len(cr_seg_scl) > 0:
        outsheet = outbook.add_worksheet("Frwy_Crash_Segment_SCL")
        col_headers = [['Segment Number/Intersection Name/Cross Road', 'int'],
                       ['Start Location (Sta. ft)', 'sta'],
                       ['End Location (Sta. ft)', 'sta'],
                       ['Length (mi)', 'decimal'],
                       ['Total Predicted Crashes for Evaluation Period', 'decimal'],
                       ['Predicted Total Crash Frequency (crashes/yr)', 'decimal'],
                       ['Predicted FI Crash Frequency (crashes/yr)', 'decimal'],
                       ['Predicted PDO Crash Frequency (crashes/yr)', 'decimal'],
                       ['Predicted Crash Rate (crashes/mi/yr)', 'decimal'],
                       ['Predicted Travel Crash Rate (crashes/million veh-mi)', 'decimal'], ]
        excluded_items = ['Segment Number/Intersection Name/Cross Road', ['Total']]
        data_to_excel(outsheet, col_headers, cr_seg_scl, excluded_items)

    # Write columns for Crash Frequencies and Rates by Segment/Intersection, Expected
    if len(exp_cr_seg) > 0:
        outsheet = outbook.add_worksheet("Frwy_Exp_Crash_Segment")
        col_headers = [['Segment Number/Intersection Name/Cross Road', 'int'],
                       ['Start Location (Sta. ft)', 'sta'],
                       ['End Location (Sta. ft)', 'sta'],
                       ['Effective Length (mi)', 'decimal'],
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

                       ['Expected Crash Rate (crashes/mi/yr)', 'decimal'],
                       ['Expected Travel Crash Rate (crashes/million veh-mi)', 'decimal'], ]
        excluded_items = ['Segment Number/Intersection Name/Cross Road', ['Total']]
        data_to_excel(outsheet, col_headers, exp_cr_seg, excluded_items)

    # Write columns for Crash Frequencies and Rates by Speed Change Lane, Expected
    if len(exp_cr_seg_scl) > 0:
        outsheet = outbook.add_worksheet("Frwy_Exp_Crash_Segment_SCL")
        col_headers = [['Segment Number/Intersection Name/Cross Road', 'int'],
                       ['Start Location (Sta. ft)', 'sta'],
                       ['End Location (Sta. ft)', 'sta'],
                       ['Length (mi)', 'decimal'],
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

                       ['Expected Crash Rate (crashes/mi/yr)', 'decimal'],
                       ['Expected Travel Crash Rate (crashes/million veh-mi)', 'decimal'], ]
        excluded_items = ['Segment Number/Intersection Name/Cross Road', ['Total']]
        data_to_excel(outsheet, col_headers, exp_cr_seg_scl, excluded_items)

    # Write columns for Horizontal Design Elements
    if len(cr_horiz) > 0:
        outsheet = outbook.add_worksheet("Frwy_HorizontalDesign")
        col_headers = [['Title', 'str'],
                       ['Start Location (Sta. ft)', 'sta'],
                       ['End Location (Sta. ft)', 'sta'],
                       ['Length (mi)', 'decimal'],
                       ['Total Predicted Crashes for Evaluation Period', 'decimal'],
                       ['Predicted Total Crash Frequency (crashes/yr)', 'decimal'],
                       ['Predicted FI Crash Frequency (crashes/yr)', 'decimal'],
                       ['Predicted PDO Crash Frequency (crashes/yr)', 'decimal'],
                       ['Predicted Crash Rate (crashes/mi/yr)', 'decimal'],
                       ['Predicted Travel Crash Rate (crashes/million veh-mi)', 'decimal']]
        data_to_excel(outsheet, col_headers, cr_horiz)

    # Write columns for Horizontal Design Elements, Expected
    if len(exp_cr_horiz) > 0:
        outsheet = outbook.add_worksheet("Frwy_Exp_HorizontalDesign")
        col_headers = [['Title', 'str'],
                       ['Start Location (Sta. ft)', 'sta'],
                       ['End Location (Sta. ft)', 'sta'],
                       ['Length (mi)', 'decimal'],
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

                       ['Expected Crash Rate (crashes/mi/yr)', 'decimal'],
                       ['Expected Travel Crash Rate (crashes/million veh-mi)', 'decimal']]
        data_to_excel(outsheet, col_headers, exp_cr_horiz)

    # Write columns for Crash Frequencies by Year
    if len(cr_year) > 0:
        outsheet = outbook.add_worksheet("Frwy_Crash_Year")
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
        outsheet = outbook.add_worksheet("Frwy_Exp_Crash_Year")
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
        outsheet = outbook.add_worksheet("Frwy_Pred_Exp_Crashes")
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
        outsheet = outbook.add_worksheet("Frwy_Crash_Sev")
        col_headers = [['Seg. No.', 'int'],
                       ['Fatal (K) Crashes (crashes)', 'decimal'],
                       ['Incapacitating Injury (A) Crashes (crashes)', 'decimal'],
                       ['Non-Incapacitating Injury (B) Crashes (crashes)', 'decimal'],
                       ['Possible Injury (C) Crashes (crashes)', 'decimal'],
                       ['No Injury (O) Crashes (crashes)', 'decimal']]
        excluded_items = ['Seg. No.', ['Total']]
        data_to_excel(outsheet, col_headers, cr_sev, excluded_items)
        col_list = ['Fatal (K) Crashes', 'Incapacitating Injury (A) Crashes',
                    'Non-Incapacitating Injury (B) Crashes', 'Possible Injury (C) Crashes',
                    'No Injury (O) Crashes']
        for s in range(len(col_list)):
            outsheet.write(0, s + 2, col_list[s])

    # Write columns for Severity, Speed Change Lane
    if len(cr_sev_scl) > 0:
        outsheet = outbook.add_worksheet("Frwy_Crash_Sev_SCL")
        col_headers = [['Seg. No.', 'int'],
                       ['Fatal (K) Crashes (crashes)', 'decimal'],
                       ['Incapacitating Injury (A) Crashes (crashes)', 'decimal'],
                       ['Non-Incapacitating Injury (B) Crashes (crashes)', 'decimal'],
                       ['Possible Injury (C) Crashes (crashes)', 'decimal'],
                       ['No Injury (O) Crashes (crashes)', 'decimal']]
        excluded_items = ['Seg. No.', ['Total']]
        data_to_excel(outsheet, col_headers, cr_sev_scl, excluded_items)
        col_list = ['Fatal (K) Crashes', 'Incapacitating Injury (A) Crashes',
                    'Non-Incapacitating Injury (B) Crashes', 'Possible Injury (C) Crashes',
                    'No Injury (O) Crashes']
        for s in range(len(col_list)):
            outsheet.write(0, s + 2, col_list[s])

    # Write columns for  Freeway Crash Type Distribution
    if len(fs_type) > 0:
        outsheet = outbook.add_worksheet("Frwy_Crash_FS_Type")
        excluded_items = ['Total Single Vehicle Crashes', 'Total Multiple Vehicle Crashes',
                          'Total Highway Segment Crashes', 'Total Crashes']
        crash_type_table(outsheet, fs_type, excluded_items)

    # Write columns for Exit Speed Change Lane Crash Type Distribution
    if len(exit_type) > 0:
        outsheet = outbook.add_worksheet("Frwy_Crash_Exit_Type")
        excluded_items = ['Total Single Vehicle Crashes', 'Total Multiple Vehicle Crashes',
                          'Total Highway Segment Crashes', 'Total Crashes']
        crash_type_table(outsheet, exit_type, excluded_items)

    # Write columns for Entrance Speed Change Lane Crash Type Distribution
    if len(entrance_type) > 0:
        outsheet = outbook.add_worksheet("Frwy_Crash_Entrance_Type")
        excluded_items = ['Total Single Vehicle Crashes', 'Total Multiple Vehicle Crashes',
                          'Total Highway Segment Crashes', 'Total Crashes']
        crash_type_table(outsheet, entrance_type, excluded_items)

    # Write columns for Evaluation Messages
    if len(eval_message) > 0:
        outsheet = outbook.add_worksheet("Frwy_Evaluation_Message")
        message_table(outsheet, eval_message)

    outbook.close()
