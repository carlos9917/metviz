
'''
Modified version of Aasmund scrpts from CARRA
'''

import numpy as np
import numpy.ma as ma
import matplotlib
matplotlib.use('Agg')
from matplotlib import cm
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import sys
import argparse
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import datetime
import copy
import glob
import pyproj

#import eccodes as ecc
import re
from collections import OrderedDict
import gc
import pygrib
#import metview as mv

import os
from os import path


def str2dict(string):
    keys = {}
    opts = string.split(',')
    for opt in opts:
        s = opt.split('=')
        keys[s[0]] = s[1]
    return keys
# based on eccodes
#def check_codes(gribfile):
#    '''
#    check some grib codes
#    '''
#    f = open(gribfile)
#    while 1:
#        gid = ecc.codes_grib_new_from_file(f)
#        if gid is None:
#            break
#        keys = ('name', 'shortName', 'levelType','typeOfLevel','level','param')
#        check_key =  ecc.codes_get(gid, "name")
#        if check_key == "Pressure":
#            for key in keys:
#                print('string %s: %s' % (key, ecc.codes_get(gid, key)))
#                print('grib codes %s: %s' % (key, ecc.codes_get(gid, key,ktype=int)))
#
#def locate_vars(gribfile):
#    '''
#    Short function to help me find the f*ing codes!
#    '''
#    f = ecc.GribFile(gribfile)
#    for i in range(len(f)):
#        msg = ecc.GribMessage(f)
#        param=msg["param"]
#        #print(f'name {msg["name"]},shortName {msg["shortName"]}')
#        if msg["name"] == "Temperature" and msg["typeOfLevel"] == "heightAboveGround" and msg["level"] == 2:
#            print("2m Temperature")
#            print(f'Parameter: {param}')
#            print(f'levelType: {msg["levelType"]}')
#            print(f'typeOfLevel: {msg["typeOfLevel"]}')
#            
#        if msg["name"] == "u-component of wind" and msg["typeOfLevel"] == "heightAboveGround" and msg["level"] == 10:
#            print("u10")
#            print(f'Parameter: {param}')
#            print(f'levelType: {msg["levelType"]}')
#            print(f'typeOfLevel: {msg["typeOfLevel"]}')
#        if msg["name"] == "v-component of wind" and msg["typeOfLevel"] == "heightAboveGround" and msg["level"] == 10:
#            print("v10")
#            print(f'Parameter: {param}')
#            print(f'levelType: {msg["levelType"]}')
#            print(f'typeOfLevel: {msg["typeOfLevel"]}')
#        if msg["name"] == "Wind speed" and msg["typeOfLevel"] == "heightAboveGround" and msg["level"] == 10:
#            print("10m wind speed")
#            print(f'Parameter: {param}')
#            print(f'levelType: {msg["levelType"]}')
#            print(f'typeOfLevel: {msg["typeOfLevel"]}')
#        if msg["name"] == "Wind direction" and msg["typeOfLevel"] == "heightAboveGround" and msg["level"] == 10:
#            print("10m wind direction")
#            print(f'Parameter: {param}')
#            print(f'levelType: {msg["levelType"]}')
#            print(f'typeOfLevel: {msg["typeOfLevel"]}')
#        if msg["shortName"] == "tp":
#            print("Total precipitation")
#            print(f'Parameter: {param}')
#            print(f'level: {msg["level"]}')
#            print(f'levelType: {msg["levelType"]}')
#            print(f'typeOfLevel: {msg["typeOfLevel"]}')
#        if msg["name"] == "Pressure" and msg["typeOfLevel"] == "heightAboveSea" and msg["level"] == 0 and msg["levelType"] == "103":
#            print(">>>>> Found mslp")
#            print(f'Parameter: {param}')
#            print(f'levelType: {msg["levelType"]}')
#            print(f'typeOfLevel: {msg["typeOfLevel"]}')
#            print(msg["name"])
#        if msg["name"] == "Mean sea level pressure": # and msg["typeOfLevel"] == "surface" and msg["level"] == 0 and msg["levelType"] == "0":
#            print(">>>>> Found msl ERA")
#            print(f'Parameter: {param}')
#            print(f'level: {msg["level"]}')
#            print(f'levelType: {msg["levelType"]}')
#            print(f'typeOfLevel: {msg["typeOfLevel"]}')
#        #if msg["name"] == "Pressure" and msg["level"] == 0:
#        #    print(f"param: {param}, name: {msg['name']}, typeOfLevel: {msg['typeOfLevel']}, levelType {msg['levelType']}")
#
#    sys.exit()

