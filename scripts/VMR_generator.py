import pathlib
import gc
import os
from fractions import Fraction
from decimal import Decimal
from argparse import ArgumentParser
parser = ArgumentParser()
#parser.add_argument("-f", "--folder", dest="aircraftFolder", help="Path to SimObjects\\Airplanes folder")
#args = parser.parse_args()

# Release Notes
# v1.2 (Nov 22, 2025): Added checking atc_parking_codes in addition to icao_airline to find airline ICAo codes for models
#                      If airline/model has no random setting, deduplicate titles when creating lines in VMR


def findCommunity():
    global communityPath
    usecomm = True
    print("\nRun VMR Generator against your Community folder? (y/n)")
    usecomm=(input().lower()=="y")
    if (usecomm):
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
    else:
        print("\nEnter full path to 'Airplanes' folder to process: ")
        communityPath=input()
    return communityPath

ModelsDirectories = [findCommunity()]
#ModelsDirectories = [args.aircraftFolder]

# Configuration options
ExcludeStubs = True   #whether to exclude models with 'STUB' in the title

def selectOption():
  print("\nSelect VMR generation option:")
  print("  1 = Same family fallback only")
  print("  2 = Cross-family fallback")
  print("  3 = Cross-family fallback unless exact model ZZZZ exists")
  print("  4 = Generate all three options")
  while True:
    choice = input("Enter option (1/2/3/4): ").strip()
    if choice in ('1', '2', '3', '4'):
      return int(choice)
    print("Invalid option, please enter 1, 2, 3, or 4.")

selectedOption = selectOption()

class Airplane:
  def __init__(self, TypeCode, Size, Manufacturer, EngineType, WideBody, neoExists, neo, Family):
    self.TypeCode = TypeCode
    self.Size = Size
    self.Manufacturer = Manufacturer
    self.EngineType = EngineType
    self.WideBody = WideBody
    self.neoExists = neoExists
    self.neo = neo
    self.Family = Family

class Model:
  def __init__(self, TypeCode, icao_airline, title, Size, Manufacturer, EngineType, WideBody, neo, random, Family):
    self.TypeCode = TypeCode
    self.icao_airline = icao_airline
    self.title = title
    self.Size = Size
    self.Manufacturer = Manufacturer
    self.EngineType = EngineType
    self.WideBody = WideBody
    self.neo = neo
    self.random = random
    self.Family = Family

class AirlineGroup:
  def __init__(self, List):
    self.List = List

class AirlineModelsClass:
  def __init__(self, Airline, AirlineModels, TypeCode):
    self.Airline = Airline
    self.AirlineModels = AirlineModels
    self.TypeCode = TypeCode

A19N = Airplane('A19N', 125.208, 'Airbus', 'jet', False, True, True, 'A320')
A20N = Airplane('A20N', 139.009, 'Airbus', 'jet', False, True, True, 'A320')
A32N = Airplane('A32N', 139.009, 'Airbus', 'jet', False, True, True, 'A320')
A21N = Airplane('A21N', 154.687, 'Airbus', 'jet', False, True, True, 'A320')
A318 = Airplane('A318', 116.328, 'Airbus', 'jet', False, True, False, 'A320')
A319 = Airplane('A319', 125.208, 'Airbus', 'jet', False, True, False, 'A320')
A320 = Airplane('A320', 139.009, 'Airbus', 'jet', False, True, False, 'A320')
A321 = Airplane('A321', 154.687, 'Airbus', 'jet', False, True, False, 'A320')
A332 = Airplane('A332', 309.3932, 'Airbus', 'jet', True, True, False, 'A330')
A333 = Airplane('A333', 334.8516, 'Airbus', 'jet', True, True, False, 'A330')
A338 = Airplane('A338', 309.3932, 'Airbus', 'jet', True, True, True, 'A330')
A339 = Airplane('A339', 334.8516, 'Airbus', 'jet', True, True, True, 'A330')
A342 = Airplane('A342', 313.632, 'Airbus', 'jet', True, False, False, 'A340')
A343 = Airplane('A343', 336.2832, 'Airbus', 'jet', True, False, False, 'A340')
A345 = Airplane('A345', 358.6704, 'Airbus', 'jet', True, False, False, 'A340')
A346 = Airplane('A346', 397.9008, 'Airbus', 'jet', True, False, False, 'A340')
A359 = Airplane('A359', 374.748, 'Airbus', 'jet', True, False, False, 'A350')
A35K = Airplane('A35K', 413.9619, 'Airbus', 'jet', True, False, False, 'A350')
A388 = Airplane('A388', 960.68, 'Airbus', 'jet', True, False, False, 'A380')
A300 = Airplane('A300', 285.5424, 'Airbus', 'jet', True, False, False, 'A300')
A30B = Airplane('A30B', 242.3172, 'Airbus', 'jet', True, False, False, 'A300')
A306 = Airplane('A306', 285.648, 'Airbus', 'jet', True, False, False, 'A300')
A3ST = Airplane('A3ST', 285.648, 'Airbus', 'jet', True, False, False, 'A300')
A310 = Airplane('A310', 246.3648, 'Airbus', 'jet', True, False, False, 'A310')

