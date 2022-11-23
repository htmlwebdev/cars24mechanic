import concurrent.futures
import json
import os
import re
import sqlite3
import time
from urllib.parse import urlparse
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

BASE_DIR = os.path.dirname((os.path.abspath(__file__))).replace("\\", "/")
headers = Headers(headers=True)

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),  # 60 * 60 * 24
    ('hours', 3600),  # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)
connection = sqlite3.connect(f"{BASE_DIR}/garage.db")
sql = "CREATE TABLE IF NOT EXISTS garage (service_id,brand_num,brand_name,model_num,model_name,fuel_num,fuel_name," \
      "service_type,service_cat,title,time,amount,desc,imgurl)"


def display_time(seconds, granularity=4):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


maindict = {"brand_num": "", "brand_name": "", "model_num": "", "model_name": "", "fuel_num": "",
            "fuel_name": "", "service_type": "", "service_id": "",
            "service_cat": "", "title": "", "time": "", "amount": "", "desc": "", "imgurl": ""}

connection.execute(sql)

session = requests.session()
services_list = ['periodic-services', 'denting-and-painting', 'batteries', 'car-spa-and-cleaning',
                 'ac-service-and-repair',
                 'tyres-and-wheels', 'accidental-car-repair', 'detailing-services', 'custom-services',
                 'windshield-and-glass', 'lights-and-fitments', 'engine-decarbonization']

listdict = {v: k for k, v in enumerate(services_list)}

cars_list = ['HONDA', 'HYUNDAI', 'MARUTI SUZUKI', 'MAHINDRA', 'TATA', 'KIA', 'SKODA', 'RENAULT', 'CHEVROLET', 'TOYOTA',
             'FIAT', 'ASTON MARTIN', 'AUDI', 'BENTLEY', 'BMW', 'FERRARI', 'JAGUAR', 'LAMBORGHINI', 'LEXUS', 'MASERATI',
             'MERCEDES', 'MINI', 'MITSUBISHI', 'PORSCHE', 'VOLVO', 'Volkswagen', 'Ford']

keyslist = ",".join(maindict.keys())


def insert_data(data_list):
    if data_list:
        query = "INSERT INTO garage ({}) VALUES ({}) ".format(keyslist, ",".join(["?"] * 14))
        connection.executemany(query, data_list)  # Insertion in database
        connection.commit()
        # return print(f"{lens} services records inserted")


def get_cars(tempdata):
    url = f"https://www.garage.movemycar.in/gurgaon/{tempdata['service_type']}/{'-'.join(tempdata['brand_name'].split())}/{'-'.join(tempdata['model_name'].split())}/{tempdata['fuel_name']}"
    print(url)
    sections_data = []
    try:
        fetch_image_response = session.get(url, headers=headers.generate())
        parsed_response = BeautifulSoup(fetch_image_response.text, 'html.parser')
        sections = parsed_response.find("section", class_="service-list-section")
        for heading, sections in zip(sections.find_all("h2"), sections.find_all("div", class_="service-list-group")):
            for service_box in sections.find_all("div", class_='service-details-box'):
                temp = {'service_id': service_box.find("a", class_='view_desc_details').attrs['id'],
                        'service_cat': " ".join(heading.find(text=True, recursive=False).split()),
                        'title': " ".join(service_box.find("h4").text.split()),
                        'time': " ".join(service_box.find("span").text.split()),
                        'amount': " ".join(service_box.find("div", class_="add-to-cart").find("strong").text.split()),
                        'desc': str(
                            [" ".join(tick.text.split()) for tick in
                             service_box.find("ul", class_="tick").find_all("li")]),
                        'imgurl': urlparse(service_box.find("img").attrs['src']).path}
                tempdata.update(temp)
                sections_data.append(tuple(tempdata.values()))
    except Exception as error:
        print(error)
    return sections_data


