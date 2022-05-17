def segmentanalysis_ramp(inputfilepath, crash_file_path, seg_dist, segmentfile, savelocation):
    from pandas import options, read_excel, ExcelWriter
    options.mode.chained_assignment = None
    from numpy import zeros
    from .helper_functions import segment_data, equiv_column, segment_crash_data, create_segmentation_df

    # Read in data input file
    df_book = read_excel(inputfilepath, sheet_name=None)
    df_curve = df_book['Horizontal Alignment']
    df_area_type = df_book['Area Type']
    df_ramp_type = df_book['Ramp Type']
    df_lanes = df_book['Lane']
    df_shoulder = df_book['Shoulder Section']
    df_ramp = df_book['Ramp Connection']
    df_leftbarrier = df_book['Left Side Barrier']
    df_rightbarrier = df_book['Right Side Barrier']
    df_cmf = df_book['User Defined CMF']

    # Read in segments file
    if segmentfile != '':
        df_segments = read_excel(segmentfile)
     # Otherwise, segment out by user specified distance, create dataframe
    else:
        df_segments = create_segmentation_df(df_lanes, seg_dist)

    # Read in crash data
    df_seg_crash = read_excel(crash_file_path, 'Ramp_Crash_Segment')

    df_sev_crash = read_excel(crash_file_path, 'Ramp_Crash_Sev')

    # Horizontal Curves
    # Create column on curvature (See equation 18-24 in HSM for Freeway Segments)
    df_curve['curvature'] = zeros((len(df_curve['Highway Alignment']), 1))
    for d in range(len(df_curve['Highway Alignment'])):
        if df_curve['Curve Radius (ft)'][d] == df_curve['Curve Radius (ft)'][d]:
            df_curve['curvature'][d] = (5730 / df_curve['Curve Radius (ft)'][d]) ** 2 * \
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

    # Area Type
    df_segments['Area Type'] = zeros((len(df_segments['Highway Name']), 1))
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_area_type['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_area_type['Highway Alignment'][d]:
                df_segments['Area Type'][f] = df_area_type['Area Type'][d]

    # Ramp Type
    df_segments['Ramp Type'] = zeros((len(df_segments['Highway Name']), 1))
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_ramp_type['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_ramp_type['Highway Alignment'][d]:
                df_segments['Ramp Type'][f] = df_ramp_type['Ramp Type'][d]


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
            df_segments['End Station'] - df_segments['Start Station'])
    df_segments['Outside Shoulder Width'] = df_segments['OS_Width_work'] / (
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


    # Left Barrier Percentage
    df_segments['Median Barrier_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Create column on equivalent column for left barrier
    equiv_column(df_leftbarrier)
    # Left barrier percentage loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_leftbarrier['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_leftbarrier['Highway Alignment'][d]:
                segment_data(df_segments, f, 'Median Barrier_work', df_leftbarrier, d, 'equiv. width')
    df_segments['Leftside Barrier'] = df_segments['Median Barrier_work'] / \
                                    (df_segments['End Station'] - df_segments['Start Station'])

    # Left Barrier Offset
    df_segments['Median Barrier Offset_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Create column on equivalent column for left barrier
    equiv_column(df_leftbarrier, df_leftbarrier['Leftside Barrier Offset from Leftside Traveled Way (ft)'],
                 df_leftbarrier['Leftside Barrier Offset from Leftside Traveled Way (ft)'])
    # Left barrier offset loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_leftbarrier['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_leftbarrier['Highway Alignment'][d]:
                segment_data(df_segments, f, 'Median Barrier Offset_work', df_leftbarrier, d, 'equiv. width')
    df_segments['Leftside Barrier Offset'] = df_segments['Median Barrier Offset_work'] / \
                                           (df_segments['End Station'] - df_segments['Start Station'])

    # Right Barrier Percentage
    df_segments['Outside Barrier_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Create column on equivalent column for right barrier
    equiv_column(df_rightbarrier)
    # Right barrier percentage loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_rightbarrier['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_rightbarrier['Highway Alignment'][d]:
                segment_data(df_segments, f, 'Outside Barrier_work', df_rightbarrier, d, 'equiv. width')
    df_segments['Rightside Barrier'] = df_segments['Outside Barrier_work'] / \
                                       (df_segments['End Station'] - df_segments['Start Station'])


    # Right Barrier Offset
    df_segments['Outside Barrier Offset_work'] = zeros((len(df_segments['Highway Name']), 1))
    # Create column on equivalent column for right barrier
    equiv_column(df_rightbarrier, df_rightbarrier['Rightside Barrier Offset from Rightside Traveled Way (ft)'],
                 df_rightbarrier['Rightside Barrier Offset from Rightside Traveled Way (ft)'])
    # Right barrier percentage loop
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_rightbarrier['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_rightbarrier['Highway Alignment'][d]:
                segment_data(df_segments, f, 'Outside Barrier Offset_work', df_rightbarrier, d, 'equiv. width')
    df_segments['Rightside Barrier Offset'] = df_segments['Outside Barrier Offset_work'] / \
                                              (df_segments['End Station'] - df_segments['Start Station'])


    # User Defined CMF
    df_segments['User Defined CMF'] = zeros((len(df_segments['Highway Name']), 1))
    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_cmf['Highway Alignment'])):
            if df_segments['Highway Name'][f] == df_cmf['Highway Alignment'][d]:
                df_segments['User Defined CMF'][f] = df_cmf['Name'][d]
    df_segments['User Defined CMF'] = df_segments['User Defined CMF'].replace(0.0,"")

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

    # Drop columns
    df_segments = df_segments.drop(columns=['Curve_work', 'Lanes_work', 'Lanes_width_work', 'IS_Width_work',
                                            'OS_Width_work', 'Gore-Taper Length_work',
                                            'Median Barrier_work', 'Median Barrier Offset_work',
                                            'Outside Barrier_work', 'Outside Barrier Offset_work'])

    # Write data to excel
    savelocation = savelocation.replace('/', '\\')  # Save folder path
    outputname = savelocation + '\\' + 'Ramp_SegmentAnalysis.xlsx'  # Adding a path to filenames
    writer = ExcelWriter(outputname)
    df_segments.to_excel(writer, 'Ramp_Segment_Analysis', index=False)
    writer.save()