B732 = Airplane('B732', 107.665, 'Boeing', 'jet', False, True, False, 'B737')
B733 = Airplane('B733', 117.902, 'Boeing', 'jet', False, True, False, 'B737') 
B734 = Airplane('B734', 128.845, 'Boeing', 'jet', False, True, False, 'B737')
B735 = Airplane('B735', 109.43, 'Boeing', 'jet', False, True, False, 'B737')
B736 = Airplane('B736', 110.136, 'Boeing', 'jet', False, True, False, 'B737')
B737 = Airplane('B737', 118.608, 'Boeing', 'jet', False, True, False, 'B737')
B738 = Airplane('B738', 139.83, 'Boeing', 'jet', False, True, False, 'B737')
B739 = Airplane('B739', 148.613, 'Boeing', 'jet', False, True, False, 'B737')
B38M = Airplane('B38M', 139.83, 'Boeing', 'jet', False, True, True, 'B737')
B39M = Airplane('B39M', 148.613, 'Boeing', 'jet', False, True, True, 'B737')
B712 = Airplane('B712', 118.881, 'Boeing', 'jet', False, False, False, 'B717')
B742 = Airplane('B742', 858.88, 'Boeing', 'jet', True, False, False, 'B747')
B744 = Airplane('B744', 866.782, 'Boeing', 'jet', True, False, False, 'B747')
B748 = Airplane('B748', 930.25, 'Boeing', 'jet', True, False, False, 'B747')
B752 = Airplane('B752', 167.442, 'Boeing', 'jet', False, False, False, 'B757')
B753 = Airplane('B753', 192.8238, 'Boeing', 'jet', False, False, False, 'B757')
B762 = Airplane('B762', 228.92, 'Boeing', 'jet', True, False, False, 'B767')
B763 = Airplane('B763', 259.128, 'Boeing', 'jet', True, False, False, 'B767')
B764 = Airplane('B764', 289.808, 'Boeing', 'jet', True, False, False, 'B767')
B772 = Airplane('B772', 373.919, 'Boeing', 'jet', True, False, False, 'B777')
B773 = Airplane('B773', 433.793, 'Boeing', 'jet', True, False, False, 'B777')
B77L = Airplane('B77L', 373.919, 'Boeing', 'jet', True, False, False, 'B777')
B77W = Airplane('B77W', 432.8196, 'Boeing', 'jet', True, False, False, 'B777')
B788 = Airplane('B788', 311.283, 'Boeing', 'jet', True, False, False, 'B787')
B789 = Airplane('B789', 344.772, 'Boeing', 'jet', True, False, False, 'B787')
B78X = Airplane('B78X', 374.967, 'Boeing', 'jet', True, False, False, 'B787')

AT45 = Airplane('AT45', 58.2619, 'ATR', 'prop', False, False, False, 'ATR')
AT46 = Airplane('AT46', 58.2619, 'ATR', 'prop', False, False, False, 'ATR') 
AT72 = Airplane('AT72', 69.8269, 'ATR', 'prop', False, False, False, 'ATR') 
AT75 = Airplane('AT75', 69.8269, 'ATR', 'prop', False, False, False, 'ATR') 
AT76 = Airplane('AT76', 69.8269, 'ATR', 'prop', False, False, False, 'ATR') 

BCS1 = Airplane('BCS1', 114.8, 'Airbus', 'jet', False, False, False, 'A220') 
BCS3 = Airplane('BCS3', 126.936, 'Airbus', 'jet', False, False, False, 'A220') 

CRJ7 = Airplane('CRJ7', 82.365, 'Bombardier', 'jet', False, False, False, 'CRJ') 
CRJ9 = Airplane('CRJ9', 93.034, 'Bombardier', 'jet', False, False, False, 'CRJ') 
CRJX = Airplane('CRJX', 99.705, 'Bombardier', 'jet', False, False, False, 'CRJ')
CL60 = Airplane('CL60', 51.9715, 'Bombardier', 'jet', False, False, False, 'CL60')
GLEX = Airplane('GLEX', 75.36501, 'Bombardier', 'jet', False, False, False, 'GLEX') 

CONC = Airplane('CONC', 162.1658, 'Concorde', 'jet', False, False, False, 'CONC') 

