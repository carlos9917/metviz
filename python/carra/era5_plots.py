import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import os
import pandas as pd
from datetime import datetime
import gc
import sys
OUTDIR="means_era5"

year="2020"
month="01"
#era5_file=f"./means_era5/{year}/{month}/monthly_mean_era5_an_sfc_{year}{month}.nc"
def plot_t2m_daily(era5_file,sizex=16,sizey=12,var="t2m"):
    ds = xr.open_dataset(era5_file) #,engine="scipy")
    ds_180 = ds.assign_coords(longitude=(((ds.lon + 180) % 360) - 180)).sortby('longitude')
    # Create Xarray Data Array
    da = ds_180[var]
    da_degc = da - 273.15
    min_val = da_degc.min().values.flatten()[0]
    max_val = da_degc.max().values.flatten()[0]
    #print(f"min and max: {min_val}, {max_val}")
    for k,time in enumerate(da_degc.time):
        this_time = pd.to_datetime(time.values)
        time_str = datetime.strftime(this_time,"%Y-%m-%d")
        fig, ax = plt.subplots(1, 1, figsize = (10, 8), subplot_kw={'projection': ccrs.PlateCarree()})
        # Plot the data
        min_val = da_degc[k,:,:].min().values.flatten()[0]
        max_val = da_degc[k,:,:].max().values.flatten()[0]
        print(f"min and max on {time_str}: {min_val}, {max_val}")
        im = plt.pcolormesh(da_degc.lon, da_degc.lat, da_degc[k,:,:], cmap='RdBu_r', vmin=-80, vmax=48) 
        
        # Set the figure title, add lat/lon grid and coastlines
        ax.set_title(f'ERA5 daily {var} for {time_str}', fontsize=16)
        ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--') 
        ax.coastlines(color='black')
        #ax.set_extent([-25, 40, 34, 72], crs=ccrs.PlateCarree())
        
        # Specify the colourbar
        #cbar = plt.colorbar(im,fraction=0.05, pad=0.04)
        cbar = plt.colorbar(im,fraction=0.05, pad=0.04,orientation="horizontal")
        cbar.set_label('Temperature (C)') 
        
        # Save the figure
        fig.savefig(os.path.join(OUTDIR,f'daily_'+var+f'_era5_{time_str}.png'))
        fig.clf()
        plt.close(fig)
        gc.collect()

def plot_t2m(era5_file,sizex=16,sizey=12,var="t2m"):
    ds = xr.open_dataset(era5_file,engine="scipy")
    ds_180 = ds.assign_coords(longitude=(((ds.longitude + 180) % 360) - 180)).sortby('longitude')
    # Create Xarray Data Array
    da = ds_180[var] #['t2m']
    da_degc = da - 273.15
    #months from 1-2 years 2012 to 2021
    da_degc = da_degc.assign_attrs(da.attrs)
    da_degc.attrs['units'] = '° C'
    for k,time in enumerate(da_degc.time):
        this_time = pd.to_datetime(time.values)
        time_str = datetime.strftime(this_time,"%Y-%m-%d")
        period = datetime.strftime(this_time,"%Y%m")
        # create the figure panel and the map using the Cartopy PlateCarree projection
        fig, ax = plt.subplots(1, 1, figsize = (10, 8), subplot_kw={'projection': ccrs.PlateCarree()})
        # Plot the data
        im = plt.pcolormesh(da_degc.longitude, da_degc.latitude, da_degc[k,:,:], cmap='RdBu_r', vmin=-80, vmax=48) 
        
        # Set the figure title, add lat/lon grid and coastlines
        ax.set_title(f'ERA5 Monthly 2m temperature for {period}', fontsize=16)
        ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--') 
        ax.coastlines(color='black')
        #ax.set_extent([-25, 40, 34, 72], crs=ccrs.PlateCarree())
        
        # Specify the colourbar
        #cbar = plt.colorbar(im,fraction=0.05, pad=0.04)
        cbar = plt.colorbar(im,fraction=0.05, pad=0.04,orientation="horizontal")
        cbar.set_label('Temperature (C)') 
        
        # Save the figure
        fig.savefig(os.path.join(OUTDIR,f'monthly_t2m_era5_{period}.png'))
        fig.clf()
        plt.close(fig)
        gc.collect()

def plot_tp(era5_file,sizex=16,sizey=12):
    ds = xr.open_dataset(era5_file,engine="scipy")
    ds_180 = ds.assign_coords(longitude=(((ds.longitude + 180) % 360) - 180)).sortby('longitude')
    da = ds_180['tp']*1000
    for k,time in enumerate(da.time):
        this_time = pd.to_datetime(time.values)
        time_str = datetime.strftime(this_time,"%Y-%m-%d")
        period = datetime.strftime(this_time,"%Y%m")
        # create the figure panel and the map using the Cartopy PlateCarree projection
        fig, ax = plt.subplots(1, 1, figsize = (sizex, sizey), subplot_kw={'projection': ccrs.PlateCarree()})
        # Plot the data
        im = plt.pcolormesh(da.longitude, da.latitude, da[k,:,:], cmap='RdBu_r', vmin=0, vmax=80) 
        
        # Set the figure title, add lat/lon grid and coastlines
        ax.set_title(f'Mean of monthly total precipitation for {period}', fontsize=16)
        ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--') 
        ax.coastlines(color='black')
        #ax.set_extent([-25, 40, 34, 72], crs=ccrs.PlateCarree())
        
        # Specify the colourbar
        cbar = plt.colorbar(im,fraction=0.05, pad=0.04,orientation="horizontal")
        cbar.set_label('Total precipitation (kg/m2)') 

        # Save the figure
        fig.savefig(os.path.join(OUTDIR,f'monthly_tp_era5_{period}.png'))
        fig.clf()
        plt.close(fig)
        gc.collect()

if __name__=="__main__":
    #era5_file=os.path.join(OUTDIR,"./era5_monthly_t2m_greenland.nc")
    #plot_t2m(era5_file,sizex=16,sizey=12,var="t2m"):


    era5_file=os.path.join(OUTDIR,"./era5_monthly_t2m_greenland.nc")
    era5_file = os.path.join(OUTDIR,"daily_mean_tmax_era5_202301.nc")
    #plot_t2m_daily(era5_file,sizex=16,sizey=12,var="mx2t")
    plot_t2m_daily(era5_file,sizex=16,sizey=12,var="mx2t")

    #era5_file=os.path.join(OUTDIR,"./era5_monthly_totprec_greenland.nc")
    #plot_tp(era5_file)
