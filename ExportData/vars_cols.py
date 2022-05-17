from pandas import DataFrame

def data_to_df(element_name, child, attribute, df):
    if attribute in child.tag:
        data_cols = get_vars(element_name, child, attribute)
        var_list = data_cols[0]
        cols_list = data_cols[1]
        for k in range(len(var_list)):
            if var_list[k] in [element_name,'Curve','Tangent','Deflection']:
                pass
            else:
                try:
                    var_list[k] = child.attrib[var_list[k]]
                except KeyError:
                    var_list[k] = ''

        df = df.append(DataFrame([var_list], columns=cols_list), ignore_index=True)
    return df

def get_vars(element_name, child, attribute):
    ## Freewway Segments, Ramp Segments, and Arterial Segments
    if attribute == 'AreaType':
        var_list = [element_name, 'startStation', 'endStation', 'areaType']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)', 'Area Type']

    elif attribute == 'FunctionalClass':
        var_list = [element_name, 'startStation', 'endStation','funcClass']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)', 'Functional Class']

    elif attribute == 'AnnualAveDailyTraffic':
        var_list = [element_name, 'startStation', 'endStation', 'adtYear', 'adtRate']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)', 'Year', 'AADT (vpd)']

    elif attribute == 'LaneNS':
        var_list = [element_name, 'startStation', 'endStation', 'sideOfRoad', 'priority', 'laneType',
                    'startWidth', 'endWidth', 'opposingPassProhib']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)', 'Side of Road', 'Priority',
                     'Type', 'Start Width (ft)', 'End Width (ft)', 'Passing Prohibited on Opposing']
    elif attribute == 'User_CMF':
        var_list = [element_name, 'title', 'description', 'startStation', 'endStation', 'startYear',
                    'endYear', 'severity', 'cmfValue']
        cols_list = ['Intersection Name', 'Name', 'Description', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)',
                     'Start CMF Year', 'End CMF Year', 'Severity', 'CMF Value']

    ## Freeway Segments and Arterial Segments
    elif attribute in ['HSimpleCurve', 'HTangent', 'HDeflection']:
        cols_list = ['Highway Alignment', 'Type', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)',
                     'Curve Radius (ft)', 'Direction of Curve', 'Radius Position', 'Deflection Angle (deg)']
        if attribute == 'HSimpleCurve':
            var_list = [element_name, 'Curve', 'startStation', 'endStation', 'radius', 'curveDirection',
                        '', '']
        elif attribute == 'HTangent':
            var_list = [element_name, 'Tangent', 'startStation', 'endStation', '', '', '', '']
        elif attribute == 'HDeflection':
            var_list = [element_name, 'Deflection', 'station', '', '', '', '', 'deflection']

    elif attribute == 'VTangent':
        var_list = [element_name, 'Tangent', 'startStation', 'endStation', 'grade', '', '', '']
        cols_list = ['Highway Alignment', 'Type', 'VPI/Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)', 'Back Grade (%)',
                     'Back Length (ft)', 'Forward Grade (%)', 'Forward Length (ft)']

    elif attribute == 'ShoulderSection':
        var_list = [element_name, 'startStation', 'endStation', 'sideOfRoad', 'insideOutsideOfRoadNB',
                    'startSlope', 'endSlope', 'startWidth', 'endWidth', 'material', 'rumbleStrips',
                    'priority']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)', 'Side of Road', 'Shoulder Side',
                     'Start Slope (%)', 'End Slope (%)', 'Start Width (ft)', 'End Width (ft)', 'Material',
                     'Rumble Strips', 'Priority']

    ## Freeway and Ramp Segments
    elif attribute == 'WeavingSection':
        var_list = [element_name, 'weavingSectionType', 'entranceRampName', 'exitRampName']
        cols_list = ['Highway Alignment', 'Weaving Section Type', 'Entrance Ramp Name', 'Exist Ramp Name']

    ## Freeway Segments
    elif attribute == 'LaneOffset':
        var_list = [element_name, 'startStation', 'endStation', 'sideOfRoad', 'laneOffset', 'beginFull',
                    'endFull']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)',
                     'Side of Road', 'Full Offset (ft)', 'Begin Loc. Full Width (Sta. ft)',
                     'End Loc. Full Width (Sta. ft)']

    elif attribute == 'CrossSlope':
        var_list = [element_name, 'station', 'sideOfRoad', 'crossSlope']
        cols_list = ['Highway Alignment', 'Location (Sta. ft)', 'Side of Road', 'Cross Slope (%)']

    elif attribute == 'HighVolumeSection':
        var_list = [element_name, 'startStation', 'startStation', 'year', 'propHighVolume']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)','Year',
                     'Proportion of AADT with High Volume']

    elif attribute == 'RampConnector':
        var_list = [element_name, 'rampName', 'rampType', 'station', 'taperLength', 'sideOfRoadNB',
                    'insideOutsideOfRoadNB', 'priority']
        cols_list = ['Highway Alignment', 'Ramp Name', 'Ramp Type', 'Gore Location (Sta. ft)',
                     'Gore-Taper Length (ft)', 'Side of Road','Ramp Side of Road', 'Alignment Priority']

    elif attribute == 'OutsideBarrier':
        var_list = [element_name, 'startStation', 'endStation', 'sideOfRoad', 'startWidth', 'endWidth']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)', 'Side of Road',
                     'Start Offset of Outside Barrier from Outside Traveled Way (ft)',
                     'End Offset of Outside Barrier from Outside Traveled Way (ft)']
    elif attribute == 'ClearZone':
        var_list = [element_name, 'startStation', 'endStation', 'sideOfRoad', 'startWidth', 'endWidth']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)', 'Side of Road',
                     'Start Width of Clear Zone (ft)', 'End Width of Clear Zone (ft)']

    ## Arterial Segments
    elif attribute == 'TWLTurnLane':
        var_list = [element_name, 'startStation', 'startCLOffset', 'beginFull', 'width', 'endFull',
                    'endCLOffset', 'endStation']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'Start Centerline Offset (ft)',
                     'Begin Loc. Full Width (Sta. ft)', 'Lane Width (ft)', 'End Loc. Full Width (Sta. ft)',
                     'End Centerline Offset (ft)', 'End Loc. (Sta. ft)']

    elif attribute == 'Median':
        var_list = [element_name, 'startStation', 'endStation', 'medianType', 'startWidth', 'endWidth']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)', 'Type', 'Start Width (ft)',
                     'End Width (ft)']

    elif attribute == 'MedianBarrier':
        var_list = [element_name, 'startStation','endStation','sideOfRoad', 'startWidth','endWidth']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)', 'Side of Road',
                     'Start Offset of Median Barrier from Inside Traveled Way (ft)',
                     'End Offset of Median Barrier from Inside Traveled Way (ft)']

    elif attribute == 'PostedSpeed':
        var_list = [element_name, 'startStation', 'endStation', 'sideOfRoad', 'speedLimit']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)', 'Side of Road',
                     'Speed Limit (mph)']

    elif attribute == 'USASpeedLevel':
        var_list = [element_name, 'startStation', 'endStation', 'speedLevel']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)', 'Speed Level']

    elif attribute == 'USADriveway':
        var_list = [element_name, 'station', 'sideOfRoad', 'drivewayType']
        cols_list = ['Highway Alignment', 'Location (Sta. ft)', 'Side of Road', 'Type']

    elif attribute == 'USARailHighwayCrossing':
        var_list = [element_name, 'station']
        cols_list = ['Highway Alignment', 'Location (Sta. ft)']

    elif attribute == 'USALighting':
        var_list = [element_name, 'startStation', 'endStation']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)']

    elif attribute == 'USAAutoSpeedEnforcement':
        var_list = [element_name, 'startStation', 'endStation']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)']

    elif attribute == 'USAFixedObject':
        var_list = [element_name, 'startStation', 'endStation', 'offset', 'density']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)', 'Offset (ft)',
                     'Density (fixed objects/mi)']

    elif attribute == 'USAParking':
        var_list = [element_name, 'startStation', 'endStation', 'sideOfRoad', 'parkingType']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)', 'Side of Road', 'Type']

    elif attribute == 'Leg':
        var_list = [element_name, 'legID', 'baseStation', 'rightOnRed']
        cols_list = ['Intersection Name', 'Leg Name', 'Leg Station', 'Prohibited']

    return var_list, cols_list


