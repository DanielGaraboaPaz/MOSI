# -*- coding: utf-8 -*-
"""
Module to translate a json dict request into THREDDS server request.

The request for thredds server use to go through url download.
This module has builtin functions to translate raw dictionary request into
url THREDDS request.

In case you want to run operational or iterative request based on date related
patterns. You can use the following struture:

This is the command to use for those folder or thredds where the subfolder
estructure depend on the download date. You should specify a
request['pattern'] in that case.

Example:
'http://mandeo.meteogalicia.gal/thredds/catalog/modelos/WRF_HIST/d01/2013/06/catalog.html'
'/wrf-galicila/{year}{month}{da}/netcdf-{year}-{month}-{day}'.format(year='2001',month='01',day='01')

"""

from urllib.request import urlretrieve
from MOSI.utils import getElements


def get_file_server_request(request):
    """Get the request fileServer for THREDDS server from a raw request.

    Args:
        request (dict): Dictionrary with raw request

    Returns:
        file_server_request (str): url with thredds fileServer request

    """
    file_server_request = request['thredds'] + request['service-id'] +\
        request['product-id']
    return file_server_request


def get_ncss_request(request):
    """Translates raw python dictionary into a THREDDS NCSS request.

    Args:
        request (dict): Raw request in python dictionary format.

    Returns:
       ncss_request (string): NCSS url type request

    """
    # Horizontal request
    if ('latitude-min' in request) or ('longitude-min' in request):
        horizontal_selection =\
            'north=' + str(request['latitude-max']) + '&' +\
            'west=' + str(request['longitude-min']) + '&' +\
            'east=' + str(request['longitude-max']) + '&' +\
            'south=' + str(request['latitude-min']) + '&'
    else:
        horizontal_selection = '&'

    if 'horizontal-stride' in request:
        horizontal_selection += 'horizStride=' + \
                                str(request['horizontal-stride'])+'&'

    # Vertical request
    if ('depth-min' in request) or ('depth-max' in request):
        vertical_selection = 'vertCoord='+str(request['depth-min']) + '&'
    else:
        vertical_selection = '&'

    if 'depth-stride' in request:
        vertical_selection += 'vertStride=' +\
            str(request['depth-stride']) + '&'

    # Time request
    if ('date-min' in request):
        date_min_format = ('T'.join(request['date-min'].split())+'Z').replace(':','%3A')
        date_max_format = ('T'.join(request['date-max'].split())+'Z').replace(':','%3A')
        time_selection = 'time_start=' + date_min_format + '&' + \
                         'time_end=' + date_max_format + '&'
    elif 'date-stride' in 'request':
        time_selection += 'timeStride=' + str(request['date-stride']) + '&'
    else:
        time_selection = '&'

    # Variable request
    if 'variable' in request:
        variableSelection = '&'.join(['var=' + variable for variable in request['variable']]) + '&'

    if 'format' in request:
        formatSelection = 'accept='+request['format']
    else:
        formatSelection = 'accept=netcdf'

    ncss_request = (request['thredds'] +
                    request['service-id'] +
                    request['product-id'] + '?' +
                    variableSelection +
                    'disableLLSubset=on&disableProjSubset=on&' +
                    horizontal_selection +
                    time_selection +
                    vertical_selection +
                    formatSelection)

    ncss_request = ncss_request.replace(' ', '')
    ncss_request = ncss_request.replace('&&', '&')
    ncss_request = ncss_request. replace('&&&', '&')

    return ncss_request


def download_thredds_request(thredds_request):
    """
    Download thredds URL request.

    Args:
        thredds_request (str): THREDDS url request.

    Returns:
        None.

    """
    urlretrieve(thredds_request,
                thredds_request['out-dir'] + thredds_request['out-name'])


def download_thredds_catalog(request):
    """
     Download thredds URL entire catalog.

    Args:
        request (dict): Raw dictionary python request

    Returns:
        None.

    """
    url_catalog = request['thredds'] + request['service-id'] + request['product-id']
    print('-> Catalog >>', url_catalog)
    catalog = getElements(url_catalog, 'dataset', 'urlPath')
    files_in_catalog = []
    for citem in catalog:
        if (citem[-3:] == '.nc' or citem[-4:] == '.nc4'):
            files_in_catalog.append(citem)
    count = 0
    for nc_file in files_in_catalog:
        count += 1
        file_url = request['thredds'] + '/fileServer/' + nc_file
        file_prefix = file_url.split('/')[-1][:-3]
        file_name = file_prefix + 'nc'
        print('-> Downloading ', count, '/',
              len(files_in_catalog), '>>', file_url)
        _ = urlretrieve(file_url, request['out-dir'] + file_name)
    return


def download(request):
    """Download the raw request for a THREDDS server.

    Args:
        request (dict): Python dictionary with raw request.

    Returns:
        None

    """

    print('-> THREDDS request >> ...')
    if '.nc' in request['product-id']:
        if 'ncss' in request['service-id']:
            thredds_request = get_ncss_request(request)
        if 'fileServer' in request['service-id']:
            thredds_request = get_file_server_request(request)
        print('\t,', thredds_request)
        download_thredds_request(thredds_request)

    if '.xml' in request['product-id']:
        print('-> Download catalog:\n')
        download_thredds_catalog(request)
