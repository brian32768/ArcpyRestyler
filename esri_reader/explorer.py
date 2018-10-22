
"""
@date:   10/18/2018 4:44:29 PM
@author: bwilson
"""
from __future__ import print_function
import os
import sys
#import logging
#import arcpy

import urllib.request
import json

__version__ = ".002" # Set this to whatever you want or just delete it.
JSONFORMAT = 'f=json'

class arcpy_script(object):
    def __init__(self):
        return

def get_services(serviceurl):
    services = {}
    try:
        with urllib.request.urlopen(serviceurl + '?' + JSONFORMAT) as url:
            jsondata = url.read().decode()
            parsed = json.loads(jsondata)
            services = parsed["services"]
            folders  = parsed["folders"]
            # There can be a folders property here too hmmm wonder if it is ever used?
    except Exception as e:
        print(e)
    return services

def describe_service(serviceurl):
    
    with urllib.request.urlopen(serviceurl + '?' + JSONFORMAT) as url:
        jsondata = url.read().decode()
        parsed = json.loads(jsondata)
        #print(json.dumps(parsed, indent=4, sort_keys=True))
        layers = parsed['layers']

        try:
            docinfo = parsed['documentInfo']
        except KeyError:
            pass

        minScale = maxScale = 0
        try:
            minScale = parsed['minScale']
        except KeyError:
            pass
        try:
            maxScale = parsed['maxScale']
        except KeyError:
            pass

        capabilities = parsed['capabilities']
        supportedQueryFormats = parsed['supportedQueryFormats'].split(',')

        print("Title: %s" % docinfo['Title'])
        sref = parsed["spatialReference"]
        print("SREF: %s" % sref['wkid'])
        pass


    if type == 'FeatureServer':
        pass

    elif type == 'MapServer':
        supportedImageFormatTypes = []
        try:
            supportedImageFormatTypes = parsed['supportedImageFormatTypes'].split(',')
        except KeyError:
            pass

    for layer in layers:
        describe_layer(serviceurl, layer)
    return


d_geometry_types = { '': 'Map Server', 'esriGeometryPolygon': 'Polygon', }

def describe_layer(service, layer):

    name  = layer['name']
    id    = layer['id']

    minScale = maxScale = 0
    try:
        minScale = layer['minScale']
    except KeyError:
        pass
    try:
        maxScale = layer['maxScale']
    except KeyError:
        pass

    layertype = ''
    try:
        layertype  = layer['type']
        pass
    except KeyError:
        pass

    geometry_type = ''
    try:
        geometry_type = layer['geometryType']
        layertype = d_geometry_types[geometry_type]
    except KeyError:
        pass

    layerurl   = "%s/%s/?%s" % (service, id, JSONFORMAT)
    visibility = True;
    try:
        visibility = layer['defaultVisibility'] == True
    except KeyError:
        pass

    print("ID: %d %s Layer name: '%s' visible? %s" % (id, layertype, name, visibility))

    with urllib.request.urlopen(layerurl) as url:
        jsondata = url.read().decode()
        parsed = json.loads(jsondata)
        #print(json.dumps(parsed, indent=4, sort_keys=True))
        
        layertype = parsed['type']
        print(layertype)
        if layertype == 'Feature Layer':
            describe_fields(parsed['fields'])

            drawingInfo  = parsed['drawingInfo']
            labelingInfo = drawingInfo['labelingInfo']

            if type(labelingInfo) is list:
                for l in labelingInfo:
                    describe_labelingInfo(l)
            else:
                describe_labelingInfo(labelingInfo)

            renderer     = drawingInfo['renderer']
            describe_renderer(renderer)

            opacity      = 1 - drawingInfo['transparency']

        elif layertype == 'Raster Layer':
            capabilities = parsed['capabilities']
            supportedQueryFormats = parsed['supportedQueryFormats'].split(',')
            pass
        else:
            pass

        try:
            sref = parsed["sourceSpatialReference"]['wkid']
        except KeyError:
            sref = ''
    return

def describe_fields(fields):
    #print("Fields:")
    oid = None
    for field in fields:
        fieldtype = field['type']
        if fieldtype == 'esriFieldTypeOID':
            oid = field
        #print("  ", field['name'], fieldtype)

def describe_labelingInfo(labelingInfo):
    if not labelingInfo: 
        return
    print("labelingInfo ----\n", json.dumps(labelingInfo, indent=4, sort_keys=True))
    label = None
    try:
        label  = labelingInfo['label']
        pass
    except:
        pass
    labelExpression = None
    try:
        labelExpression  = labelingInfo['labelExpression']
        pass
    except:
        pass

    symbol = labelingInfo['symbol']
    describe_color(symbol["color"])
    try:
        outline = symbol["outline"]
        print("outline: width %d" % outline['width'])
        describe_color(outline["color"])
    except:
        pass
    return

def describe_renderer(styles):
    if styles['type'] == 'uniqueValue':
        #print(styles)
        pass
    elif styles['type'] == 'simple':
        #print(styles)
        describe_symbol(styles['symbol'])
    else:
        for style in styles:
            describe_style(style)
    return

def describe_style(style):
    print("label: '%s' '%s'" % (style['label'], style['value']))
    symbol = style['symbol']
    return

def describe_symbol(symbol):
    type  = symbol['type']
    print("Symbol type: %s" % type)
    if type == 'esriPMS':
        image = symbol['imageData']
        contentType = symbol['contentType']
    elif type == 'esriSFS': # simple fill symbol
        style = symbol['style']
        describe_color(symbol['color'])
        try:
            outline = symbol['outline']
            print("outline: width %d" % outline['width'])
            describe_symbol(outline)
        except:
            pass
    elif type == 'esriSLS': # simple line symbol
        describe_color(symbol['color'])
    elif type == 'esriSMS': # marker
        print(symbol)
    elif type == 'esriPFS': # marker
        print(symbol)
    else:
        print("???")
        pass

def describe_color(color):
    print("color: ", color)

def get_folders(serviceurl):
    folders = {}
    try:
        with urllib.request.urlopen(serviceurl + '?' + JSONFORMAT) as url:
            jsondata = url.read().decode()
            parsed = json.loads(jsondata)
            folders = parsed["folders"]
    except Exception as e:
        print(e)
    return folders

# ===================================================================================
if __name__ == "__main__":

    server = "https://arcgisweb.carteretcountync.gov/arcgis/rest/services/"
    folders = get_folders(server)
    for folder in folders:
        services = get_services(server + folder)
        for service in services:
            servicename = service['name']
            servicetype = service['type']
            serviceurl = server + servicename + '/' + servicetype
            print(serviceurl)
            describe_service(serviceurl)
        print()
    taxlots_vectortiles    = all_services + "/Hosted/WM_taxlots"
    taxlots_featureservice = all_services + "/Assessment_and_Taxation/Taxlots_3857/FeatureServer/"
    zoning_featureservice  = all_services + "/Zoning_3857/FeatureServer/"

    for service in [zoning_featureservice]:
        describe_feature_service(service)

# That's all!
