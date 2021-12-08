'''
Make some plots for the CARRA CDS release
Based on the CERRA scripts provided by Semjon
'''

import pygrib

import numpy as np
import math

import matplotlib
matplotlib.use('Agg')

import cartopy.crs as ccrs

from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

#import cdo
from cdo import *
cdo   = Cdo()

# Path to Grib data
root_grib = 'IGB_S3_ref/2021/08/14/12/'
dom="IGB_S3_test"
root_fig = dom+'_'
grib = root_grib + 'ICMSHHARM+0003_IGB_S3_ref.grib'
grbs = pygrib.open(grib)
def crop_image(image_path,coords=(220,170,1000,1000)):
    from PIL import Image
    # the coordinates are given as top-left (x,y) and right-bottom (x,y)
    #0,0 is in the upper left corner of the domain!!!
    #things grow from there in "south east" direction
    image = Image.open(image_path)
    width, height = image.size
    print("Width and height: {},{}".format(width,height))
    left = 0
    top = 750 #height/2 # height / 4
    right = 500
    bottom = height # 3 * height / 4
    #coords=(left, top, right, bottom)
    #coords=(220,150,900,1000)
    print("Box: left-top, right-bottom {}".format(coords))
    cropped_image = image.crop(coords)
    saved_location=image_path.replace(".png","_cropped.png")
    cropped_image.save(saved_location)
    #cropped_image.show()


def centerMap(lats,lons,scale):
    '''
    Function to detect the center of the map
    '''
    import spheredistance as sd

    #Assumes -90 < Lat < 90 and -180 < Lon < 180, and
    # latitude and logitude are in decimal degrees
    earthRadius = 6378100.0 #earth's radius in meters

    northLat = max(lats)
    southLat = min(lats)
    westLon = max(lons)
    eastLon = min(lons)
    print("min and max lat {} {}".format(southLat,northLat))
    print("min and max lon {} {}".format(eastLon,westLon))

    # average between max and min longitude 
    lon0 = ((westLon-eastLon)/2.0)+eastLon

    # a = the height of the map
    b = sd.spheredist(northLat,westLon,northLat,eastLon)*earthRadius/2
    c = sd.spheredist(northLat,westLon,southLat,lon0)*earthRadius

    # use pythagorean theorom to determine height of plot
    mapH = pow(pow(c,2)-pow(b,2),1./2)
    arcCenter = (mapH/2)/earthRadius

    lat0 = sd.secondlat(southLat,arcCenter)

    # distance between max E and W longitude at most souther latitude
    mapW = sd.spheredist(southLat,westLon,southLat,eastLon)*earthRadius

    return lat0,lon0,mapW*scale,mapH*scale