def data_to_df_ramp(element_name, child, attribute, df):
    if attribute in child.tag:
        data_cols = get_vars_ramp(element_name, child, attribute)
        var_list = data_cols[0]
        cols_list = data_cols[1]
        for k in range(len(var_list)):
            if var_list[k] in [element_name,'Curve','Tangent','Deflection']:
                pass
            else:
                try:
                    var_list[k] = child.attrib[var_list[k]]
                except KeyError:
                    var_list[k] = ''

        df = df.append(DataFrame([var_list], columns=cols_list), ignore_index=True)
    return df

def get_vars_ramp(element_name, child, attribute):
    if attribute in ['HSimpleCurve','HTangent','HDeflection']:
        cols_list = ['Highway Alignment', 'Type', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)',
                     'Curve Radius (ft)', 'Direction of Curve', 'Radius Position', 'Deflection Angle (deg)',
                     'Ave. Entering Speed (mph)']
        if attribute == 'HSimpleCurve':
            var_list = [element_name, 'Curve', 'startStation', 'endStation', 'radius', 'curveDirection',
                        '', '','rampCurveSpeed']
        elif attribute == 'HTangent':
            var_list = [element_name, 'Tangent', 'startStation', 'endStation', '', '', '', '','']
        elif attribute == 'HDeflection':
            var_list = [element_name, 'Deflection', 'station', '', '', '', '', 'deflection', '']
    elif attribute == 'RampConnector':
        var_list = [element_name, 'rampName', 'rampType', 'station', 'taperLength',
                    'insideOutsideOfRoadNB', 'priority']
        cols_list = ['Highway Alignment', 'Ramp Name', 'Ramp Type', 'Gore Location (Sta. ft)',
                     'Gore-Taper Length (ft)', 'Ramp Side of Road', 'Alignment Priority']

    elif attribute == 'MedianBarrier':
        var_list = [element_name, 'startStation', 'endStation', 'startWidth', 'endWidth']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)',
                     'Start Leftside Barrier Offset from Leftside Traveled Way (ft)',
                     'End Leftside Barrier Offset from Leftside Traveled Way (ft)']

    elif attribute == 'OutsideBarrier':
        var_list = [element_name, 'startStation', 'endStation', 'startWidth', 'endWidth']
        cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)',
                     'Start Rightside Barrier Offset from Rightside Traveled Way (ft)',
                     'End Rightside Barrier Offset from Rightside Traveled Way (ft)']

    elif attribute == 'Leg':
        var_list = [element_name, 'legTitle', 'baseStation', 'classification', 'trafficControl',
                    'leftTurnPhasing', 'rightTurnTrafficControl', 'channelization', 'skewAngle',
                    'rampTerminalSide']
        cols_list = ['Ramp Terminal Name', 'Leg Name', 'Leg Station', 'Classification', 'Control',
                     'Left Turn Lane Phasing', 'Right Turn Lane Phasing', 'Channelization', 'Skew Angle',
                     'Ramp Terminal Side']

    elif attribute == 'User_CMF':
        var_list = [element_name, 'title', 'description', 'startYear', 'endYear', 'severity', 'cmfValue']
        cols_list = ['Intersection Name', 'Name', 'Description', 'Start CMF Year', 'End CMF Year', 'Severity', 'CMF Value']

    return var_list, cols_list


























