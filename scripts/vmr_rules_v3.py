import pathlib
import gc
import os
from fractions import Fraction
from decimal import Decimal
ModelsDirectories = ['']
ExcludeStubs = True

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

# As you can see, this is pretty much identical to your code
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("-f", "--folder", dest="aircraftFolder", help="Scan aircraft folder")
parser.add_argument("-o", "--output", dest="outputFolder", help="VMR output folder")
args = parser.parse_args()
aircraftFolder = args.aircraftFolder + '/Airplanes'
outputFolder = args.outputFolder


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
CL60 = Airplane('CL60', 51.9715, 'Bombadier', 'jet', False, False, False, 'CL60')
GLEX = Airplane('GLEX', 75.36501, 'Bombadier', 'jet', False, False, False, 'GLEX') 

CONC = Airplane('CONC', 162.1658, 'Concorde', 'jet', False, False, False, 'CONC') 

DH8B = Airplane('DH8B', 56.07, 'de Havilland Canada', 'prop', False, False, False, 'DHC8') 
DH8C = Airplane('DH8C', 64.507, 'de Havilland Canada', 'prop', False, False, False, 'DHC8') 
DH8D = Airplane('DH8D', 82.328, 'de Havilland Canada', 'prop', False, False, False, 'DHC8') 

E170 = Airplane('E170', 81.926, 'Embraer', 'jet', False, False, False, 'EJet') 
E190 = Airplane('E190', 99.2976, 'Embraer', 'jet', False, False, False, 'EJet') 
E195 = Airplane('E195', 105.901, 'Embraer', 'jet', False, False, False, 'EJet') 

F70 = Airplane('F70', 95.821, 'Fokker', 'jet', False, False, False, 'Fokker') 
F100 = Airplane('F100', 110.143, 'Fokker', 'jet', False, False, False, 'Fokker') 

MD11 = Airplane('MD11', 265.5721, 'McDonnell Douglas', 'jet', True, False, False, 'MD11') 
MD82 = Airplane('MD82', 96.6492, 'McDonnell Douglas', 'jet', False, False, False, 'MD80') 
MD83 = Airplane('MD83', 96.6492, 'McDonnell Douglas', 'jet', False, False, False, 'MD80') 
MD88 = Airplane('MD88', 96.6492, 'McDonnell Douglas', 'jet', False, False, False, 'MD80') 

SF34 = Airplane('SF34', 43.406, 'Saab', 'prop', False, False, False, 'SF34') 

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
RegionalExpressGroup = AirlineGroup(['RXA', 'ZL'])
SingaporeAirlinesGroup = AirlineGroup(['SIA', 'SQ'])
EmiratesGroup = AirlineGroup(['UAE', 'EK'])
QatarGroup = AirlineGroup(['QTR', 'QR'])
MalaysiaAirlinesGroup = AirlineGroup(['MAS', 'MH'])
FijiAirwaysGroup = AirlineGroup(['FJI', 'FJ'])
BritishAirwaysGroup = AirlineGroup(['BAW', 'BA', 'SHT'])
#TigerAirGroup = AirlineGroup(['TTW', 'TGG', 'TT', 'IT'])
CathayPacificGroup = AirlineGroup(['CPA', 'CX'])
AirFranceGroup = AirlineGroup(['AFR', 'AF'])

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

