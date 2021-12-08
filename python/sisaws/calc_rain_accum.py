'''
Calculate the 1h rain accumulations
'''
import sys
import pygrib
import numpy as np
import math
from collections import OrderedDict
#import cdo
from cdo import *
cdo   = Cdo()
import pathlib

# Path to Grib data
TIME="2021/08/14/12/"
IGB="IGB_S3_test"
gpath=os.path.join(IGB,TIME)
variable="Rain"
vlevel = 0

allgribs = list(pathlib.Path(gpath).glob('*.grib'))
allfiles= [str(f) for f in sorted(allgribs)]
print(allfiles)
#grib = root_grib + 'ICMSHFULL+0003_IGB_S3_test.grib'
only_check = False
if only_check:
    grbs = pygrib.open(allfiles[2])
    for grb in grbs: 
        level = grb.level
        name = grb.name
        units = grb.units
        print(f"{name} at level {level} with units {units}")
    sys.exit(0)

#unit = 'K' #'m/s'
import re
hours = [] #OrderedDict()
for gfile in allfiles:
    hour = int(re.search('\+(.*)_IGB',gfile.split("/")[-1]).group(1))
    hours.append(hour)
for k,stuff in enumerate(hours,start=1):
    print(k)
    if (hours[k] - hours[k-1]) == 1:
        print(allfiles[k-1])
        grb1 = pygrib.open(allfiles[k-1])
        print(allfiles[k])
        grb2 = pygrib.open(allfiles[k])
        for grb in grb1:
            if grb.name == variable and grb.level==vlevel:
                data1 = grb.values
                break
        for grb in grb2:
            if grb.name == variable and grb.level==vlevel:
                data2 = grb.values
                break
        data = data2 - data1
