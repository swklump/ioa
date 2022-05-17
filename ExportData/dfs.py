# This file creates empty dataframes for all element types
from pandas import DataFrame

df_dict_fs = {'df_horiz': DataFrame(), 'df_vert':DataFrame(),'df_areatype':DataFrame(),'df_funcclass':DataFrame(),
              'df_aadt':DataFrame(),'df_lane':DataFrame(), 'df_laneoffset':DataFrame(),'df_shoulder':DataFrame(),
              'df_crossslope':DataFrame(), 'df_median':DataFrame(), 'df_hvs':DataFrame(), 'df_weave':DataFrame(),
              'df_rampconn':DataFrame(), 'df_medianbarr':DataFrame(), 'df_outbarr':DataFrame(),
              'df_clearzone':DataFrame(), 'df_cmf':DataFrame()}

df_dict_ramps = {'df_horiz': DataFrame(), 'df_vert':DataFrame(), 'df_ramptype':DataFrame(), 'df_areatype':DataFrame(),
                 'df_funcclass':DataFrame(), 'df_aadt':DataFrame(), 'df_lane':DataFrame(), 'df_shoulder':DataFrame(),
                 'df_rampconn':DataFrame(), 'df_weave':DataFrame(), 'df_lbarrier': DataFrame(),
                 'df_rbarrier':DataFrame(), 'df_cmf':DataFrame()}

df_dict_rampterminals = {'df_int':DataFrame(), 'df_leg':DataFrame(), 'df_cmf':DataFrame()}

df_dict_artseg = {'df_horiz': DataFrame(), 'df_vert': DataFrame(), 'df_areatype': DataFrame(),
                  'df_funcclass': DataFrame(), 'df_aadt': DataFrame(), 'df_lane': DataFrame(),
                  'df_twltl': DataFrame(), 'df_shoulder': DataFrame(),'df_median': DataFrame(),
                  'df_medianbarr': DataFrame(), 'df_postedspeed': DataFrame(), 'df_speedcat': DataFrame(),
                  'df_driveway': DataFrame(), 'df_rail': DataFrame(), 'df_lighting': DataFrame(),
                  'df_enforce': DataFrame(),'df_object': DataFrame(), 'df_parking': DataFrame(),
                  'df_cmf': DataFrame()}

df_dict_artint = {'df_int':DataFrame(), 'df_leg':DataFrame(), 'df_cmf':DataFrame()}