# -*- coding: utf-8 -*-

"""
Module to translate the raw json request dictionary into a MOTU request

Example of a common MOTU request:
    python -m motuclient
    --user your_user(1)
    --pwd your_password(1)
    --motu 'http://nrt-cmems-du.eu/motu-web/Motu'
    --service-id 'GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS'
    --product-id 'global-analysis-forecast-phy-001-024'
    --longitude-min '-100' --longitude-max '100'
    --latitude-min '-80' --latitude-max '90'
    --date-min '2018-02-10 12:00:00'
    --date-max '2018-02-10 12:00:00'
    --depth-min '0.493' --depth-max '0.4942'
    --variable 'bottomT' --variable 'uo' --variable 'vo'
    --out-dir your_output_directory(1) --out-name your_output_file_name(1)
    --proxy-server your_proxy_server_url:your_proxy_port_number(2)
    --proxy-user your_proxy_user_login(3)
    --proxy-pwd your_proxy_user_password(3)

"""

import os

attempts = 1


def get_motu_request(request, arguments='', command='python -m motuclient'):
    """Translates raw python dictionary into a MOTUclient request.

    Args:
        request (dict): Raw request in python dictionary format.
        arguments (str, optional): DESCRIPTION. Defaults to ''.
        command (str, optional): System commandline to run the motuclient.
            Defaults to 'python -m motuclient'.

    Returns:
       motu_request (string): MOTU request

    """

    for key, value in request.items():
        if key == 'variable':
            for var in value:
                arguments += ' --' + str(key) + '=' + var
        else:
            arguments += ' --' + str(key) + '=' + str(value)
    motu_request = command + arguments
    return motu_request


def download(request):
    motu_request = get_motu_request(request)
    print('-> CMEMS request >> ...\n')
    print('\t', motu_request)
    print('\n')
    for n in range(0, attempts):
        print('-> Donwload attempt >> ', n)
        if os.path.isfile(request['out-name']) is False:
            _ = os.system(motu_request)
        else:
            break