def msg2ds(vars):
    ds = {}
    for param in vars:
        msghit = vars[param]['msg']
        #print("Here it is crashing")
        nx = msghit['Nx']
        ny = msghit['Ny']
        date = msghit['date']
        hour = msghit['hour']
        fcstep = msghit['step']
        lons = msghit['longitudes'].reshape((ny,nx))
        lats = msghit['latitudes'].reshape((ny,nx))
        lat0 = msghit['LaDInDegrees']
        lon0 = msghit['LoVInDegrees']
        lat1 = msghit['Latin1InDegrees']
        lat2 = msghit['Latin2InDegrees']
        val = ma.masked_values(msghit['values'].reshape((ny,nx)),msghit['missingValue'])
        name = msghit['parameterName']
        vars[param]['field'] = val
        dt = datetime.datetime.strptime(str(date)+str(hour),"%Y%m%d%H")
        lons2 = np.where(lons>180,lons-360,lons)
        lon0 = np.where(lon0>180,lon0-360,lon0)
        proj = ccrs.LambertConformal(central_latitude=lat0,
                                 central_longitude=lon0,
                                 standard_parallels=(lat1, lat2))
        ds['misc'] = {'date':dt,
                      'lons':lons2,
                      'lats':lats,
                      'proj':proj,
                      'fcstep':fcstep}
        ds['params'] = vars
    return ds

def read_mslp_tp(gfile0,gfile1,gfile2):
    '''
    Reads the mslp from the first file. Reads tot prec from the files 1 and 2 
    and takes the difference to calculate total prec

    '''
    ds = {}

    param ={"tp":{"param":"61.253","level":0,"typeOfLevel":"heightAboveGround","levelType":"sfc"}}
    vars1 = copy.deepcopy(param)

    param ={"tp":{"param":"61.253","level":0,"typeOfLevel":"heightAboveGround","levelType":"sfc"},
            "mslp":{"param":"1.253","level":0,"typeOfLevel":"heightAboveSea","levelType":"103"}}
    vars2 = copy.deepcopy(param)

    f0 = pygrib.open(gfile0)
    f1 = pygrib.open(gfile1)
    f2 = pygrib.open(gfile2)
    for msg in f1:
        if vars1['tp']['param']== msg['param'] and vars1['tp']["level"]==msg["level"] and vars1['tp']["typeOfLevel"]==msg['typeOfLevel'] and vars1['tp']["levelType"]==msg["levelType"]:
            #print('found tp1')
            #print(f'time {msg["time"]}')
            #print(f'step {msg["step"]}')
            vars1['tp']['msg'] = msg

    for msg in f2:
        if vars2['tp']['param']== msg['param'] and vars2['tp']["level"]==msg["level"] and vars2['tp']["typeOfLevel"]==msg['typeOfLevel'] and vars2['tp']["levelType"]==msg["levelType"]:
            #print('found tp2')
            #print(f'time {msg["time"]}')
            #print(f'step {msg["step"]}')
            vars2['tp']['msg'] = msg

    for msg in f0:
        if vars2['mslp']['param']== msg['param'] and vars2['mslp']["level"]==msg["level"] and vars2['mslp']["typeOfLevel"]==msg['typeOfLevel'] and vars2['mslp']["levelType"]==msg["levelType"]:
            #print('found mslp')
            #print(f'time {msg["time"]}')
            #print(f'step {msg["step"]}')
            vars2['mslp']['msg'] = msg
    ds1 = msg2ds(vars1)
    ds2 = msg2ds(vars2)
    
    ds2["params"]["tp"]["field"] = ds2["params"]["tp"]["field"]-ds1["params"]["tp"]["field"]
    return ds2

