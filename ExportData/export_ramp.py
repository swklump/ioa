
def exp_ramp_helper(ramp_fnames, rampterminal_fnames, prefix, df_dict_ramps, df_dict_rampterminals):

    from xml.etree import ElementTree as ET
    from .vars_cols import data_to_df, data_to_df_ramp
    from .helper_functions import get_elementname, get_vals_other
    from pandas import DataFrame

    # Add data to dataframe from xml for ramp segments
    m = 0
    while m < len(ramp_fnames):
        # Parse xml file
        root = ET.parse(ramp_fnames[m]).getroot()

        # Get element name
        element_name = get_elementname(root, prefix, 'title')

        # Assign data from XML to dataframe
        for child in root[0]:

            var_list = [[element_name, root[0].attrib['rampType']]]
            cols_list = ['Highway Alignment', 'Ramp Type']
            df_dict_ramps['df_ramptype'] = df_dict_ramps['df_ramptype'].append(DataFrame(var_list, columns=cols_list),
                                                                               ignore_index=True)

            if 'HorizontalElements' in child.tag:
                for gchild in child:
                    df_dict_ramps['df_horiz'] = data_to_df_ramp(element_name, gchild, 'HSimpleCurve',
                                                                df_dict_ramps['df_horiz'])
                    df_dict_ramps['df_horiz'] = data_to_df_ramp(element_name, gchild, 'HTangent',
                                                                df_dict_ramps['df_horiz'])
                    df_dict_ramps['df_horiz'] = data_to_df_ramp(element_name, gchild, 'HDeflection',
                                                                df_dict_ramps['df_horiz'])

            if 'VerticalElements' in child.tag:
                for gchild in child:
                    df_dict_ramps['df_vert'] = data_to_df(element_name, gchild, 'VTangent', df_dict_ramps['df_vert'])

            attr_dict = {'AreaType': 'df_areatype', 'FunctionalClass': 'df_funcclass',
                         'AnnualAveDailyTraffic': 'df_aadt', 'LaneNS':'df_lane', 'ShoulderSection':'df_shoulder',
                         'WeavingSection':'df_weave', 'User_CMF':'df_cmf'}
            for k in attr_dict.keys():
                df_dict_ramps[attr_dict[k]] = data_to_df(element_name, child, k, df_dict_ramps[attr_dict[k]])

            attr_dict = {'RampConnector': 'df_rampconn', 'MedianBarrier':'df_lbarrier', 'OutsideBarrier':'df_rbarrier'}
            for k in attr_dict.keys():
                df_dict_ramps[attr_dict[k]] = data_to_df_ramp(element_name, child, k,
                                                              df_dict_ramps[attr_dict[k]])

        m += 1

    # Add data to dataframe from xml for ramp terminals
    n = 0
    while n < len(rampterminal_fnames):
        # Parse xml file
        root = ET.parse(rampterminal_fnames[n]).getroot()

        # Get element name
        element_name = get_elementname(root, prefix, 'intersectionName')

        var_list = [element_name, 'trafficControl', 'numDrivewaysOutside', 'rampTerminalType']
        cols_list = ['Ramp Terminal Name', 'Control Type', 'Number of Driveways Outside Terminal',
                     'Ramp Terminal Type']
        df_dict_rampterminals['df_int'] = get_vals_other(var_list, cols_list, root[0], element_name,
                                                         df_dict_rampterminals['df_int'])

        for child in root[0]:
            df_dict_rampterminals['df_leg'] = data_to_df_ramp(element_name, child, 'Leg', df_dict_rampterminals['df_leg'])
            df_dict_rampterminals['df_cmf'] = data_to_df_ramp(element_name, child, 'User_CMF', df_dict_rampterminals['df_cmf'])

        n += 1

    return df_dict_ramps, df_dict_rampterminals