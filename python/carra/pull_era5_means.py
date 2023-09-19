#!/usr/bin/env python
import cdsapi
import os
URL = 'https://cds.climate.copernicus.eu/api/v2'
KEY = os.getenv("CDS_UID")
c = cdsapi.Client()
DATADIR = './means_era5' #path where the data will be downloaded
years=[str(i) for i in range(2012,2022)]
years = ["2013"]
times = [str(i).zfill(2)+":00" for i in range(22)]
months = [str(i).zfill(i) for i in range(13)]
area_greenland = [85,-75,60,-10]
out_cds=os.path.join(DATADIR,"era5_monthly_t2m_greenland.nc")
print("Doing temperature")
if not os.path.isfile(out_cds):
    c.retrieve(
        'reanalysis-era5-single-levels-monthly-means',
        {
            'product_type': 'monthly_averaged_reanalysis',
            'variable': '2m_temperature',
            'year': years,
            "month" : months,
            #'month': [
            #    '01', '02', '03',
            #    '04', '05', '06',
            #    '07', '08', '09',
            #    '10', '11', '12',
            #],
            'time': times, #'00:00',
            'area': area_greenland,
            'format': 'netcdf',
        },
        out_cds)
else:
    print(f"{out_cds} already downloaded")


print("Doing tot prec")
out_cds=os.path.join(DATADIR,"era5_monthly_tp_mslp_greenland.nc")
if not os.path.isfile(out_cds):
    c.retrieve(
        'reanalysis-era5-single-levels-monthly-means',
        {
            'product_type': 'monthly_averaged_reanalysis',
            'variable': ['total_precipitation',"mean_sea_level_pressure"],
            'year': years,
            "month": months,
            #'month': [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', ],
            'time': times,#'00:00',
            'area': area_greenland,
            'format': 'netcdf',
        },
        out_cds)
else:
    print(f"{out_cds} already downloaded")
