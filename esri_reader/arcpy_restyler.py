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
JSONFORMAT = 'f=json'

class arcpy_script(object):
    def __init__(self):
        return

def describe_feature_service(service):
    serviceurl = service + '?' + JSONFORMAT
    with urllib.request.urlopen(serviceurl) as url:
        rawdata = url.read()
        jsondata = rawdata.decode()
        parsed = json.loads(jsondata)
        #print(json.dumps(parsed, indent=4, sort_keys=True))
        layers = parsed['layers']
        docinfo = parsed['documentInfo']
        print("Title: %s" % docinfo['Title'])
        sref = parsed["spatialReference"]
        print("SREF: %s" % sref['wkid'])
        pass

    for layer in layers:
        describe_layer(service, layer)
    return

d_geometry_types = { 'esriGeometryPolygon': 'Polygon', }

def describe_layer(service, layer):
    #print(layer)
    name  = layer['name']
    id    = layer['id']
    geometry_type = layer['geometryType']
    layerurl   = "%s/%s/?%s" % (service, id, JSONFORMAT)
    visibility = layer['defaultVisibility'] == True
    #other properties: minScale, maxScale, type=Feature Layer

    print("ID: %d %s Layer name: '%s' visible? %s" % (id, d_geometry_types[geometry_type], name, visibility))

    with urllib.request.urlopen(layerurl) as url:
        rawdata = url.read()
        jsondata = rawdata.decode()
        parsed = json.loads(jsondata)
        #print(json.dumps(parsed, indent=4, sort_keys=True))
        print("Fields:")
        oid = None
        fields = parsed['fields']
        for field in fields:
            fieldtype = field['type']
            if fieldtype == 'esriFieldTypeOID':
                oid = field
            #print("  ", field['name'], fieldtype)

        sref         = parsed["sourceSpatialReference"]['wkid']
        styleinfo    = parsed['drawingInfo']
        labelinginfo = styleinfo['labelingInfo']
        renderer     = styleinfo['renderer']
        opacity   = 1 - styleinfo['transparency']
        describe_label_style(labelinginfo)
        describe_renderer(renderer)
        pass
    return

def describe_label_style(style):
    if not style: 
        return
    print("labelingInfo ----\n", json.dumps(style, indent=4, sort_keys=True))
    label  = style['label']
    symbol = style['symbol']
    describe_color(symbol["color"])
    try:
        outline = symbol["outline"]
        print("outline: width %d" % outline['width'])
        describe_color(outline["color"])
    except:
        pass
    return

def describe_renderer(styles):
    #print("renderer  -------\n", json.dumps(style, indent=4, sort_keys=True))
    for style in styles:
        describe_style(style)
    return

def describe_style(style):
    print("label: '%s' '%s'" % (style['label'], style['value']))
    symbol = style['symbol']
    describe_color(symbol['color'])
    try:
        outline = symbol['outline']
        print("outline: width %d" % outline['width'])
        describe_color(outline['color'])
    except:
        pass
    return

def describe_color(color):
    print("color: %d %d %d %d" % color)

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
    all_services    = "https://cc-gis.clatsop.co.clatsop.or.us/arcgis/rest/services"
    # for folder in folders:
    #    describe_service(service + '/' + folder)
    # for layerservice in services:
    #     describe_service(service + '/' + layerservice)

    taxlots_vectortiles    = all_services + "/Hosted/WM_taxlots"
    taxlots_featureservice = all_services + "/Assessment_and_Taxation/Taxlots_3857/FeatureServer/"
    zoning_featureservice  = all_services + "/Zoning_3857/FeatureServer/"

    for service in [zoning_featureservice]:
        describe_feature_service(service)

# That's all!
