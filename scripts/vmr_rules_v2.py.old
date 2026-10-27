import re
import collections
class Plane:
    def __init__(self, model, type, airline):
        self.model = model
        self.type = type
        self.airline = airline
class VS_Entity:
    def __init__(self,name,path):
        self.name=name
        self.path=path

import os


# As you can see, this is pretty much identical to your code
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("-f", "--folder", dest="aircraftFolder", help="Scan aircraft folder")
parser.add_argument("-o", "--output", dest="outputFolder", help="VMR output folder")
args = parser.parse_args()
aircraftFolder = args.aircraftFolder
outputFolder = args.outputFolder

path = aircraftFolder
print("looking in " + aircraftFolder)

vs_entities = []
mask = re.compile("FSLTL_*")
for root, dirs, files in os.walk(path):
    for directory in dirs:
        if mask.match(directory):
           
            path2 = os.path.dirname(os.path.join(root,directory))
            for root, dirs, files in os.walk(path2):
                for file in files:
                    if file.lower() == 'aircraft.cfg':
                        n=directory
                        p=os.path.join(root,file)
                        ve = VS_Entity(n,p)
                       
                        vs_entities.append(ve)
                

filelist = []


for root, dirs, files in os.walk(path):
    for file in files:
        if file.lower() == 'aircraft.cfg':
            filelist.append(os.path.join(root,file))

models = []
blanks = []
print("Found " + str(len(filelist)) + " variants" )
for file in filelist:
    print("\nReading " + file)
    model = ''
    icao_type = ''
    icao_airline = ''
    model_match = False
    with open(file, 'r') as f:
        for line in f:
            if line.startswith('title = '):
                match = re.search('["].*["]', line)
                model = match.group().strip('"')
            elif line.startswith('icao_type_designator ='):
                match = re.search('["].*["]', line)
                icao_type = match.group().strip('"')
            elif line.startswith('icao_airline ='):
                match = re.search('["].*["]', line)
                icao_airline = match.group().strip('"')
                if icao_airline == 'ZZZZ' or icao_airline == 'VIP' or icao_airline == '':
                    plane = Plane(model, icao_type, icao_airline)
                    blanks.append(plane)
                else:
                    for plane_model in models:
                        if plane_model.type == icao_type and plane_model.airline == icao_airline:
                            plane_model.model = '%s//%s' % (plane_model.model, model)
                            model_match = True
                            break
                    if not model_match:
                        plane = Plane(model, icao_type, icao_airline)
                        models.append(plane)
                print(model, icao_type, icao_airline)
                model = ''
                icao_airline = ''
                model_match = False
                                
s = sorted(models, key=lambda Plane: Plane.airline )
with open(outputFolder + '/FSLTL_Rules.vmr', 'w') as f:
    
    f.write('<?xml version="1.0" encoding="utf-8"?><ModelMatchRuleSet>\n')
    for plane in s:
        f.write('\t<ModelMatchRule CallsignPrefix="%s" TypeCode="%s" ModelName="%s"/>\n' % (plane.airline, plane.type, plane.model))
    for blank in blanks:
        f.write('\t<ModelMatchRule TypeCode="%s" ModelName="%s"/>\n' % (blank.type, blank.model))
    f.write('</ModelMatchRuleSet>')
