# -*- coding: utf-8 -*-
import json
import pandas as pd
from urllib.request import urlopen
from xml.dom import minidom


def get_operational_request(request, operational_time_limit):
    """
    Get the raw request from today date to the operational_time_limit.

    This function is to work with MOSI in operational modes. It just
    sets the time range of downloaded data starting at the date of
    today and it finisth in the operational time limit timdelta with format.
    "ammountunits". Example '1d','15d'

    Args:
        request (dict): Raw python dictionary with request.
        operational_time_limit (str): Time delta to download from today.

    Returns:
        request (dict): Raw python dictionary with updated request.

    """
    today_date = pd.datetime.today()
    str_year = today_date.strftime('%Y')
    str_month = today_date.strftime('%m')
    str_day = today_date.strftime('%d')
    date_str_min = today_date.strftime('%Y-%m-%d')
    time_limit_delta = operational_time_limit[:-1]
    time_limit_units = operational_time_limit[1]
    date_str_max = (
                    today_date + pd.to_timedelta(int(time_limit_delta),
                                                 unit=time_limit_units)
                    ).strftime('%Y-%m-%d')
    request['date-min'] = date_str_min + request['date-min'][10:]
    request['date-max'] = date_str_max + request['date-max'][10:]
    for key, _ in request.items():
        if isinstance(request[key], str):
            request[key] = request[key].format(year=str_year,
                                               month=str_month,
                                               day=str_day)
    return request


def split_request_on_time(request, freq):
    """
    Split a raw request in time deltas passed in freq.

    This function split a long request into chunks of size freq.
    freq shoul be provided in the pandas timedelta format. Example '1d','15d'

    Args:
        request (dict): Raw python dictionary with request.
        operational_time_limit (str): Time delta to split the request.

    Returns:
        requests (list): List with the different requests.

    """
    requests = []
    date_format = '%Y-%m-%d %H:%M:%S'
    _date_range = pd.date_range(start=request['date-min'],
                                end=request['date-max'],
                                freq=freq)
    t = 0
    for date in range(0, len(_date_range)-1):
        request_time = {
            **request,
            'date-min': _date_range[t].strftime(date_format),
            'date-max': _date_range[t+1].strftime(date_format),
            'out-name': (_date_range[t].strftime(date_format)).replace(' ', '')
            }
        requests.append(request_time)
        t += 1
    print(request)
    return requests


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
