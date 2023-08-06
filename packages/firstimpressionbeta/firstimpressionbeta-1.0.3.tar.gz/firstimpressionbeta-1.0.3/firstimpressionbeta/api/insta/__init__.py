from firstimpressionbeta.constants import APIS
from firstimpressionbeta.constants import TEMP_FOLDER
from firstimpressionbeta.constants import LOCAL_INTEGRATED_FOLDER
from firstimpressionbeta.constants import ENGLISH_INDEX
from firstimpressionbeta.constants import DUTCH_INDEX
from firstimpressionbeta.file import update_directories_api
from firstimpressionbeta.file import check_too_old
from firstimpressionbeta.file import write_root_to_xml_files
from firstimpressionbeta.file import download_install_media
from firstimpressionbeta.file import list_files_dir
from firstimpressionbeta.time import change_language
from firstimpressionbeta.time import parse_string_to_string
from firstimpressionbeta.text import remove_emoji
from firstimpressionbeta.scala import variables
from firstimpressionbeta.api.request import request_json
import xml.etree.ElementTree as ET
import os
import glob

##################################################################################################
# CONSTANTS
##################################################################################################

NAME = APIS['insta']

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

LOCAL_PATH = os.path.join(LOCAL_INTEGRATED_FOLDER, NAME)

URL = 'https://fiapi.nl:8080/instagram_post/'

##################################################################################################
# MAIN FUNCTIONS API
##################################################################################################

def run_api(api_key, tags, max_minutes, max_characters, max_items, language):
    
    max_file_age = 60 * max_minutes

    if language == 'NL':
        change_language(DUTCH_INDEX)
        datetime_format_new = '%d %B %Y'
        language_index = DUTCH_INDEX
    else:
        change_language(ENGLISH_INDEX)
        datetime_format_new = '%B %d %Y'
        language_index = ENGLISH_INDEX

    headers = {
        'Authorization': 'Token {}'.format(api_key)
    }

    update_directories_api(NAME)

    tag_counter = 0

    for tag in tags:
        if tag.startswith('#'):
            xml_temp_path = os.path.join(TEMP_FOLDER, NAME, 'tag_{}.xml'.format(tag[1:]))
            tag_counter += 1
        else:
            xml_temp_path = os.path.join(TEMP_FOLDER, NAME, '{}.xml'.format(tag))
        
        if check_too_old(xml_temp_path, max_file_age):
            params = {
                'subscribed_to': tag,
                'number_of_posts': max_items
            }

            response_json = request_json(URL, headers, params, False)

            root = ET.Element("root")

            for post in response_json:
                item = ET.SubElement(root, "item")
                ET.SubElement(item, "subscribed_to").text = get_subscription_name(post)
                ET.SubElement(item, "comment").text = crop_message(remove_emoji(get_message(post)), max_characters, language_index)
                ET.SubElement(item, "date").text = parse_string_to_string(get_creation_date(post), DATETIME_FORMAT, datetime_format_new)
                ET.SubElement(item, "hashtags").text = get_hashtags(post)

                thumbnail_url = get_thumbnail_url(post)

                if thumbnail_url is None:
                    media_link = 'Content:\\placeholders\\img.png'
                else:
                    thumbnail_url = thumbnail_url.split('?').pop(0)
                    media_link = download_install_media(thumbnail_url, TEMP_FOLDER, NAME)
                
                ET.SubElement(item, "image").text = media_link
            
            write_root_to_xml_files(root, xml_temp_path, NAME)

def check_api(max_minutes):
    svars = variables()

    max_file_age = 60 * max_minutes

    for file in list_files_dir(LOCAL_PATH):
        if 'xml' in file:
            file_path = os.path.join(LOCAL_PATH, file)
            if check_too_old(file_path):
                svars['skipscript'] = True
                break
            else:
                svars['skipscript'] = False


##################################################################################################
# MEDIA FUNCTIONS
##################################################################################################


##################################################################################################
# GET FUNCTIONS
##################################################################################################

def get_subscription_name(post):
    return post.get('subscribed_to', '')


def get_thumbnail_url(post):
    return post.get('thumbnail_url', None)


def get_message(post):
    return post.get('message', '')


def get_creation_date(post):
    return post.get('created_at', '')[:-6]


def get_hashtags(post):
    hashtags = post.get('hashtags', [''])
    return ' '.join(hashtags)

##################################################################################################
# PARSE FUNCTIONS
##################################################################################################

def crop_message(text, max_length, language):
    if language == 1:
        append_text = "Lees verder op Instagram"
    else:
        append_text = "Read more on Instagram"

    if len(text) > max_length:
        return text[:max_length-3] + "...\n{}".format(append_text)
    else:
        return text



