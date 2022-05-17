
from decimal import Decimal

def ramp_helper(ET, ramp_fnames, ramp_project_fnames, prefix, df_book, included_elements, remove_elements, ns,
                remove_elements1, el_dict, angle):
    m = 0
    while m < len(ramp_fnames):

        # Parse xml file
        data = ET.parse(ramp_fnames[m])
        root = data.getroot()

        # Get alignment name of ramp
        data_project = ET.parse(ramp_project_fnames[m])
        root_project = data_project.getroot()
        alg_name = root_project.attrib['title'].replace(prefix, "")

        # Get coordinate data
        for child in root[0]:
            if 'HorizontalElements' in child.tag:
                for gchild in child:
                    if 'HHeading' in gchild.tag:
                        heading = gchild.attrib['heading']
                        heading_station = gchild.attrib['station']
                        gchild.attrib.pop('heading', None)
                        gchild.set('heading', str(Decimal(heading) + Decimal(angle)))
                    if 'HCoordinate' in gchild.tag:
                        x_coord = gchild.attrib['x']
                        y_coord = gchild.attrib['y']
                        coord_station = gchild.attrib['station']

        # Only run if alignment name in excel file
        if len(df_book['Directory'][df_book['Directory']['Element Type'] == alg_name]):

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

            # Horizontal Alignment
            horiz_alg_sheet = df_book['Horizontal Alignment']
            if included_elements[0].lower() == 'all' or 'horizontal alignment' in included_elements:
                df = horiz_alg_sheet[horiz_alg_sheet['Highway Alignment'] == alg_name]
                if len(df) > 0:
                    # Clear out existing horizontal curvature data
                    for c in root[0].findall('HorizontalElements'):
                        root[0].remove(c)
                    for c in root[0].findall('xmlns:HorizontalElements', ns):
                        root[0].remove(c)
                    # Add back in coordinate and heading data
                    try:
                        direct = ET.SubElement(root[0], 'HorizontalElements')
                        direct1 = ET.SubElement(direct, 'HHeading')
                        direct1.set('heading', str(Decimal(heading) + Decimal(angle)))
                        direct1.set('station', str(heading_station))
                        direct1 = ET.SubElement(direct, 'HCoordinate')
                        direct1.set('x', str(x_coord))
                        direct1.set('y', str(y_coord))
                        direct1.set('station', str(coord_station))
                    except Exception:
                        pass

                    # Add data from spreadsheet
                    for i in range(len(df['Highway Alignment'])):
                        if df['Type'].iloc[i] == 'Tangent':
                            direct1 = ET.SubElement(direct, 'HTangent')
                            direct1.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                            direct1.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))
                        elif df['Type'].iloc[i] == 'Curve':
                            direct1 = ET.SubElement(direct, 'HSimpleCurve')
                            direct1.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                            direct1.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))
                            direct1.set('radius', str(df['Curve Radius (ft)'].iloc[i]))
                            direct1.set('curveDirection', str(df['Direction of Curve'].iloc[i].lower()))
                            direct1.set('rampCurveSpeed', str(df['Ave. Entering Speed (mph)'].iloc[i]))
                        elif df['Type'].iloc[i] == 'Deflection':
                            direct1 = ET.SubElement(direct, 'HDeflection')
                            direct1.set('station', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                            direct1.set('deflection', str(df['Deflection Angle (deg)'].iloc[i]))

            # Vertical Alignment
            vert_alg_sheet = df_book['Vertical Alignment']
            if included_elements[0].lower() == 'all' or 'vertical alignment' in included_elements:
                df = vert_alg_sheet[vert_alg_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'VerticalElements')
                    direct1 = ET.SubElement(direct, 'VTangent')
                    direct1.set('startStation', str(df['VPI/Start Loc. (Sta. ft)'].iloc[i]))
                    direct1.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))
                    direct1.set('grade', str(df['Back Grade (%)'].iloc[i]))
                    direct2 = ET.SubElement(direct, 'VElevation')
                    direct2.set('station', str(df['VPI/Start Loc. (Sta. ft)'].iloc[i]))
                    direct2.set('elevation', '0')

            # Ramp Type
            ramptype_sheet = df_book['Ramp Type']
            if included_elements[0].lower() == 'all' or 'ramp type' in included_elements:
                df = ramptype_sheet[ramptype_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    root[0].attrib.pop("rampType", None)
                    root[0].set('rampType', df['Ramp Type'].iloc[i].lower())

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
                    if df['Functional Class'].iloc[i] == 'Freeway C-D Road and System Ramp':
                        direct.set('funcClass', 'cdRoad')
                    else:
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
                    direct.set('priority', str(df['Priority'].iloc[i]))
                    direct.set('laneType', df['Type'].iloc[i].lower())
                    direct.set('startWidth', str(df['Start Width (ft)'].iloc[i]))
                    direct.set('endWidth', str(df['End Width (ft)'].iloc[i]))

            # Shoulder Section
            shoulder_sheet = df_book['Shoulder Section']
            if included_elements[0].lower() == 'all' or 'shoulder section' in included_elements:
                df = shoulder_sheet[shoulder_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    direct = ET.SubElement(root[0], 'ShoulderSection')
                    direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                    direct.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))
                    direct.set('insideOutsideOfRoadNB', df['Shoulder Side'].iloc[i].lower())
                    direct.set('startSlope', str(df['Start Slope (%)'].iloc[i]))
                    direct.set('endSlope', str(df['End Slope (%)'].iloc[i]))
                    direct.set('startWidth', str(df['Start Width (ft)'].iloc[i]))
                    direct.set('endWidth', str(df['End Width (ft)'].iloc[i]))
                    direct.set('material', df['Material'].iloc[i].lower())
                    direct.set('rumbleStrips', str(df['Rumble Strips'].iloc[i]))
                    direct.set('priority', str(df['Priority'].iloc[i]))

            # Median Barrier
            median_barrier_sheet = df_book['Left Side Barrier']
            if included_elements[0].lower() == 'all' or 'left side barrier' in included_elements:
                df = median_barrier_sheet[median_barrier_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    if str(df['Start Loc. (Sta. ft)'].iloc[i]).lower() == 'no barrier':
                        pass
                    else:
                        direct = ET.SubElement(root[0], 'MedianBarrier')
                        direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                        direct.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))
                        direct.set('horizMedianBarrierOffset',
                                   str(df['Leftside Barrier Offset from Leftside Traveled Way (ft)'].iloc[i]))

            # Outside Barrier
            outside_barrier_sheet = df_book['Right Side Barrier']
            if included_elements[0].lower() == 'all' or 'right side barrier' in included_elements:
                df = outside_barrier_sheet[outside_barrier_sheet['Highway Alignment'] == alg_name]
                for i in range(len(df['Highway Alignment'])):
                    if str(df['Start Loc. (Sta. ft)'].iloc[i]).lower() == 'no barrier':
                        pass
                    else:
                        direct = ET.SubElement(root[0], 'OutsideBarrier')
                        direct.set('startStation', str(df['Start Loc. (Sta. ft)'].iloc[i]))
                        direct.set('endStation', str(df['End Loc. (Sta. ft)'].iloc[i]))
                        direct.set('horizOutsideBarrierOffset',
                                   str(df['Rightside Barrier Offset from Rightside Traveled Way (ft)'].iloc[i]))

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
            data.write(ramp_fnames[m])
            m += 1

        else:
            m += 1
            pass