DH8B = Airplane('DH8B', 56.07, 'de Havilland Canada', 'prop', False, False, False, 'DHC8') 
DH8C = Airplane('DH8C', 64.507, 'de Havilland Canada', 'prop', False, False, False, 'DHC8') 
DH8D = Airplane('DH8D', 82.328, 'de Havilland Canada', 'prop', False, False, False, 'DHC8') 
DHC6 = Airplane('DHC6', 27.5975, 'de Havilland Canada', 'prop', False, False, False, 'DHC6')

E170 = Airplane('E170', 81.926, 'Embraer', 'jet', False, False, False, 'EJet') 
E75S = Airplane('E75S', 86.7758, 'Embraer', 'jet', False, False, False, 'EJet') 
E75L = Airplane('E75L', 86.7758, 'Embraer', 'jet', False, False, False, 'EJet') 
E190 = Airplane('E190', 99.2976, 'Embraer', 'jet', False, False, False, 'EJet') 
E195 = Airplane('E195', 105.901, 'Embraer', 'jet', False, False, False, 'EJet') 
E290 = Airplane('E290', 99.325, 'Embraer', 'jet', False, False, False, 'EJet') 
E295 = Airplane('E295', 113.7374, 'Embraer', 'jet', False, False, False, 'EJet') 

F70 = Airplane('F70', 95.821, 'Fokker', 'jet', False, False, False, 'Fokker') 
F100 = Airplane('F100', 110.143, 'Fokker', 'jet', False, False, False, 'Fokker') 
F28 = Airplane('F28', 91.76, 'Fokker', 'jet', False, False, False, 'Fokker')
F27 = Airplane('F27', 62.65, 'Fokker', 'prop', False, False, False, 'Fokker')

MD11 = Airplane('MD11', 265.5721, 'McDonnell Douglas', 'jet', True, False, False, 'MD11') 
MD82 = Airplane('MD82', 96.6492, 'McDonnell Douglas', 'jet', False, False, False, 'MD80') 
MD83 = Airplane('MD83', 96.6492, 'McDonnell Douglas', 'jet', False, False, False, 'MD80') 
MD88 = Airplane('MD88', 96.6492, 'McDonnell Douglas', 'jet', False, False, False, 'MD80') 

SF34 = Airplane('SF34', 43.406, 'Saab', 'prop', False, False, False, 'SF34') 

SU95 = Airplane('SU95', 97.0056, 'Sukhoi', 'jet', False, False, False, 'SU95')

A225 = Airplane('A225', 1075.2, 'Antonov', 'jet', True, False, False, 'A225') 

B461 = Airplane('B461', 85.1489, 'BAe', 'jet', False, False, False, 'B146') 
B462 = Airplane('B462', 92.82176, 'BAe', 'jet', False, False, False, 'B146') 
B463 = Airplane('B463', 100.7872, 'BAe', 'jet', False, False, False, 'B146') 

LJ25 = Airplane('LJ25', 21.3664, 'Learjet', 'jet', False, False, False, 'LJ2') 

P28A = Airplane('P28A', 7.171, 'Piper', 'prop', False, False, False, 'P28')
PA44 = Airplane('PA44', 28.728, 'Piper', 'prop', False, False, False, 'PA')

C208 = Airplane('C208', 18.745, 'Cessna', 'prop', False, False, False, 'C208') 
C25C = Airplane('C25C', 23.961, 'Cessna', 'jet', False, False, False, 'C25') 
C700 = Airplane('C700', 43.708, 'Cessna', 'jet', False, False, False, 'C700')
C510 = Airplane('C510', 17.318, 'Cessna', 'jet', False, False, False, 'C510')
C172 = Airplane('C172', 8.3, 'Cessna', 'prop', False, False, False, 'C172') 
C152 = Airplane('C152', 7.4134, 'Cessna', 'prop', False, False, False, 'C152') 

DA40 = Airplane('DA40', 9.858, 'Diamond', 'prop', False, False, False, 'DA40') 
DA62 = Airplane('DA62', 12.3809, 'Diamond', 'prop', False, False, False, 'DA62') 

B350 = Airplane('B350', 19.4814, 'Beechcraft', 'prop', False, False, False, 'B350') 
BE36 = Airplane('BE36', 8.9666, 'Beechcraft', 'prop', False, False, False, 'BE36')
BE55 = Airplane('BE55', 29.8704, 'Beechcraft', 'prop', False, False, False, 'BE55') 

SR22 = Airplane('SR22', 9.8632, 'Cirrus', 'prop', False, False, False, 'SR22')
SF50 = Airplane('SF50', 14.6952, 'Cirrus', 'jet', False, False, False, 'SF50')

TBM9 = Airplane('TBM9', 42.91584, 'Daher', 'prop', False, False, False, 'TBM')


Airplanes = []
for Object in gc.get_objects():
  if isinstance(Object, Airplane):
    Airplanes.append(Object)

Airlines = []
Models = []


