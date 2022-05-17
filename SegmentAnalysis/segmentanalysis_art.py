def segmentanalysis_art(inputfilepath, crash_file_path, seg_dist, segmentfile, savelocation):
    from pandas import options, read_excel, ExcelWriter
    options.mode.chained_assignment = None
    from numpy import zeros
    from .helper_functions import segment_data, equiv_column, create_segmentation_df, segment_crash_data

    # Read in data input file
    df_book = read_excel(inputfilepath, sheet_name=None)
    df_lanes = df_book['Lane']
    df_median = df_book['Median']
    df_driveway = df_book['Driveway']
    df_lighting = df_book['Lighting']
    df_speedenforc = df_book['Automated Speed Enforcement']
    df_fixobj = df_book['Fixed Object']
    df_parking = df_book['On-Street Parking']

    # Read in segments file
    if segmentfile != '':
        df_segments = read_excel(segmentfile)
    # Otherwise, segment out by user specified distance, create dataframe
    else:
        df_segments = create_segmentation_df(df_lanes, seg_dist)

    # Read in crash data
    df_seg_crash = read_excel(crash_file_path, 'Art_Crash_Segment')
    df_sev_crash = read_excel(crash_file_path, 'Art_Crash_Sev')


    # Median Widths
    # Create column on equivalent median width
    df_median['equiv. width'] = (df_median['End Width (ft)'] + df_median['Start Width (ft)']) / 2 * \
                                (df_median['End Loc. (Sta. ft)'] - df_median['Start Loc. (Sta. ft)'])
    # Create working median width column
    df_segments['Med_Width_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Median width loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_median['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_median['Highway Alignment'][d]:
                segment_data(df_segments, f, 'Med_Width_work', df_median, d, 'equiv. width')
    # Get length adjusted median widths
    df_segments['Median Width'] = df_segments['Med_Width_work'] / (
            df_segments['End Station'] - df_segments['Start Station'])


    # Create working columns for driveways
    df_segments['MajComm_Driveways'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['MinComm_Driveways'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['MajInd_Driveways'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['MinInd_Driveways'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['MajRes_Driveways'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['MinRes_Driveways'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['Other_Driveways'] = zeros((len(df_segments['Highway Name']), 1))
    # Driveways loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_driveway['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_driveway['Highway Alignment'][d]:
                if df_driveway['Location (Sta. ft)'][d] >= df_segments['Start Station'][f] \
                        and df_driveway['Location (Sta. ft)'][d] < df_segments['End Station'][f]:
                    if df_driveway['Side of Road'][d] == 'Both':
                        if df_driveway['Type'][d]  == 'Major Commercial':
                            df_segments['MajComm_Driveways'][f] += 2
                        elif df_driveway['Type'][d]  == 'Minor Commercial':
                            df_segments['MinComm_Driveways'][f] += 2
                        elif df_driveway['Type'][d]  == 'Major Industrial/Institutional':
                            df_segments['MajInd_Driveways'][f] += 2
                        elif df_driveway['Type'][d]  == 'Minor Industrial/Institutional':
                            df_segments['MinInd_Driveways'][f] += 2
                        elif df_driveway['Type'][d]  == 'Major Residential':
                            df_segments['MajRes_Driveways'][f] += 2
                        elif df_driveway['Type'][d]  == 'Minor Residential':
                            df_segments['MinRes_Driveways'][f] += 2
                        elif df_driveway['Type'][d]  == 'Other':
                            df_segments['Other_Driveways'][f] += 2
                    else:
                        if df_driveway['Type'][d]  == 'Major Commercial':
                            df_segments['MajComm_Driveways'][f] += 1
                        elif df_driveway['Type'][d]  == 'Minor Commercial':
                            df_segments['MinComm_Driveways'][f] += 1
                        elif df_driveway['Type'][d]  == 'Major Industrial/Institutional':
                            df_segments['MajInd_Driveways'][f] += 1
                        elif df_driveway['Type'][d]  == 'Minor Industrial/Institutional':
                            df_segments['MinInd_Driveways'][f] += 1
                        elif df_driveway['Type'][d]  == 'Major Residential':
                            df_segments['MajRes_Driveways'][f] += 1
                        elif df_driveway['Type'][d]  == 'Minor Residential':
                            df_segments['MinRes_Driveways'][f] += 1
                        elif df_driveway['Type'][d]  == 'Other':
                            df_segments['Other_Driveways'][f] += 1



    # Lighting
    # Create column on equivalent lighting
    equiv_column(df_lighting)
    # Create working lighting column
    df_segments['Lighting_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Lighting loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_lighting['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_lighting['Highway Alignment'][d]:
                segment_data(df_segments, f, 'Lighting_work', df_lighting, d, 'equiv. width')
    # Get length adjusted lighting
    df_segments['Lighting'] = df_segments['Lighting_work'] / (
            df_segments['End Station'] - df_segments['Start Station'])


    # Auto Speed Enforcement
    # Create column on equivalent speed enforcement
    equiv_column(df_speedenforc)
    # Create working speed enforcement column
    df_segments['SpeedEnforce_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Speed enforcement loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_speedenforc['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_speedenforc['Highway Alignment'][d]:
                segment_data(df_segments, f, 'SpeedEnforce_work', df_speedenforc, d, 'equiv. width')
    # Get length adjusted speed enforcement
    df_segments['SpeedEnforcement'] = df_segments['SpeedEnforce_work'] / (
            df_segments['End Station'] - df_segments['Start Station'])


    # Fixed Object
    # Create column on equivalent fixed object
    equiv_column(df_fixobj)
    # Create working fixed object column
    df_segments['FixedObj_Density_work'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['FixedObj_Offset_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Fixed object loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_fixobj['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_fixobj['Highway Alignment'][d]:
                segment_data(df_segments, f, 'FixedObj_Density_work', df_fixobj, d, 'equiv. width')
                segment_data(df_segments, f, 'FixedObj_Offset_work', df_fixobj, d, 'equiv. width')
    # Get length adjusted fixed object column
    df_segments['FixedObj_Density'] = df_segments['FixedObj_Density_work'] / (
            df_segments['End Station'] - df_segments['Start Station'])
    df_segments['FixedObj_Offset'] = df_segments['FixedObj_Offset_work'] / (
            df_segments['End Station'] - df_segments['Start Station'])


    # Parking
    # Create column on equivalent parking
    equiv_column(df_parking)
    # Create working columns for parking
    df_segments['Parking_Para_Res_work'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['Parking_Para_Comm_work'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['Parking_Angle_Res_work'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['Parking_Angle_Comm_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Parking loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_parking['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_parking['Highway Alignment'][d]:
                if df_parking['Type'][d] == 'Parallel, Residential/Other':
                    segment_data(df_segments, f, 'Parking_Para_Res_work', df_parking, d, 'equiv. width')
                elif df_parking['Type'][d] == 'Parallel, Commercial/Industrial/Institutional':
                    segment_data(df_segments, f, 'Parking_Para_Comm_work', df_parking, d, 'equiv. width')
                elif df_parking['Type'][d] == 'Angle, Residential/Other':
                    segment_data(df_segments, f, 'Parking_Angle_Res_work', df_parking, d, 'equiv. width')
                elif df_parking['Type'][d] == 'Angle, Commercial/Industrial/Institutional':
                    segment_data(df_segments, f, 'Parking_Angle_Comm_work', df_parking, d, 'equiv. width')
    # Get length adjusted parking
    df_segments['Parking_Para_Res'] = df_segments['Parking_Para_Res_work'] / (
            df_segments['End Station'] - df_segments['Start Station'])
    df_segments['Parking_Para_Comm'] = df_segments['Parking_Para_Comm_work'] / (
            df_segments['End Station'] - df_segments['Start Station'])
    df_segments['Parking_Angle_Res'] = df_segments['Parking_Angle_Res_work'] / (
            df_segments['End Station'] - df_segments['Start Station'])
    df_segments['Parking_Angle_Comm'] = df_segments['Parking_Angle_Comm_work'] / (
            df_segments['End Station'] - df_segments['Start Station'])



    # Create columns for crashes
    # Assign crash data to segments
    arterial = 'yes'
    segment_crash_data(df_segments, df_seg_crash, df_sev_crash, arterial)
    # Assign crash data to segments
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_seg_crash['Highway Name'])):
            if df_seg_crash['Highway Name'][d] == df_segments['Highway Name'][f]:
                if df_seg_crash['Start Location (Sta. ft)'][d] >= df_segments['Start Station'][f] and \
                    df_seg_crash['Start Location (Sta. ft)'][d] < df_segments['End Station'][f]:
                    if df_seg_crash['Length (mi)'][d] == df_seg_crash['Length (mi)'][d]:
                        df_segments['Total Crashes'][f] += df_seg_crash['Predicted Total Crash Frequency (crashes/yr)'][d]
                        df_segments['FI Crashes'][f] += df_seg_crash['Predicted FI Crash Frequency (crashes/yr)'][d]
                        if df_seg_crash['Predicted Travel Crash Rate (crashes/million veh-mi)'][d] == 0 or \
                            df_seg_crash['Predicted Travel Crash Rate (crashes/million veh-mi)'][d] != df_seg_crash['Predicted Travel Crash Rate (crashes/million veh-mi)'][d]:
                            pass
                        else:
                            df_segments['MVMT'][f] += df_seg_crash['Predicted Total Crash Frequency (crashes/yr)'][d] / \
                                                  df_seg_crash['Predicted Travel Crash Rate (crashes/million veh-mi)'][d]
                        for s in range(len(df_sev_crash)):
                            if df_seg_crash['Highway Name'][d] == df_sev_crash['Highway Name'][s] and \
                               df_seg_crash['Segment Number/Intersection Name/Cross Road'][d] == df_sev_crash['Seg. No.'][s] and \
                                df_sev_crash['Type'][s] == 'USASegment':
                                    df_segments['K Crashes'][f] += df_sev_crash['Fatal (K) Crashes'][s]
                                    df_segments['A Crashes'][f] += df_sev_crash['Incapacitating Injury (A) Crashes'][s]
                                    df_segments['B Crashes'][f] += df_sev_crash['Non-Incapacitating Injury (B) Crashes'][s]
                                    df_segments['C Crashes'][f] += df_sev_crash['Possible Injury (C) Crashes'][s]
                                    df_segments['O Crashes'][f] += df_sev_crash['No Injury (O) Crashes'][s]

    # Drop columns
    df_segments = df_segments.drop(columns=['Med_Width_work', 'FixedObj_Density_work',
                                            'FixedObj_Offset_work', 'Lighting_work',
                                            'SpeedEnforce_work', 'Parking_Para_Res_work', 'Parking_Para_Comm_work',
                                            'Parking_Angle_Res_work', 'Parking_Angle_Comm_work'])


    # Write data to excel
    savelocation = savelocation.replace('/', '\\')  # Save folder path
    outputname = savelocation + '\\' + 'Arterial_SegmentAnalysis.xlsx'  # Adding a path to filenames
    writer = ExcelWriter(outputname)
    df_segments.to_excel(writer, 'Art_Segment_Analysis', index=False)
    writer.save()