def read_vars(gribfile,params):
    '''
    Reads a file that contains only one time step
    '''
    ds = {}
    vars = copy.deepcopy(params)
    f = pygrib.open(gribfile)
    for msg in f:
        for param in vars:
            if vars[param]['param']== msg['param'] and vars[param]["level"]==msg["level"] and vars[param]["typeOfLevel"]==msg['typeOfLevel'] and vars[param]["levelType"]==msg["levelType"]:
                print(f'found {vars[param]}')
                vars[param]['msg'] = msg
            
    for param in vars:
        msghit = vars[param]['msg']
        nx = msghit['Nx']
        ny = msghit['Ny']
        date = msghit['date']
        hour = msghit['hour']
        fcstep = msghit['step']
        lons = msghit['longitudes'].reshape((ny,nx))
        lats = msghit['latitudes'].reshape((ny,nx))
        lat0 = msghit['LaDInDegrees']
        lon0 = msghit['LoVInDegrees']
        lat1 = msghit['Latin1InDegrees']
        lat2 = msghit['Latin2InDegrees']
        val = ma.masked_values(msghit['values'].reshape((ny,nx)),msghit['missingValue'])
        name = msghit['parameterName']
        vars[param]['field'] = val
        dt = datetime.datetime.strptime(str(date)+str(hour),"%Y%m%d%H")
        lons2 = np.where(lons>180,lons-360,lons)
        lon0 = np.where(lon0>180,lon0-360,lon0)
        proj = ccrs.LambertConformal(central_latitude=lat0,
                                 central_longitude=lon0,
                                 standard_parallels=(lat1, lat2))
        ds['misc'] = {'date':dt,
                      'lons':lons2,
                      'lats':lats,
                      'proj':proj,
                      'fcstep':fcstep}
        ds['params'] = vars

    return ds

# -------------------------
# Functions to do the plots
# -------------------------

def mslp_precip(ds,accum_time="3"):
    '''
    This function uses only one file as input     
    '''
    lons = ds['misc']['lons']
    lats = ds['misc']['lats']
    proj = ds['misc']['proj']
    dt = ds['misc']['date']
    fcstep = ds['misc']['fcstep']

    PRJ = pyproj.Proj(proj.proj4_init)

    # Plotting parameters
    pcontours = np.arange(960,1060,2)
    precip_levels = [0.5,2,4,10,25,50,100,250]
    precip_colors = ['aqua','dodgerblue','blue','m','magenta','darkorange','red']

    # Fields to plot
    mslp = ds['params']['mslp']['field']/100
    precip = ds['params']['tp']['field']
    fig = plt.figure(figsize=[12,9],edgecolor='k')
    ax = plt.axes(projection=proj)
    CS = ax.contour(lons,lats,mslp,
                    transform=ccrs.PlateCarree(),
                    levels=pcontours,
                    colors='k',
                    zorder=3,
                    linewidths=[2,1,1,1,1])
    ax.clabel(CS,inline=1,fmt='%d')
    #if there is no precipitation, do not plot it??
    if precip.max() != 0.0:
        #print("No precipitation on this day!")
        #precip_levels = [0.0,0.5]
        #precip_colors = ['aqua','dodgerblue']
        CS2 = ax.contourf(lons,lats,precip,
                          transform=ccrs.PlateCarree(),
                          levels=precip_levels,
                          colors=precip_colors,
                          zorder=2,
                          alpha=0.9)
        plt.colorbar(CS2,shrink=0.5,orientation='vertical')
        title_pre=accum_time+"h accumulated prec and MSLP \n"
    else:
        print("WARNING: No precipitation on this day! Not plotting tot prec")
        title_pre="MSLP (acc precip zero!) \n"
    land_50m = cfeature.NaturalEarthFeature('physical', 'land', '50m',
                                            edgecolor='face',
                                            facecolor=cfeature.COLORS['land'])
    ax.add_feature(land_50m)
    ax.coastlines('50m')
    ax.gridlines()

    x0,y0 = PRJ(lons[0,0],lats[0,0])
    x1,y1 = PRJ(lons[-1,-1],lats[-1,-1])
    #print(f"Plot limits: x0,y0: {x0,y0} and x1,y1: {x1,y1}")
    N = 10000
    ax.set_xlim(x0-N,x1+N)
    ax.set_ylim(y0-N,y1+N)
    #plt.title("acc precip and MSLP \n%s UTC + %dh" % (dt.strftime('%Y-%m-%d %H:00'), fcstep))
    plt.title(title_pre+"%s UTC + %dh" % (dt.strftime('%Y-%m-%d %H:00'), fcstep))
    return fig