cars_dict = {1: {'HONDA': {'16': {'Accord': {'16': 'Petrol', '17': 'CNG'}}, '32': {'Accord Hybrid': {'32': 'Petrol'}},
                           '3': {'Amaze': {'3': 'Petrol', '4': 'CNG', '5': 'Diesel'}},
                           '9': {'Brio': {'9': 'Petrol', '10': 'CNG'}}, '30': {'BRV': {'30': 'Petrol', '31': 'Diesel'}},
                           '6': {'City ': {'6': 'Petrol', '7': 'CNG', '8': 'Diesel'}},
                           '26': {'City IDTEC': {'26': 'Diesel'}}, '1': {'City IVTEC ': {'1': 'Petrol', '2': 'CNG'}},
                           '18': {'City ZX': {'18': 'Petrol', '19': 'CNG', '20': 'Diesel'}},
                           '14': {'Civic': {'14': 'Petrol', '15': 'CNG'}},
                           '27': {'CRV': {'27': 'Petrol', '28': 'CNG', '29': 'Diesel'}},
                           '11': {'Jazz': {'11': 'Petrol', '12': 'CNG', '13': 'Diesel'}},
                           '23': {'Mobilio': {'23': 'Petrol', '24': 'CNG', '25': 'Diesel'}},
                           '21': {'WRV': {'21': 'Petrol', '22': 'Diesel'}}}}, 2: {
    'HYUNDAI': {'60': {'Accent ': {'60': 'Petrol', '61': 'CNG', '62': 'Diesel'}},
                '82': {'Accent Viva': {'82': 'Petrol', '83': 'CNG', '84': 'Diesel'}},
                '95': {'Aura': {'95': 'Petrol', '96': 'Diesel'}},
                '51': {'Creta': {'51': 'Petrol', '52': 'CNG', '53': 'Diesel'}},
                '68': {'Elantra': {'68': 'Petrol', '69': 'CNG', '70': 'Diesel'}},
                '48': {'Elite i20': {'48': 'Petrol', '49': 'CNG', '50': 'Diesel'}},
                '43': {'Eon': {'43': 'Petrol', '44': 'CNG'}}, '71': {'Getz': {'71': 'Petrol', '72': 'CNG'}},
                '80': {'Getz Prime': {'80': 'Petrol', '81': 'Diesel'}},
                '33': {'Grand i10': {'33': 'Petrol', '34': 'CNG', '35': 'Diesel'}},
                '75': {'Grand i10 Nios': {'75': 'Petrol', '76': 'Diesel'}},
                '36': {'i10': {'36': 'Petrol', '37': 'CNG'}},
                '38': {'i20': {'38': 'Petrol', '39': 'CNG', '40': 'Diesel'}},
                '65': {'i20 Active': {'65': 'Petrol', '66': 'CNG', '67': 'Diesel'}},
                '85': {'SantaFE': {'85': 'Petrol', '86': 'CNG', '87': 'Diesel'}},
                '63': {'Santro': {'63': 'Petrol', '64': 'Diesel'}},
                '41': {'Santro Xing': {'41': 'Petrol', '42': 'CNG'}},
                '89': {'Sonata': {'89': 'Petrol', '90': 'CNG', '91': 'Diesel'}},
                '92': {'Sonata Embera': {'92': 'Petrol', '93': 'CNG', '94': 'Diesel'}},
                '97': {'Sonata Transform': {'97': 'Petrol', '98': 'CNG', '99': 'Diesel'}},
                '88': {'Tucson': {'88': 'Diesel'}}, '73': {'Venue': {'73': 'Petrol', '74': 'Diesel'}},
                '57': {'Verna': {'57': 'Petrol', '58': 'CNG', '59': 'Diesel'}},
                '54': {'Verna Fluidic': {'54': 'Petrol', '55': 'CNG', '56': 'Diesel'}},
                '77': {'Verna Transform': {'77': 'Petrol', '78': 'CNG', '79': 'Diesel'}},
                '45': {'Xcent': {'45': 'Petrol', '46': 'CNG', '47': 'Diesel'}}}}, 3: {
    'MARUTI SUZUKI': {'136': {'800': {'136': 'Petrol', '137': 'CNG'}},
                      '140': {'A-Star': {'140': 'Petrol', '141': 'CNG'}},
                      '111': {'Alto': {'111': 'Petrol', '112': 'CNG'}},
                      '127': {'Alto 800': {'127': 'Petrol', '128': 'CNG'}},
                      '122': {'Alto K10': {'122': 'Petrol', '123': 'CNG'}},
                      '108': {'Baleno': {'108': 'Petrol', '109': 'CNG', '110': 'Diesel'}},
                      '116': {'Celerio': {'116': 'Petrol', '117': 'CNG', '118': 'Diesel'}},
                      '119': {'Ciaz': {'119': 'Petrol', '120': 'CNG', '121': 'Diesel'}},
                      '148': {'Eeco': {'148': 'Petrol', '149': 'CNG'}},
                      '124': {'Ertiga': {'124': 'Petrol', '125': 'CNG', '126': 'Diesel'}},
                      '150': {'Esteem': {'150': 'Petrol', '151': 'CNG'}},
                      '131': {'Estilo': {'131': 'Petrol', '132': 'CNG'}},
                      '156': {'Grand Vitara': {'156': 'Petrol', '157': 'CNG', '158': 'Diesel'}},
                      '159': {'Gypsy': {'159': 'Petrol', '160': 'CNG', '161': 'Diesel'}},
                      '142': {'Ignis': {'142': 'Petrol', '143': 'CNG', '144': 'Diesel'}},
                      '162': {'Kizashi': {'162': 'Petrol', '163': 'CNG', '164': 'Diesel'}},
                      '152': {'Omni': {'152': 'Petrol', '153': 'CNG'}},
                      '113': {'Ritz': {'113': 'Petrol', '114': 'CNG', '115': 'Diesel'}},
                      '145': {'S-Cross': {'145': 'Petrol', '146': 'CNG', '147': 'Diesel'}},
                      '154': {'S-Presso': {'154': 'Petrol', '155': 'Diesel'}},
                      '100': {'Swift': {'100': 'Petrol', '101': 'CNG', '102': 'Diesel'}},
                      '105': {'Swift Dzire': {'105': 'Petrol', '106': 'CNG', '107': 'Diesel'}},
                      '133': {'SX4': {'133': 'Petrol', '134': 'CNG', '135': 'Diesel'}},
                      '165': {'Versa': {'165': 'Petrol', '166': 'CNG'}},
                      '129': {'Vitara Brezza': {'129': 'Petrol', '130': 'Diesel'}},
                      '103': {'Wagonr': {'103': 'Petrol', '104': 'CNG'}},
                      '167': {'XL6': {'167': 'Petrol', '168': 'CNG', '169': 'Diesel'}},
                      '138': {'Zen': {'138': 'Petrol', '139': 'CNG'}}}}, 4: {
    'MAHINDRA': {'194': {'Alturas G4': {'194': 'Diesel'}}, '178': {'Bolero': {'178': 'Diesel'}},
                 '187': {'Bolero Camper': {'187': 'Diesel'}}, '192': {'Bolero Pickup': {'192': 'Diesel'}},
                 '195': {'E20 Plus': {'195': 'Diesel'}}, '179': {'Imperio': {'179': 'Diesel'}},
                 '173': {'KUV 100': {'173': 'Petrol', '174': 'Diesel'}},
                 '180': {'Logan': {'180': 'Petrol', '181': 'Diesel'}}, '190': {'Marazzo': {'190': 'Diesel'}},
                 '188': {'Nuvosport': {'188': 'Petrol', '189': 'Diesel'}}, '177': {'Quanto': {'177': 'Diesel'}},
                 '172': {'Scorpio': {'172': 'Diesel'}}, '193': {'Scorpio Getaway': {'193': 'Diesel'}},
                 '186': {'Thar': {'186': 'Diesel'}}, '176': {'TUV 300': {'176': 'Diesel'}},
                 '182': {'Verito': {'182': 'Petrol', '183': 'Diesel'}}, '191': {'Verito Vibe CS': {'191': 'Diesel'}},
                 '184': {'XUV 300': {'184': 'Petrol', '185': 'Diesel'}},
                 '170': {'XUV 500': {'170': 'Petrol', '171': 'Diesel'}}, '175': {'Xylo': {'175': 'Diesel'}}}}, 5: {
    'TATA': {'238': {'Altroz': {'238': 'Petrol', '239': 'Diesel'}},
             '240': {'Aria': {'240': 'Petrol', '241': 'CNG', '242': 'Diesel'}},
             '226': {'Bolt': {'226': 'Petrol', '227': 'CNG', '228': 'Diesel'}},
             '243': {'Harrier': {'243': 'Petrol', '244': 'Diesel'}},
             '245': {'Hexa': {'245': 'Petrol', '246': 'Diesel'}},
             '213': {'Indica': {'213': 'Petrol', '214': 'CNG', '215': 'Diesel'}},
             '235': {'Indica eV2': {'235': 'Petrol', '236': 'CNG', '237': 'Diesel'}},
             '223': {'Indica V2': {'223': 'Petrol', '224': 'CNG', '225': 'Diesel'}},
             '205': {'Indica Vista': {'205': 'Petrol', '206': 'CNG', '207': 'Diesel'}},
             '216': {'Indigo': {'216': 'Petrol', '217': 'CNG', '218': 'Diesel'}},
             '229': {'Indigo CS': {'229': 'Petrol', '230': 'CNG', '231': 'Diesel'}},
             '220': {'Indigo eCS': {'220': 'Petrol', '221': 'CNG', '222': 'Diesel'}},
             '248': {'Indigo Marina': {'248': 'Petrol', '249': 'CNG', '250': 'Diesel'}},
             '254': {'Indigo XL': {'254': 'Petrol', '255': 'CNG', '256': 'Diesel'}},
             '210': {'Manza': {'210': 'Petrol', '211': 'CNG', '212': 'Diesel'}},
             '198': {'Nano': {'198': 'Petrol', '199': 'CNG'}}, '233': {'Nano Genx': {'233': 'Petrol', '234': 'CNG'}},
             '203': {'Nexon': {'203': 'Petrol', '204': 'Diesel'}}, '219': {'Safari': {'219': 'Diesel'}},
             '232': {'Safari Storme': {'232': 'Diesel'}}, '251': {'Sumo Gold': {'251': 'Diesel'}},
             '247': {'Sumo Grande': {'247': 'Diesel'}}, '252': {'Sumo Grande MK II': {'252': 'Diesel'}},
             '257': {'Sumo Spacio': {'257': 'Diesel'}}, '260': {'Sumo Victa': {'260': 'Diesel'}},
             '196': {'Tiago': {'196': 'Petrol', '197': 'Diesel'}}, '208': {'Tigor': {'208': 'Petrol', '209': 'Diesel'}},
             '253': {'Venture': {'253': 'Diesel'}}, '258': {'Winger': {'258': 'Petrol'}},
             '259': {'Xenon': {'259': 'Diesel'}}, '200': {'Zest': {'200': 'Petrol', '201': 'CNG', '202': 'Diesel'}}}},
             6: {'KIA': {'261': {'Carnival': {'261': 'Petrol', '262': 'Diesel'}},
                         '263': {'Seltos': {'263': 'Petrol', '264': 'Diesel'}},
                         '265': {'Sonet': {'265': 'Petrol', '266': 'Diesel'}}}}, 7: {
        'SKODA': {'270': {'Fabia': {'270': 'Petrol', '271': 'CNG', '272': 'Diesel'}},
                  '283': {'Fabia Scout': {'283': 'Petrol', '284': 'CNG', '285': 'Diesel'}},
                  '286': {'Kodiaq': {'286': 'Petrol', '287': 'Diesel'}},
                  '276': {'Laura': {'276': 'Petrol', '277': 'Diesel'}},
                  '278': {'Octavia': {'278': 'Petrol', '279': 'CNG', '280': 'Diesel'}},
                  '267': {'Rapid': {'267': 'Petrol', '268': 'CNG', '269': 'Diesel'}},
                  '273': {'Superb': {'273': 'Petrol', '274': 'CNG', '275': 'Diesel'}},
                  '281': {'Yeti': {'281': 'Petrol', '282': 'Diesel'}}}}, 8: {
        'RENAULT': {'306': {'Captur': {'306': 'Petrol', '307': 'Diesel'}},
                    '291': {'Duster': {'291': 'Petrol', '292': 'Diesel'}},
                    '299': {'Fluence': {'299': 'Petrol', '300': 'CNG', '301': 'Diesel'}},
                    '309': {'Kiger': {'309': 'Petrol'}}, '308': {'Koleos': {'308': 'Diesel'}},
                    '288': {'Kwid': {'288': 'Petrol', '289': 'CNG', '290': 'Diesel'}},
                    '305': {'Lodgy': {'305': 'Diesel'}},
                    '296': {'Pulse': {'296': 'Petrol', '297': 'CNG', '298': 'Diesel'}},
                    '293': {'Scala': {'293': 'Petrol', '294': 'CNG', '295': 'Diesel'}},
                    '302': {'Triber': {'302': 'Petrol', '303': 'CNG', '304': 'Diesel'}}}}, 9: {
        'CHEVROLET': {'318': {'Aveo': {'318': 'Petrol', '319': 'CNG', '320': 'Diesel'}},
                      '310': {'Beat': {'310': 'Petrol', '311': 'CNG', '312': 'Diesel'}},
                      '342': {'Captiva': {'342': 'Diesel'}},
                      '315': {'Cruze': {'315': 'Petrol', '316': 'CNG', '317': 'Diesel'}},
                      '324': {'Enjoy': {'324': 'Petrol', '325': 'CNG', '326': 'Diesel'}},
                      '343': {'Forester': {'343': 'CNG', '344': 'Diesel'}},
                      '330': {'Optra': {'330': 'Petrol', '331': 'CNG', '332': 'Diesel'}},
                      '336': {'Optra Magnum': {'336': 'Petrol', '337': 'CNG', '338': 'Diesel'}},
                      '340': {'Optra SRV': {'340': 'Petrol', '341': 'CNG'}},
                      '321': {'Sail': {'321': 'Petrol', '322': 'CNG', '323': 'Diesel'}},
                      '333': {'Sail Hatchback': {'333': 'Petrol', '334': 'CNG', '335': 'Diesel'}},
                      '313': {'Spark': {'313': 'Petrol', '314': 'CNG'}}, '339': {'Tavera': {'339': 'Diesel'}},
                      '345': {'Trailblazer': {'345': 'Diesel'}},
                      '327': {'UVA': {'327': 'Petrol', '328': 'CNG', '329': 'Diesel'}}}}, 10: {
        'TOYOTA': {'372': {'Camry': {'372': 'Petrol', '373': 'CNG'}},
                   '362': {'Corolla': {'362': 'Petrol', '363': 'CNG', '364': 'Diesel'}},
                   '352': {'Corolla Altis': {'352': 'Petrol', '353': 'CNG', '354': 'Diesel'}},
                   '347': {'Etios': {'347': 'Petrol', '348': 'CNG', '349': 'Diesel'}},
                   '367': {'Etios Cross': {'367': 'Petrol', '368': 'CNG', '369': 'Diesel'}},
                   '355': {'Etios Liva': {'355': 'Petrol', '356': 'CNG', '357': 'Diesel'}},
                   '358': {'Fortuner': {'358': 'Petrol', '359': 'Diesel'}},
                   '374': {'Glanza': {'374': 'Petrol', '375': 'CNG', '376': 'Diesel'}},
                   '350': {'Innova': {'350': 'Petrol', '351': 'Diesel'}},
                   '360': {'Innova Crysta': {'360': 'Petrol', '361': 'Diesel'}},
                   '377': {'Land Cruiser': {'377': 'Diesel'}}, '378': {'Land Cruiser Prado': {'378': 'Diesel'}},
                   '365': {'Qualis': {'365': 'Petrol', '366': 'Diesel'}}, '346': {'Sera': {'346': 'Petrol'}},
                   '379': {'Urban Cruiser': {'379': 'Petrol'}}, '370': {'Yaris': {'370': 'Petrol', '371': 'CNG'}}}},
             11: {'FIAT': {'406': {'Abarth Punto': {'406': 'Petrol', '407': 'Diesel'}},
                           '400': {'Adventure': {'400': 'Petrol', '401': 'CNG', '402': 'Diesel'}},
                           '391': {'Avventura': {'391': 'Petrol', '392': 'CNG', '393': 'Diesel'}},
                           '383': {'Linea': {'383': 'Petrol', '384': 'CNG', '385': 'Diesel'}},
                           '397': {'Linea Classic': {'397': 'Petrol', '398': 'CNG', '399': 'Diesel'}},
                           '388': {'Palio D': {'388': 'Petrol', '389': 'CNG', '390': 'Diesel'}},
                           '403': {'Palio NV': {'403': 'Petrol', '404': 'CNG', '405': 'Diesel'}},
                           '394': {'Palio Stile': {'394': 'Petrol', '395': 'CNG', '396': 'Diesel'}},
                           '413': {'Petra': {'413': 'Petrol', '414': 'CNG', '415': 'Diesel'}},
                           '380': {'Punto': {'380': 'Petrol', '381': 'CNG', '382': 'Diesel'}},
                           '386': {'Punto Evo': {'386': 'Petrol', '387': 'Diesel'}},
                           '410': {'Uno': {'410': 'Petrol', '411': 'CNG', '412': 'Diesel'}},
                           '408': {'Urban Cross': {'408': 'Petrol', '409': 'Diesel'}}}}, 12: {
        'ASTON MARTIN': {'416': {'DB 9': {'416': 'Petrol'}}, '417': {'Rapide': {'417': 'Petrol'}},
                         '418': {'Vanquish': {'418': 'Petrol'}}, '419': {'Vantage': {'419': 'Petrol'}}}}, 13: {
        'AUDI': {'420': {'A3': {'420': 'Diesel', '421': 'Petrol'}}, '422': {'A4': {'422': 'Diesel', '423': 'Petrol'}},
                 '424': {'A5': {'424': 'Diesel', '425': 'Petrol'}}, '426': {'A6': {'426': 'Diesel', '427': 'Petrol'}},
                 '428': {'A7': {'428': 'Diesel', '429': 'Petrol'}}, '430': {'A8': {'430': 'Diesel', '431': 'Petrol'}},
                 '432': {'A8 L': {'432': 'Diesel', '433': 'Petrol'}}, '434': {'Q2': {'434': 'Diesel', '435': 'Petrol'}},
                 '436': {'Q3': {'436': 'Diesel', '437': 'Petrol'}}, '438': {'Q5': {'438': 'Diesel', '439': 'Petrol'}},
                 '440': {'Q7': {'440': 'Diesel', '441': 'Petrol'}}, '442': {'Q8': {'442': 'Petrol'}},
                 '443': {'R8': {'443': 'Petrol'}}, '444': {'RS3': {'444': 'Petrol'}}, '445': {'RS5': {'445': 'Petrol'}},
                 '446': {'S4': {'446': 'Petrol'}}, '447': {'TT': {'447': 'Petrol'}}}}, 14: {
        'BENTLEY': {'448': {'Continental': {'448': 'Petrol'}}, '449': {'Flying Spur': {'449': 'Petrol'}},
                    '450': {'Mulsanne': {'450': 'Petrol'}}}}, 15: {
        'BMW': {'451': {'1 Series': {'451': 'Diesel', '452': 'Petrol'}},
                '453': {'2 Series': {'453': 'Diesel', '454': 'Petrol'}},
                '455': {'3 Series': {'455': 'Diesel', '456': 'Petrol'}},
                '457': {'3 Series GT': {'457': 'Diesel', '458': 'Petrol'}},
                '459': {'5 Series': {'459': 'Diesel', '460': 'Petrol'}},
                '461': {'5 Series GT': {'461': 'Diesel', '462': 'Petrol'}},
                '463': {'6 Series': {'463': 'Diesel', '464': 'Petrol'}},
                '465': {'6 Series GT': {'465': 'Diesel', '466': 'Petrol'}},
                '467': {'7 Series': {'467': 'Diesel', '468': 'Petrol'}}, '469': {'M3': {'469': 'Petrol'}},
                '470': {'M5': {'470': 'Petrol'}}, '471': {'X1': {'471': 'Diesel', '472': 'Petrol'}},
                '473': {'X3': {'473': 'Diesel', '474': 'Petrol'}}, '475': {'X4': {'475': 'Diesel', '476': 'Petrol'}},
                '477': {'X5': {'477': 'Diesel', '478': 'Petrol'}}, '479': {'X6': {'479': 'Diesel', '480': 'Petrol'}},
                '481': {'X7': {'481': 'Diesel', '482': 'Petrol'}}, '483': {'Z4': {'483': 'Petrol'}}}}, 16: {
        'FERRARI': {'485': {'458 Italia': {'485': 'Petrol'}}, '486': {'458 Speciale': {'486': 'Petrol'}},
                    '484': {'488': {'484': 'Petrol'}}, '487': {'California': {'487': 'Petrol'}},
                    '488': {'F12 Berlinetta': {'488': 'Petrol'}}, '489': {'FF': {'489': 'Petrol'}}}}, 17: {
        'JAGUAR': {'490': {'F Pace': {'490': 'Diesel', '491': 'Petrol'}}, '492': {'F Type': {'492': 'Petrol'}},
                   '493': {'XE': {'493': 'Diesel', '494': 'Petrol'}}, '495': {'XF': {'495': 'Diesel', '496': 'Petrol'}},
                   '497': {'XJ': {'497': 'Diesel', '498': 'Petrol'}}, '499': {'XJR': {'499': 'Petrol'}}}}, 18: {
        'LAMBORGHINI': {'500': {'Aventador': {'500': 'Petrol'}}, '501': {'Gallardo': {'501': 'Petrol'}},
                        '502': {'Huracan': {'502': 'Petrol'}}}}, 19: {
        'LEXUS': {'503': {'ES': {'503': 'Petrol'}}, '504': {'LC': {'504': 'Petrol'}}, '505': {'LS': {'505': 'Petrol'}},
                  '506': {'LX': {'506': 'Diesel', '507': 'Petrol'}}, '508': {'NX': {'508': 'Petrol'}},
                  '509': {'RX': {'509': 'Petrol'}}}}, 20: {
        'MASERATI': {'510': {'Ghibli': {'510': 'Diesel', '511': 'Petrol'}},
                     '512': {'GranCabrio': {'512': 'Diesel', '513': 'Petrol'}},
                     '514': {'GranTurismo': {'514': 'Diesel', '515': 'Petrol'}},
                     '516': {'Quattroporte': {'516': 'Diesel', '517': 'Petrol'}}}}, 21: {
        'MERCEDES': {'518': {'A-Class': {'518': 'Diesel', '519': 'Petrol'}}, '520': {'AMG GT': {'520': 'Petrol'}},
                     '521': {'B-Class': {'521': 'Diesel', '522': 'Petrol'}},
                     '523': {'C-Class': {'523': 'Diesel', '524': 'Petrol'}},
                     '525': {'CLA Class': {'525': 'Diesel', '526': 'Petrol'}},
                     '527': {'CLS Class': {'527': 'Diesel', '528': 'Petrol'}},
                     '529': {'E-Class': {'529': 'Diesel', '530': 'Petrol'}},
                     '531': {'G63 AMGr': {'531': 'Diesel', '532': 'Petrol'}},
                     '533': {'GL Class': {'533': 'Diesel', '534': 'Petrol'}},
                     '535': {'GLA Class': {'535': 'Diesel', '536': 'Petrol'}},
                     '537': {'GLC': {'537': 'Diesel', '538': 'Petrol'}}, '539': {'GLE 43 AMG': {'539': 'Petrol'}},
                     '540': {'GLE Class': {'540': 'Diesel', '541': 'Petrol'}},
                     '542': {'GLS': {'542': 'Diesel', '543': 'Petrol'}},
                     '544': {'ML Class': {'544': 'Diesel', '545': 'Petrol'}},
                     '546': {'R Class': {'546': 'Diesel', '547': 'Petrol'}},
                     '548': {'S-Class': {'548': 'Diesel', '549': 'Petrol'}}, '550': {'SL 500 AMG': {'550': 'Petrol'}},
                     '551': {'SLK Class': {'551': 'Petrol'}}, '552': {'V-Class': {'552': 'Diesel'}}}}, 22: {
        'MINI': {'553': {'Clubman': {'553': 'Petrol'}}, '554': {'Cooper': {'554': 'Diesel', '555': 'Petrol'}},
                 '556': {'Countryman': {'556': 'Diesel', '557': 'Petrol'}}}}, 23: {
        'MITSUBISHI': {'558': {'Cedia': {'558': 'Diesel', '559': 'Petrol'}},
                       '560': {'Lancer': {'560': 'Diesel', '561': 'Petrol'}}, '562': {'Montero': {'562': 'Diesel'}},
                       '563': {'Outlander': {'563': 'Diesel', '564': 'Petrol'}}, '565': {'Pajero': {'565': 'Diesel'}},
                       '566': {'Pajero Sport': {'566': 'Diesel'}}}}, 24: {
        'PORSCHE': {'567': {'911': {'567': 'Petrol'}}, '568': {'Boxter': {'568': 'Petrol'}},
                    '569': {'Cayenne': {'569': 'Diesel', '570': 'Petrol'}},
                    '571': {'Cayman': {'571': 'Diesel', '572': 'Petrol'}},
                    '573': {'Macan': {'573': 'Diesel', '574': 'Petrol'}},
                    '575': {'Panamera': {'575': 'Diesel', '576': 'Petrol'}}}}, 25: {
        'VOLVO': {'577': {'S40': {'577': 'Petrol'}}, '578': {'S60': {'578': 'Diesel', '579': 'Petrol'}},
                  '580': {'S60 Cross Country': {'580': 'Diesel', '581': 'Petrol'}},
                  '582': {'S80': {'582': 'Diesel', '583': 'Petrol'}},
                  '584': {'S90': {'584': 'Diesel', '585': 'Petrol'}},
                  '586': {'V40': {'586': 'Diesel', '587': 'Petrol'}},
                  '588': {'V40 Cross Country': {'588': 'Diesel', '589': 'Petrol'}},
                  '590': {'V60': {'590': 'Diesel', '591': 'Petrol'}},
                  '592': {'V90': {'592': 'Diesel', '593': 'Petrol'}},
                  '594': {'XC40': {'594': 'Diesel', '595': 'Petrol'}},
                  '596': {'XC60': {'596': 'Diesel', '597': 'Petrol'}},
                  '598': {'XC90': {'598': 'Diesel', '599': 'Petrol'}}}}, 26: {
        'Volkswagen': {'606': {'Ameo': {'606': 'Petrol', '607': 'Diesel'}}, '619': {'Beetel': {'619': 'Petrol'}},
                       '608': {'Cross polo': {'608': 'Petrol', '609': 'CNG', '610': 'Diesel'}},
                       '611': {'Jetta': {'611': 'Petrol', '612': 'CNG', '613': 'Diesel'}},
                       '614': {'Passat': {'614': 'Petrol', '615': 'CNG', '616': 'Diesel'}},
                       '600': {'Polo': {'600': 'Petrol', '601': 'CNG', '602': 'Diesel'}},
                       '617': {'T-Roc': {'617': 'Petrol', '618': 'Diesel'}}, '620': {'Tiguan': {'620': 'Diesel'}},
                       '603': {'Vento': {'603': 'Petrol', '604': 'CNG', '605': 'Diesel'}}}}, 27: {
        'Ford': {'624': {'Eco sport': {'624': 'Petrol', '625': 'CNG', '626': 'Diesel'}},
                 '639': {'Endeavour': {'639': 'Diesel'}},
                 '646': {'Escort': {'646': 'Petrol', '647': 'CNG', '648': 'Diesel'}},
                 '630': {'Fiesta': {'630': 'Petrol', '631': 'CNG', '632': 'Diesel'}},
                 '633': {'Fiesta Classic': {'633': 'Petrol', '634': 'CNG', '635': 'Diesel'}},
                 '621': {'Figo': {'621': 'Petrol', '622': 'CNG', '623': 'Diesel'}},
                 '627': {'Figo Aspire ': {'627': 'Petrol', '628': 'CNG', '629': 'Diesel'}},
                 '640': {'Free Style': {'640': 'Petrol', '641': 'CNG', '642': 'Diesel'}},
                 '643': {'Fusion': {'643': 'Petrol', '644': 'CNG', '645': 'Diesel'}},
                 '636': {'Ikon': {'636': 'Petrol', '637': 'CNG', '638': 'Diesel'}},
                 '649': {'Mondeo': {'649': 'Petrol', '650': 'CNG', '651': 'Diesel'}}}}}

