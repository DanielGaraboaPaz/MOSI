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
import argparse
import json

from MOSI import cds, thredds, cmems
from MOSI.utils import pprint, bcolors
from MOSI.utils import split_request_on_time, get_operational_request


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
