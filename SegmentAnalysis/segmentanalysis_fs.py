def segmentanalysis_fs(inputfilepath, crash_file_path, seg_dist, segmentfile, savelocation):
    from pandas import options, read_excel, ExcelWriter
    options.mode.chained_assignment = None
    from numpy import zeros
    from .helper_functions import segment_data, equiv_column, segment_crash_data, create_segmentation_df

    # Read in data input file
    df_book = read_excel(inputfilepath, sheet_name=None)
    df_curve = df_book['Horizontal Alignment']
    df_lanes = df_book['Lane']
    df_shoulder = df_book['Shoulder Section']
    df_median = df_book['Median']
    df_ramp = df_book['Ramp Connection']
    df_medbarrier = df_book['Median Barrier']
    df_outbarrier = df_book['Outside Barrier']
    df_clearzone = df_book['Clear Zone']

    # Read in segments file
    if segmentfile != '':
        df_segments = read_excel(segmentfile)
    # Otherwise, segment out by user specified distance, create dataframe
    else:
        df_segments = create_segmentation_df(df_lanes, seg_dist)

    # Read in crash data
    df_seg_crash = read_excel(crash_file_path, 'Frwy_Crash_Segment')
    df_seg_crash_scl = read_excel(crash_file_path, 'Frwy_Crash_Segment_SCL')
    df_sev_crash = read_excel(crash_file_path, 'Frwy_Crash_Sev')
    df_sev_crash_scl = read_excel(crash_file_path, 'Frwy_Crash_Sev_SCL')


    # Horizontal Curves
    # Create column on curvature (See equation 18-24 in HSM for Freeway Segments)
    df_curve['curvature'] = zeros((len(df_curve['Highway Alignment']), 1))
    for d in range(len(df_curve['Highway Alignment'])):
        if df_curve['Curve Radius (ft)'][d] == df_curve['Curve Radius (ft)'][d]:
            df_curve['curvature'][d] = (5730/df_curve['Curve Radius (ft)'][d])**2 *\
                                       (df_curve['End Loc. (Sta. ft)'][d] - df_curve['Start Loc. (Sta. ft)'][d])
        else:
            df_curve['curvature'][d] = 0
    # Create working curve column
    df_segments['Curve_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Curve loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_curve['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_curve['Highway Alignment'][d]:
                # Only if the curve radius isn't zero
                if df_curve['Curve Radius (ft)'][d] == df_curve['Curve Radius (ft)'][d]:
                    segment_data(df_segments, f, 'Curve_work', df_curve, d, 'curvature')
    # Get length adjusted curvature
    df_segments['Horizontal Curvature'] = df_segments['Curve_work'] / \
                                          (df_segments['End Station'] - df_segments['Start Station'])


    # Lanes
    # Create working columns
    df_segments['Lanes_work'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['Lanes_width_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Create column on equivalent lane width
    equiv_column(df_lanes, df_lanes['Start Width (ft)'], df_lanes['End Width (ft)'])
    # Lane width loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_lanes['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_lanes['Highway Alignment'][d]:
                segment_data(df_segments, f, 'Lanes_width_work', df_lanes, d, 'equiv. width')

    # Create column on equivalent number of lanes
    equiv_column(df_lanes)
    # Number of lanes loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_lanes['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_lanes['Highway Alignment'][d]:
                segment_data(df_segments, f, 'Lanes_work', df_lanes, d, 'equiv. width')
    # Get length adjusted lane width
    df_segments['Number of Lanes'] = df_segments['Lanes_work'] / \
                                    (df_segments['End Station'] - df_segments['Start Station'])
    # Get length adjusted number of lanes
    df_segments['Average Lane Width'] = df_segments['Lanes_width_work'] / \
                                        (df_segments['End Station'] - df_segments['Start Station']) / \
                                        df_segments['Number of Lanes']


    # Shoulder Widths
    # Create column on equivalent shoulder width
    equiv_column(df_shoulder, df_shoulder['Start Width (ft)'], df_shoulder['End Width (ft)'])
    # Create working shoulder width columns
    df_segments['IS_Width_work'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['OS_Width_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Shoulder width loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_shoulder['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_shoulder['Highway Alignment'][d]:
                if df_shoulder['Shoulder Side'][d] == 'Inside':
                    segment_data(df_segments, f, 'IS_Width_work', df_shoulder, d, 'equiv. width')
                elif df_shoulder['Shoulder Side'][d] == 'Outside':
                    segment_data(df_segments, f, 'OS_Width_work', df_shoulder, d, 'equiv. width')
    # Get length adjusted shoulder widths
    df_segments['Inside Shoulder Width'] = df_segments['IS_Width_work'] / (
            (df_segments['End Station'] - df_segments['Start Station']) * 2)
    df_segments['Outside Shoulder Width'] = df_segments['OS_Width_work'] / (
            (df_segments['End Station'] - df_segments['Start Station']) * 2)


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


    # Ramp Connection/Gore taper length
    df_segments['Ramp Connections'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['Gore-Taper Length_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Ramp connection loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_ramp['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_ramp['Highway Alignment'][d]:
                if df_ramp['Gore Location (Sta. ft)'][d] >= df_segments['Start Station'][f] \
                        and df_ramp['Gore Location (Sta. ft)'][d] < df_segments['End Station'][f]:
                    df_segments['Ramp Connections'][f] += 1
                    df_segments['Gore-Taper Length_work'][f] += df_ramp['Gore-Taper Length (ft)'][d]
    # Get length adjusted gore taper length
    df_segments['Gore-Taper Length'] = df_segments['Gore-Taper Length_work'] / df_segments['Ramp Connections']


    # Median Barrier Percentage
    df_segments['Median Barrier_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Create column on equivalent column for median barrier
    equiv_column(df_medbarrier)
    # Median barrier percentage loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_medbarrier['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_medbarrier['Highway Alignment'][d]:
                segment_data(df_segments, f, 'Median Barrier_work', df_medbarrier, d, 'equiv. width')
    df_segments['Median Barrier'] = df_segments['Median Barrier_work'] / \
                ((df_segments['End Station'] - df_segments['Start Station']) * 2)


    # Median Barrier Offset
    df_segments['Median Barrier Offset_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Create column on equivalent column for median barrier
    equiv_column(df_medbarrier, df_medbarrier['Median Barrier Offset from Inside Traveled Way (ft)'],
                 df_medbarrier['Median Barrier Offset from Inside Traveled Way (ft)'])
    # Median barrier offset loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_medbarrier['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_medbarrier['Highway Alignment'][d]:
                segment_data(df_segments, f, 'Median Barrier Offset_work', df_medbarrier, d, 'equiv. width')
    df_segments['Median Barrier Offset'] = df_segments['Median Barrier Offset_work'] / \
                                    ((df_segments['End Station'] - df_segments['Start Station']) * 2)


    # Outside Barrier Percentage
    df_segments['Outside Barrier_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Create column on equivalent column for median barrier
    equiv_column(df_outbarrier)
    # Outside barrier percentage loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_outbarrier['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_outbarrier['Highway Alignment'][d]:
                segment_data(df_segments, f, 'Outside Barrier_work', df_outbarrier, d, 'equiv. width')
    df_segments['Outside Barrier'] = df_segments['Outside Barrier_work'] / (
            (df_segments['End Station'] - df_segments['Start Station']) * 2)


    # Outside Barrier Offset
    df_segments['Outside Barrier Offset_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Create column on equivalent column for median barrier
    equiv_column(df_outbarrier, df_outbarrier['Outside Barrier Offset from Outside Traveled Way (ft)'],
                 df_outbarrier['Outside Barrier Offset from Outside Traveled Way (ft)'])
    # Outside barrier percentage loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_outbarrier['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_outbarrier['Highway Alignment'][d]:
                segment_data(df_segments, f, 'Outside Barrier Offset_work', df_outbarrier, d, 'equiv. width')
    df_segments['Outside Barrier Offset'] = df_segments['Outside Barrier Offset_work'] / (
            (df_segments['End Station'] - df_segments['Start Station']) * 2)


    # Clear Zone
    # Create column on equivalent clear zone width
    equiv_column(df_clearzone, df_clearzone['Start Width of Clear Zone (ft)'], df_clearzone['End Width of Clear Zone (ft)'])
    # Create working clear zone columns
    df_segments['CZ_Width_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Main loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_clearzone['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_clearzone['Highway Alignment'][d]:
                segment_data(df_segments, f, 'CZ_Width_work', df_clearzone, d, 'equiv. width')
    # Get length adjusted clear zones
    df_segments['Clear Zone Width'] = df_segments['CZ_Width_work'] / (
            (df_segments['End Station'] - df_segments['Start Station']) * 2)


    # Assign crash data to segments
    arterial = 'no'
    # Create columns for crashes
    df_segments['Total Crashes'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['FI Crashes'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['MVMT'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['K Crashes'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['A Crashes'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['B Crashes'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['C Crashes'] = zeros((len(df_segments['Highway Name']), 1))
    df_segments['O Crashes'] = zeros((len(df_segments['Highway Name']), 1))
    segment_crash_data(df_segments, df_seg_crash, df_sev_crash, arterial)

    # Assign crash data to segments for SCL
    segment_crash_data(df_segments, df_seg_crash_scl, df_sev_crash_scl, arterial)

    # Drop columns
    df_segments = df_segments.drop(columns=['Curve_work', 'Lanes_work', 'Lanes_width_work', 'IS_Width_work',
                                            'OS_Width_work', 'Med_Width_work', 'Gore-Taper Length_work',
                                            'Median Barrier_work', 'Median Barrier Offset_work',
                                            'Outside Barrier_work', 'Outside Barrier Offset_work', 'CZ_Width_work'])


    # Write data to excel
    savelocation = savelocation.replace('/', '\\')  # Save folder path
    outputname = savelocation + '\\' + 'Freeway_SegmentAnalysis.xlsx'  # Adding a path to filenames
    writer = ExcelWriter(outputname)
    df_segments.to_excel(writer, 'Frwy_Segment_Analysis', index=False)
    writer.save()
