"""
@date:   10/18/2018 4:44:29 PM
@author: bwilson
"""
from __future__ import print_function
import os
import sys
import logging
import arcpy

import urllib.request
import json

__version__ = ".001" # Set this to whatever you want or just delete it.

class arcpy_script(object):
    def __init__(self):
        return

# ===================================================================================
if __name__ == "__main__":

    import config

    MYNAME  = os.path.splitext(os.path.split(__file__)[1])[0]
    LOGFILE = MYNAME + ".log"
    logging.basicConfig(filename=LOGFILE, level=logging.DEBUG, format=config.LOGFORMAT)
    print("Writing log to %s" % LOGFILE)

    # You can put unit test code here
    # or you can set up this code to run standalone from command line

    #s = arcpy_script()

    service = "https://cc-gis.clatsop.co.clatsop.or.us/arcgis/rest/services/Assessment_and_Taxation/Taxlots_3857/FeatureServer/1/?f=json"
    with urllib.request.urlopen(service) as url:
        rawdata = url.read()
        jsondata = rawdata.decode()
        parsed = json.loads(jsondata)
        print(json.dumps(parsed, indent=4, sort_keys=True))

    pass

# That's all!