parsed = {}
for brandnum, branddata in cars_dict.items():
    for brandname, brandinfo in branddata.items():
        info = {}
        for modelnum, modeldata in brandinfo.items():
            for modelname, fueltypes in modeldata.items():
                info[modelnum] = f"{modelname}-{''.join([fuelname[0] for fuelname in list(fueltypes.values())])}"
        parsed[brandnum] = {"name": brandname, "data": info}


def cars_dict_data():
    for i in range(0, len(cars_list)):
        print(f"{i} -> {cars_list[i]}")
        response = session.post("https://www.garage.movemycar.in/fetch-model-new", data={"brand_id": f'{i + 1}'},
                                headers=headers.generate())
        temp = {}
        for option in BeautifulSoup(response.text, 'html.parser').find_all("option")[1:]:
            model_id = option.attrs['value']
            model_name = option.text
            resp = session.post("https://www.garage.movemycar.in/fetch-fuel", data={"model_id": model_id,
                                                                                    "model_name": model_name})
            temp[model_id] = {model_name: resp.json()}
        cars_dict[i + 1] = {cars_list[i]: temp}
        print(temp)
        print("*" * 100)
    print(cars_dict)


def fetch_all():
    total = 7811
    count = 7770
    start = time.time()
    mainlist = []
    for brand_num, brand_data in cars_dict.items():
        for brand_name, models in brand_data.items():
            for model_num, model_data in models.items():
                for model_name, fuel_type in model_data.items():
                    for fuel_num, fuel_name in fuel_type.items():
                        for service_type in services_list:
                            temp = {'brand_num': brand_num, 'brand_name': brand_name, 'model_num': model_num,
                                    'model_name': model_name, 'fuel_num': fuel_num, 'fuel_name': fuel_name,
                                    "service_type": service_type}
                            mainlist.append(temp)
    mainlist = mainlist[7770:]
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    tasks = {executor.submit(get_cars, tempdata) for tempdata in mainlist}
    for task in concurrent.futures.as_completed(tasks):
        result = task.result()
        count += 1
        insert_data(result)
        if count % 10 == 0:
            print(f"Completed: {count} service pages")
            print(f"Speed {count / (time.time() - start)} pages per sec")
            print(f"Total Time Taken: {display_time(time.time() - start)}")
            print(
                f"Estimate time left for {total - count} pages: {display_time(seconds=((total - count) / (count / (time.time() - start))))}")