def plotting(lons, lats, data, name, unit, level, color,dom):
    """
    A funktion to plotting europ map
    Input are lons=longitude, lats = latitude, data = data sets, name = parameter name, 
    unit = parameter unit, level =levels, color = colors, ensemble = true/false
    Return a figure for each parameter
    """
    plt.figure(figsize=(10, 10))   
    #ax = plt.subplot(111)
    #To check where the center of the map is located
    check_center=centerMap(lats.flatten(),lons.flatten(),1)
    print("Center of the {} map: (lat0,lon0) {}".format(dom,check_center))
    #lat0,lon0 = check_center(0),check_center(1)
    if dom=="West":
        #lat0,lon0 72.33888870843114, -35.988615420221564
        m = Basemap(llcrnrlon=-55, llcrnrlat=55.8, urcrnrlon=80, urcrnrlat=80, lat_1=72, lat_0=72., lon_0=-36, resolution='h', projection='lcc')
    elif dom=="East":
        #73.81490280472737, 34.112985883582525,
        #m = Basemap(llcrnrlon=10, llcrnrlat=65.8, urcrnrlon=90, urcrnrlat=80, lat_1=72, lat_0=73., lon_0=34., resolution='h', projection='lcc')
        #m = Basemap(llcrnrlon=0, llcrnrlat=45, urcrnrlon=90, urcrnrlat=80, lat_1=72, lat_0=73., lon_0=34., resolution='h', projection='lcc')
        # 170
        m = ccrs.LambertConformal(central_longitude = 34, central_latitude = 73.8)
    #x, y = m(lons, lats)
    #ax = plt.axes(projection=m)
    #matrixLon, matrixLat = np.meshgrid(lons, lats)
    #convert data to Celsius
    data = data - 273.15 
    # Plot data
    import matplotlib as mpl
    cmap = mpl.cm.coolwarm
    cmap = mpl.cm.RdBu_r
    print("min and max of data {} {}".format(min(data.flatten()),max(data.flatten())))
    minVal = min(data.flatten())
    maxVal = max(data.flatten())
    #minX = min(x.flatten())
    #minY = min(y.flatten())
    #maxX = max(x.flatten())
    #maxY = max(y.flatten())
    #print("min and max X {} {}".format(minX,maxX))
    #print("min and max Y {} {}".format(minY,maxY))
    #  min and max X -127648.8447510614 2543830.092723324
    # min and max Y 45336.648333039135 3217092.540390645

    clev = np.arange(minVal,maxVal,0.01)
    norm = mpl.colors.Normalize(vmin=minVal, vmax=maxVal)
    #CS_tmp = m.contourf(x,y,data,clev,cmap=plt.cm.coolwarm)
    CS_tmp = plt.contourf(lons,lats,data,transform=ccrs.PlateCarree())#,clev,cmap=plt.cm.coolwarm)

    clb = plt.colorbar(CS_tmp,fraction=0.03,ticks=[-50,-40,-30,-20,-10,0,10,20])
    
    # Countries and coasts lines
    #m.drawcountries(linewidth=0.4, color='k', zorder=4)
    #m.drawcoastlines(linewidth=0.4, color='k', zorder=4)

    # Grid
    #parallels = np.arange(0.,81,5.)
    #m.drawparallels(parallels,labels=[True,False,False,False], fontsize=15, labelstyle='+/-', linewidth=0.2)
    #meridians = np.arange(0.,360.,5.)
    #m.drawmeridians(meridians,labels=[False,False,False,True], fontsize=15, labelstyle='+/-', linewidth=0.2)

    # fig.axes.get_xaxis().set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Title and labels
    #plt.title(name, fontsize=20) #,position=(1208090,1585877))
    plt.text(0.5,0.8,name,fontsize=20,transform=ax.transAxes,
       horizontalalignment='center', verticalalignment='center')
    plt.ylabel(u'latitude', fontsize=20, labelpad=45)
    plt.xlabel(u'longitude', fontsize=20, labelpad=25)
    #clb.ax.set_title('['+ unit + ']', fontdict = {'fontsize': 15}, pad=5)
    
    # Save figure
    plt.tight_layout()
    image_path = root_fig + name.replace(' ', '_').replace('/', '_').replace(',', '').replace(':', '_') + '.png'
    plt.savefig(image_path)
    plt.close('all')
    return image_path

if __name__ == '__main__':
    #for grb in grbs: 
    #    level = grb.level
    #    name = grb.name
    #    print(f"{name} at level {level}")
    #sys.exit(0)
    variable="Temperature"
    vlevel = 2
    unit = "K"
    level_step = 10
    outpath="."

    for grb in grbs:
        if grb.name == variable and grb.level==vlevel:
            data = grb.values
            lats, lons = grb.latlons()
            name = grb.name # + " 01/01/2019 06:00 AM"
            color = 'RdBu_r'
            print('Plotting figure for: ' + name)
            image_path=plotting(lons, lats, data, name, unit, vlevel, color,dom)
           # image_path=plotting(lons, lats, data, name, unit, level_step, color,dom,outpath)
            #chmod_fig(image_path)
            #crop_image(image_path,coords=(220,160,1000,1000))
            sys.exit()

    #for grb in grbs:
    #    data = grb.values
    #    lats, lons = grb.latlons()
    #    name = grb.name # + " 01/01/2019 06:00 AM"
    #    level = [0] #,1,2,3,4,5,6,7,8,9,10,12,14,16,18,20,25,30,35,40]
    #    color = 'RdBu_r'
    #    #color = 'jet'
    #    unit = 'K' #'m/s'
    #    print('Plotting figure for: ' + name)        
    #    image_path=plotting(lons, lats, data, name, unit, level, color,dom)
    #    crop_image(image_path)
   

    



