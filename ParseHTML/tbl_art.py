def art_tables(arterial_files, arterial_highwaynames, savelocation):
    from pandas import read_html
    from xlsxwriter import Workbook
    from decimal import Decimal
    from bs4 import BeautifulSoup as bs
    from .helper_tables import data_to_excel, crash_type_table, crash_summ_table, message_table

    # Dictionaries for each arterial table. Keys are highway name, values are tables
    obs_crashes = {}
    homog_seg = {}
    crash_homog_seg = {}
    eval_int = {}
    crash_eval_int = {}
    eval_rt = {}
    crash_eval_rt = {}
    summ = {}
    cr_seg = {}
    exp_cr_seg = {}
    cr_horiz = {}
    exp_cr_horiz = {}
    cr_year = {}
    exp_cr_year = {}
    pred_exp_cr = {}
    cr_sev = {}
    cr_sev_rt = {}
    six_lane_type = {}
    five_lane_type = {}
    one_way_type = {}
    cr_type = {}
    eval_message = {}

    # Add html tables to lists for arterials
    for h in range(len(arterial_files)):
        tbl = bs(open(arterial_files[h]), 'html.parser').find_all('table', {'class': 'Base'})
        tables = read_html(arterial_files[h])
        place = 0
        for t in range(len(tables)):
            if list(tables[t])[0] in ['Seg. No.', 'Inter. No.', 'Year']:
                if place == 0:
                    place = t
        del tables[0:place]
        for t in range(len(tbl)):

            table_title = tbl[t].find('span', {'class': 'TableCaption'}).text
            for r in (('\n', ''), (' ', '')):
                table_title = table_title.replace(*r)

            # Observed Crashes
            if 'ObservedCrashesUsedintheEvaluation' in table_title:
                obs_crashes[arterial_highwaynames[h]] = tables[t]

            # Homogeneous Segments/Intersections
            elif 'EvaluationHighway-HomogeneousSegments' in table_title:
                homog_seg[arterial_highwaynames[h]] = tables[t]
            # Crash Homogeneous Segments
            elif 'CrashHighwayHighway-HomogeneousSegments' in table_title:
                crash_homog_seg[arterial_highwaynames[h]] = tables[t]
            elif 'EvaluationIntersection' in table_title:
                eval_int[arterial_highwaynames[h]] = tables[t]
            elif 'CrashHistoryIntersection' in table_title:
                crash_eval_int[arterial_highwaynames[h]] = tables[t]
            elif 'EvaluationRampTerminal-Site' in table_title:
                eval_rt[arterial_highwaynames[h]] = tables[t]
            elif 'CrashHighwayRampTerminal-Site' in table_title:
                crash_eval_rt[arterial_highwaynames[h]] = tables[t]

            # Crash Summary
            elif 'PredictedHighwayCrashRatesandFrequenciesSummary' in table_title or \
                    'ExpectedHighwayCrashRatesandFrequenciesSummary' in table_title:
                summ[arterial_highwaynames[h]] = tables[t]

            # Crashes by Segments
            elif 'PredictedCrashFrequenciesandRatesbyHighwaySegment/Intersection' in table_title:
                cr_seg[arterial_highwaynames[h]] = tables[t]
            # Expected Crashes by Segments
            elif 'ExpectedCrashFrequenciesandRatesbyHighwaySegment/Intersection' in table_title:
                exp_cr_seg[arterial_highwaynames[h]] = tables[t]

            # Crashes by Horizontal Design Element
            elif 'PredictedCrashFrequenciesandRatesbyHorizontalDesignElement' in table_title:
                cr_horiz[arterial_highwaynames[h]] = tables[t]
            # Crashes by Horizontal Design Element, Expected
            elif 'ExpectedCrashFrequenciesandRatesbyHorizontalDesignElement' in table_title:
                exp_cr_horiz[arterial_highwaynames[h]] = tables[t]

            # Crashes by Year
            elif 'PredictedCrashFrequenciesbyYear' in table_title:
                cr_year[arterial_highwaynames[h]] = tables[t]
            # Crashes by Year, Expected
            elif 'ExpectedCrashFrequenciesbyYear' in table_title:
                exp_cr_year[arterial_highwaynames[h]] = tables[t]

            # Comparing Predicted and Expected Crashes
            elif 'ComparingPredictedandExpectedCrashesfortheEvaluationPeriod' in table_title:
                pred_exp_cr[arterial_highwaynames[h]] = tables[t]

            # Crashes by Severity
            elif 'PredictedCrashSeveritybyUrbanArterial' in table_title or \
                    'ExpectedCrashSeveritybyUrbanArterial' in table_title:
                cr_sev[arterial_highwaynames[h]] = tables[t]
            elif 'PredictedCrashSeveritybyRampTerminalorRoundabout' in table_title or \
                    'ExpectedCrashSeveritybyRampTerminalorRoundabout' in table_title:
                cr_sev_rt[arterial_highwaynames[h]] = tables[t]

            # Crashes by Type - Arterials
            elif 'PredictedSixLaneorGreaterCrashTypeDistribution' in table_title or \
                    'ExpectedSixLaneorGreaterCrashTypeDistribution' in table_title:
                six_lane_type[arterial_highwaynames[h]] = tables[t]
            elif 'PredictedFiveLaneorFewerCrashTypeDistribution' in table_title or \
                    'ExpectedFiveLaneorFewerCrashTypeDistribution' in table_title:
                five_lane_type[arterial_highwaynames[h]] = tables[t]
            elif 'PredictedOne-wayArterialCrashTypeDistribution' in table_title or \
                    'ExpectedOne-wayArterialCrashTypeDistribution' in table_title:
                one_way_type[arterial_highwaynames[h]] = tables[t]
            elif 'PredictedCrashTypeDistribution' in table_title or \
                    'ExpectedCrashTypeDistribution' in table_title:
                cr_type[arterial_highwaynames[h]] = tables[t]

            # Evaluation Messages
            elif 'EvaluationMessage' in table_title:
                eval_message[arterial_highwaynames[h]] = tables[t]

    outbook = Workbook(savelocation + '/' + 'parsed_arterialsegment.xlsx')

    # Write columns for Observed Crashes
    if len(obs_crashes) > 0:
        outsheet = outbook.add_worksheet("Art_ObservedCrashes")
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
        outsheet = outbook.add_worksheet("Art_HomogSegments")
        col_headers = [ ['Seg. No.', 'int'],
                        ['Type', 'str'],
                        ['Start Location (Sta. ft)', 'sta'],
                        ['End Location (Sta. ft)', 'sta'],
                        ['Length (ft)', 'decimal'],
                        ['Length(mi)', 'decimal'],
                        ['AADT', 'str'],
                        ['Number Major Commericial Driveways', 'int'],
                        ['Number Minor Commericial Driveways', 'int'],
                        ['Number Major Industial/Institutional', 'int'],
                        ['Number Minor Industial/Institutional', 'int'],
                        ['Number Major Residential Driveways', 'int'],
                        ['Number Minor Residential Driveways', 'int'],
                        ['Number Other Driveways', 'int'],
                        ['Lighting', 'str'],
                        ['Automated Speed Enforcement', 'str'],
                        ['Density (fixed objects/mi)', 'decimal'],
                        ['Median Width (ft)', 'decimal'],
                        ['Effective Median Width (ft)', 'decimal'],
                        ['Speed Level', 'str'],
                        ['Number Rail Highway Crossings', 'int'],
                        ['Average Shoulder Width (ft)', 'decimal'],
                        ['Average Lane Width (ft)', 'decimal'], ]
        data_to_excel(outsheet, col_headers, homog_seg)

    # Write columns for Homogeneous Segments, Expected
    if len(crash_homog_seg) > 0:
        outsheet = outbook.add_worksheet("Art_CrashHomogSegments")
        col_headers = [ ['Seg. No.', 'int'],
                        ['Type', 'str'],
                        ['Start Location (Sta. ft)', 'sta'],
                        ['End Location (Sta. ft)', 'sta'],
                        ['Length (ft)', 'decimal'],
                        ['Length(mi)', 'decimal'],
                        ['AADT', 'str'],
                        ['Number Major Commericial Driveways', 'int'],
                        ['Number Minor Commericial Driveways', 'int'],
                        ['Number Major Industial/Institutional', 'int'],
                        ['Number Minor Industial/Institutional', 'int'],
                        ['Number Major Residential Driveways', 'int'],
                        ['Number Minor Residential Driveways', 'int'],
                        ['Number Other Driveways', 'int'],
                        ['Lighting', 'str'],
                        ['Automated Speed Enforcement', 'str'],
                        ['Density (fixed objects/mi)', 'decimal'],
                        ['Median Width (ft)', 'decimal'],
                        ['Effective Median Width (ft)', 'decimal'],
                        ['Speed Level', 'str'],
                        ['Number Rail Highway Crossings', 'int'],
                        ['Average Shoulder Width (ft)', 'decimal'],
                        ['Average Lane Width (ft)', 'decimal'], ]
        data_to_excel(outsheet, col_headers, crash_homog_seg)

    # Write columns for Evaluation Intersection
    if len(eval_int) > 0:
        outsheet = outbook.add_worksheet("Art_EvalIntersection")
        col_headers = [ ['Inter. No.', 'int'],
                        ['Title', 'str'],
                        ['Location (Sta. ft)', 'sta'],
                        ['Major AADT', 'str'],
                        ['Minor AADT', 'str'],
                        ['Legs', 'int'],
                        ['Traffic Control', 'str'],
                        ['Intersection Type', 'str'],
                        ['Approaches w/Left Turn Lanes', 'int'],
                        ['Approaches w/Right Turn Lanes', 'int'],
                        ['Approaches w/o Right Turn on Red', 'int'],
                        ['Pedestrian Volume (crossings/day)', 'int'],
                        ['Lighted at Night', 'str'],
                        ['Red Light Camera', 'str'],
                        ['School Nearby', 'str'],
                        ['Number of Bus Stops', 'int'],
                        ['Number of Alcohol Sales Establishments', 'int'],
                        ['Max Lanes Crossed', 'int'] ]
        data_to_excel(outsheet, col_headers, eval_int)

    # Write columns for Evaluation Intersection, Expected
    if len(crash_eval_int) > 0:
        outsheet = outbook.add_worksheet("Art_CrashEvalIntersection")
        col_headers = [ ['Inter. No.', 'int'],
                        ['Title', 'str'],
                        ['Location (Sta. ft)', 'sta'],
                        ['Major AADT', 'str'],
                        ['Minor AADT', 'str'],
                        ['Legs', 'int'],
                        ['Traffic Control', 'str'],
                        ['Intersection Type', 'str'],
                        ['Approaches w/Left Turn Lanes', 'int'],
                        ['Approaches w/Right Turn Lanes', 'int'],
                        ['Approaches w/o Right Turn on Red', 'int'],
                        ['Pedestrian Volume (crossings/day)', 'int'],
                        ['Lighted at Night', 'str'],
                        ['Red Light Camera', 'str'],
                        ['School Nearby', 'str'],
                        ['Number of Bus Stops', 'int'],
                        ['Number of Alcohol Sales Establishments', 'int'],
                        ['Max Lanes Crossed', 'int'] ]
        data_to_excel(outsheet, col_headers, crash_eval_int)

    # Write columns for Evaluation Ramp Terminal
    if len(eval_rt) > 0:
        outsheet = outbook.add_worksheet("Art_EvalRampTerminal")
        col_headers = [ ['Inter. No.', 'int'],
                        ['Title', 'str'],
                        ['Ramp Terminal Type', 'str'],
                        ['Area Type', 'str'],
                        ['Legs', 'int'],
                        ['Location (Sta. ft)', 'sta'],
                        ['Traffic Control', 'str'],
                        ['AADT', 'str'] ]
        data_to_excel(outsheet, col_headers, eval_rt)

    # Write columns for Evaluation Ramp Terminal, Expected
    if len(crash_eval_rt) > 0:
        outsheet = outbook.add_worksheet("Art_CrashEvalRampTerminal")
        col_headers = [ ['Inter. No.', 'int'],
                        ['Title', 'str'],
                        ['Ramp Terminal Type', 'str'],
                        ['Area Type', 'str'],
                        ['Legs', 'int'],
                        ['Location (Sta. ft)', 'sta'],
                        ['Traffic Control', 'str'],
                        ['AADT', 'str'] ]
        data_to_excel(outsheet, col_headers, eval_rt)

    # Write columns for Crash Rates and Frequencies Summary
    if len(summ) > 0:
        outsheet = outbook.add_worksheet("Art_Crash_Summary")
        crash_summ_table(outsheet, summ)

    # Write columns for Crash Frequencies and Rates by Segment/Intersection
    if len(cr_seg) > 0:
        outsheet = outbook.add_worksheet("Art_Crash_Segment")
        col_headers = [['Segment Number/Intersection Name/Cross Road', 'int'],
                       ['Start Location (Sta. ft)', 'sta'],
                       ['End Location (Sta. ft)', 'sta'],
                       ['Length (mi)', 'decimal'],
                       ['Total Predicted Crashes for Evaluation Period', 'decimal'],
                       ['Predicted Total Crash Frequency (crashes/yr)', 'decimal'],
                       ['Predicted FI Crash Frequency (crashes/yr)', 'decimal'],
                       ['Predicted PDO Crash Frequency (crashes/yr)', 'decimal'],
                       ['Predicted Crash Rate (crashes/mi/yr)', 'decimal'],
                       ['Predicted Travel Crash Rate (crashes/million veh-mi)', 'decimal'],
                       ['Predicted Intersection Travel Crash Rate (crashes/million veh)', 'decimal'], ]
        excluded_items = ['Segment Number/Intersection Name/Cross Road', ['Total', 'All Segments', 'All Intersections']]
        data_to_excel(outsheet, col_headers, cr_seg, excluded_items)

    # Write columns for Crash Frequencies and Rates by Segment/Intersection
    if len(exp_cr_seg) > 0:
        outsheet = outbook.add_worksheet("Art_Exp_Crash_Segment")
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
                       ['Expected Travel Crash Rate (crashes/million veh-mi)', 'decimal'],
                       ['Expected Intersection Travel Crash Rate (crashes/million veh)', 'decimal'],]
        excluded_items = ['Segment Number/Intersection Name/Cross Road', ['Total', 'All Segments', 'All Intersections']]
        data_to_excel(outsheet, col_headers, exp_cr_seg, excluded_items)

    # Write columns for Horizontal Design Elements
    if len(cr_horiz) > 0:
        outsheet = outbook.add_worksheet("Art_HorizontalDesign")
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
        outsheet = outbook.add_worksheet("Art_Exp_HorizontalDesign")
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
        outsheet = outbook.add_worksheet("Art_Crash_Year")
        col_headers = [['Year', 'int', ['Total', 'Average']],
                       ['Total Crashes', 'decimal'],
                       ['FI Crashes', 'decimal'],
                       ['Percent FI (%)', 'decimal'],
                       ['PDO Crashes', 'decimal'],
                       ['Percent PDO (%)', 'decimal']]
        excluded_items = ['Year', ['Total', 'Average']]
        data_to_excel(outsheet, col_headers, cr_year, excluded_items)

    # Write columns for Crash Frequencies by Year, Expected
    if len(exp_cr_year) > 0:
        outsheet = outbook.add_worksheet("Art_Exp_Crash_Year")
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
        outsheet = outbook.add_worksheet("Art_Pred_Exp_Crashes")
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
        outsheet = outbook.add_worksheet("Art_Crash_Sev")
        col_headers = [['Seg. No.', 'int'],
                       ['Type', 'str'],
                       ['Fatal (K) Crashes (crashes)', 'decimal'],
                       ['Incapacitating Injury (A) Crashes (crashes)', 'decimal'],
                       ['Non-Incapacitating Injury (B) Crashes (crashes)', 'decimal'],
                       ['Possible Injury (C) Crashes (crashes)', 'decimal'],
                       ['No Injury (O) Crashes (crashes)', 'decimal']]
        excluded_items = ['Seg. No.', ['Total', 'All Segments', 'All Intersections']]
        data_to_excel(outsheet, col_headers, cr_sev, excluded_items)

        col_list = ['Fatal (K) Crashes', 'Incapacitating Injury (A) Crashes',
                    'Non-Incapacitating Injury (B) Crashes', 'Possible Injury (C) Crashes', 'No Injury (O) Crashes']
        for s in range(len(col_list)):
            outsheet.write(0, s + 3, col_list[s])

    # Write columns for Severity, Ramp Terminal or Roundabout
    if len(cr_sev_rt) > 0:
        outsheet = outbook.add_worksheet("Art_Crash_Sev_RT")
        col_headers = [['Seg. No.', 'int'],
                       ['Type', 'str'],
                       ['Fatal (K) Crashes (crashes)', 'decimal'],
                       ['Incapacitating Injury (A) Crashes (crashes)', 'decimal'],
                       ['Non-Incapacitating Injury (B) Crashes (crashes)', 'decimal'],
                       ['Possible Injury (C) Crashes (crashes)', 'decimal'],
                       ['No Injury (O) Crashes (crashes)', 'decimal']]
        excluded_items = ['Seg. No.', ['Total', 'All Segments', 'All Intersections']]
        data_to_excel(outsheet, col_headers, cr_sev_rt, excluded_items)

        col_list = ['Fatal (K) Crashes', 'Incapacitating Injury (A) Crashes',
                    'Non-Incapacitating Injury (B) Crashes', 'Possible Injury (C) Crashes', 'No Injury (O) Crashes']
        for s in range(len(col_list)):
            outsheet.write(0, s + 3, col_list[s])

    # Excluded items for crash type tables
    excluded_items = ['Total Segment Single Vehicle Crashes', 'Total Single Vehicle Crashes',
                      'Total Segment Multiple Vehicle Crashes', 'Total Multiple Vehicle Crashes',
                      'Total Highway Segment Crashes', 'Total Intersection Total Vehicle Crashes',
                      'Total Intersection Single Vehicle Crashes', 'Total Intersection Multiple Vehicle Crashes',
                      'Total Intersection Crashes', 'Total Ramp Terminal Crashes', 'Total Crashes']

    # Write columns for Six Lane or Greater Crash Type Distribution
    if len(six_lane_type) > 0:
        outsheet = outbook.add_worksheet("Art_Crash_6Plus_Type")
        crash_type_table(outsheet, six_lane_type, excluded_items)

    # Write columns for Five Lane or Fewer Crash Type Distribution
    if len(five_lane_type) > 0:
        outsheet = outbook.add_worksheet("Art_Crash_5Minus_Type")
        crash_type_table(outsheet, five_lane_type, excluded_items)

    # Write columns for One way Crash Type Distribution
    if len(one_way_type) > 0:
        outsheet = outbook.add_worksheet("Art_Crash_OneWay_Type")
        crash_type_table(outsheet, one_way_type, excluded_items)

    # Write columns for Standard Crash Type Distribution
    if len(cr_type) > 0:
        outsheet = outbook.add_worksheet("Art_Crash_Type")
        crash_type_table(outsheet, cr_type, excluded_items)

    # Write columns for Evaluation Messages
    if len(eval_message) > 0:
        outsheet = outbook.add_worksheet("Art_Evaluation_Message")
        message_table(outsheet, eval_message)

    outbook.close()