title = {0: 'Doorstep Accidental Inspection', 1: 'Windshield Replacement(Insurance)', 2: 'Towing(Insurance)',
         3: 'Tyre Replacement(Insurance)', 4: 'Insurance Claim', 5: 'Know Your Policy', 6: 'Basic AC Service',
         7: 'Major AC Service', 8: 'Cooling Coil Replacement', 9: 'Condenser Replacement', 10: 'Compressor Replacement',
         11: 'V-Belt Replacement', 12: 'Radiator Replacement', 13: 'Radiator Flush & Clean', 14: '3M"! Ceramic Coating',
         15: '3M"! Car Rubbing & Polishing', 16: '3M"! Teflon Coating', 17: '3M"! Anti Rust Underbody Coating',
         18: 'Basic Service', 19: 'Normal Service', 20: 'Premium Service', 21: 'Front Brake Discs',
         22: 'Front Brake Pads', 23: 'Rear Brake Shoes', 24: 'Disc Turning', 25: 'Brake Drums Turning',
         26: 'Monsoon Package', 27: 'Car Interior Dry Cleaning', 28: 'Complete car cleaning service',
         29: 'Rat/Pest Repellent Treatment', 30: 'Sunroof Service', 31: 'Avery PPF-Paint Protection Film',
         32: 'Silencer Coating', 33: 'Car Inspection/Diagnostics', 34: 'Complete Car Inspection', 35: 'Engine Scanning',
         36: 'Complete Suspension Inspection', 37: 'Car Fluids Check', 38: 'Front Shock Absorber Replacement',
         39: 'Rear Shock Absorber Replacement', 40: 'Car Waterlog Assistance', 41: 'Car Engine Issues',
         42: 'Problem with Car Brakes & Wheels', 43: 'Clutch & Transmission Troubles',
         44: 'Noises with Car Suspension & Steering', 45: 'Faulty Electricals', 46: 'Damagaed Car Body or Interiors',
         47: 'Front Headlight', 48: 'Rear Taillight', 49: 'Fog Light', 50: 'Front Windshield Replacement',
         51: 'Rear Windshield Replacement', 52: 'Door Glass Replacement', 53: 'CEAT Milaze', 54: 'CEAT Milaze X3',
         55: 'Apollo Amazer 4G Life', 56: 'Apollo Alnac 4Gs', 57: 'MRF ZTX', 58: 'MRF ZLX', 59: 'MRF ZVTV',
         60: 'BRIDGESTONE S248', 61: 'BRIDGESTONE TURANZA AR20', 62: 'Complete Wheel Care', 63: 'Mud Flaps',
         64: 'Amaron(55 Months Warranty)', 65: 'Exide(55 Months Warranty)', 66: 'Livguard(60 Months Warranty)',
         67: 'Livguard(72 Months Warranty)', 68: 'Alternator Replacement', 69: 'Alternator Repair',
         70: 'Battery Jumpstart', 71: 'Front Bumper', 72: 'Bonnet', 73: 'Rear Bumper', 74: 'Boot Paint',
         75: 'Full Body Dent Paint', 76: 'Alloy Paint', 77: 'Left Fender Paint', 78: 'Left Front Door Paint',
         79: 'Left Rear Door Paint', 80: 'Left Quarter Panel Paint', 81: 'Left Running Board Paint',
         82: 'Right Fender Paint', 83: 'Right Front Door Paint', 84: 'Right Rear Door Paint',
         85: 'Right Quarter Panel Paint', 86: 'Right Running Board Paint', 87: 'Engine Decarbonization',
         88: 'Clutch Set Replacement', 89: 'Clutch Bearing Replacement', 90: 'Flywheel Replacement',
         91: 'Clutch Overhaul', 92: 'Front Bumper Replacement', 93: 'Rear Bumper Replacement',
         94: 'Engine Mounting Replacement', 95: 'Gear Box Mounting Replacement', 96: 'Dickey Shocker Replacement',
         97: 'Starter Motor Repair', 98: 'Horn Replacement'}
#title = {v: k for k, v in title.items()}
time = {0: '4 Hours', 1: '1 Day', 2: '2 Hours', 3: '8 Hours', 4: '6 Hours', 5: '3 Days', 6: '24 Hours', 7: '5 Hours',
        8: '3 Hours', 9: '4 Days', 10: 'Work Time Approx 30 Minutes', 11: '20-30 min', 12: '8 Days', 13: '1 Hour',
        14: ''}
