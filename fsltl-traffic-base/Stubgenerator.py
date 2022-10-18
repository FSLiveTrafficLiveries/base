version = "2.1.0"
import csv,re,os,json, pathlib
from collections import defaultdict
here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, "stub-source.txt")
class VS_Entity:
    def __init__(self,name,path):
        self.name=name
        self.path=path
print("FSLTL Stub Generator version: "+version+"\n")
input("Press Enter to start\n")
def readCsv():
# initializing the titles and rows list
    # reading csv file
    with open(filename, 'r') as csvfile:
        global rows
        rows = []
        # creating a csv reader object
        csvreader = csv.reader(csvfile, delimiter = '|')
    
        # extracting each data row one by one
        for row in csvreader:
            if row[3] == 'C':
                row[3] = 'cargo'
            else:
                row[3] = 'airline'
            rows.append(row)
        # get total number of rows
        print("Total no. of rows: %d"%(csvreader.line_num))

def findCommunity():
    global communityPath
    try:
        communityPath=str(os.environ.get("LOCALAPPDATA")+"\\Packages\\Microsoft.FlightSimulator_8wekyb3d8bbwe\\LocalCache\\UserCfg.opt")
        print("Community folder found: "+communityPath)
    except:
        try:
            communityPath=str(os.environ.get("APPDATA")+"\\Microsoft Flight Simulator\\UserCfg.opt")
            print("Community folder found: "+communityPath)
        except:
            print("Community wasn't located, aborting")
            input("Press Enter to exit")
    with open(communityPath,"r") as fi:
            id = []
            for ln in fi:
                if ln.startswith("InstalledPackagesPath"):
                    id.append(ln[22:])
            communityPath=(id[0]).replace('"', '').replace("\n", "")+"\\Community\\fsltl-traffic-base\\SimObjects\\Airplanes"

def UpdateFsltlLiveries():
    planes = defaultdict(list)
    path = communityPath
    print("looking in: "+ path)
    vs_entities = []
    filelist = []
    mask = re.compile("FSLTL_*")
    for root, dirs, files in os.walk(path):
        for directory in dirs:
            if mask.match(directory):
                path2 = os.path.dirname(os.path.join(root,directory))
                for root, dirs, files in os.walk(path2):
                    for file in files:
                        if file.lower() == 'aircraft.cfg':
                            filelist.append(os.path.join(root,file))
                            n=directory
                            p=os.path.join(root,file)
                            path = pathlib.PurePath(root)
                            ve = VS_Entity(path.name,p)
                            vs_entities.append(ve)
                
    print("Found " + str(len(filelist)) + " variants" )
    for file in filelist:
        print("Reading " + file)
        icao_type = ''
        icao_airline = ''
        with open(file, 'r') as f:
            line = ''
            while not line.startswith('icao_manufacturer ='):
                line = f.readline()
                if  line == '':
                    #print("No base aircraft found... ")
                    with open(file, 'r') as f:
                        line = ''
                        while not line.startswith('base_container ='):
                            line = f.readline()
                            if  line == '':
                                print("Nothing found!")
                                break
                    break
            if line != '':          
                if line.startswith('base_container ='):
                    vs_name=re.search('([A-Z])\w+', line)
                    vs_name=vs_name.group().strip('"')
                    print("Looking for base aircraft " + vs_name)
                    line=''
                    for vs_entity in vs_entities:
                        if vs_entity.name.upper() == vs_name.upper() or vs_entity.name.upper()+"F" == vs_name.upper():
                            with open(vs_entity.path, 'r') as f:
                                line = ''
                                while not line.startswith('icao_type_designator ='):
                                    line = f.readline()
                                    if  line == '':
                                        print("ERROR! Can't find ICAO in base aircraft.cfg!")
                                        break
                                break
                    if line == '':
                        print("ERROR! Can't find base aircraft.cfg!")
                    else:
                        match = re.search('["].*["]', line)
                        icao_type = match.group().strip('"')
                        with open(file, 'r') as f:
                            for line in f:
                                if line.startswith('icao_airline ='):
                                    match = re.search('["].*["]', line)
                                    icao_airline = match.group().strip('"')
                                    if icao_airline == 'ZZZZ' or icao_airline == 'VIP' or icao_airline == '':
                                        pass
                                    else:
                                        planes[icao_type].append(icao_airline)
                                        print(icao_type, icao_airline)
                                    icao_airline = ''
                            icao_type = ''                                           
    return planes