def t2m_rh2m(ds,extra_title,ptype):
    lons = ds['misc']['lons']
    lats = ds['misc']['lats']
    proj = ds['misc']['proj']
    dt = ds['misc']['date']
    fcstep = ds['misc']['fcstep']
    #cmap = mpl.cm.RdBu_r
    # Plotting parameters. Original colours used by CARRA gallery
    #t_colors = ['#ffffff','#e6e6e6','#cccccc','#b3b3b3','#ae99ae','#7a667a','#330066','#590080','#8000ff',
    #            '#0080ff','#00ccff','#00ffff','#26e699','#66bf26','#bfe626','#ffff80','#ffff00','#ffda00',
    #            '#ffb000','#ff7300','#ff0000','#cc0000','#80002c','#cc3d6e','#ff00ff','#ff80ff','#ffbfff',
    #            '#e6cce6','#e6e6e6']
    #t_levels = np.array([-80,-70,-60,-52,-48,-44,-40,-36,-32,-28,-24,-20,-16,-12,-8,-4,0,
    #            4,8,12,16,20,24,28,32,36,40,44,48,52,56])

    # Fields to plot
    if ptype != "diff": #only convert to C if I am not plotting the difference
        t2m = ds['params']['t2m']['field'] - 273.15
    else:
        t2m = ds['params']['t2m']['field']

    fig = plt.figure(figsize=[12,9])
    ax = plt.axes(projection=proj)
    data = t2m.flatten()
    import math
    minVal = math.floor(min(data))
    maxVal = math.floor(max(data))
    print(f"min and max are {minVal}, {maxVal}")
    #clev = np.arange(round(minVal,2),round(maxVal,2),2)
    clev = np.array([-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6])
    #CARRA orig
    #CS = ax.contourf(lons,lats,t2m,transform=ccrs.PlateCarree(),colors=t_colors,levels=t_levels)
    CS = ax.contourf(lons,lats,t2m,transform=ccrs.PlateCarree(),cmap=plt.cm.coolwarm,levels=clev)
    #CS = ax.contour(lons,lats,t2m,transform=ccrs.PlateCarree()) #,cmap=plt.cm.coolwarm,levels=clev)
    plt.colorbar(CS,shrink=0.5,orientation='vertical')

    ax.coastlines('50m')
    ax.gridlines()

    plt.title(extra_title+" T2M \n%s UTC + %dh" % (dt.strftime('%Y-%m-%d %H:00'), fcstep))

    return fig

def wind_vel(ds):
    u = ds['params']['u10']['field']
    v = ds['params']['v10']['field']
    lons = ds['misc']['lons']
    lats = ds['misc']['lats']
    proj = ds['misc']['proj']
    dt = ds['misc']['date']
    fcstep = ds['misc']['fcstep']#
    PRJ = pyproj.Proj(proj.proj4_init)
    wind_speed = np.sqrt(u**2 + v**2)
    ws_levels = [5,10,15,20,25,30,40,50]
    jet = cm.get_cmap('jet',25)
    newcolors = jet(np.linspace(0, 1, 256))
    white = np.array([1,1,1,1])
    lightgrey = np.array([200/256,200/256,200/256,1])
    darkgrey = np.array([100/256,100/256,100/256,1])
    newcolors[0:5,:] = white
    newcolors[5:19, :] = lightgrey
    newcolors[19:38,:] = darkgrey
    newcmp = ListedColormap(newcolors)
    ny,nx = lons.shape
    sx = slice(0,nx,35)
    sy = slice(0,ny,35)
    fig = plt.figure(figsize=[12,9],edgecolor='k')
    ax = plt.axes(projection=proj)
    CS = ax.quiver(lons[sy,sx],lats[sy,sx],u[sy,sx],v[sy,sx],
                   scale=300,
                   transform=ccrs.PlateCarree(),
                   zorder=3)
    CS2 = ax.pcolormesh(lons,lats,wind_speed,
                      transform=ccrs.PlateCarree(),
                      cmap=newcmp,
                      vmin=0,vmax=40,
                      zorder=1,
                      alpha=0.9)
    plt.colorbar(CS2,shrink=0.5,orientation='vertical')
    ax.coastlines('50m',zorder=2)
    ax.gridlines()
    x0,y0 = PRJ(lons[0,0],lats[0,0])
    x1,y1 = PRJ(lons[-1,-1],lats[-1,-1])
    N = 10000
    ax.set_xlim(x0-N,x1+N)
    ax.set_ylim(y0-N,y1+N)
    plt.title("Wind velocity \n%s UTC + %dh" % (dt.strftime('%Y-%m-%d %H:00'), fcstep))
    return fig

