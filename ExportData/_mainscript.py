def export_data(project_folder, prefix, savelocation):

    from glob import glob
    from .export_fs import exp_fs_helper
    from .export_ramp import exp_ramp_helper
    from .export_art import exp_art_helper
    from pandas import ExcelWriter, options, to_numeric
    from os import path
    from xml.etree import ElementTree as ET
    from .dfs import df_dict_fs, df_dict_ramps, df_dict_rampterminals, df_dict_artseg, df_dict_artint
    from .numeric_columns import num_cols_dict_fs, num_cols_dict_artseg, num_cols_dict_artint, num_cols_dict_ramp, \
        num_cols_dict_rampterminal
    options.mode.chained_assignment = None

    # Get interchange folders
    ihsdm_folders = glob(project_folder + '//' + '*/')
    segment_folders = []
    rampterminal_folders = []
    intch_folders = []
    intx_folders = []
    for h in ihsdm_folders:
        if h.replace(project_folder, '')[1] == 'h':
            segment_folders.append(h)
        if h.replace(project_folder, '')[1] == 'r':
            rampterminal_folders.append(h)
        if h.replace(project_folder, '')[1] == 'c':
            intch_folders.append(h)
        if h.replace(project_folder, '')[1] == 'i':
            intx_folders.append(h)

    # Get freeway, ramp, and arterial segment file names
    frwy_fnames = []
    artseg_fnames = []
    ramp_fnames = []
    for f in segment_folders:
        if path.isfile(f + 'highway.1.xml') == True:
            data = ET.parse(f + 'highway.1.xml').getroot()
            for child in data[0]:
                if 'FunctionalClass' in child.tag:
                    if child.attrib['funcClass'] in ['freeway']:
                        frwy_fnames.append(f + 'highway.1.xml')
                    elif child.attrib['funcClass'] in ['arterial']:
                        artseg_fnames.append(f + 'highway.1.xml')
                    elif child.attrib['funcClass'] in ['ramp', 'cdRoad']:
                        ramp_fnames.append(f + 'highway.1.xml')
    frwy_fnames = sorted(frwy_fnames)
    artseg_fnames = sorted(artseg_fnames)
    ramp_fnames = sorted(ramp_fnames)

    # Get intersection file names
    artint_fnames = sorted([f + 'intersection.1.xml' for f in intx_folders])

    # Get ramp terminal file names
    rampterminal_fnames = []
    for f in rampterminal_folders:
        if path.isfile(f + 'rampterminal.2.xml') == True:
            rampterminal_fnames.append(f + 'rampterminal.2.xml')
        elif path.isfile(f + 'rampterminal.1.xml') == True:
            rampterminal_fnames.append(f + 'rampterminal.1.xml')

    # Run loop through interchange folders
    j = 0
    while j < len(intch_folders):
        # Get ramp folders
        ramp_folders1 = glob(intch_folders[j] + '//' + '*/')
        ramp_folders = []
        rampterminal_folders = []
        for r in ramp_folders1:
            if r.replace(intch_folders[j], '')[0] == 'h':
                ramp_folders.append(r)
            if r.replace(intch_folders[j], '')[0] == 'r':
                rampterminal_folders.append(r)

        for f in ramp_folders:
            if path.isfile(f + 'highway.1.xml') == True:
                data = ET.parse(f + 'highway.1.xml').getroot()
                for child in data[0]:
                    if 'FunctionalClass' in child.tag:
                        if child.attrib['funcClass'] in ['ramp','cdRoad']:
                            ramp_fnames.append(f + 'highway.1.xml')
        for f in rampterminal_folders:
            if path.isfile(f + 'rampterminal.2.xml') == True:
                rampterminal_fnames.append(f + 'rampterminal.2.xml')
            elif path.isfile(f + 'rampterminal.1.xml') == True:
                rampterminal_fnames.append(f + 'rampterminal.1.xml')
        j += 1

    ramp_fnames = sorted(ramp_fnames)
    rampterminal_fnames = sorted(rampterminal_fnames)

    # Run loop of files - freeway segments
    df_dict_fs = exp_fs_helper(frwy_fnames, prefix, df_dict_fs)
    # Run loop of files - arterial segments and arterial intersections
    dfs = exp_art_helper(artseg_fnames, artint_fnames, prefix, df_dict_artseg, df_dict_artint)
    df_dict_artseg = dfs[0]
    df_dict_artint = dfs[1]
    # Run loop of files - ramps and ramp terminals
    dfs = exp_ramp_helper(ramp_fnames, rampterminal_fnames, prefix, df_dict_ramps, df_dict_rampterminals)
    df_dict_ramps = dfs[0]
    df_dict_rampterminals = dfs[1]

    # Change certain columns to numeric
    def cols_to_numeric(df_dict, num_cols_dict):
        for k in df_dict.keys():
            for l in num_cols_dict.keys():
                if k == l:
                    for c in num_cols_dict[l]:
                        if df_dict[k].empty:
                            pass
                        else:
                            try:
                                test = df_dict[k][c]
                            except KeyError:
                                pass
                            else:
                                df_dict[k][c] = to_numeric(df_dict[k][c])

    # Run for freeway segments
    cols_to_numeric(df_dict_fs, num_cols_dict_fs)
    # Run for arterials
    cols_to_numeric(df_dict_artseg, num_cols_dict_artseg)
    cols_to_numeric(df_dict_artint, num_cols_dict_artint)
    # Run for ramps
    cols_to_numeric(df_dict_ramps, num_cols_dict_ramp)
    cols_to_numeric(df_dict_rampterminals, num_cols_dict_rampterminal)

    # Create Excel Files
    savelocation = savelocation.replace('/', '\\')  # Save folder path

    # Set up Frwy Seg Excel file
    outputname_fs = savelocation + '\\' + 'ExportedData_FrwySeg.xlsx'
    writer = ExcelWriter(outputname_fs)
    # Excel Tab Names
    columns_list_fs = [[df_dict_fs['df_horiz'], 'Horizontal Alignment'],
                           [df_dict_fs['df_vert'], 'Vertical Alignment'],
                           [df_dict_fs['df_areatype'], 'Area Type'],
                           [df_dict_fs['df_funcclass'], 'Functional Class'],
                           [df_dict_fs['df_aadt'], 'Average Annual Daily Traffic'],
                           [df_dict_fs['df_lane'], 'Lane'],
                           [df_dict_fs['df_laneoffset'], 'Lane Offset'],
                           [df_dict_fs['df_shoulder'], 'Shoulder Section'],
                           [df_dict_fs['df_crossslope'], 'Cross Slope'],
                           [df_dict_fs['df_median'], 'Median'],
                           [df_dict_fs['df_hvs'], 'High Volume Section'],
                           [df_dict_fs['df_weave'], 'Weaving Section'],
                           [df_dict_fs['df_rampconn'], 'Ramp Connection'],
                           [df_dict_fs['df_medianbarr'], 'Median Barrier'],
                           [df_dict_fs['df_outbarr'], 'Outside Barrier'],
                           [df_dict_fs['df_clearzone'], 'Cear Zone'],
                           [df_dict_fs['df_cmf'], 'User Defined CMF']]
    for r in columns_list_fs:
        if r[0].empty:
            pass
        else:
            r[0].to_excel(writer, r[1], index=False)
    writer.save()

    # Set up Art Seg Excel file
    outputname_artseg = savelocation + '\\' + 'ExportedData_ArtSeg.xlsx'
    writer = ExcelWriter(outputname_artseg)
    # Excel Tab Names
    columns_list_artseg = [[df_dict_artseg['df_horiz'], 'Horizontal Alignment'],
                          [df_dict_artseg['df_vert'], 'Vertical Alignment'],
                          [df_dict_artseg['df_areatype'], 'Area Type'],
                          [df_dict_artseg['df_funcclass'], 'Functional Class'],
                          [df_dict_artseg['df_aadt'], 'Average Annual Daily Traffic'],
                          [df_dict_artseg['df_lane'], 'Lane'],
                          [df_dict_artseg['df_twltl'], 'Two-Way Left Turn Lane'],
                          [df_dict_artseg['df_shoulder'], 'Shoulder Section'],
                          [df_dict_artseg['df_median'], 'Median'],
                          [df_dict_artseg['df_medianbarr'], 'Median Barrier'],
                          [df_dict_artseg['df_postedspeed'], 'Posted Speed'],
                          [df_dict_artseg['df_speedcat'], 'Speed Category'],
                          [df_dict_artseg['df_driveway'], 'Driveways'],
                          [df_dict_artseg['df_rail'], 'Rail Crossings'],
                          [df_dict_artseg['df_lighting'], 'Lighting'],
                          [df_dict_artseg['df_enforce'], 'Speed Enforcement'],
                          [df_dict_artseg['df_object'], 'Object Density'],
                          [df_dict_artseg['df_parking'], 'Parking'],
                          [df_dict_artseg['df_cmf'], 'User Defined CMF']]
    for r in columns_list_artseg:
        if r[0].empty:
            pass
        else:
            r[0].to_excel(writer, r[1], index=False)
    writer.save()

    # Set up Art Int Excel file
    outputname_artint = savelocation + '\\' + 'ExportedData_ArtInt.xlsx'
    writer = ExcelWriter(outputname_artint)
    columns_list_artint = [[df_dict_artint['df_int'], 'Intersection Inputs'],
                          [df_dict_artint['df_leg'], 'Leg Inputs'],
                          [df_dict_artint['df_cmf'], 'User Defined CMF']]
    for r in columns_list_artint:
        if r[0].empty:
            pass
        else:
            r[0].to_excel(writer, r[1], index=False)
    writer.save()

    # Set up Ramp Segment Excel file
    outputname_ramp = savelocation + '\\' + 'ExportedData_Ramp.xlsx'
    writer = ExcelWriter(outputname_ramp)
    # Excel Tab Names
    columns_list_ramps = [[df_dict_ramps['df_horiz'], 'Horizontal Alignment'],
                          [df_dict_ramps['df_vert'], 'Vertical Alignment'],
                          [df_dict_ramps['df_ramptype'], 'Ramp Type'],
                          [df_dict_ramps['df_areatype'], 'Area Type'],
                          [df_dict_ramps['df_funcclass'], 'Functional Class'],
                          [df_dict_ramps['df_aadt'], 'Average Annual Daily Traffic'],
                          [df_dict_ramps['df_lane'], 'Lane'],
                          [df_dict_ramps['df_shoulder'], 'Shoulder Section'],
                          [df_dict_ramps['df_rampconn'], 'Ramp Connection'],
                          [df_dict_ramps['df_weave'], 'Weaving Section'],
                          [df_dict_ramps['df_lbarrier'], 'Left Side Barrier'],
                          [df_dict_ramps['df_rbarrier'], 'Right Side Barrier'],
                          [df_dict_ramps['df_cmf'], 'User Defined CMF']]
    for r in columns_list_ramps:
        if r[0].empty:
            pass
        else:
            r[0].to_excel(writer, r[1], index=False)
    writer.save()
    # Set up Ramp Terminal Excel file
    outputname_rampterminal = savelocation + '\\' + 'ExportedData_RampTerminal.xlsx'
    writer = ExcelWriter(outputname_rampterminal)
    columns_list_rampterminals = [[df_dict_rampterminals['df_int'], 'Intersection Inputs'],
                                  [df_dict_rampterminals['df_leg'], 'Leg Inputs'],
                                  [df_dict_rampterminals['df_cmf'], 'User Defined CMF']]
    for r in columns_list_rampterminals:
        if r[0].empty:
            pass
        else:
            r[0].to_excel(writer, r[1], index=False)

    writer.save()

