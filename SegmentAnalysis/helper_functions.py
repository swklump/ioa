from numpy import where, zeros
from pandas import DataFrame

# Create equivalent column
def equiv_column(df, start_width_var=1, end_width_var=1):
    try:
        df['equiv. width'] = where(df['Side of Road'] == 'Both',
                                         (end_width_var + start_width_var) / 2 *
                                         (df['End Loc. (Sta. ft)'] - df['Start Loc. (Sta. ft)']) * 2,
                                         (end_width_var + start_width_var) / 2 *
                                         (df['End Loc. (Sta. ft)'] - df['Start Loc. (Sta. ft)']))
    except KeyError:
        df['equiv. width'] = where(1==1,
                                   (end_width_var + start_width_var) / 2 *
                                   (df['End Loc. (Sta. ft)'] - df['Start Loc. (Sta. ft)']),
                                   (end_width_var + start_width_var) / 2 *
                                   (df['End Loc. (Sta. ft)'] - df['Start Loc. (Sta. ft)']))

# Assign input data to user defined segments
def segment_data(df_segments, seg_index, seg_var, df_attribute, attr_index, attr_var):
    
    # Case 1 (start and end outside)
    if df_segments['Start Station'][seg_index] <= df_attribute['Start Loc. (Sta. ft)'][attr_index] \
    and df_segments['End Station'][seg_index] >= df_attribute['End Loc. (Sta. ft)'][attr_index]:
        df_segments[seg_var][seg_index] += df_attribute[attr_var][attr_index]

    # Case 2 (end station in between)
    elif df_segments['Start Station'][seg_index] <= df_attribute['Start Loc. (Sta. ft)'][attr_index] \
    and df_segments['End Station'][seg_index] < df_attribute['End Loc. (Sta. ft)'][attr_index] \
    and df_segments['End Station'][seg_index] >= df_attribute['Start Loc. (Sta. ft)'][attr_index]:
        df_segments[seg_var][seg_index] += df_attribute[attr_var][attr_index] * \
                (df_segments['End Station'][seg_index] - df_attribute['Start Loc. (Sta. ft)'][attr_index]) / \
                (df_attribute['End Loc. (Sta. ft)'][attr_index] - df_attribute['Start Loc. (Sta. ft)'][attr_index])

    # Case (start station in between)
    elif df_segments['Start Station'][seg_index] > df_attribute['Start Loc. (Sta. ft)'][attr_index] \
    and df_segments['Start Station'][seg_index] <= df_attribute['End Loc. (Sta. ft)'][attr_index] \
    and df_segments['End Station'][seg_index] >= df_attribute['End Loc. (Sta. ft)'][attr_index]:
        df_segments[seg_var][seg_index] += df_attribute[attr_var][attr_index] * \
                (df_attribute['End Loc. (Sta. ft)'][attr_index] - df_segments['Start Station'][seg_index]) / \
                (df_attribute['End Loc. (Sta. ft)'][attr_index] - df_attribute['Start Loc. (Sta. ft)'][attr_index])

    # Case 4 (start and end inside)
    elif df_segments['Start Station'][seg_index] > df_attribute['Start Loc. (Sta. ft)'][attr_index] \
    and df_segments['End Station'][seg_index] < df_attribute['End Loc. (Sta. ft)'][attr_index]:
        df_segments[seg_var][seg_index] += df_attribute[attr_var][attr_index] * \
                (df_segments['End Station'][seg_index] - df_segments['Start Station'][seg_index]) / \
                (df_attribute['End Loc. (Sta. ft)'][attr_index] - df_attribute['Start Loc. (Sta. ft)'][attr_index])