AirlineGroups = []
QantasGroup = AirlineGroup(['QFA', 'QF', 'QJE', 'QLK', 'QNZ', 'NWK'])
VirginAustraliaGroup = AirlineGroup(['VOZ', 'VA'])
JetstarGroup = AirlineGroup(['JST', 'JQ'])
AirNewZealandGroup = AirlineGroup(['ANZ', 'NZ'])
#AirNewZealandGroup = AirlineGroup(['ANZ', 'NZ', 'NZA'])
#CargoluxGroup = AirlineGroup(['CLX', 'ADB'])
AmericanAirlinesGroup = AirlineGroup(['AAL', 'AA'])
UnitedGroup = AirlineGroup(['UAL', 'UA'])
DeltaGroup = AirlineGroup(['DAL', 'DL'])
AnsettAustraliaGroup = AirlineGroup(['AAA', 'AN'])
DHLGroup = AirlineGroup(['DHK', 'DHL'])
LufthansaGroup = AirlineGroup(['DLH', 'CLH', 'LH'])
AirCanadaGroup = AirlineGroup(['ACA', 'AC'])
RegionalExpressGroup = AirlineGroup(['RXA', 'REX', 'ZL'])
SingaporeAirlinesGroup = AirlineGroup(['SIA', 'SQ'])
EmiratesGroup = AirlineGroup(['UAE', 'EK'])
QatarGroup = AirlineGroup(['QTR', 'QR'])
MalaysiaAirlinesGroup = AirlineGroup(['MAS', 'MH'])
FijiAirwaysGroup = AirlineGroup(['FJI', 'FJ'])
BritishAirwaysGroup = AirlineGroup(['BAW', 'BA', 'SHT'])
#TigerAirGroup = AirlineGroup(['TTW', 'TGG', 'TT', 'IT'])
CathayPacificGroup = AirlineGroup(['CPA', 'CX'])
#AirFranceGroup = AirlineGroup(['AFR', 'AF'])

CargoFlights = [
  ('ANA', 'B763', '7000-9999'),
  ('ASA', 'B737', '7000-9999'),
  ('ASA', 'B738', '7000-9999'),
  ('ETH', 'B738', '3000-3999'),
  ('ETH', 'B77L', '3000-3999'),
  ('JAL', 'B763', '6700-6799'),
  ('JAL', 'B77W', '6700-6799'),
  ('KQA', 'B738', '2200-2799'),
  ('MAS', 'A332', '6000-6699'),
  ('QFA', 'A321', '7000-9999'),
  ('QFA', 'A332', '7000-9999'),
  ('QTR', 'B77L', '8000-8999'),
  ('SCX', 'B738', '3000-3999'),
  ('THY', 'A332', '6000-6699'),
  ('UAE', 'B77L', '9000-9999'),
  ('UKV', 'B738', '7000-7999'),
  ('UKV', 'B748', '7000-7999'),
  ('UKV', 'B77L', '7000-7999'),
]

for Object in gc.get_objects():
  if isinstance(Object, AirlineGroup):
    AirlineGroups.append(Object)

def CutDownString(String, RemoveString):
  if RemoveString != 'title':
    String = String.replace('-', '')
  String = String.replace(RemoveString, '')
  String = String.replace('"', '')
  String = String.replace('=', '')
  String = String.replace(';', '')
  String = String.replace('#', '')
  String = String.replace('Variation name', '')
  String = String.replace('AIRLINE NAME', '')
  String = String.strip()
  return String