#time = {v: k for k, v in time.items()}
amt = {0: '1.00', 1: '2250.00', 2: '3700.00', 3: '4700.00', 4: '4300.00', 5: '20000.00', 6: '650.00', 7: '5000.00',
       8: '900.00', 9: '4290.00', 10: '5300.00', 11: '1700.00', 12: '1800.00', 13: '2000.00', 14: '550.00',
       15: '750.00', 16: '501.00', 17: '1550.00', 18: '2150.00', 19: '1300.00', 20: '55499.00', 21: '1900.00',
       22: '1450.00', 23: '499.00', 24: '700.00', 25: '850.00', 26: '3000.00', 27: '2800.00', 28: '3600.00',
       29: '2200.00', 30: '1600.00', 31: '4000.00', 32: '3500.00', 33: '4413.00', 34: '4750.00', 35: '600.00',
       36: '4099.00', 37: '3200.00', 38: '27000.00', 39: '2500.00', 40: '2400.00', 41: '26500.00', 42: '800.00',
       43: '2875.00', 44: '9200.00', 45: '2700.00', 46: '6000.00', 47: '1850.00', 48: '1750.00', 49: '950.00',
       50: '50499.00', 51: '1400.00', 52: '1150.00', 53: '3050.00', 54: '3465.00', 55: '4437.50', 56: '1050.00',
       57: '1100.00', 58: '1250.00', 59: '450.00', 60: '10000.00', 61: '2100.00', 62: '24000.00', 63: '500.00',
       64: '3450.00', 65: '8000.00', 66: '400.00', 67: '1650.00', 68: '350.00', 69: '2600.00', 70: '1200.00',
       71: '3150.00', 72: '3630.00', 73: '4725.00', 74: '11500.00', 75: '2300.00', 76: '2900.00', 77: '3300.00',
       78: '4265.00', 79: '8400.00', 80: '2450.00', 81: '2650.00', 82: '1500.00', 83: '1350.00', 84: '23000.00',
       85: '3100.00', 86: '15000.00', 87: '11.00', 88: '3400.00', 89: '3350.00', 90: '3850.00', 91: '4955.00',
       92: '3250.00', 93: '16000.00', 94: '25000.00', 95: '3685.00', 96: '4667.50', 97: '8800.00', 98: '8500.00',
       99: '14450.00', 100: '16500.00', 101: '4450.00', 102: '5500.00', 103: '4500.00', 104: '4620.00', 105: '5760.00',
       106: '3750.00', 107: '3800.00', 108: '5100.00', 109: '1950.00', 110: '4100.00', 111: '9250.00', 112: '6100.00',
       113: '4150.00', 114: '4785.00', 115: '52450.00', 116: '2350.00', 117: '9500.00', 118: '2750.00', 119: '14500.00',
       120: '7500.00', 121: '1000.00', 122: '60490.00', 123: '2860.00', 124: '4840.00', 125: '6900.00', 126: '2915.00',
       127: '5070.00', 128: '7350.00', 129: '2550.00', 130: '3520.00', 131: '5530.00', 132: '65499.00', 133: '2050.00',
       134: '19000.00', 135: '21000.00', 136: '4400.00', 137: '0.00', 138: '4250.00', 139: '8200.00', 140: '26000.00',
       141: '7400.00', 142: '20500.00', 143: '5587.50', 144: '7800.00', 145: '4380.00', 146: '24500.00',
       147: '17500.00', 148: '7300.00', 149: '7650.00', 150: '49500.00', 151: '23500.00', 152: '3080.00',
       153: '7000.00', 154: '8650.00', 155: '2585.00', 156: '4552.50', 157: '45499.00', 158: '1960.00', 159: '2530.00',
       160: '300.00', 161: '22500.00', 162: '11000.00', 163: '6500.00', 164: '6800.00', 165: '2970.00', 166: '3135.00',
       167: '5242.50', 168: '15500.00', 169: '7250.00', 170: '2850.00', 171: '2520.00', 172: '2380.00', 173: '17000.00',
       174: '2660.00', 175: '3245.00', 176: '13000.00', 177: '8600.00', 178: '2310.00', 179: '2315.00', 180: '1130.00',
       181: '1830.00', 182: '13500.00', 183: '39999.00', 184: '22000.00', 185: '49999.00', 186: '5875.00',
       187: '6300.00', 188: '6105.00', 189: '7100.00', 190: '6700.00', 191: '6750.00', 192: '4800.00', 193: '6200.00',
       194: '54999.00', 195: '1630.00', 196: '5817.50', 197: '6350.00', 198: '19500.00', 199: '3950.00', 200: '2950.00',
       201: '3960.00', 202: '6335.00', 203: '4600.00', 204: '6850.00', 205: '2615.00', 206: '12500.00', 207: '6160.00',
       208: '8520.00', 209: '6380.00', 210: '8865.00', 211: '13200.00', 212: '4350.00', 213: '18000.00',
       214: '12100.00', 215: '4200.00', 216: '35000.00', 217: '12650.00', 218: '15305.00', 219: '44999.00',
       220: '4015.00', 221: '10475.00', 222: '5990.00', 223: '9000.00', 224: '6600.00', 225: '8250.00', 226: '3900.00',
       227: '8470.00', 228: '10820.00', 229: '8300.00', 230: '69999.00', 231: '4675.00', 232: '6220.00',
       233: '28000.00', 234: '64999.00', 235: '4730.00', 236: '30000.00', 237: '5700.00', 238: '4180.00',
       239: '5645.00', 240: '4510.00', 241: '4070.00', 242: '5600.00', 243: '5150.00', 244: '4950.00', 245: '6450.00',
       246: '4900.00', 247: '6050.00', 248: '32000.00', 249: '29000.00', 250: '6400.00', 251: '5040.00', 252: '4565.00',
       253: '5850.00', 254: '230.00', 255: '5460.00', 256: '55000.00', 257: '5185.00', 258: '5350.00', 259: '39990.00',
       260: '5900.00', 261: '59999.00', 262: '3410.00', 263: '34000.00', 264: '1499.00', 265: '1399.00', 266: '2199.00',
       267: '2999.00', 268: '74999.00', 269: '1999.00', 270: '599.00', 271: '5199.00', 272: '6599.00', 273: '9999.00',
       274: '3099.00', 275: '3499.00', 276: '999.00', 277: '1199.00', 278: '899.00', 279: '5050.00', 280: '559.00',
       281: '2399.00', 282: '6499.00', 283: '7999.00', 284: '1703.00', 285: '11744.00', 286: '799.00', 287: '699.00',
       288: '24999.00', 289: '4999.00', 290: '6488.00', 291: '14990.00', 292: '13990.00', 293: '14000.00',
       294: '1449.00', 295: '18499.00', 296: '2499.00', 297: '15800.00', 298: '14220.00', 299: '30788.00',
       300: '19399.00', 301: '11700.00', 302: '3199.00', 303: '4299.00', 304: '5499.00', 305: '2599.00', 306: '2899.00',
       307: '1099.00', 308: '3999.00', 309: '1564.00', 310: '1299.00', 311: '17999.00', 312: '5699.00', 313: '8999.00',
       314: '10999.00', 315: '8379.00', 316: '9299.00', 317: '5200.00', 318: '4599.00', 319: '6299.00', 320: '7050.00',
       321: '7575.00', 322: '7200.00', 323: '10500.00', 324: '649.00', 325: '5599.00', 326: '3299.00', 327: '5899.00',
       328: '4199.00', 329: '7699.00', 330: '2299.00', 331: '6899.00', 332: '4790.00', 333: '1048.00', 334: '5800.00',
       335: '3599.00', 336: '1699.00', 337: '15600.00', 338: '9700.00', 339: '3760.00', 340: '1385.00', 341: '5400.00',
       342: '1599.00', 343: '4549.00', 344: '4899.00', 345: '14099.00', 346: '5799.00', 347: '14999.00', 348: '5399.00',
       349: '8399.00', 350: '1899.00', 351: '13900.00', 352: '2699.00', 353: '3799.00', 354: '4499.00', 355: '9199.00',
       356: '13999.00', 357: '5299.00', 358: '7599.00', 359: '1799.00', 360: '2099.00', 361: '22900.00', 362: '3699.00',
       363: '4650.00', 364: '1049.00', 365: '6399.00', 366: '1588.00', 367: '15300.00', 368: '3650.00', 369: '11999.00',
       370: '22099.00', 371: '10599.00', 372: '6099.00', 373: '6799.00', 374: '5099.00', 375: '4788.00',
       376: '35999.00', 377: '21999.00', 378: '16999.00', 379: '22999.00', 380: '6199.00', 381: '4699.00',
       382: '7799.00', 383: '9100.00', 384: '1249.00', 385: '7499.00', 386: '18099.00', 387: '12099.00', 388: '5999.00',
       389: '11499.00', 390: '7700.00', 391: '15099.00', 392: '9599.00', 393: '6699.00', 394: '3683.00', 395: '7199.00',
       396: '2590.00', 397: '12999.00', 398: '1560.00', 399: '29500.00', 400: '11099.00', 401: '7899.00',
       402: '9600.00', 403: '8799.00', 404: '1596.00', 405: '11043.00', 406: '2240.00', 407: '5857.00', 408: '4631.00',
       409: '6190.00', 410: '15345.00', 411: '18999.00', 412: '7550.00', 413: '7600.00', 414: '1248.00', 415: '9349.00',
       416: '6999.00', 417: '8299.00', 418: '14800.00', 419: '18200.00', 420: '10900.00', 421: '99.00', 422: '659.00',
       423: '13600.00', 424: '14200.00', 425: '38000.00', 426: '18400.00', 427: '12300.00', 428: '3788.00',
       429: '14400.00', 430: '30800.00', 431: '10099.00', 432: '16900.00', 433: '1826.00', 434: '1549.00',
       435: '8099.00', 436: '13800.00', 437: '8199.00', 438: '4399.00', 439: '5775.00', 440: '3899.00', 441: '8599.00',
       442: '26900.00', 443: '9400.00', 444: '3990.00', 445: '9800.00', 446: '11841.00', 447: '18500.00',
       448: '12000.00', 449: '11800.00', 450: '12600.00', 451: '9499.00', 452: '23999.00', 453: '25400.00',
       454: '8700.00', 455: '4799.00', 456: '2799.00', 457: '29999.00', 458: '19900.00', 459: '17900.00',
       460: '8499.00', 461: '16899.00', 462: '12700.00', 463: '12900.00', 464: '3399.00', 465: '2181.00',
       466: '27500.00', 467: '5250.00', 468: '11400.00', 469: '21500.00', 470: '7900.00', 471: '13599.00',
       472: '4850.00', 473: '1240.00', 474: '1610.00', 475: '9099.00', 476: '3550.00', 477: '13899.00', 478: '551.00',
       479: '14900.00', 480: '7299.00', 481: '10866.00', 482: '31500.00', 483: '8100.00', 484: '3311.00',
       485: '3695.00', 486: '12200.00', 487: '31600.00', 488: '24900.00', 489: '9900.00', 490: '33700.00',
       491: '30999.00', 492: '10600.00', 493: '15900.00', 494: '19999.00', 495: '43999.00', 496: '12400.00',
       497: '10499.00', 498: '19700.00', 499: '10799.00', 500: '7399.00', 501: '33200.00', 502: '2011.00',
       503: '33000.00', 504: '1202.00', 505: '1470.00', 506: '9300.00', 507: '18700.00', 508: '4535.00', 509: '3010.00',
       510: '14100.00', 511: '20100.00', 512: '11100.00', 513: '39000.00', 514: '27300.00', 515: '4025.00',
       516: '30200.00', 517: '8900.00', 518: '25800.00', 519: '53000.00', 520: '1948.00', 521: '40000.00',
       522: '37400.00', 523: '16200.00', 524: '18900.00', 525: '10300.00', 526: '24800.00', 527: '2502.00',
       528: '3798.00', 529: '4050.00', 530: '22700.00', 531: '2762.00', 532: '30700.00', 533: '19300.00',
       534: '30300.00', 535: '29700.00', 536: '1211.00', 537: '10200.00', 538: '79999.00', 539: '31000.00',
       540: '5750.00', 541: '21900.00', 542: '27900.00', 543: '44500.00', 544: '2595.00', 545: '1290.00',
       546: '1521.00', 547: '6570.00', 548: '6548.00', 549: '31100.00', 550: '19100.00', 551: '10400.00',
       552: '14600.00', 553: '7099.00', 554: '11300.00', 555: '4490.00', 556: '13300.00', 557: '48999.00',
       558: '79500.00', 559: '219000.00', 560: '196000.00', 561: '353000.00', 562: '248000.00', 563: '27800.00',
       564: '125000.00', 565: '110000.00', 566: '45000.00', 567: '16800.00', 568: '17300.00', 569: '25500.00',
       570: '36000.00', 571: '41000.00', 572: '16100.00', 573: '42000.00', 574: '40500.00', 575: '58000.00',
       576: '42500.00', 577: '17100.00', 578: '126000.00', 579: '15400.00', 580: '11200.00', 581: '46000.00',
       582: '43400.00', 583: '64000.00', 584: '10100.00', 585: '44000.00', 586: '51500.00', 587: '45500.00',
       588: '127000.00', 589: '43000.00', 590: '56000.00', 591: '19400.00', 592: '27400.00', 593: '266000.00',
       594: '52100.00', 595: '56900.00', 596: '53500.00', 597: '49000.00', 598: '35400.00', 599: '276000.00',
       600: '102000.00', 601: '59000.00', 602: '64500.00', 603: '27600.00', 604: '59600.00', 605: '40100.00',
       606: '39500.00', 607: '65000.00', 608: '36500.00', 609: '42100.00', 610: '117000.00', 611: '46500.00',
       612: '43900.00', 613: '13100.00', 614: '19600.00', 615: '41500.00', 616: '57500.00', 617: '95000.00',
       618: '85500.00', 619: '134000.00', 620: '60000.00', 621: '75500.00', 622: '71500.00', 623: '27200.00',
       624: '52000.00', 625: '57000.00', 626: '87000.00', 627: '30500.00', 628: '111000.00', 629: '352000.00',
       630: '119000.00', 631: '139000.00', 632: '132000.00', 633: '37000.00', 634: '15999.00', 635: '143000.00',
       636: '136000.00', 637: '77000.00', 638: '24600.00', 639: '70000.00', 640: '47500.00', 641: '45100.00',
       642: '48000.00', 643: '88000.00', 644: '129650.00', 645: '40999.00', 646: '17800.00', 647: '133000.00',
       648: '50500.00', 649: '47600.00', 650: '52500.00', 651: '28200.00', 652: '19200.00', 653: '176000.00',
       654: '62000.00', 655: '72000.00', 656: '68000.00', 657: '68500.00', 658: '61500.00', 659: '17099.00',
       660: '28500.00', 661: '185000.00', 662: '130000.00', 663: '73000.00', 664: '65500.00', 665: '28999.00',
       666: '74000.00', 667: '67000.00', 668: '131000.00', 669: '32200.00', 670: '17600.00', 671: '54500.00',
       672: '154000.00', 673: '90100.00', 674: '44900.00', 675: '42400.00', 676: '32300.00', 677: '80999.00',
       678: '34999.00', 679: '52900.00', 680: '46900.00', 681: '54000.00', 682: '48500.00', 683: '96800.00',
       684: '48900.00', 685: '56500.00', 686: '19099.00', 687: '23099.00', 688: '20700.00', 689: '16300.00',
       690: '126600.00', 691: '67500.00', 692: '60500.00', 693: '23100.00', 694: '63500.00', 695: '63000.00',
       696: '40200.00', 697: '79000.00', 698: '71000.00', 699: '146000.00', 700: '147000.00', 701: '165000.00',
       702: '156000.00', 703: '20200.00', 704: '124000.00', 705: '152000.00', 706: '10350.00', 707: '123000.00',
       708: '50000.00', 709: '75000.00', 710: '214000.00', 711: '51000.00', 712: '93500.00', 713: '90000.00',
       714: '97000.00', 715: '28400.00', 716: '142000.00', 717: '58500.00', 718: '247000.00', 719: '17200.00',
       720: '25999.00', 721: '26999.00', 722: '32500.00', 723: '5175.00', 724: '101000.00', 725: '209000.00',
       726: '198000.00', 727: '91000.00', 728: '47000.00', 729: '137000.00', 730: '69000.00', 731: '118000.00',
       732: '61000.00', 733: '10800.00', 734: '11600.00', 735: '89000.00', 736: '112000.00', 737: '59500.00',
       738: '99000.00', 739: '96000.00', 740: '86000.00', 741: '252000.00', 742: '101500.00', 743: '98000.00',
       744: '93000.00', 745: '182000.00', 746: '85000.00', 747: '81000.00', 748: '14700.00', 749: '1980.00',
       750: '180000.00', 751: '171000.00', 752: '80000.00', 753: '35500.00', 754: '960000.00', 755: '38500.00',
       756: '177000.00', 757: '92000.00', 758: '13400.00', 759: '24200.00', 760: '277000.00', 761: '103000.00',
       762: '37500.00', 763: '100000.00', 764: '20099.00', 765: '83000.00', 766: '11299.00', 767: '568.00',
       768: '17700.00', 769: '7892.00', 770: '3155.00', 771: '4571.00', 772: '10700.00', 773: '36900.00',
       774: '2751.00', 775: '3280.00', 776: '64900.00', 777: '20800.00', 778: '21200.00', 779: '8111.00',
       780: '2410.00', 781: '2116.00', 782: '5027.00', 783: '25900.00', 784: '12944.00', 785: '25700.00'}
