from firstimpressionbeta.constants import APIS, TEMP_FOLDER
from firstimpressionbeta.api.request import request
from firstimpressionbeta.file import update_directories_api
from firstimpressionbeta.file import check_too_old
from firstimpressionbeta.file import write_root_to_xml_files
import xml.etree.ElementTree as ET
import os

##################################################################################################
# CONSTANTS
##################################################################################################

NAME = APIS['solaredge']
URL = 'https://monitoringpublic.solaredge.com/solaredge-web/p/kiosk/kioskData?locale=nl_NL'
GUID = 'df83c872-7416-4817-8578-80240d3e03dc'

XML_TEMP_PATH = os.path.join(TEMP_FOLDER, NAME, 'data.xml')

MAX_FILE_AGE = 60 * 5



##################################################################################################
# MAIN FUNCTIONS API
##################################################################################################

def run_api(guid):

    update_directories_api(NAME)

    if check_too_old(XML_TEMP_PATH, MAX_FILE_AGE):

        root = ET.Element("root")

        response = request(URL, params={'guid':guid}, method='post').text.split('\n')

        co2_saved = ''
        trees_saved = ''
        last_day_energy = ''

        for elem in response:
            if 'CO2EmissionSaved' in elem:
                co2_saved = str(round(float(elem.split(':')[1].split(' ')[0][1:]),0)) + ' kg'
            if 'treesEquivalentSaved' in elem:
                trees_saved = str(round(float(elem.split(':')[1][1:-2]),0))
            if 'lastDayEnergy' in elem:
                last_day_energy = elem.split(':')[1][1:-2]

        ET.SubElement(root, "EmissionSaved").text = co2_saved
        ET.SubElement(root, "TreesSaved").text = trees_saved
        ET.SubElement(root, "EnergyToday").text = last_day_energy

        write_root_to_xml_files(root, XML_TEMP_PATH, NAME)


    


##################################################################################################
# MEDIA FUNCTIONS
##################################################################################################


##################################################################################################
# GET FUNCTIONS
##################################################################################################


##################################################################################################
# PARSE FUNCTIONS
##################################################################################################

run_api(GUID)