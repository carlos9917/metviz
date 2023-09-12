import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import os
import pandas as pd
from datetime import datetime
import gc
import sys
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def get_codes(param) -> dict():
    if param == "mslp":
        params = {'mlsp':{"param":"151","level":0,"typeOfLevel":"meanSea","levelType":"sfc"}}
    elif param == "t2m":
        params = {'t2m':{"param":"167","level":2,"typeOfLevel":"heightAboveGround","levelType":"sfc"}}
    elif param == "tp":
        params = {'tp':{"param":"228228","level":0,"typeOfLevel":"surface","levelType":"sfc"}}
    elif param == "mn2t":
        params = {'mn2t':{"param":"202","level":2,"typeOfLevel":"heightAboveGround","levelType":"sfc"}}
    elif param == "mx2t":
        params = {'mx2t':{"param":"201","level":2,"typeOfLevel":"heightAboveGround","levelType":"sfc"}}
    else:
        print(f"Parameter {param} not found!")
        sys.exit(1)
    return params


#era5_file=f"./means_era5/{year}/{month}/monthly_mean_era5_an_sfc_{year}{month}.nc"

import copy
import pygrib
import numpy.ma as ma
import datetime
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

def read_vars(gribfile,params):
    '''
    Reads a file that contains only one time step
    '''
    ds = {}
    vars = copy.deepcopy(params)
    f = pygrib.open(gribfile)
    was_found=False
    for msg in f:
        for param in vars:
            if vars[param]['param']== str(msg['param']) and vars[param]["level"]==msg["level"] and vars[param]["typeOfLevel"]==msg['typeOfLevel'] and vars[param]["levelType"]==msg["levelType"]:
                print(f'found {vars[param]}')
                vars[param]['msg'] = msg
                was_found=True
        if not was_found:
            #quick check for when it doesnt find anything
            for param in vars:
                print(vars[param]['param'])
                if vars[param]['param']== str(msg['param']):
                    print(f"{param} not found. Printing some info")
                    this_param=msg["param"]
                    this_level=msg["level"]
                    this_tlevel=msg['typeOfLevel']
                    this_ltype=msg["levelType"]
                    print("level :{this_level}")
                    print("typeOfLevel {this_tlevel}")
                    print("levelType {this_ltype}")
                    print("Original params:")
                    print(params)
                    for key in ["param","level","typeOfLevel","levelType"]:
                        new_params = {param:{"param":this_param,"level":this_level,
                                             "typeOfLevel":this_tlevel,"levelType":this_ltype}}
                    print(new_params)
                    sys.exit(0)

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

def plot_t2minmax(ds,period,sizex=18,sizey=14):
    lons = ds['misc']['lons']
    lats = ds['misc']['lats']
    proj = ds['misc']['proj']
    dt = ds['misc']['date']
    fcstep = ds['misc']['fcstep']
    variable = [key for key in ds["params"].keys()][0]
    t2m = ds['params'][variable]['field'] - 273.15
    print(f"Min and max for {variable}: {t2m.min()} {t2m.max()}")
    fig = plt.figure(figsize=(sizex,sizey))
    ax = plt.axes(projection=ccrs.PlateCarree())

    #CS = ax.contourf(lons,lats,t2m,transform=ccrs.PlateCarree(),colors=t_colors,levels=t_levels)
    im = plt.pcolormesh(lons,lats, t2m, cmap='RdBu_r', vmin=-80, vmax=48) 
    ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--') 
    ax.coastlines(color='black')
    ax.set_title(f'CARRA daily {variable} for {period}', fontsize=16)
    # Specify the colourbar
    cbar = plt.colorbar(im,fraction=0.05, pad=0.04,orientation="horizontal")
    cbar.set_label('Temperature (C)')
    fig.savefig(os.path.join(OUTDIR,f'daily_{variable}_carra_{period}.png'))
    fig.clf()
    plt.close(fig)
    gc.collect()

