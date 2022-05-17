# This script edits the XML files in an IHSDM project
def import_arterial(project_folder, prefix, included_elements, angle, df_book):

    from xml.etree import ElementTree as ET
    from glob import glob
    from decimal import Decimal
    ns = {'xmlns': 'http://www.ihsdm.org/schema/Highway-1.0'}

    # Get IHSDM xml file
    ihsdm_folders1 = glob(project_folder + '//' + '*/')
    ihsdm_folders = []
    for h in ihsdm_folders1:
        if h.replace(project_folder, '')[1] == 'h':
            ihsdm_folders.append(h)

    ihsdm_fnames = [f + 'highway.1.xml' for f in ihsdm_folders]
    ihsdm_fnames = sorted(ihsdm_fnames)

    ihsdm_project_fnames = [f + 'highway.xml' for f in ihsdm_folders]
    ihsdm_project_fnames = sorted(ihsdm_project_fnames)

    # Dictionaries for removing elements from xml
    el_dict = {'VerticalElements': 'Vertical Alignment', 'AreaType': 'Area Type', 'FunctionalClass': 'Functional Class',
               'AnnualAveDailyTraffic': 'Annual Average Daily Traffic', 'LaneNS': 'Lane',
               'TWLTurnLane': 'Two-way Left Turn Lane',
               'ShoulderSection': 'Shoulder Section', 'Median': 'Median', 'MedianBarrier': 'Median Barrier',
               'PostedSpeed': 'Posted Speed', 'USASpeedLevel': 'Speed Category', 'USADriveway': 'Driveway',
               'USARailHighwayCrossing': 'Rail Highway Crossing', 'USALighting': 'Lighting',
               'USAAutoSpeedEnforcement': 'Automated Speed Enforcement', 'USAFixedObject': 'Fixed Object',
               'USAParking': 'On-Street Parking', 'User_CMF': 'User Defined CMF'}

    remove_elements = ['xmlns:VerticalElements', 'xmlns:AreaType', 'xmlns:FunctionalClass',
                       'xmlns:AnnualAveDailyTraffic',
                       'xmlns:LaneNS', 'xmlns:TWLTurnLane', 'xmlns:ShoulderSection', 'xmlns:Median',
                       'xmlns:MedianBarrier', 'xmlns:PostedSpeed',
                       'xmlns:USASpeedLevel', 'xmlns:USADriveway', 'xmlns:USARailHighwayCrossing', 'xmlns:USALighting',
                       'xmlns:USAAutoSpeedEnforcement',
                       'xmlns:USAFixedObject', 'xmlns:USAParking', 'xmlns:User_CMF']
    remove_elements1 = ['VerticalElements', 'AreaType', 'FunctionalClass', 'AnnualAveDailyTraffic', 'LaneNS',
                        'TWLTurnLane',
                        'ShoulderSection', 'Median', 'MedianBarrier', 'PostedSpeed', 'USASpeedLevel', 'USADriveway',
                        'USARailHighwayCrossing',
                        'USALighting', 'USAAutoSpeedEnforcement', 'USAFixedObject', 'USAParking', 'User_CMF']

    # Run loop of files
    j = 0
    while j < len(ihsdm_fnames):
        data = ET.parse(ihsdm_fnames[j])
        root = data.getroot()

        # Get alignment name of file
        data_project = ET.parse(ihsdm_project_fnames[j])
        root_project = data_project.getroot()
        alg_name = root_project.attrib['title'].replace(prefix, "")

        # Get alignment names from excel template
        excel_alg_names = df_book['Directory'].iloc[:, 0][2:]

        # Only run if alignment name in excel file
        if len(df_book['Directory'][df_book['Directory']['Element Type'] == alg_name]):

            # Change the alignment heading
            for child in root[0]:
                if 'HorizontalElements' in child.tag:
                    for gchild in child:
                        if 'HHeading' in gchild.tag:
                            heading = gchild.attrib['heading']
                            gchild.attrib.pop('heading', None)
                            gchild.set('heading', str(Decimal(heading) + Decimal(angle)))

            # Clear out existing data in xml
            if included_elements[0].lower() == 'all':
                for el in remove_elements:
                    for r in root[0].findall(el, ns):
                        root[0].remove(r)
                for el in remove_elements1:
                    for r in root[0].findall(el):
                        root[0].remove(r)
            else:
                for el in remove_elements:
                    for k, v in el_dict.items():
                        if el[6:] == k:
                            if v.lower() in included_elements:
                                for r in root[0].findall(el, ns):
                                    root[0].remove(r)
                for el in remove_elements1:
                    for k, v in el_dict.items():
                        if el == k:
                            if v.lower() in included_elements:
                                for r in root[0].findall(el):
                                    root[0].remove(r)

            # Vertical Alignment
            vert_alg_sheet = df_book['Vertical Alignment']
            if included_elements[0].lower() == 'all' or 'vertical alignment' in included_elements:
                df = vert_alg_sheet[vert_alg_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'VerticalElements')
                    direct1 = ET.SubElement(direct, 'VTangent')
                    direct1.set('startStation', str(df['VPI/Start Loc. (Sta. ft)'].iloc[i]))
                    direct1.set('endStation', str(df['End. Loc. (Sta. ft)'].iloc[i]))
                    direct1.set('grade', str(df['Back Grade (%)'].iloc[i]))
                    direct2 = ET.SubElement(direct, 'VElevation')
                    direct2.set('station', str(df['VPI/Start Loc. (Sta. ft)'].iloc[i]))
                    direct2.set('elevation', '0')

            # Area Type
            area_type_sheet = df_book['Area Type']
            if included_elements[0].lower() == 'all' or 'area type' in included_elements:
                df = area_type_sheet[area_type_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'AreaType')
                    direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('endStation', str(df['End Loc. (Sta ft)'].iloc[i]))
                    direct.set('areaType', df['Area Type'].iloc[i].lower())

            # Functional Class
            func_class_sheet = df_book['Functional Class']
            if included_elements[0].lower() == 'all' or 'functional class' in included_elements:
                df = func_class_sheet[func_class_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'FunctionalClass')
                    direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('endStation', str(df['End Loc. (Sta ft)'].iloc[i]))
                    direct.set('funcClass', df['Functional Class'].iloc[i].lower())

            # AADT
            aadt_sheet = df_book['Annual Average Daily Traffic']
            if included_elements[0].lower() == 'all' or 'annual average daily traffic' in included_elements:
                df = aadt_sheet[aadt_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'AnnualAveDailyTraffic')
                    direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))
                    direct.set('adtRate', str(df['AADT (vpd)'].iloc[i]))
                    direct.set('adtYear', str(df['Year'].iloc[i]))

            # Lanes
            lane_sheet = df_book['Lane']
            if included_elements[0].lower() == 'all' or 'lane' in included_elements:
                df = lane_sheet[lane_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'LaneNS')
                    direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))
                    direct.set('sideOfRoad', df['Side of Road'].iloc[i].lower())
                    direct.set('priority', str(df['Priority'].iloc[i]))
                    direct.set('laneType', df['Type'].iloc[i].lower())
                    direct.set('startWidth', str(df['Start Width (ft)'].iloc[i]))
                    direct.set('endWidth', str(df['End Width (ft)'].iloc[i]))
                    direct.set('opposingPassProhib', str(df['Passing Prohibited On Opposing'].iloc[i]).lower())

            # TWLTL
            twltl_sheet = df_book['Two-way Left Turn Lane']
            if included_elements[0].lower() == 'all' or 'two-way left turn lane' in included_elements:
                df = twltl_sheet[twltl_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'TWLTurnLane')
                    direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('startCLOffset', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('beginFull', str(df['Begin Loc. Full Width (Sta. ft)'].iloc[i]))
                    direct.set('width', str(df['Lane Width (ft)'].iloc[i]))
                    direct.set('endFull', str(df['End Loc. Full Width (Sta. ft)'].iloc[i]))
                    direct.set('endCLOffset', str(df['End Centerline Offset (ft)'].iloc[i]))
                    direct.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))

            # Shoulder Section
            shoulder_sheet = df_book['Shoulder Section']
            if included_elements[0].lower() == 'all' or 'shoulder section' in included_elements:
                df = shoulder_sheet[shoulder_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'ShoulderSection')
                    direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))
                    direct.set('sideOfRoad', df['Side of Road'].iloc[i].lower())
                    direct.set('insideOutsideOfRoadNB', df['Shoulder Side'].iloc[i].lower())
                    direct.set('startSlope', str(df['Start Slope (%)'].iloc[i]))
                    direct.set('endSlope', str(df['End Slope (%)'].iloc[i]))
                    direct.set('startWidth', str(df['Start Width (ft)'].iloc[i]))
                    direct.set('endWidth', str(df['End Width (ft)'].iloc[i]))
                    direct.set('material', df['Material'].iloc[i].lower())
                    direct.set('rumbleStrips', str(df['Rumble Strips'].iloc[i]))
                    direct.set('priority', str(df['Priority'].iloc[i]))

            # Median
            median_sheet = df_book['Median']
            if included_elements[0].lower() == 'all' or 'median' in included_elements:
                df = median_sheet[median_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'Median')
                    direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))
                    direct.set('startWidth', str(df['Start Width (ft)'].iloc[i]))
                    direct.set('endWidth', str(df['End Width (ft)'].iloc[i]))
                    if df['Type'].iloc[i].lower() == 'non-traversible median':
                        direct.set('medianType', 'non_trav')
                    elif df['Type'].iloc[i].lower() == 'traversible median':
                        direct.set('medianType', 'trav')

            # Median Barrier
            median_barrier_sheet = df_book['Median Barrier']
            if included_elements[0].lower() == 'all' or 'median barrier' in included_elements:
                df = median_barrier_sheet[median_barrier_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'MedianBarrier')
                    direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))
                    direct.set('sideOfRoad', df['Side of Road'].iloc[i].lower())
                    direct.set('horizMedianBarrierOffset',
                               str(df['Median Barrier Offset from Inside Traveled Way (ft)'].iloc[i]))

            # Posted Speed
            posted_speed_sheet = df_book['Posted Speed']
            if included_elements[0].lower() == 'all' or 'posted speed' in included_elements:
                df = posted_speed_sheet[posted_speed_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'PostedSpeed')
                    direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))
                    direct.set('sideOfRoad', df['Side of Road'].iloc[i].lower())
                    direct.set('speedLimit', str(df['Speed Limit (mph)'].iloc[i]))

            # Speed Category
            speed_cat_sheet = df_book['Speed Category']
            if included_elements[0].lower() == 'all' or 'speed category' in included_elements:
                df = speed_cat_sheet[speed_cat_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'USASpeedLevel')
                    direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))
                    direct.set('speedLevel', df['Speed Level'].iloc[i].lower())

            # Driveway
            driveway_sheet = df_book['Driveway']
            if included_elements[0].lower() == 'all' or 'driveway' in included_elements:
                df = driveway_sheet[driveway_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'USADriveway')
                    direct.set('station', str(df['Location (Sta. ft)'].iloc[i]))
                    direct.set('sideOfRoad', df['Side of Road'].iloc[i].lower())
                    direct.set('drivewayType', df['Type'].iloc[i].lower())

            # Railroad Crossing
            railroad_sheet = df_book['Rail Highway Crossing']
            if included_elements[0].lower() == 'all' or 'rail highway crossing' in included_elements:
                df = railroad_sheet[railroad_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'USARailHighwayCrossing')
                    direct.set('station', str(df['Location (Sta. ft)'].iloc[i]))

            # Lighting
            lighting_sheet = df_book['Lighting']
            if included_elements[0].lower() == 'all' or 'lighting' in included_elements:
                df = lighting_sheet[lighting_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'USALighting')
                    direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))

            # Auto Speed Enforcement
            enforce_sheet = df_book['Automated Speed Enforcement']
            if included_elements[0].lower() == 'all' or 'automated speed enforcement' in included_elements:
                df = enforce_sheet[enforce_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'USAAutoSpeedEnforcement')
                    direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))

            # Fixed Object
            fixedobj_sheet = df_book['Fixed Object']
            if included_elements[0].lower() == 'all' or 'fixed object' in included_elements:
                df = fixedobj_sheet[fixedobj_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'USAFixedObject')
                    direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))
                    direct.set('offset', str(df['Offset (ft)'].iloc[i]))
                    direct.set('density', str(df['Offset (ft)'].iloc[i]))

            # On-Street Parking
            parking_sheet = df_book['On-Street Parking']
            if included_elements[0].lower() == 'all' or 'on-street parking' in included_elements:
                df = parking_sheet[parking_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'USAParking')
                    direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))
                    direct.set('sideOfRoad', df['Side of Road'].iloc[i].lower())
                    direct.set('parkingType', df['Type'].iloc[i].lower())

            # User Defined CMF
            cmf_sheet = df_book['User Defined CMF']
            if included_elements[0].lower() == 'all' or 'user defined cmf' in included_elements:
                df = cmf_sheet[cmf_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'User_CMF')
                    direct.set('crashType', 'allType')
                    direct.set('title', df['Name'].iloc[i])
                    direct.set('description', df['Description'].iloc[i])
                    direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))
                    direct.set('startYear', str(df['Start CMF Year'].iloc[i]))
                    direct.set('endYear', str(df['End CMF Year'].iloc[i]))
                    direct.set('severity', df['Severity'].iloc[i])
                    direct.set('cmfValue', str(df['CMF Value'].iloc[i]))

            # Write new xml file
            data.write(ihsdm_fnames[j])
            j += 1

        else:
            j += 1
            pass
