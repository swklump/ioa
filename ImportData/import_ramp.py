#This script edits the XML files in an IHSDM project
def import_ramp(project_folder, prefix,included_elements,angle,df_book):

    from xml.etree import ElementTree as ET
    from glob import glob
    from .ramp_helper import ramp_helper
    ns = {'xmlns':'http://www.ihsdm.org/schema/Highway-1.0'}

    #Get interchange folders
    int_folders1 = glob(project_folder+'//'+'*/')
    int_folders = []
    for h in int_folders1:
        if h.replace(project_folder,'')[1] == 'c':
            int_folders.append(h)
            
    #Dictionaries for removing elements from xml
    el_dict = {'VerticalElements':'Vertical Alignment','rampType':'Ramp Type','AreaType':'Area Type','FunctionalClass':'Functional Class',
               'AnnualAveDailyTraffic':'Annual Average Daily Traffic','LaneNS':'Lane','ShoulderSection':'Shoulder Section',
               'MedianBarrier':'Left Side Barrier','OutsideBarrier':'Right Side Barrier','User_CMF':'User Defined CMF'}
    
    #Remove data from existing xml
    remove_elements = ['xmlns:VerticalElements','xmlns:rampType','xmlns:AreaType','xmlns:FunctionalClass','xmlns:AnnualAveDailyTraffic',
    'xmlns:LaneNS','xmlns:ShoulderSection','xmlns:MedianBarrier','xmlns:OutsideBarrier','xmlns:User_CMF']
    remove_elements1 = ['VerticalElements','rampType','AreaType','FunctionalClass','AnnualAveDailyTraffic',
    'LaneNS','ShoulderSection','MedianBarrier','OutsideBarrier','User_CMF']
    
    #Run loop through interchange folders, if any
    j = 0
    while j < len(int_folders):

        #Get ramp folders
        ramp_folders1 = glob(int_folders[j]+'//'+'*/')
        ramp_folders = []
        for r in ramp_folders1:
            if r.replace(int_folders[j],'')[0] == 'h':
                ramp_folders.append(r)

        #Get ramp filenames
        ramp_fnames = [f+'highway.1.xml' for f in ramp_folders]
        ramp_fnames = sorted(ramp_fnames)

        #Need for ramp alignment names
        ramp_project_fnames = [f+'highway.xml' for f in ramp_folders]
        ramp_project_fnames = sorted(ramp_project_fnames)

        #Run loop through ramp folders within interchange folders
        ramp_helper(ET, ramp_fnames, ramp_project_fnames, prefix, df_book, included_elements, remove_elements,
                    ns, remove_elements1, el_dict, angle)
        j += 1

    # If ramps aren't stored in interchanges
    # Get IHSDM xml file
    ihsdm_folders1 = glob(project_folder + '//' + '*/')
    ihsdm_folders = []
    for h in ihsdm_folders1:
        if h.replace(project_folder, '')[1] == 'h':
            ihsdm_folders.append(h)

    ramp_fnames = [f + 'highway.1.xml' for f in ihsdm_folders]
    ramp_fnames = sorted(ramp_fnames)

    ramp_project_fnames = [f + 'highway.xml' for f in ihsdm_folders]
    ramp_project_fnames = sorted(ramp_project_fnames)

    # Run loop of files
    ramp_helper(ET, ramp_fnames, ramp_project_fnames, prefix, df_book, included_elements, remove_elements,
                ns, remove_elements1, el_dict, angle)