def plot_t2m(ds,period,sizex=18,sizey=14):
    lons = ds['misc']['lons']
    lats = ds['misc']['lats']
    proj = ds['misc']['proj']
    dt = ds['misc']['date']
    fcstep = ds['misc']['fcstep']

    variable = [key for key in ds["params"].keys()][0]
    t2m = ds['params'][variable]['field'] - 273.15
    print(f"Min and max for {variable}: {t2m.min()} {t2m.max()}")

    fig = plt.figure(figsize=(sizex,sizey))
    ax = plt.axes(projection=ccrs.PlateCarree())

    #CS = ax.contourf(lons,lats,t2m,transform=ccrs.PlateCarree(),colors=t_colors,levels=t_levels)
    im = plt.pcolormesh(lons,lats, t2m, cmap='RdBu_r', vmin=-80, vmax=48) 
    ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--') 
    ax.coastlines(color='black')
    ax.set_title(f'CARRA monthly 2m temperature for {period}', fontsize=16)
    # Specify the colourbar
    #cbar = plt.colorbar(im,fraction=0.05, pad=0.04)
    cbar = plt.colorbar(im,fraction=0.05, pad=0.04,orientation="horizontal")
    cbar.set_label('Temperature (C)')
    #plt.colorbar(CS,shrink=0.5,orientation='vertical')
    #ax.coastlines('50m')
    #ax.gridlines()
    ##plt.title("T2M \n%s UTC + %dh" % (dt.strftime('%Y-%m-%d %H:00'), fcstep))
    #period=dt.strftime('%Y%m')
    #plt.title(f"{variable} {period}")
    fig.savefig(os.path.join(OUTDIR,f'monthly_t2m_carra_{period}.png'))
    fig.clf()
    plt.close(fig)
    gc.collect()



def plot_tp(ds,period,sizex=18,sizey=14):
    lons = ds['misc']['lons']
    lats = ds['misc']['lats']
    proj = ds['misc']['proj']
    dt = ds['misc']['date']
    fcstep = ds['misc']['fcstep']

    variable = [key for key in ds["params"].keys()][0]
    tp = ds['params'][variable]['field']
    print(f"Min and max for tp: {tp.min()} {tp.max()}")
    fig = plt.figure(figsize=(sizex,sizey))
    ax = plt.axes(projection=ccrs.PlateCarree())

    #CS = ax.contourf(lons,lats,tp,transform=ccrs.PlateCarree(),colors=t_colors,levels=t_levels)
    im = plt.pcolormesh(lons,lats, tp, cmap='RdBu_r', vmin=0, vmax=80) 
    ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--') 
    ax.coastlines(color='black')
    ax.set_title(f'CARRA monthly total precipitation for {period}', fontsize=16)
    # Specify the colourbar
    #cbar = plt.colorbar(im,fraction=0.05, pad=0.04)
    cbar = plt.colorbar(im,fraction=0.05, pad=0.04,orientation="horizontal")
    cbar.set_label('Total precipitation (kg/m2)')
    #plt.colorbar(CS,shrink=0.5,orientation='vertical')
    #ax.coastlines('50m')
    #ax.gridlines()
    ##plt.title("T2M \n%s UTC + %dh" % (dt.strftime('%Y-%m-%d %H:00'), fcstep))
    #period=dt.strftime('%Y%m')
    #plt.title(f"{variable} {period}")
    fig.savefig(os.path.join(OUTDIR,f'monthly_tp_carra_{period}.png'))
    fig.clf()
    plt.close(fig)
    gc.collect()

def plot_tp_mslp(ds,period,sizex=18,sizey=14):

if __name__=="__main__":
    OUTDIR="means_gribmean"
    from pathlib import Path
    year="2012"
    params = {'t2m':{"param":"167","level":2,"typeOfLevel":"heightAboveGround","levelType":"sfc"}}
    for month in range(1,7):
        period=year+str(month).zfill(2)    
        #monthly_mean_no-ar-cw_an_sfc_201201.grib2
        gfile=os.path.join(OUTDIR,year,"monthly_mean_no-ar-cw_an_sfc_"+period+".grib2")
        ds = read_vars(gfile,params)   
        plot_t2m(ds,period)
    
    sys.exit(0)

    year="2023"
    params = {'tp':{"param":"228228","level":0,"typeOfLevel":"surface","levelType":"sfc"}}
    for month in range(1,7):
        period=year+str(month).zfill(2)    
        gfile=os.path.join(OUTDIR,year,"monthly_mean_accum_no-ar-cw_fc_sfc_"+period+".grib2")
        ds = read_vars(gfile,params)   
        plot_tp(ds,period)
    sys.exit(0)

    year="2023"
    gfile = os.path.join(OUTDIR,year,"daily_mean_no-ar-cw_fc_sfc_20230101.grib2")
    params = {'mn2t':{"param":"202","level":2,"typeOfLevel":"heightAboveGround","levelType":"sfc"}}
    params = {'mx2t':{"param":"201","level":2,"typeOfLevel":"heightAboveGround","levelType":"sfc"}}
    ds = read_vars(gfile,params)   
    period="2023-01-01"
    plot_t2minmax(ds,period)

    #era5_file=os.path.join(OUTDIR,"./era5_monthly_t2m_greenland.nc")
    #plot_t2m(era5_file)
    #era5_file=os.path.join(OUTDIR,"./era5_monthly_totprec_greenland.nc")
    #plot_tp(era5_file)