for ModelsDirectory in ModelsDirectories: #to find all models
  if ModelsDirectory == '':
    ModelsDirectory = os.path.dirname(os.path.realpath(__file__))
  ModelsDirectory = ModelsDirectory.replace('\\', '/')
  ModelsDirectory = pathlib.Path(ModelsDirectory)
  if os.path.exists(ModelsDirectory):
    for folderpath in ModelsDirectory.iterdir():
      folderpath = folderpath.__str__()
      if os.path.exists(folderpath + '\\aircraft.cfg'):
        AircraftFile = open(folderpath + '\\aircraft.cfg', 'r')
        icao_airline = ''
        atc_parking_codes = []
        TypeCode = ''
        title = ''
        Size = 0
        Manufacturer = ''
        EngineType = ''
        WideBody = ''
        neo = ''
        random = 0
        Family = ''
        exclude = False
        for line in AircraftFile:
          if line.find('title') != -1:
            if title != '':
              if not exclude:
                # Combine icao_airline and atc_parking_codes, deduplicate
                all_airline_codes = []
                if icao_airline:
                  all_airline_codes.append(icao_airline)
                for code in atc_parking_codes:
                  if code not in all_airline_codes:
                    all_airline_codes.append(code)
                # Create a model for each airline code
                for airline_code in all_airline_codes:
                  for airplane in Airplanes:
                    if airplane.TypeCode == TypeCode:
                      Size = airplane.Size
                      Manufacturer = airplane.Manufacturer
                      EngineType = airplane.EngineType
                      WideBody = airplane.WideBody
                      neo = airplane.neo
                      Family = airplane.Family
                  Models.append(Model(TypeCode, airline_code, title, Size, Manufacturer, EngineType, WideBody, neo, random, Family))
              icao_airline = ''
              atc_parking_codes = []
              title = ''
              random = 0
              Family = ''
              exclude = False
            title = CutDownString(line, 'title')
            if title.find('STUB') != -1 and ExcludeStubs:
              exclude = True
            if title.find('FSLTL_Medium_Generic') != -1:
              exclude = True
          else:
            line = line.upper()
            if line.find('ICAO_TYPE_DESIGNATOR') != -1:
              TypeCode = CutDownString(line, 'ICAO_TYPE_DESIGNATOR')
              if TypeCode == '737':
                TypeCode = 'B737'
            elif line.find('ICAO_AIRLINE') != -1:
              icao_airline = CutDownString(line, 'ICAO_AIRLINE')
              if icao_airline == 'ZZZ' or icao_airline == '':
                icao_airline = 'ZZZZ'
              if icao_airline != 'ZZZZ':
                icao_airline = icao_airline[:3]
              if icao_airline not in Airlines:
                Airlines.append(icao_airline)
            elif line.find('ATC_PARKING_CODES') != -1:
              atc_code_string = CutDownString(line, 'ATC_PARKING_CODES')
              # Split by comma and process each code
              for code in atc_code_string.split(','):
                code = code.strip()
                # Skip if code is empty or contains spaces (likely comment remnant)
                if code and ' ' not in code:
                  # Normalize: ZZZ becomes ZZZZ, others become 3 chars
                  if code == 'ZZZ' or code == '':
                    code = 'ZZZZ'
                  else:
                    code = code[:3]
                  if code not in atc_parking_codes:
                    atc_parking_codes.append(code)
                  if code not in Airlines:
                    Airlines.append(code)
            elif line.find('RANDOM') != -1:
              random = CutDownString(line, 'RANDOM')
              Numerator = ''
              Denominator = ''
              PassedNumerator = False
              for a in random:
                if a == '/' or a == '\\':
                  PassedNumerator = True
                elif PassedNumerator:
                  Denominator = Denominator + a
                else:
                  Numerator = Numerator + a
              Numerator = int(Numerator)
              if Denominator == '':
                random = Fraction(Numerator, 100)
              else:
                Denominator = int(Denominator)
                random = Fraction(Numerator, Denominator)
            elif line.find('EXCLUDE') != -1:
              if line.find('TRUE') != -1:
                exclude = True
        if title != '' and not exclude:
          for airplane in Airplanes:
            if airplane.TypeCode == TypeCode:
              Size = airplane.Size
              Manufacturer = airplane.Manufacturer
              EngineType = airplane.EngineType
              WideBody = airplane.WideBody
              neo = airplane.neo
              Family = airplane.Family
          # Combine icao_airline and atc_parking_codes, deduplicate
          all_airline_codes = []
          if icao_airline:
            all_airline_codes.append(icao_airline)
          for code in atc_parking_codes:
            if code not in all_airline_codes:
              all_airline_codes.append(code)
          # Create a model for each airline code
          for airline_code in all_airline_codes:
            Models.append(Model(TypeCode, airline_code, title, Size, Manufacturer, EngineType, WideBody, neo, random, Family))

def ResetModelsToUse(TestingModels):
  ModelsToUse = []
  for TestModel in TestingModels:
    ModelsToUse.append(TestModel)
  return ModelsToUse

def ResetTestingModels(ModelsToUse):
  TestingModels = []
  for ModelToUse in ModelsToUse:
    TestingModels.append(ModelToUse)
  return TestingModels

