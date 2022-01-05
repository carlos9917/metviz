'''
plot surface variables
'''
import utils_plotting as up
import gc
import pygrib

import numpy as np
import math

import matplotlib
#matplotlib.use('TkAgg')
#matplotlib.use('qt4agg')
matplotlib.use('Agg')
import subprocess

#from mpl_toolkits.basemap import Basemap

from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

#from mpl_toolkits.basemap import interp
import os

from configparser import ConfigParser
config = ConfigParser()
config.read("settings.ini")
TIME = config['plots']['TIME']
dom = config['plots']['dom']
testcase = config['plots']['testcase']
variable = config['plots']['variable']
var_img = config['plots']['var_img']
vlevel = config.getint('plots','vlevel')
unit = config['plots']['unit']
level_step = config.getint('plots','level_step')
HOUR1 = config['plots']['HOUR1']
HOUR2 = config['plots']['HOUR2']
outpath = config['plots']['outpath']
root_grib = config['plots']['root_grib']
labelfig = config.get('plots','labelfig')
plot_diffs = config.getboolean('plots','plot_diffs')
single_plot = config.getboolean("plots","single_plot")
only_check = config.getboolean('plots', 'only_check')
color = 'RdBu_r'


if __name__ == '__main__':
    import sys
    var_img = variable.replace(" ","_")
    if variable == "Temperature":
        root_fig = "_".join([labelfig,var_img,TIME.replace("/","")])
        params = {'t2m':{"param":"11.253","level":2,"typeOfLevel":"heightAboveGround","levelType":"sfc"}}
        if testcase == "diff":
            grib1 = os.path.join(root_grib,'IGB_S3_test',TIME,'ICMSHHARM+'+HOUR1+'_IGB_S3_test.grib')
            grib2 = os.path.join(root_grib,'IGB_S3_ref',TIME,'ICMSHHARM+'+HOUR1+'_IGB_S3_ref.grib')
            ds1 = up.read_vars(grib1,params)
            ds2 = up.read_vars(grib2,params)
            ds1["params"]["t2m"]["field"] = ds1["params"]["t2m"]["field"]-ds2["params"]["t2m"]["field"]
            clev = np.array([-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6])
            fig=up.t2m_rh2m(ds1,"Difference between ref - test exp.","diff",clev)
        else:
            grib = os.path.join(root_grib,'IGB_S3_'+testcase,TIME,'ICMSHHARM+'+HOUR1+'_IGB_S3_'+testcase+'.grib')

            clev = np.array([-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12,14,16,18,20,22,24])
            ds = up.read_vars(grib,params)
            fig=up.t2m_rh2m(ds,testcase+" experiment ","std",clev)

        plt.savefig(root_fig) #'t2m.png')
        fig.clf()
        plt.close(fig)
        gc.collect()

    if variable == "Rain":
        params ={"tp":{"param":"181.253","level":0,"typeOfLevel":"heightAboveGround","levelType":"sfc"}}
                  #"mslp":{"param":"1.253","level":0,"typeOfLevel":"heightAboveSea","levelType":"103"}}

        if labelfig == "hourly":
            root_fig = "_".join([labelfig,testcase,var_img,HOUR1,HOUR2,TIME.replace("/","")])
            grib1 = os.path.join(root_grib,'IGB_S3_'+testcase,TIME,'PRECIP+'+HOUR1+'_IGB_S3_'+testcase+'.grib')
            grib2 = os.path.join(root_grib,'IGB_S3_'+testcase,TIME,'PRECIP+'+HOUR2+'_IGB_S3_'+testcase+'.grib')
            ds1 = up.read_vars(grib1,params)
            ds2 = up.read_vars(grib2,params)
            ds2["params"]["tp"]["field"] = ds2["params"]["tp"]["field"]-ds1["params"]["tp"]["field"]
            #clev = np.array([-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6])
            clev = np.arange(0.01,25,1)
            clev = np.array([0.01,0.1,1,2,5,10,15,20,25])
            #clev=None
            fig=up.precip(ds2,"Difference hours "+HOUR1+" "+HOUR2+" "+testcase+" ","hourly",clev)
        else:
            grib = os.path.join(root_grib,'IGB_S3_'+testcase,TIME,'PRECIP+'+HOUR1+'_IGB_S3_'+testcase+'.grib')
            ds = up.read_vars(grib,params)
            clev = None
            clev = np.array([0,10,20])
            clev = np.arange(0,30,4)
            fig=up.precip(ds,testcase+" experiment ","std",clev)
        plt.savefig(root_fig)
        fig.clf()
        plt.close(fig)
        gc.collect()