def create_segmentation_df(df_lanes, seg_dist):
    df_segments = DataFrame(columns = ['Highway Name', 'Segment Name', 'Start Station', 'End Station'])
    highway_names = df_lanes['Highway Alignment'].unique()
    # Make variables for min and max stations for each alignment
    min_stations = []
    max_stations = []
    # Loop through each alignment to get stations
    for h in range(len(highway_names)):
        start_stations = []
        end_stations = []
        for t in range(len(df_lanes['Highway Alignment'])):
            if df_lanes['Highway Alignment'][t] == highway_names[h]:
                start_stations.append(df_lanes['Start Loc. (Sta. ft)'][t])
                end_stations.append(df_lanes['End Loc. (Sta. ft)'][t])
        # Append the max and min station for each highway to the lists
        min_stations.append(min(start_stations))
        max_stations.append(max(end_stations))

    # Loop through highway names to create segments
    for h in range(len(highway_names)):
        num_segments = int((max_stations[h] - min_stations[h]) / (seg_dist*5280))
        if num_segments < 1:
            num_segments = 1
            just_one = 'yes'
        else:
            just_one = 'no'
        # Find out if number of segments was rounded down
        if ((max_stations[h] - min_stations[h]) / (seg_dist*5280)) > num_segments:
            add_one = 'yes'
        else:
            add_one = 'no'
        # Loop through number of segments, add segments and start/end stations to dataframe
        for n in range(num_segments):
            if just_one == 'yes':
                new_row = {'Highway Name': highway_names[h], 'Segment Name': highway_names[h] + ': Segment ' + str(n + 1),
                           'Start Station': min_stations[h] + (seg_dist * 5280 * n),
                           'End Station': max_stations[h]}
            else:
                new_row = {'Highway Name':highway_names[h], 'Segment Name': highway_names[h] + ': Segment ' + str(n + 1),
                           'Start Station':min_stations[h] + (seg_dist * 5280 * n),
                           'End Station':min_stations[h] + (seg_dist * 5280 * (n+1))}
            df_segments = df_segments.append(new_row, ignore_index=True)
        # If the number of segments was rounded down, add one last segment
        if add_one == 'yes':
            new_row = {'Highway Name': highway_names[h], 'Segment Name': highway_names[h] + ': Segment ' + str(num_segments + 1),
                       'Start Station': df_segments['End Station'][len(df_segments['Start Station'])-1],
                       'End Station': max_stations[h]}
            df_segments = df_segments.append(new_row, ignore_index=True)

    return df_segments

