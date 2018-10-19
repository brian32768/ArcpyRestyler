"""
$project$ common configuration properties
@author: bwilson
@date:   10/18/2018 4:44:29 PM
"""
import os
LOGFORMAT = '%(asctime)s %(message)s'

# You need to change these, most likely.
GIS_FILESERVER  = "\\\\cc-storage\\GIS" # Normally mapped as the "K:"
LISDATA         = os.path.join(GIS_FILESERVER, "LISData")
LOCAL_GDB       = "C:\\GeoModel\\AGE_maintenance\\DataLoader\\DataLoader.gdb"
ENTERPRISE_GDB     = os.path.join(GIS_FILESERVER, "ORMAP_CONVERSION\\scripts\\connections\\cc-gis.sde")
ENTERPRISE_SANDBOX = os.path.join(GIS_FILESERVER, "ORMAP_CONVERSION\\scripts\\connections\\cc-gis_sandbox.sde")
