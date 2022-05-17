
def exp_art_helper(artseg_fnames, artint_fnames, prefix, df_dict_artseg, df_dict_artint):

    from xml.etree import ElementTree as ET
    from .vars_cols import data_to_df, data_to_df_ramp
    from .helper_functions import get_elementname
    from pandas import DataFrame

    # Add data to dataframe from xml for ramp segments
    m = 0
    while m < len(artseg_fnames):
        # Parse xml file
        root = ET.parse(artseg_fnames[m]).getroot()

        # Get element name
        element_name = get_elementname(root,prefix,'title')

        # Assign data from XML to dataframe
        for child in root[0]:
            if 'HorizontalElements' in child.tag:
                for gchild in child:
                    df_dict_artseg['df_horiz'] = data_to_df(element_name, gchild, 'HSimpleCurve',
                                                            df_dict_artseg['df_horiz'])
                    df_dict_artseg['df_horiz'] = data_to_df(element_name, gchild, 'HTangent',
                                                            df_dict_artseg['df_horiz'])
                    df_dict_artseg['df_horiz'] = data_to_df(element_name, gchild, 'HDeflection',
                                                            df_dict_artseg['df_horiz'])

            if 'VerticalElements' in child.tag:
                for gchild in child:
                    df_dict_artseg['df_vert'] = data_to_df(element_name, gchild, 'VTangent',
                                                           df_dict_artseg['df_vert'])

            attr_dict = {'AreaType':'df_areatype', 'FunctionalClass':'df_funcclass', 'AnnualAveDailyTraffic':'df_aadt',
                         'LaneNS':'df_lane', 'TWLTurnLane':'df_twltl', 'ShoulderSection':'df_shoulder',
                         'Median':'df_median', 'MedianBarrier':'df_medianbarr', 'PostedSpeed':'df_postedspeed',
                         'USASpeedLevel':'df_speedcat', 'USADriveway':'df_driveway', 'USARailHighwayCrossing':'df_rail',
                         'USALighting':'df_lighting', 'USAAutoSpeedEnforcement':'df_enforce',
                         'USAFixedObject':'df_object', 'USAParking':'df_parking', 'User_CMF':'df_cmf'}
            for k in attr_dict.keys():
                df_dict_artseg[attr_dict[k]] = data_to_df(element_name, child, k,
                                                          df_dict_artseg[attr_dict[k]])
        m += 1

    n = 0
    while n < len(artint_fnames):
        # Parse xml file
        root = ET.parse(artint_fnames[n]).getroot()

        # Get element name
        element_name = get_elementname(root, prefix, 'intersectionName')

        # Assign data from XML to dataframe
        num_legs = 0
        for child in root[0]:
            df_dict_artint['df_cmf'] = data_to_df_ramp(element_name, child, 'User_CMF', df_dict_artint['df_cmf'])
            df_dict_artint['df_leg'] = data_to_df(element_name, child, 'Leg', df_dict_artint['df_leg'])
            if 'Leg' in child.tag:
                num_legs += 1

        var_list = [[element_name, root[0].attrib['trafficControl'], num_legs, root[0].attrib['baseHighwayTitle'],
                    root[0].attrib['baseStation'], root[0].attrib['lighting'], root[0].attrib['redLightCamera']]]
        cols_list = ['Intersection Name', 'Traffic Control', 'Number of Legs', 'Crossroad Name', 'Crossroad Station',
                     'Lighting', 'Red Light Camera']
        df_dict_artint['df_int'] = df_dict_artint['df_int'].append(DataFrame(var_list, columns=cols_list),
                                                                   ignore_index=True)

        n += 1

    return df_dict_artseg, df_dict_artint