# Assign crashes to user defined segments
def segment_crash_data(df_segments, df_seg_crash, df_sev_crash, arterial):

    for f in range(len(df_segments['Highway Name'])):
        for d in range(len(df_seg_crash['Highway Name'])):
            if df_seg_crash['Highway Name'][d] == df_segments['Highway Name'][f]:
                crash_seg_dist = (
                            df_seg_crash['End Location (Sta. ft)'][d] - df_seg_crash['Start Location (Sta. ft)'][d])
                perc_crashes_to_seg = 0
                # if entire crash file segment is within user defined segment
                if df_segments['Start Station'][f] <= df_seg_crash['Start Location (Sta. ft)'][d] and \
                        df_segments['End Station'][f] >= df_seg_crash['End Location (Sta. ft)'][d]:
                    perc_crashes_to_seg = 1
                # if only the start sta in crash file is within user defined segment
                elif df_segments['Start Station'][f] <= df_seg_crash['Start Location (Sta. ft)'][d] and \
                        df_segments['End Station'][f] > df_seg_crash['Start Location (Sta. ft)'][d]:
                    perc_crashes_to_seg = (df_segments['End Station'][f] - df_seg_crash['Start Location (Sta. ft)'][d]) / crash_seg_dist
                # if only the end sta in crash file is within user defined segment
                elif df_segments['Start Station'][f] < df_seg_crash['End Location (Sta. ft)'][d] and \
                        df_segments['End Station'][f] >= df_seg_crash['End Location (Sta. ft)'][d]:
                    perc_crashes_to_seg = (df_seg_crash['End Location (Sta. ft)'][d] - df_segments['Start Station'][f]) / crash_seg_dist
                # else, user defined segment completely within the crash file segment
                elif df_segments['Start Station'][f] > df_seg_crash['Start Location (Sta. ft)'][d] and \
                        df_segments['End Station'][f] < df_seg_crash['End Location (Sta. ft)'][d]:
                    perc_crashes_to_seg = (df_segments['End Station'][f] - df_segments['Start Station'][f]) / crash_seg_dist

                # For arterial segments
                if arterial == 'yes':
                    if df_seg_crash['Length (mi)'][d] == df_seg_crash['Length (mi)'][d]:
                        df_segments['Total Crashes'][f] += df_seg_crash['Predicted Total Crash Frequency (crashes/yr)'][d] * perc_crashes_to_seg
                        df_segments['FI Crashes'][f] += df_seg_crash['Predicted FI Crash Frequency (crashes/yr)'][d] * perc_crashes_to_seg
                        if df_seg_crash['Predicted Travel Crash Rate (crashes/million veh-mi)'][d] == 0 or \
                                df_seg_crash['Predicted Travel Crash Rate (crashes/million veh-mi)'][d] != \
                                df_seg_crash['Predicted Travel Crash Rate (crashes/million veh-mi)'][d]:
                            pass
                        else:
                            df_segments['MVMT'][f] += (df_seg_crash['Predicted Total Crash Frequency (crashes/yr)'][d] / \
                                                      df_seg_crash['Predicted Travel Crash Rate (crashes/million veh-mi)'][d]) * perc_crashes_to_seg
                        for s in range(len(df_sev_crash)):
                            if df_seg_crash['Highway Name'][d] == df_sev_crash['Highway Name'][s] and \
                                    df_seg_crash['Segment Number/Intersection Name/Cross Road'][d] == \
                                    df_sev_crash['Seg. No.'][s] and \
                                    df_sev_crash['Type'][s] == 'USASegment':
                                df_segments['K Crashes'][f] += df_sev_crash['Fatal (K) Crashes'][s] * perc_crashes_to_seg
                                df_segments['A Crashes'][f] += df_sev_crash['Incapacitating Injury (A) Crashes'][s] * perc_crashes_to_seg
                                df_segments['B Crashes'][f] += df_sev_crash['Non-Incapacitating Injury (B) Crashes'][s] * perc_crashes_to_seg
                                df_segments['C Crashes'][f] += df_sev_crash['Possible Injury (C) Crashes'][s] * perc_crashes_to_seg
                                df_segments['O Crashes'][f] += df_sev_crash['No Injury (O) Crashes'][s] * perc_crashes_to_seg

                # For freeways and ramps
                else:
                    # Add crashes to segments based on the percent calculated
                    # df_segments['Total Crashes'][f] += (df_seg_crash['Predicted Total Crash Frequency (crashes/yr)'][d]) * perc_crashes_to_seg
                    # df_segments['FI Crashes'][f] += df_seg_crash['Predicted FI Crash Frequency (crashes/yr)'][d] * perc_crashes_to_seg
                    if df_seg_crash['Predicted Travel Crash Rate (crashes/million veh-mi)'][d] == 0:
                        pass
                    else:
                        df_segments['MVMT'][f] += (df_seg_crash['Predicted Total Crash Frequency (crashes/yr)'][d] / \
                                                   df_seg_crash['Predicted Travel Crash Rate (crashes/million veh-mi)'][d]) * perc_crashes_to_seg
                        for s in range(len(df_sev_crash)):
                            if df_seg_crash['Highway Name'][d] == df_sev_crash['Highway Name'][s] and \
                                df_seg_crash['Segment Number/Intersection Name/Cross Road'][d] == df_sev_crash['Seg. No.'][s]:
                                df_segments['K Crashes'][f] += df_sev_crash['Fatal (K) Crashes'][s] * perc_crashes_to_seg
                                df_segments['A Crashes'][f] += df_sev_crash['Incapacitating Injury (A) Crashes'][s] * perc_crashes_to_seg
                                df_segments['B Crashes'][f] += df_sev_crash['Non-Incapacitating Injury (B) Crashes'][s] * perc_crashes_to_seg
                                df_segments['C Crashes'][f] += df_sev_crash['Possible Injury (C) Crashes'][s] * perc_crashes_to_seg
                                df_segments['O Crashes'][f] += df_sev_crash['No Injury (O) Crashes'][s] * perc_crashes_to_seg
                                df_segments['Total Crashes'][f] += (df_sev_crash['Fatal (K) Crashes'][s]+df_sev_crash['Incapacitating Injury (A) Crashes'][s]+
                                                                    df_sev_crash['Non-Incapacitating Injury (B) Crashes'][s]+df_sev_crash['Possible Injury (C) Crashes'][s]+
                                                                    df_sev_crash['No Injury (O) Crashes'][s]) * perc_crashes_to_seg
                                df_segments['FI Crashes'][f] += (df_sev_crash['Fatal (K) Crashes'][s]+df_sev_crash['Incapacitating Injury (A) Crashes'][s]+
                                                                    df_sev_crash['Non-Incapacitating Injury (B) Crashes'][s]+df_sev_crash['Possible Injury (C) Crashes'][s]) * perc_crashes_to_seg