ModelsDirectory = os.path.dirname(os.path.realpath(aircraftFolder))
ModelsDirectory = ModelsDirectory.replace('\\', '/')
print(ModelsDirectory)
ModelsDirectory = pathlib.Path(ModelsDirectory)
if os.path.exists(ModelsDirectory):
    for folderpath in ModelsDirectory.iterdir():
      folderpath = folderpath.__str__()
      print(folderpath)
      if os.path.exists(folderpath + '\\aircraft.cfg'):
        AircraftFile = open(folderpath + '\\aircraft.cfg', 'r')
        icao_airline = ''
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
                for airplane in Airplanes:
                  if airplane.TypeCode == TypeCode:
                    Size = airplane.Size
                    Manufacturer = airplane.Manufacturer
                    EngineType = airplane.EngineType
                    WideBody = airplane.WideBody
                    neo = airplane.neo
                    Family = airplane.Family
                Models.append(Model(TypeCode, icao_airline, title, Size, Manufacturer, EngineType, WideBody, neo, random, Family))
              icao_airline = ''
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
              if icao_airline == 'ZZZ' or '':
                icao_airline = 'ZZZZ'
              if icao_airline != 'ZZZZ':
                icao_airline = icao_airline[:3]
              if icao_airline not in Airlines:
                Airlines.append(icao_airline)
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
              Models.append(Model(TypeCode, icao_airline, title, Size, Manufacturer, EngineType, WideBody, neo, random, Family))

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
              if model.icao_airline in airlinegroup.List:
                AirlineModels.append(model)
        else:
          if model.icao_airline == icao_airline:
            AirlineModels.append(model)
      if len(AirlineModels) == 0:
        for model in Models:
          if model.icao_airline == 'ZZZZ' or model.icao_airline == 'ZZZ' or model.icao_airline == '':
            AirlineModels.append(model)
      for airplane in Airplanes:
        ModelsToUse = ResetModelsToUse(AirlineModels)
        TestingModels = ResetTestingModels(ModelsToUse)
        for TestModel in TestingModels:
          if TestModel.EngineType != airplane.EngineType:
            ModelsToUse.remove(TestModel)
          if len(ModelsToUse) == 0:
            for model in Models:
              if model.icao_airline == 'ZZZZ' or model.icao_airline == 'ZZZ' or model.icao_airline == '':
                ModelsToUse.append(model)
          TestingModels = ResetTestingModels(ModelsToUse)
        for TestModel in TestingModels:
          if TestModel.WideBody != airplane.WideBody:
            ModelsToUse.remove(TestModel)
          if len(ModelsToUse) == 0:
            for model in Models:
              if model.icao_airline == 'ZZZZ' or model.icao_airline == 'ZZZ' or model.icao_airline == '':
                ModelsToUse.append(model)
          TestingModels = ResetTestingModels(ModelsToUse)
        for TestModel in TestingModels:
          if TestModel.TypeCode != airplane.TypeCode:
            ModelsToUse.remove(TestModel)
        if len(ModelsToUse) == 0:
          ModelsToUse = ResetModelsToUse(TestingModels)
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
          for TestModel in TestingModels:
            if TestModel.Family != airplane.Family:
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
        if len(ModelsToUse) > 1:
          TestingModels = ResetTestingModels(ModelsToUse)
          CargoModels = []
          for TestModel in TestingModels:
            if TestModel.title.find(TestModel.TypeCode + 'F') != -1:
              CargoModels.append(TestModel)
          if len(CargoModels) < len(TestingModels):
            for CargoModel in CargoModels:
              ModelsToUse.remove(CargoModel)
        if len(ModelsToUse) > 1:
          TestingModels = ResetTestingModels(ModelsToUse)
          for TestModel in TestingModels:
            if TestModel.title.find('B73X') != -1:
              ModelsToUse.remove(TestModel)
        AirlineModelClasses.append(AirlineModelsClass(icao_airline, ModelsToUse, airplane.TypeCode))

vmr = open(outputFolder + '/FSLTL_Rules.vmr', 'w')
print('Writing VMR : ' + outputFolder + '/FSLTL_Rules.vmr')
vmr.write('<?xml version="1.0" encoding="utf-8"?> \n')
vmr.write('<ModelMatchRuleSet> \n')

def WriteModels(airlinemodelclass):
  if airlinemodelclass.Airline == 'ZZZZ' or airlinemodelclass.Airline == 'ZZZ' or airlinemodelclass.Airline == '':
    Modelstr = '<ModelMatchRule TypeCode = "' + airlinemodelclass.TypeCode + '" ModelName ="'
  else:
    Modelstr = '<ModelMatchRule CallsignPrefix="' + airlinemodelclass.Airline + '" TypeCode = "' + airlinemodelclass.TypeCode + '" ModelName ="'
  AddSlashes = False
  AircraftWithoutRandom = 0
  RandomAircraft = 0
  for ModelToUse in airlinemodelclass.AirlineModels:
    if ModelToUse.random != 0:
      RandomAircraft = RandomAircraft + 1
    else:
      AircraftWithoutRandom = AircraftWithoutRandom + 1
  if RandomAircraft == 0:
    for ModelToUse in airlinemodelclass.AirlineModels:
      if AddSlashes:
        Modelstr = Modelstr + "//"
      AddSlashes = True
      Modelstr = Modelstr + ModelToUse.title
  else:
    TotalFraction = 0
    for ModelToUse in airlinemodelclass.AirlineModels:
      TotalFraction = TotalFraction + ModelToUse.random 
    for ModelToUse in airlinemodelclass.AirlineModels:
      AmountNeeded = 0
      if ModelToUse.random != 0:
        AmountNeeded = TotalFraction.denominator / ModelToUse.random.denominator * ModelToUse.random.numerator
      Amount = 0
      if AmountNeeded == 0:
        AmountNeeded = TotalFraction.denominator - TotalFraction.numerator
        AmountNeeded = AmountNeeded / AircraftWithoutRandom
      while Amount < AmountNeeded:
        Amount = Amount + 1
        if AddSlashes:
          Modelstr = Modelstr + '//'
        AddSlashes = True
        Modelstr = Modelstr + ModelToUse.title
  Modelstr = Modelstr + '" /> \n'
  vmr.write(Modelstr)

for airlinemodelclass in AirlineModelClasses:
  if len(airlinemodelclass.Airline) != 2:
    WriteModels(airlinemodelclass)
for airlinemodelclass in AirlineModelClasses:
  if len(airlinemodelclass.Airline) == 2:
    WriteModels(airlinemodelclass)

vmr.write('</ModelMatchRuleSet>')
