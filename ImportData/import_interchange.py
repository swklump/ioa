#This script edits the XML files in an IHSDM project
def import_interchange(project_folder, excel_fname):
    
    import xlrd
    from xml.etree import ElementTree as ET
    from glob import glob

    #Get IHSDM xml file
    ihsdm_folders1 = glob(project_folder+'//'+'*/')
    ihsdm_folders = []
    for h in ihsdm_folders1:
        if h.replace(project_folder,'')[1] == 'c':
            ihsdm_folders.append(h)
    
    ihsdm_fnames = [f+'interchange.xml' for f in ihsdm_folders]
    ihsdm_fnames = sorted(ihsdm_fnames)

    #Get data from spreadsheet
    book = xlrd.open_workbook(excel_fname)
    interchange_sheet = book.sheet_by_index(0)
    
    #Run loop of files
    j = 0
    while j < len(ihsdm_fnames):
        data = ET.parse(ihsdm_fnames[j])
        root = data.getroot()
        
        #Clear out existing data in xml          
        for r in root.findall('Interchange'):
            root.remove(r)

        #Input Interchange Data       
        root.set('name',ihsdm_folders[j].replace(project_folder,'')[1:len(ihsdm_folders[j].replace(project_folder,''))-1])
        root.set('title',interchange_sheet.cell_value(j+2,0))
        root.set('freewayName','Alignment ' + interchange_sheet.cell_value(j+2,1))
        root.set('minFreewayStation',str(interchange_sheet.cell_value(j+2,2)))
        root.set('maxFreewayStation',str(interchange_sheet.cell_value(j+2,3)))
        root.set('freewayStation',str(interchange_sheet.cell_value(j+2,4)))
        root.set('crossroadName','Alignment z_' + interchange_sheet.cell_value(j+2,5))
        root.set('minCrossroadStation',str(interchange_sheet.cell_value(j+2,6)))
        root.set('maxCrossroadStation',str(interchange_sheet.cell_value(j+2,7)))
        root.set('crossroadStation',str(interchange_sheet.cell_value(j+2,8)))
        root.set('comment','-')
        root.set('created','-')
        root.set('showNetworkID','true')
        
        #Write new xml file
        data.write(ihsdm_fnames[j])
        j += 1
