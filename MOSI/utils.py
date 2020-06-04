# -*- coding: utf-8 -*-
import json
from urllib.request import urlopen
from xml.dom import minidom

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def pprint(_dict):
    """
    Pretty line print for dictionaries.

    Args:
        _dict (dict): Dictionary to be printed

    Returns:
        None.

    """
    for key, value in _dict.items():
        print('\t', key, ':', value)


def dump_request_to_json(_dict, filename):
    """
    It dumps a dictionary to a file.

    Args:
        _dict (dict): Dictionary to be dumped to file.
        filename (str): file path to write.

    Returns:
        None.

    """
    with open(filename, 'w') as f:
        json.dump(_dict, f, ensure_ascii=False, indent=4)
        f.close()


def getElements(url, tag_name, attribute_name):
    """Get elements from an XML file"""
    # usock = urllib2.urlopen(url)
    usock = urlopen(url)
    xmldoc = minidom.parse(usock)
    usock.close()
    tags = xmldoc.getElementsByTagName(tag_name)
    attributes = []
    for tag in tags:
        attribute = tag.getAttribute(attribute_name)
        attributes.append(attribute)
    return attributes