def produceFltsim(icao_type,model_author,input_default_model,manufacturer,heavy,gates,soundai,exclude,actype):
    data = ""
    
    data+=("[FLTSIM.0]\ntitle = \"FSLTL_"+icao_type+("F" if actype=="cargo" else "")+"_ZZZZ\" ; Variation name\nmodel = \""+input_default_model+"\" ; model folder\ntexture = \""+input_default_model+"\"; texture folder\natc_airline = \"\" ; airline name\nui_manufacturer = \""+manufacturer.upper()+"\" ; e.g. Boeing, Cessna\nui_type = \""+manufacturer.upper()+" "+icao_type.upper()+("F" if actype=="cargo" else "")+"\" ; e.g. 747-400, 172\nui_variation = \"ZZZZ\" ; e.g. World Air, IFR Panel\nui_typerole = \""+("Cargo Freighter" if actype=="cargo" else "Commercial Airliner")+"\"\natc_parking_codes = \"\" ; Comma separated and may be as small as one character each\natc_parking_types = \""+("CARGO," if actype=="cargo" else ("GATE," if gates else ""))+"RAMP\"\natc_heavy = "+str(heavy)+" ; heavy?\nisairtraffic = 1 ; airtraffic flag for variations\nisuserselectable = 0 ; flag off for non selectable planes\natc_id_enable = 1 ; enable tail number\neffects = \"\"\nicao_airline = \"ZZZZ\" ;\npanel = \"\" ; panel folder\nsound = \"" + soundai + "\" ; sound folder\n\n")
    i = 1
    for row in rows:
        skip=0
        for line in exclude:
            if line==row[0]:
                skip=1
                break
        if skip != 1:
            if row[3]==actype and icao_type in row[4]: 
                data+=("[FLTSIM."+str(i)+"]\ntitle = \"FSLTL_"+icao_type+("F" if row[3]=="cargo" else "")+"_"+row[0]+"-"+row[2]+"-"+"STUB\" ; Variation name\nmodel = \""+input_default_model+"\" ; model folder\ntexture = \""+input_default_model+"\"; texture folder\natc_airline = \""+row[2]+"\" ; airline name\nui_manufacturer = \""+manufacturer.upper()+"\" ; e.g. Boeing, Cessna\nui_type = \""+manufacturer.upper()+" "+icao_type.upper()+("F" if row[3]=="cargo" else "")+"\" ; e.g. 747-400, 172\nui_variation = \""+row[1]+"\" ; e.g. World Air, IFR Panel\nui_typerole = \""+("Cargo Freighter" if row[3]=="cargo" else "Commercial Airliner")+"\"\natc_parking_codes = \""+row[0]+"\" ; Comma separated and may be as small as one character each\natc_parking_types = \""+("CARGO,RAMP" if row[3]=="cargo" else ("GATE,RAMP" if gates else "RAMP"))+"\"\natc_heavy = "+str(heavy)+" ; heavy?\nisairtraffic = 1 ; airtraffic flag for variations\nisuserselectable = 0 ; flag off for non selectable planes\natc_id_enable = 1 ; enable tail number\neffects = \"\"\nicao_airline = \""+row[0]+"\" ;\npanel = \"\" ; panel folder\nsound = \"" + soundai + "\" ; sound folder\n\n")
                i+=1
    return data

def writefile(data,icao_type,sub_icao_type):
    targetCfg = communityPath+"\\FSLTL_"+sub_icao_type.upper()+"\\aircraft.cfg"
    with open (targetCfg, "r") as text_file:
        sep="[FLTSIM.0]"
        stripped = text_file.read().split(sep, 1)[0]
        data = stripped + data
    text_file.close()
    with open (targetCfg,"w") as testCfg:
        print(data, file=testCfg)

def main(planes):
    exclude=[]
    soundFolders = []
    models = {}
    cmodels = {}
    soundai = ""
    default_model = ""
    default_cargo_model = ""
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, "../Livery_Packaging_tool/FSLTL_Aircraft.json")
    FSLTL_Aricraft = open (filename, "r")
    my_json=json.load(FSLTL_Aricraft)
    for item in my_json["aircraft"]:
            icao_type=item["icao_type"]
            print ("Processing "+icao_type)
            model_author=item["model_author"]
            manufacturer=item["manufacturer"]
            heavy=int(item["heavy"])
            gates=int(item["gates"])
            isarline = bool(False)
            iscargo = bool(False)
            if "airline" in item["models"]:
                isarline = bool(True)
                for mdlname, mdlxml in item["models"]["airline"].items():
                    models[mdlname]=mdlxml
                default_model=""+next(iter(models))
            if "cargo" in item["models"]:
                iscargo = bool(True)
                for cmdlname, cmdlxml in item["models"]["cargo"].items():
                    cmodels[cmdlname]=cmdlxml
                default_cargo_model=""+next(iter(cmodels))
            for snd in item["sound"]:
                soundFolders.append(snd)
            for icao in planes[icao_type]:
                print ("Excluding " + icao)
                exclude.append(icao)
            try:
                soundai=soundFolders[0]
            except:
                soundai=""
            print ("Models", default_model, default_cargo_model)
            if isarline:
                data = produceFltsim(icao_type, model_author,default_model,manufacturer,heavy,gates,soundai,exclude,"airline")
                writefile (data,icao_type,icao_type)
            if iscargo:
                datac = produceFltsim(icao_type, model_author,default_cargo_model,manufacturer,heavy,gates,soundai,exclude,"cargo")
                writefile (datac,icao_type,icao_type+"F")
            icao_type=""
            model_author=""
            default_model=""
            default_cargo_model=""
            manufacturer=""
            heavy=0
            soundai=""
            exclude=[]
            soundFolders=[]
            models = {}
            cmodels = {}

readCsv()
findCommunity()
main(UpdateFsltlLiveries())
input("Press Enter to exit")





