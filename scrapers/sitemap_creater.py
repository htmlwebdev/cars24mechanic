import datetime
import json
import os
import re
import xml.etree.cElementTree as ET
from datetime import datetime
import unicodedata
from lxml import etree
from pytz import timezone

BASE_DIR = os.path.dirname((os.path.abspath(__file__))).replace("\\", "/")


def prettyPrintXml(xmlFilePathToPrettyPrint):
    assert xmlFilePathToPrettyPrint is not None
    parser = etree.XMLParser(resolve_entities=False, strip_cdata=False)
    document = etree.parse(xmlFilePathToPrettyPrint, parser)
    document.write(xmlFilePathToPrettyPrint, pretty_print=True, encoding='utf-8')


def create_sitemap(extras, filenumber):
    root = ET.Element('urlset')
    root.attrib[
        'xsi:schemaLocation'] = "http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
    root.attrib['xmlns'] = "http://www.sitemaps.org/schemas/sitemap/0.9"
    root.attrib['xmlns:xsi'] = "http://www.w3.org/2001/XMLSchema-instance"
    doc = ET.SubElement(root, "url")
    ET.SubElement(doc, "loc").text = "https://covistan.com/"
    nowtime = (datetime.now(timezone("Asia/Kolkata"))).strftime('%Y-%m-%dT%H:%M:%S+00:00')
    for extra in extras:
        doc = ET.SubElement(root, "url")
        ET.SubElement(doc, "loc").text = extra
        ET.SubElement(doc, "lastmod").text = nowtime
    tree = ET.ElementTree(root)
    tree.write(filenumber, encoding='utf-8', xml_declaration=True)
    return print("Sitemap Created")


def create_geo_sitemap():
    categorylist = []
    data = json.load(open(f"{BASE_DIR}/data_pretty.json"))
    services = data['encoded_list']
    for brand_id, brand_data in data['cars_info'].items():
        brand_name = "_".join(brand_data['name'].split(" "))
        for model_id, model_data in brand_data['data'].items():
            model_id = int(model_id)
            model_name = "-".join(" ".join(model_data.split("-")[:-1]).split(" "))
            fuel_info = list(model_data.split("-")[-1])
            for fuel_num, fuel_name in enumerate(fuel_info):
                fuel_id = fuel_num + model_id
                if fuel_name == "P":
                    fuel_type = "petrol"
                elif fuel_name == "C":
                    fuel_type = "cng"
                else:
                    fuel_type = "diesel"
                for service in services:
                    strr = f"https://cars24mechanic.com/services.html?service={service}&brand_name={brand_name}&model_name={model_name}&fuel_type={fuel_type}&brand_id={brand_id}&model_id={model_id}&fuel_id={fuel_id}"
                    categorylist.append(strr)
    path = f'{BASE_DIR}/sitemap_.xml'
    create_sitemap(categorylist, path)
    prettyPrintXml(path)
    return print("Geo Sitemap created")


create_geo_sitemap()
