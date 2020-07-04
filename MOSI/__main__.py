# -*- coding: utf-8 -*-
"""
Main MOSI module.

MOSI is Met-Ocean Server inquirer to download data from difente types of
server. The main idea is to define a common dictionary which uses the main
keys for multiple  diferent server request into a specific kind of request.
MOSI act as a tranlator.

At this momment MOSI support the following request tranlator:
    JSON -> THREDDS server url request
    JSON -> CDS request
    JSON -> CMEMS request.

The main idea is the request are defined in the following way:

Example:
    request = {}
    request['user']='' # CMEMS USERNAME
    request['pwd']=''  # CMEMS PASSWORD
    request['motu']='http://nrt.cmems-du.eu/motu-web/Motu'
    request['service-id']='IBI_ANALYSIS_FORECAST_WAV_005_005-TDS'
    request['product-id']='dataset-ibi-analysis-forecast-phys-005-001-hourly'
    request['product-id']='dataset-ibi-analysis-forecast-wav-005-005-hourly'
    request['date-min']="2016-01-01 00:30:00"
    request['date-max']="2019-04-15 23:30:00"
    request['latitude-min']=26
    request['latitude-max']=56
    request['longitude-min']=-19
    request['longitude-max']=5
    request['depth-min']=0.493
    request['depth-max']=0.4942
    request['variable']=['uo','vo']
    #Request['proxy-server']=None
    #Request['proxy-user']=None
    #Request['proxy-pwd']=None
    #request['out-dir']='./CURRENTS'
    request['out-dir']='./CURRENTS'
    request['out-name']='./ibe.nc'

Then the request is passed to command line by:
    python -m MOSI -j json_file_request.json -s SERVENAME[THREEDS,CDS,CMEMS]

"""
import os
import pandas as pd
import argparse
import json


from MOSI import cds, thredds, cmems
from MOSI.utils import pprint, bcolors


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
    return requests


def main():
    parser = argparse.ArgumentParser(description='MOSI: MetOcean Server Inquirer')
    parser.add_argument("-i", "--input",
                        dest="input",
                        help='json file with request')
    parser.add_argument("-s", "--server",
                        dest="server",
                        help='server type. Choose: CMEMS,CDS,THREDDS,ECWMF')
    parser.add_argument("-f", "--freq",
                        dest="frequency",
                        help='frequency interval download')
    parser.add_argument("-o", "--oper",
                        dest="operational",
                        help="date limit to download from, today")
    args = parser.parse_args()

    jsonFile = open(args.input)
    request = json.load(jsonFile)
    jsonFile.close()

    print(f"{bcolors.OKBLUE}-->> MOSI: a MetOcean Server Inquirer  <<--.{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}-->> Daniel Garaboa Paz, GFNL, USC     <<--.{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}-->> Vicente Perez Muñuzuri, GFNL, USC <<--.{bcolors.ENDC}")
    print('\n')
    print('-> json file   >> ', args.input)
    print('-> frequency   >> ', args.frequency)
    print('-> server type >> ', args.server)

    if args.operational:
        print('-> OPERATIONAL:', args.operational)

    if args.operational:
        request = get_operational_request(request, args.operational)

    if args.frequency is not None:
        request_list = split_request_on_time(request, args.frequency)
        print('-> WARNING: You did a splitted time request.')
        print('-> The request[''out-name''] will be overwriten')
        print('-> WARNING: with the min time dataset')
    else:
        request_list = [request]

    for request in request_list:
        print('-> RAW request >> ...')
        pprint(request)

        if not os.path.exists(request['out-dir']):
            os.makedirs(request['out-dir'])

        if args.server == 'CMEMS':
            cmems.download(request)

        if args.server == 'CDS':
            cds.download(request)

        if args.server == 'THREDDS':
            thredds.download(request)

    if args.server == 'ECWMF':
        print('>> IN NEXT RELEASE if it is not deprecated...')


main()