dict_desc = {0: ['25 points checklist', 'Insurance claim guidance', 'Body damage inspection', 'Policy inspection'],
             1: ['Insured cashless service', 'Doorstep available', 'Claim intimation', 'Surveyors estimate approval',
                 'Co-ordination with insurance company'],
             2: ['Free towing', 'Cashless facility', 'Real time claim tracking mechanism', 'Claim intimation',
                 'Towing reimbursement'],
             3: ['Genuine tyres', 'Cashless facility', 'Real time claim tracking mechanism', 'Genuine tyres',
                 'Claim intimation'],
             4: ['Free pick up & drop', 'Dedicated service buddy', 'Real time claim tracking', 'Cashless facility',
                 'Work status updates on whatsapp'],
             5: ['Call within 2 hours', 'Regarding doubts with claim intimation',
                 'Complete information about your policy', 'Expenditure assessment',
                 'Suggestion on purchase of new policy'],
             6: ['Includes 5 services', 'AC gas top-up', 'Condenser cleaning', 'AC filter cleaning',
                 'AC vent cleaning'],
             7: ['9 services included', 'AC gas replacement(upto 600 grams)', 'Dashboard removing refitting',
                 'Compressor oil topup (upto 200 ml)', 'Cooling coil cleaning(front +rear)'],
             8: ['Spare part price only', 'Better air recirculation', 'Cooling coil replacement(OES)',
                 'Spare part cost only', 'AC pipe,expansion valve,sensors additional'],
             9: ['Spare part price only', 'Condenser replacement(OES)', 'AC pipe,expansion valve,sensors additional',
                 'AC gas,compressor oil additional', 'Free pickup & drop'],
             10: ['FREE AC SERVICE', 'Spare part price only', 'Ccompressor replacement(OES)', 'Spare part cost only',
                  'AC pipe,expansion valve,sensors additional'],
             11: ['Prevents vehicle breakdown', 'V-belt replacement(OES)', 'Opening & fitting of V-belt',
                  'Pulleys,bearing,timing additional', 'Scanning additional'],
             12: ['Spare part price only', 'Prevents engine overheating', 'Radiator replacement(OES)',
                  'Spare part cost only', 'Radiator hoses,thermostart valves,additional'],
             13: ['Prevents engine over heating', 'Coolant draining', 'Radiator flushing',
                  'Anti-freeze coolant replacement', 'Radiator cleaning'],
             14: ['FREE ALL ROUND CLEANING', 'Complete paint correction', 'Complete paint correction',
                  '3M"! 9H nano coating', '3 layers of coating'],
             15: ['Pressure washing', 'Rubbing with 3M"! Compound', '3M"! wax polishing', 'Machine rubbing',
                  'Tyre dressing & alloy polishing'],
             16: ['Full body 3M"! teflon paint protection coating', 'Pre-coating rubbing & polishing',
                  '3M"! Exterior anti-rust treatment'],
             17: ['Monsoon special', '3M"! underbody teflon coating', '3M"! protective anti-corrosion treatment',
                  'Insulation & rust protection'],
             18: ['Engine oil replacement', 'Oil filter replacement', 'Air filter cleaning', 'Coolant top up',
                  'Wiper fluid replacement'],
             19: ['Engine oil replacement', 'Oil filter replacement', 'Air filter replacement', 'Fuel filter checking',
                  'Cabin filter/ac filter cleaning'],
             20: ['Engine oil replacement', 'Oil filter replacement', 'Air filter replacement', 'Fuel filter checking',
                  'Cabin filter/ac filter replacement'],
             21: ['Complete braking safety', 'Corrosion resistance', 'Materail + labor included',
                  'Front brake disc replacement(singlr oes unit)', 'Opening & fitting of front brake disc'],
             22: ['Opening & fitting of brakes', 'Front brake pads replacement(oes)', 'Front brake disc cleaning'],
             23: ['Materail + labor included', 'Opening & fitting of brakes', 'Rear brake shoes replacement(oes)',
                  'Rear brake disc cleaning'], 24: ['Labour rates only', 'Spare part charges will be extra',
                                                    'Opening & fitting +inspection of below items',
                                                    'Resurfacing of brake discs/rotors',
                                                    'Applicable for set of 2 discs'],
             25: ['Improves brake efficiency', 'Spare part charges will be extra', 'Brake drums turning',
                  'Opening & fitting of brake drums', 'Refacing of brake drums'],
             26: ['Free pickup & drop', 'Protects car wiring from pests', 'Anti dust underbody coating',
                  'Rat/pest repellent treatment & car interior spa', 'Under body anti-corrosion treatment'],
             27: ['Interior wet cleaning', 'Interior shampooing', 'Fix and loose carpet cleaning',
                  'Anti viral & bacterial treatment', 'Interior vacuum cleaning'],
             28: ['Dry cleaning included', 'Interior vacuum cleaning', 'Dashboard polishing',
                  'Interior wet shampooing and detailing', 'Pressure washing'],
             29: ['Protects car from pests', 'Rat repellent treatment', 'Sprayed on underbody and engine bay',
                  'Protects car wiring from pests', 'Prevents pest breeding inside car'],
             30: ['Roof opening+refitting', 'Sunroof lubrication', 'Drainage tube clog/debris removal',
                  'Sunroof cleaning'],
             31: ['Ultra shine polish', 'Complete paint correction', 'Avery PPF-paint protection film',
                  'Protects OEM paint', 'Strain & fade resistance'],
             32: ['2 layers of protection', 'Silencer anti rust coating', 'Silencer corrosion protection',
                  '2 layers of protection'],
             33: ['Test drive inspection', '25 points checklist', 'Upfront estimate', 'Underbody inspection',
                  '25 points checklist'],
             34: ['50% Points checkup', 'Upfront genuine estimate', 'Available at doorstep', 'Takes only 30 minutes'],
             35: ['OEM scanning', 'Code reset', 'Scanner report provided', 'Electrical scanning',
                  'Error code deletion'],
             36: ['25 points check', 'Upfront estimate', 'Front shocker check', 'Rear shocker check',
                  'Shocker mount check'],
             37: ['Free pickup included', 'Brake fluid check', 'Coolant check', 'Engine oil check',
                  'Power steering oil check'],
             38: ['Reduces suspension noise', 'Shocker strut/damper OES replacement(single unit)',
                  'Opening & fitting of front shock absorber', 'Shocker mount,shocker coil spring additional charges'],
             39: [],
             40: ['Headlight OES(price for single unit)', 'Opening& fitting of bumper/headlight', 'Free pickup & drop',
                  'Projector/LEDs/DRLs Additional(if applicable)'],
             41: ['Taillight OES(price for single unit)', 'Opening& fitting of tailight', 'Free pickup & drop',
                  'Bulbs/LEDs Additional(if applicable)', 'Taillight price will differ from car model to model'],
             42: ['Fog light assembly replacement( single unit)', 'Opening& fitting of bumper+ fog lamp',
                  'Free pickup & drop', 'Projector/LEDs/DRLs Additional(if applicable)',
                  'Switch/ harness wiring check'],
             43: ['Windshield(AIS Approved)', 'Opening & fitting of new windshield',
                  'Consumables-sealant/bond/adhesive', 'Free pickup & drop',
                  'Sensor chargesadditional( if applicable)'],
             44: ['Windshield(AIS Approved)', 'Opening & fitting of new windshield',
                  'Consumables-sealant/bond/adhesive', 'Free pickup & drop',
                  'Defogger charges additional (if applicable)'],
             45: ['Door glass(AIS Approved)', 'Opening & fitting of new door glass', 'Consumables-bond/adhesive',
                  'Free pickup & drop', 'UV glass charges additional (if applicable)'],
             46: ['Tubeless', '2 years warranty', '165/80 R14 85S', 'Free pickup & drop',
                  'Tyre replacement at service center'],
             47: ['Tubeless', '185/65 R15', '4970 rs', 'Free pickup & drop', 'Tyre replacement at service center'],
             48: ['Tubeless', '165/65 R15 88T', 'Free pickup & drop', 'Tyre replacement at service center',
                  'Tyre inspection for tread'],
             49: ['Tubeless', '165/65 R15 88H', 'Free pickup & drop', 'Tyre replacement at service center',
                  'Tyre inspection for tread'],
             50: ['Tubeless', '165/80 R14 85 TL', 'Free pickup & drop', 'Tyre replacement at service center',
                  'Tyre inspection for tread'],
             51: ['Tubeless', '165/80 R14 TL', 'Free pickup & drop', 'Tyre replacement at service center',
                  'Tyre inspection for tread'],
             52: ['Tubeless', '165/65 R14 88TL', 'Free pickup & drop', 'Tyre replacement at service center',
                  'Tyre inspection for tread'],
             53: ['Tubeless', '165/80 R14 81S', 'Free pickup & drop', 'Tyre replacement at service center',
                  'Tyre inspection for tread'],
             54: ['Tubeless', '185/65 R15 88V', 'Free pickup & drop', 'Tyre replacement at service center',
                  'Tyre inspection for tread'],
             55: ['Alignment & balancing', 'Automated wheel balancing', 'Weight correction',
                  'Wheel rigidity inspection', 'Alloy weights additional'],
             56: ['Ehanced durability', 'Excellent durability', 'Mud flaps set of 4', 'Prevents soil accumulation',
                  'Protects car underbody'],
             57: ['Free pickup and drop', 'Free installation', 'Existing battery replacement', 'Available at doorstep'],
             58: ['Improves battery life', 'Alternator replacement', 'Opening & fitting of alternator',
                  'Alternator belt additional', 'Free pickup & drop'],
             59: ['Improves battery life', 'Alternator repair', 'Opening & fitting of alternator',
                  'Alternator belt additional', 'Free pickup & drop'],
             60: ['Available at Doorstep', 'Takes 20-30 minutes', 'Battery checkup'],
             61: ['100% color match', 'Grade a primer', 'Premium DuPont paint', '4 layers of painting',
                  'Panel rubbing polishing'],
             62: ['Alloy preservation', 'Price for 1 tyre only', '100% color match', 'Grade a primer',
                  'High temperature paint'],
             63: ['Increase Mileage Upto 5km', 'Increase engine life span', 'Improve vehicle performance',
                  'Decrease engine noise and vibration', 'Reduce black smoke'],
             64: ['CLUTCH SET REPLACEMENT', 'Free 50 point inspection', 'Labor + spare part rates',
                  'Clutch set OES(CLUCTH set + pressure plate) replace', 'Opening & fitting of clutch set'],
             65: ['Improve gear shifting', 'Spare part price only', 'Clutch bearing OES replacement',
                  'Clutch cable/wire,release bearing/clutch cylinder', 'Flywheel,slave cylinder in add ons,clutch set'],
             66: ['Improves performance', 'Spare part price only', 'Flywheel OES replacement',
                  'Clutch cable/wire,release bearing/clutch cylinder', 'Flywheel,slave cylinder in add ons,clutch set'],
             67: ['Labor rates only', 'Spare part charges will be extra',
                  'Opening & fitting+ inspection of below items', 'Clutch plate', 'Pressure plate'],
             68: ['Bumper spare price only', 'Genuine spare parts', 'Opening & fitting of front bumper',
                  'Front bumper replacement(black color)', 'Freee pickup & drop'],
             69: ['Bumper spare price only', 'Genuine spare parts', 'Opening & fitting of rear bumper',
                  'Rear bumper replacement(black color)', 'Freee pickup & drop'],
             70: ['Prevents engine damage', 'Spare part price only', 'Engine mounting replacement(OES)',
                  'Single unit only', 'Free pickup & drop'],
             71: ['Prevents engine damage', 'Spare part price only', 'Gear box mounting replacement(OES)',
                  'Single unit only', 'Free pickup & drop'],
             72: ['Dickey shocker OES replacement(Set of 2)', 'Opening & fitting of dickey shocker',
                  'Boot/trunk hinges additional', 'Free pickup & drop'],
             73: ['Starter Motor Repair', 'Opening & Fitting of starter motor', 'Free Pickup & Delivery',
                  'Armature Additional if required'],
             74: ['Enhanced durability', 'Mud flaps set of 4', 'Prevents soil accumulation', 'Protects car underbody',
                  'Easy fitment'], 75: ['Frequency=450 hz', 'Sound intensity=90-110 db', 'Opening & fitting of bumper',
                                        'Horn replacement(set of 2)', 'Relay/couple faults check'],
             76: ['Reduces suspension noise', 'Free pickup & drop', 'Shocker strut/damper OES replacement(single unit)',
                  'Opening & fitting of front shock absorber', 'Shocker mount,shocker coil spring additional charges']}

