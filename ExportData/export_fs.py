
def exp_fs_helper(fs_fnames, prefix, df_dict_fs):

    from xml.etree import ElementTree as ET
    from .vars_cols import data_to_df
    from .helper_functions import get_elementname, get_vals_other

    # Add data to dataframe from xml for ramp segments
    m = 0
    while m < len(fs_fnames):
        # Parse xml file
        root = ET.parse(fs_fnames[m]).getroot()

        # Get element name
        element_name = get_elementname(root, prefix, 'title')

        # Assign data from XML to dataframe
        for child in root[0]:
            if 'HorizontalElements' in child.tag:
                for gchild in child:
                    df_dict_fs['df_horiz'] = data_to_df(element_name, gchild, 'HSimpleCurve',
                                                        df_dict_fs['df_horiz'])
                    df_dict_fs['df_horiz'] = data_to_df(element_name, gchild, 'HTangent',
                                                        df_dict_fs['df_horiz'])
                    df_dict_fs['df_horiz'] = data_to_df(element_name, gchild, 'HDeflection',
                                                        df_dict_fs['df_horiz'])

            if 'VerticalElements' in child.tag:
                for gchild in child:
                    df_dict_fs['df_vert'] = data_to_df(element_name, gchild, 'VTangent', df_dict_fs['df_vert'])

            attr_dict = {'AreaType': 'df_areatype', 'FunctionalClass': 'df_funcclass',
                         'AnnualAveDailyTraffic': 'df_aadt', 'LaneNS': 'df_lane', 'LaneOffset':'df_laneoffset',
                         'ShoulderSection':'df_shoulder', 'CrossSlope':'df_crossslope',
                         'HighVolumeSection':'df_hvs', 'WeavingSection':'df_weave', 'RampConnector':'df_rampconn',
                         'MedianBarrier':'df_medianbarr','OutsideBarrier':'df_outbarr', 'ClearZone':'df_clearzone',
                         'User_CMF':'df_cmf'}
            for k in attr_dict.keys():
                df_dict_fs[attr_dict[k]] = data_to_df(element_name, child, k, df_dict_fs[attr_dict[k]])

            if 'Median' in child.tag:
                var_list = [element_name, 'startStation', 'endStation', 'startWidth', 'endWidth']
                cols_list = ['Highway Alignment', 'Start Loc. (Sta. ft)', 'End Loc. (Sta. ft)', 'Start Width (ft)',
                             'End Width (ft)']
                df_dict_fs['df_median'] = get_vals_other(var_list, cols_list, child, element_name,
                                                                 df_dict_fs['df_median'])

        m += 1

    return df_dict_fs