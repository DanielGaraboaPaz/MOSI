# -*- coding: utf-8 -*-
"""
Module to translate the raw json request dictionary into a CDS request.

if you want to perform a request you can do it on this webpage.
https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=form
https://cds.climate.copernicus.eu/api-how-to#use-the-cds-api-client-for-data-access

Example of common script with a CDS request:
    #!/usr/bin/env python
    import cdsapi
    c = cdsapi.Client()
    c.retrieve("reanalysis-era5-pressure-levels",
    {
    "variable": "temperature",
    "pressure_level": "1000",
    "product_type": "reanalysis",
    "year": "2008",
    "month": "01",
    "day": "01",
    "time": "12:00",
    "format": "grib"
    },
    "download.grib")
"""

import cdsapi
import os
import pandas as pd


attempts = 1


def get_cds_request(request):
    """
    Translates raw python dictionary into cdsapi.client request.

    Args:
        request (dict): Raw request in python dictionary format.

    Returns:
        request_cds (list): CDS request type ready to cdsapi.client.

    """

    date_cds = pd.date_range(request['date-min'],
                             request['date-max'],
                             freq='H')

    inner_dict = {'variable': request['variable'],
                  'product_type': request['product-id'],
                  'format': request['format'],
                  'date': request['date-min'][:10]+'/'+request['date-max'][:10],
                  "time": list(date_cds.strftime('%H:%M').unique())}

    # if "depth-min" or "depth-max" in self.request:
    #     innerDict['pressure_level'] = str(self.request['depth-min'])+'/to/'+str(self.request['depth-max'])

    if "pressure_level" in request:
        inner_dict['pressure_level'] = request['pressure_level']

    if ('latitude-min' in request) or ('longitude-min' in request):
        inner_dict['area'] = [request['latitude-max'],
                              request['longitude-min'],
                              request['latitude-min'],
                              request['longitude-max']]

    request_cds = [request['service-id'],
                   inner_dict,
                   request['out-dir'] + request['out-name'] + '.nc']

    return request_cds


def download(request):

    request_cds = get_cds_request(request)

    print('-> CDS request >> ...')
    print('\t', request_cds)
    print('\n')

    c = cdsapi.Client()
    for n in range(0, attempts):
        print('-> Donwload Attempt >> ', n)
        out_nc_filename = request['out-dir'] + request['out-name'] + '.nc'
        if os.path.isfile(out_nc_filename) is False:
            c.retrieve(*request_cds)
        else:
            print('-> This file exist. Continue with next one')
            break