imgs = {0: 'packages/57-doorstep-accidental-inspection.jpg', 1: 'packages/58-windshield-replacement-insurance.jpg',
        2: 'packages/59-towing-insurance.png', 3: 'packages/60-tyre-replacement-insurance.jpg',
        4: 'packages/61-insurance-claim.jpg', 5: 'packages/62-know-your-policy.jpg',
        6: 'packages/41-regular-ac-service.jpg', 7: 'packages/42-high-performance-ac-service.jpg',
        8: 'packages/43-cooling-coil-replacement.jpg', 9: 'packages/44-condenser-replacement.jpg',
        10: 'packages/45-compressor-replacement.jpg', 11: 'packages/46-v-belt-replacement.jpg',
        12: 'packages/47-radiator-replacement.jpeg', 13: 'packages/48-radiator-flush-clean.jpeg',
        14: 'packages/63-3m-ceramic-coating.jpg', 15: 'packages/64-3m-car-rubbing-polishing.jpg',
        16: 'packages/65-3m-teflon-coating.jpg', 17: 'packages/66-3manti-rust-underbody-coating.jpg',
        18: 'packages/basic_service.jpg', 19: 'packages/standard_service.jpg', 20: 'packages/comprehensive_service.jpg',
        21: 'packages/5-ford-brake-discs.jpg', 22: 'packages/6-ford-brake-pads.jpg',
        23: 'packages/7-rear-brake-shoes.jpg', 24: 'packages/8-disc-turning.jpg',
        25: 'packages/9-brake-drums-turning.jpg', 26: 'packages/32-monsoon-package.jpg',
        27: 'packages/34-car-interior-spa.jpg', 28: 'packages/35-deep-all-round-spa.jpeg',
        29: 'packages/36-rat-pest-repellent-treatment.jpg', 30: 'packages/37-sunroof-service.jpg',
        31: 'packages/38-avery-ppf-paint-protection-film.jpg', 32: 'packages/39-silencer-coating.jpg',
        33: 'packages/40-car-inspection-diagnostics.jpg', 34: 'scanning.jpg', 35: 'packages/71-engine-scanning.jpg',
        36: 'packages/72-complete-suspension-inspection.jpg', 37: 'packages/73-car-fluids-check.jpg',
        38: 'packages/78-radiator-replacement.jpg', 39: 'packages/79-radiator-flush-clean.jpg',
        40: 'packages/80-front-shock-absorber-replacement.jpg', 41: 'packages/81-rear-shock-absorber-replacement.jpg',
        42: 'packages/82-car-waterlog-assistance.jpg', 43: 'packages/83-car-engine-issues.jpg',
        44: 'packages/84-problem-with-car-brakes-wheels.jpg', 45: 'packages/85-clutch-and-transmission-troubles.jpg',
        46: 'packages/86-noises-with-car-suspension-and-steering.jpg', 47: 'packages/87-faulty-electricals.jpg',
        48: 'packages/88-damaged-car-body-or-interiors.jpg', 49: 'packages/90-front-windshield-replacement.jpg', 50: '',
        51: 'packages/92-door-glass-replacement.jpg', 52: 'packages/ceat_milaze.png', 53: 'packages/ceat_milaze_x3.png',
        54: 'packages/50-apollo-alnac-4gs.jpg', 55: 'packages/apollo_alnac_4gs.png', 56: 'packages/mrf_ztx.png',
        57: 'packages/mrf-165-80-r14-tl.jpeg', 58: 'packages/51-mrf-zvtv.jpg', 59: 'packages/bridgestone-s248.png',
        60: 'packages/bridgestone-turanza-ar20.jpg', 61: 'packages/55-complete-wheel-care.jpg',
        62: 'packages/56-mud-flaps.jpeg', 63: 'packages/26-amaron-55-months-warranty.png',
        64: 'packages/26-exide-55-months-warranty.jpg', 65: 'packages/27-livguard-60-months-warranty.jpg',
        66: 'packages/29-livguard-72-months-warranty.jpg', 67: 'packages/30-alternator-replacement.jpg',
        68: 'packages/31-alternator-repair.png', 69: 'batteries31.jpg', 70: 'packages/10-front-bumper.jpg',
        71: 'packages/11-bonnet.jpg', 72: 'packages/12-rear-bumper.jpg', 73: 'packages/13-boot-paint.jpg',
        74: 'packages/14-full-body-dent-paint.png', 75: 'packages/15-alloy-paint.jpg',
        76: 'packages/16-left-fender-paint.png', 77: 'packages/17-left-front-door-paint.jpg',
        78: 'packages/18-left-rear-door-paint.jpg', 79: 'packages/19-left-quarter-panel-paint.jpg',
        80: 'packages/20-left-running-board-paint.png', 81: 'packages/21-right-fender-paint.jpg',
        82: 'packages/22-right-front-door-paint.jpg', 83: 'packages/23-right-rear-door-paint.png',
        84: 'packages/24-right-quarter-panel -paint.jpg', 85: 'packages/25-right-running-board-paint.jpg',
        86: 'decarbonization.jpeg', 87: 'packages/74-clutch-set-replacement.jpg',
        88: 'packages/75-clutch-bearing-replacement.jpg', 89: 'packages/76-flywheel-replacement.jpg',
        90: 'packages/77-clutch-overhaul.jpg', 91: 'packages/103-front-bumper-replacement.jpg',
        92: 'packages/104-rear-bumper-replacement.jpg', 93: 'packages/105-engine-mounting-replacement.jpg',
        94: 'packages/106-gear-box-mounting-replacement.jpg', 95: 'packages/107-mud-flaps.jpg',
        96: 'packages/108-horn-replacement.jpg', 97: 'packages/109-front-shock-absorber-replacement.png'}