def WriteModels(airlinemodelclass):
  Modelstr = ''
  ModelstrCargo = ''
  if airlinemodelclass.Airline == 'ZZZZ' or airlinemodelclass.Airline == 'ZZZ' or airlinemodelclass.Airline == '':
    Modelstr = '<ModelMatchRule TypeCode="' + airlinemodelclass.TypeCode + '" ModelName="'
  else:
    cargo_range = None
    for airline, typecode, range_str in CargoFlights:
      if airline == airlinemodelclass.Airline and typecode == airlinemodelclass.TypeCode:
        cargo_range = range_str
        ModelstrCargo = '<ModelMatchRule CallsignPrefix="' + airlinemodelclass.Airline + '" FlightNumberRange="' + cargo_range + '" TypeCode="' + airlinemodelclass.TypeCode + '" ModelName="'
        break
    Modelstr = '<ModelMatchRule CallsignPrefix="' + airlinemodelclass.Airline + '" TypeCode="' + airlinemodelclass.TypeCode + '" ModelName="'
  AddSlashes = False
  AddSlashesCargo = False
  AircraftWithoutRandom = 0
  RandomAircraft = 0
  for ModelToUse in airlinemodelclass.AirlineModels:
    if ModelToUse.random != 0:
      RandomAircraft = RandomAircraft + 1
    else:
      AircraftWithoutRandom = AircraftWithoutRandom + 1
  if RandomAircraft == 0:
    # Deduplicate titles while preserving order
    unique_titles = []
    for ModelToUse in airlinemodelclass.AirlineModels:
      if ModelToUse.title not in unique_titles:
        unique_titles.append(ModelToUse.title)
    for title in unique_titles:
      if ModelstrCargo and '_Cargo' in title:
        if AddSlashesCargo:
          ModelstrCargo = ModelstrCargo + "//"
        AddSlashesCargo = True
        ModelstrCargo = ModelstrCargo + title
      else:
        if AddSlashes:
          Modelstr = Modelstr + "//"
        AddSlashes = True
        Modelstr = Modelstr + title
  else:
    TotalFraction = 0
    for ModelToUse in airlinemodelclass.AirlineModels:
      TotalFraction = TotalFraction + ModelToUse.random
    FractionNumerator = TotalFraction.numerator
    FractionDenominator = TotalFraction.denominator
    if TotalFraction.numerator < RandomAircraft: #if fraction simplyfies to an amount lower than the amount of random aircraft
      CorrectFraction = RandomAircraft / TotalFraction.numerator
      FractionNumerator = FractionNumerator * CorrectFraction
      FractionDenominator = FractionDenominator * CorrectFraction
    for ModelToUse in airlinemodelclass.AirlineModels:
      AmountNeeded = 0
      if ModelToUse.random != 0:
        AmountNeeded = FractionDenominator / ModelToUse.random.denominator * ModelToUse.random.numerator
      Amount = 0
      if AmountNeeded == 0: #the amount needed for the aircraft without random
        AmountNeeded = FractionDenominator - FractionNumerator
        AmountNeeded = AmountNeeded / AircraftWithoutRandom
      while Amount < AmountNeeded:
        Amount = Amount + 1
        if ModelstrCargo and '_Cargo' in ModelToUse.title:
          if AddSlashesCargo:
            ModelstrCargo = ModelstrCargo + '//'
          AddSlashesCargo = True
          ModelstrCargo = ModelstrCargo + ModelToUse.title
        else:
          if AddSlashes:
            Modelstr = Modelstr + '//'
          AddSlashes = True
          Modelstr = Modelstr + ModelToUse.title
  if ModelstrCargo and AddSlashesCargo:
    ModelstrCargo = ModelstrCargo + '" /> \n'
    vmr.write(ModelstrCargo)
  if AddSlashes:
    Modelstr = Modelstr + '" /> \n'
    vmr.write(Modelstr)

