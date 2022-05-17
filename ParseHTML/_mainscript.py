def parse_html(savelocation):
    from glob import glob
    from bs4 import BeautifulSoup as bs
    from .tbl_fs import frwy_tables
    from .tbl_ramp import ramp_tables
    from .tbl_art import art_tables
    from .tbl_rt import rt_tables
    from .tbl_rab import roundabout_tables
    
    #Getting the file names in the selected folder
    if len(glob(savelocation+'\\'+'*.htm')) > 0:
        htmlfiles = glob(savelocation+'\\'+'*.htm')
        m_or_l = 'm'
    else:
        htmlfiles = glob(savelocation+'\\'+'*.html')
        m_or_l = 'l'
    htmlfiles = [h.replace('/','\\') for h in htmlfiles]
    htmlfiles = sorted(htmlfiles)
    
    if m_or_l == 'm':
        highwaynames = [h.replace(savelocation.replace('/','\\')+'\\','')[:-4] for h in htmlfiles] #Manipulation to get clean highway names
    else:
        highwaynames = [h.replace(savelocation.replace('/','\\')+'\\','')[:-5] for h in htmlfiles]
   
   #Get model types
    freeway_files = []
    freeway_highwaynames = []
    ramp_files = []
    ramp_highwaynames = []
    arterial_files = []
    arterial_highwaynames = []
    rampterminal_files = []
    rampterminal_highwaynames = []
    roundabout_files = []
    roundabout_highwaynames = []
    for h in range(len(htmlfiles)):    
        file = bs(open(htmlfiles[h]),'html.parser').find_all('font')
        for f in file:
            if 'Model Category' in f.text.replace('\n',''):
                index = f.text.find(':')
                if f.text[index+2:].replace('\n','') == 'Freeway Segment':
                    freeway_files.append(htmlfiles[h])
                    freeway_highwaynames.append(highwaynames[h])
                elif f.text[index+2:].replace('\n','') in ['Freeway Service Ramp', 'C-D Road & System Ramp']:
                    ramp_files.append(htmlfiles[h])
                    ramp_highwaynames.append(highwaynames[h])
                elif f.text[index+2:].replace('\n','') in ['Urban/Suburban Arterial','Rural, Two Lane']:
                    arterial_files.append(htmlfiles[h])
                    arterial_highwaynames.append(highwaynames[h])
            elif 'Intersection:' in f.text:
                rampterminal_files.append(htmlfiles[h])
                rampterminal_highwaynames.append(highwaynames[h])
                roundabout_files.append(htmlfiles[h])
                roundabout_highwaynames.append(highwaynames[h])

    if len(freeway_files) > 0:
        frwy_tables(freeway_files,freeway_highwaynames,savelocation)
    if len(ramp_files) > 0:
        ramp_tables(ramp_files,ramp_highwaynames,savelocation)
    if len(arterial_files) > 0:
        art_tables(arterial_files,arterial_highwaynames,savelocation)
    if len(rampterminal_files) > 0:
        rt_tables(rampterminal_files,rampterminal_highwaynames,savelocation)
    if len(roundabout_files) > 0:
        roundabout_tables(roundabout_files,roundabout_highwaynames,savelocation)
        