service_category = {0: 'Accidental Repairs', 1: 'Know Your Policy', 2: 'Service Packages', 3: 'AC Fitments',
                    4: 'Radiator', 5: '3M Services', 6: 'Scheduled Packages', 7: 'Brake Maintenance',
                    8: 'Revival Package', 9: 'Spa', 10: 'Coating', 11: 'Inspection', 12: 'Inspections',
                    13: 'Suspension', 14: 'Custom Services', 15: 'Used Car', 16: 'Glasses', 17: 'Custom Issues',
                    18: 'CEAT', 19: 'Apollo', 20: 'MRF', 21: 'Bridgestone', 22: 'Wheel Care Services', 23: 'Amaron',
                    24: 'Exide', 25: 'Livguard', 26: 'Alternator', 27: 'Jumpstart', 28: 'Front Side', 29: 'Rear Side',
                    30: 'Whole Body', 31: 'Left Side', 32: 'Right Side', 33: 'Engine Decarbonization', 34: 'Fitments',
                    35: 'Stereos'}

#amt = {v: k for k, v in amt.items()}
#dict_desc = {str(v): k for k, v in dict_desc.items()}
#imgs = {v: k for k, v in imgs.items()}
#service_category = {v: k for k, v in service_category.items()}

services_list = ['Periodic Services', 'Denting And Painting', 'Batteries', 'Car Spa And Cleaning',
                'AC Service And Repair', 'Tyres And Wheels', 'Accidental Car Repair', 'Detailing Services',
                'Custom Services', 'Windshield And Glass', 'Lights And Fitments', 'Engine Decarbonization']

encoded_list = ['periodic-services', 'denting-and-painting', 'batteries', 'car-spa-and-cleaning',
                'ac-service-and-repair', 'tyres-and-wheels', 'accidental-car-repair', 'detailing-services',
                'custom-services', 'windshield-and-glass', 'lights-and-fitments', 'engine-decarbonization']
data_dict={"cars_info":parsed,"service_title":title,"desc":dict_desc,"timevalue":time,"imgs":imgs,"amt":amt,
           "service_category":service_category,"services_list":services_list,"encoded_list":encoded_list}
json.dump(fp=open(f"{BASE_DIR}/data_raw.json","w"),obj=data_dict)
exit()
def fetchinfo():
    conection_ = sqlite3.connect("{}/garage.db".format(BASE_DIR))
    conection_.row_factory = sqlite3.Row
    c = conection_.cursor()
    tempdataframe = {}
    temp_new = {}
    print(temp_new)
    count = 0
    for temp in c.execute("SELECT * FROM garage").fetchall():
        fuel_id = f"{temp['fuel_num']}-{listdict[temp['service_type']]}"
        category = f"{service_category[temp['service_cat']]}"
        if fuel_id not in tempdataframe:
            tempdataframe[fuel_id] = {}
        if category not in tempdataframe[fuel_id]:
            tempdataframe[fuel_id][category] = []
        try:
            temp_new = {"title": title[re.sub(r'[^A-Za-z0-9 /"&!()-]+', '', temp['title'])],
                        "time": time[temp['time']],
                        "amount": amt[temp['amount']], "desc": dict_desc[temp['desc'].replace(r'\x00', "")],
                        "img": imgs[temp['imgurl'].replace("/admin/public/assets/uploads/", "")]}
            print(count)
            count += 1
        except Exception as error:

            print(error)
            print(temp['desc'].replace(r'\x00', ""))
            print(dict(temp))
        tempdataframe[fuel_id][category].append(temp_new)
    mainlist = [{"fuel_id": k, "data": v} for k, v in tempdataframe.items()]
    df = pd.DataFrame(mainlist)
    df.to_excel('{}/sqlitedata.xlsx'.format(BASE_DIR),
                header=['fuel_id', "data"],
                index=False)



#fetchinfo()

# print({k: v for k, v in enumerate(imgs.split("\n"))})
# dd = {k: v for k, v in enumerate(a.split("\n"))}
# print({k:eval(a) for k,a in enumerate(abcd.split("\n"))})
# print(dd)
# fetch_all()
# fetchinfo()
# print(json.dumps(get_cars("lights-and-fitments", "ford", "fusion", "petrol"),indent=4))
