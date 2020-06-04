# -*- coding: utf-8 -*-

from ecmwfapi import ECMWFDataServer
from MOSI.utils import *
import os


class ECWMFDownload:
    
    """ 
    This type of recuest is outdated. It has been replaced by CDS service
    """
    #ERA interim request example
    #wind_request = {}
    #wind_request["class"] = "ei",
    #wind_request["dataset"] = "era5",
    #wind_request["date"]= "20160101/to/20190401",
    #wind_request["expver]"= "1",
    #wind_request["grid"]= "0.75/0.75",
    #wind_request["levtype"]= "sfc",
    #wind_request["param"]= "165.128/166.128",
    #wind_request["step"]= "0",
    #wind_request["area"]= "-19/56/5/26",
    #wind_request["stream"]= "oper",
    #wind_request["time"]= "00:00:00/06:00:00/12:00:00/18:00:00",
    #wind_request["type"]= "fc",
    #wind_request["target"]= '20160101.nc',
    #wind_request["format"]= 'netcdf'
    
        
    def __init__(self,request):
        
        self.request = request
        self.attempts = []

    def getECWMFRequest(request):
        return
        

    def download(self):
                
        print('REQUEST CMEMS....\n')
        self.pprint()
        
        for n in range(0, self.attempts):
            print('Donwload Attempt:', n)
            if os.path.isfile(self.request['request']) == False:
                server.retrieve(self.request)
            else:
                break