def GenerateVMR(SameFamily, ExcludeTypeBlank, filename):
  global vmr
  AirlineModelClasses = []
  for Airline in Airlines:
    icao_airlines = []
    InAirlineGroup = False
    AlreadyDoneAirline = False
    for airlinegroup in AirlineGroups:
      if Airline in airlinegroup.List:
        InAirlineGroup = True
        if airlinegroup.List.index(Airline) != 0:
          AlreadyDoneAirline = True
        icao_airlines = airlinegroup.List
    if icao_airlines == []:
      icao_airlines = [Airline]
    if not AlreadyDoneAirline:
      for icao_airline in icao_airlines:
        AirlineModels = []
        for model in Models:
          if InAirlineGroup:
            for airlinegroup in AirlineGroups:
              if icao_airline in airlinegroup.List:
                if model.icao_airline in airlinegroup.List: #add all models in airline group
                  AirlineModels.append(model)
          else:
            if model.icao_airline == icao_airline: #add all models in airline
              AirlineModels.append(model)
        if len(AirlineModels) == 0: #if cant find any models for airline, use default models
          if not SameFamily:  # Only load all generics if SameFamily is off
            for model in Models:
              if model.icao_airline == 'ZZZZ' or model.icao_airline == 'ZZZ' or model.icao_airline == '':
                AirlineModels.append(model)
        for airplane in Airplanes:
          ModelsToUse = ResetModelsToUse(AirlineModels)
          TestingModels = ResetTestingModels(ModelsToUse)
          # Only filter by family if SameFamily is True (but not for generic ZZZZ entries)
          if SameFamily and icao_airline not in ['ZZZZ', 'ZZZ', '']:
            for TestModel in TestingModels:
              if TestModel.Family != airplane.Family:
                ModelsToUse.remove(TestModel)
          # After filtering by family (if enabled), if we have no models, load appropriate generics based on SameFamily
          if len(ModelsToUse) == 0:
            for model in Models:
              if model.icao_airline == 'ZZZZ' or model.icao_airline == 'ZZZ' or model.icao_airline == '':
                if not SameFamily or model.Family == airplane.Family:
                  ModelsToUse.append(model)
            TestingModels = ResetTestingModels(ModelsToUse)
          if len(ModelsToUse) == 0:
            if SameFamily:
              for model in Models:
                if model.icao_airline == 'ZZZZ' or model.icao_airline == 'ZZZ' or model.icao_airline == '':
                  if model.Family == airplane.Family:
                    ModelsToUse.append(model)
              if len(ModelsToUse) == 0:
                ModelsToUse = ResetModelsToUse(TestingModels)
                for model in Models:
                  if model not in ModelsToUse:
                    if model.icao_airline == 'ZZZZ' or model.icao_airline == 'ZZZ' or model.icao_airline == '':
                      if not SameFamily or model.Family == airplane.Family:
                        ModelsToUse.append(model)
            else:
              ModelsToUse = ResetModelsToUse(TestingModels)
          TestingModels = ResetTestingModels(ModelsToUse)
          for TestModel in TestingModels:
            if TestModel.TypeCode != airplane.TypeCode:
              ModelsToUse.remove(TestModel)
          if len(ModelsToUse) == 0:
            ModelsToUse = ResetModelsToUse(TestingModels)
            TestingModels = ResetTestingModels(ModelsToUse)
            for TestModel in TestingModels:
              if TestModel.Family != airplane.Family:
                ModelsToUse.remove(TestModel)
            if len(ModelsToUse) == 0:
              ModelsToUse = ResetModelsToUse(TestingModels)
            else:
              TestingModels = ResetTestingModels(ModelsToUse)
            for TestModel in TestingModels:
              if TestModel.EngineType != airplane.EngineType:
                ModelsToUse.remove(TestModel)
            if len(ModelsToUse) == 0: #if can't find any models with same engine type, use default models
              for model in Models:
                if model.icao_airline == 'ZZZZ' or model.icao_airline == 'ZZZ' or model.icao_airline == '':
                  if not SameFamily or model.Family == airplane.Family:
                    ModelsToUse.append(model)
              if len(ModelsToUse) == 0:
                ModelsToUse = ResetModelsToUse(TestingModels)
            TestingModels = ResetTestingModels(ModelsToUse)
            for TestModel in TestingModels:
              if TestModel.WideBody != airplane.WideBody:
                ModelsToUse.remove(TestModel)
            if len(ModelsToUse) == 0: #if can't find any models that are the same widebody type, use default models
              for model in Models:
                if model.icao_airline == 'ZZZZ' or model.icao_airline == 'ZZZ' or model.icao_airline == '':
                  if not SameFamily or model.Family == airplane.Family:
                    ModelsToUse.append(model)
              if len(ModelsToUse) == 0:
                ModelsToUse = ResetModelsToUse(TestingModels)
            TestingModels = ResetTestingModels(ModelsToUse)
            for TestModel in TestingModels:
              if TestModel.EngineType != airplane.EngineType:
                ModelsToUse.remove(TestModel)
            if len(ModelsToUse) == 0:
              ModelsToUse = ResetModelsToUse(TestingModels)
            TestingModels = ResetTestingModels(ModelsToUse)
            for TestModel in TestingModels:
              if TestModel.WideBody != airplane.WideBody:
                ModelsToUse.remove(TestModel)
            if len(ModelsToUse) == 0:
              ModelsToUse = ResetModelsToUse(TestingModels)
            TestingModels = ResetTestingModels(ModelsToUse)
            for TestModel in TestingModels:
              SizeDifference = TestModel.Size - airplane.Size
              SizeDifference = abs(SizeDifference)
              if SizeDifference > (airplane.Size / 400 * 150):
                ModelsToUse.remove(TestModel)
            SmallestSizeDifference = 1000
            if len(ModelsToUse) == 0:
              ModelsToUse = ResetModelsToUse(TestingModels)
              for TestModel in TestingModels:
                SizeDifference = TestModel.Size - airplane.Size
                SizeDifference = abs(SizeDifference)
                if SizeDifference < SmallestSizeDifference:
                  SmallestSizeDifference = SizeDifference
              for TestModel in TestingModels:
                SizeDifference = TestModel.Size - airplane.Size
                SizeDifference = abs(SizeDifference)
                if SizeDifference - SmallestSizeDifference > (airplane.Size / 400 * 150):
                  ModelsToUse.remove(TestModel)
            TestingModels = ResetTestingModels(ModelsToUse)
            for TestModel in TestingModels:
              if TestModel.Manufacturer != airplane.Manufacturer:
                ModelsToUse.remove(TestModel)
            if len(ModelsToUse) == 0:
              ModelsToUse = ResetModelsToUse(TestingModels)
            else:
              TestingModels = ResetTestingModels(ModelsToUse)
            SmallestSizeDifference = 1000
            for TestModel in TestingModels:
              SizeDifference = TestModel.Size - airplane.Size
              SizeDifference = abs(SizeDifference)
              if SizeDifference < SmallestSizeDifference:
                SmallestSizeDifference = SizeDifference
            for TestModel in TestingModels:
              SizeDifference = TestModel.Size - airplane.Size
              SizeDifference = abs(SizeDifference)
              if SizeDifference > SmallestSizeDifference:
                ModelsToUse.remove(TestModel)
            TestingModels = ResetTestingModels(ModelsToUse)
            for TestModel in TestingModels:
              if airplane.neoExists:
                if TestModel.neo != airplane.neo:
                  ModelsToUse.remove(TestModel)
            if len(ModelsToUse) == 0:
              ModelsToUse = ResetModelsToUse(TestingModels)
          TestingModels = ResetTestingModels(ModelsToUse)
          for TestModel in TestingModels:
            if TestModel.title.find(TestModel.TypeCode + 'F') != -1:
              ModelsToUse.remove(TestModel)
          if len(ModelsToUse) == 0:
            ModelsToUse = ResetModelsToUse(TestingModels)
          TestingModels = ResetTestingModels(ModelsToUse)
          for TestModel in TestingModels:
            if TestModel.title.find('B73X') != -1:
              ModelsToUse.remove(TestModel)
          if len(ModelsToUse) == 0:
            ModelsToUse = ResetModelsToUse(TestingModels)
          TestingModels = ResetTestingModels(ModelsToUse)
          for TestModel in TestingModels:
            if TestModel.icao_airline == 'ZZZZ' or TestModel.icao_airline == 'ZZZ' or TestModel.icao_airline == '':
              ModelsToUse.remove(TestModel)
          if len(ModelsToUse) == 0:
            ModelsToUse = ResetModelsToUse(TestingModels)
          # Only add if it's ZZZZ, or if it's a specific airline WITH actual airline models
          # For airline groups, also accept if we have any models from the group (not generic ZZZZ)
          if icao_airline in ['ZZZZ', 'ZZZ', ''] or any(m.icao_airline == icao_airline for m in ModelsToUse) or (InAirlineGroup and any(m.icao_airline in icao_airlines for m in ModelsToUse)):
            # ExcludeTypeBlank check: if using cross-family airline liveries when exact-type ZZZZ exists, skip
            ShouldExclude = False
            if ExcludeTypeBlank and not SameFamily and icao_airline not in ['ZZZZ', 'ZZZ', '']:
              # Check if ModelsToUse contains airline-specific (non-ZZZZ) models from different families
              has_airline_models = any(m.icao_airline == icao_airline for m in ModelsToUse)
              if has_airline_models:
                # Check if any model in ModelsToUse is from a different family than current airplane
                cross_family_fallback = any(m.Family != airplane.Family for m in ModelsToUse)
                if cross_family_fallback:
                  # Check if exact-type ZZZZ or same-family ZZZZ exists
                  exact_type_zzzz_exists = any((m.TypeCode == airplane.TypeCode or m.Family == airplane.Family) and (m.icao_airline == 'ZZZZ' or m.icao_airline == 'ZZZ') for m in Models)
                  if exact_type_zzzz_exists:
                    ShouldExclude = True

            if not ShouldExclude:
              AirlineModelClasses.append(AirlineModelsClass(icao_airline, ModelsToUse, airplane.TypeCode))
  vmr = open(os.path.dirname(os.path.realpath(__file__)) + '/' + filename, 'w')
  vmr.write('<?xml version="1.0" encoding="utf-8"?> \n')
  vmr.write('<ModelMatchRuleSet> \n')
  for airlinemodelclass in AirlineModelClasses:
    if len(airlinemodelclass.Airline) != 2:
      WriteModels(airlinemodelclass)
  for airlinemodelclass in AirlineModelClasses:
    if len(airlinemodelclass.Airline) == 2:
      WriteModels(airlinemodelclass)

  vmr.write('</ModelMatchRuleSet>')
  print('Generated: ' + filename)

if selectedOption == 4:
  GenerateVMR(True, False, 'FSLTL_rules_Option1.vmr')
  GenerateVMR(False, False, 'FSLTL_rules_Option2.vmr')
  GenerateVMR(False, True, 'FSLTL_rules_Option3.vmr')
else:
  options = {
    1: (True, False, 'FSLTL_rules_Option1.vmr'),
    2: (False, False, 'FSLTL_rules_Option2.vmr'),
    3: (False, True, 'FSLTL_rules_Option3.vmr'),
  }
  sf, etb, fname = options[selectedOption]
  GenerateVMR(sf, etb, fname)
