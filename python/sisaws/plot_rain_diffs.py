'''
Make some plots for the SISAWS experiments
Based on the scripts I used for the CDS plots for CARRA.
Still using basemap here, just for convenience,
but I should move this to cartopy
'''

import pygrib
import numpy as np
import math
import matplotlib
#matplotlib.use('TkAgg')
#matplotlib.use('qt4agg')
matplotlib.use('Agg')
import subprocess
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import interp
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
# Path to Grib data
#root_fig = dom+'_'
#TIME="2021/08/14/12/"
#dom="IGB"
#testcase="ref"
#variable = "Rain"
#var_img="Rain"
#vlevel = 0
#unit = ''
#level_step=1
#HOUR1="0005"
#HOUR2="0006"
#outpath='.'
only_check = False
plot_diffs = False
root_fig = "_".join(['diff',testcase,HOUR1,HOUR2,var_img,TIME.replace("/","")])
def chmod_fig(image_path):
    cmd = "chmod 755 "+image_path
    try:
        ret=subprocess.check_output(cmd,shell=True)
    except subprocess.CalledProcessError as err:
        print("Error in subprocess {}".format(err))

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
    #chmod_fig(saved_location)
    #cropped_image.show()
    rotated_image = image.rotate(-23)
    saved_location=image_path.replace(".png","_rotated.png")
    rotated_image.save(saved_location)
    #chmod_fig(saved_location)


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
    #print("min and max lat {} {}".format(southLat,northLat))
    #print("min and max lon {} {}".format(eastLon,westLon))

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

def plotting(lons, lats, data, name, unit, level_step, color,dom,image_path):
    """
    plotting europ map
    Input are lons=longitude, lats = latitude, data = data sets, name = parameter name, 
    unit = parameter unit, color = colors, ensemble = true/false
    Return a figure for each parameter
    """
    plt.figure(figsize=(10, 10))   
    ax = plt.subplot(111)
    #To check where the center of the map is located
    check_center=centerMap(lats.flatten(),lons.flatten(),1)
    #print("Center of the {} map: (lat0,lon0) {}".format(dom,check_center))
    if dom=="IGB":
        m = Basemap(llcrnrlon=-55, llcrnrlat=55.8, urcrnrlon=80, urcrnrlat=80, lat_1=72, lat_0=72., lon_0=-36, resolution='h', projection='lcc')
    elif dom=="East":
        m = Basemap(resolution="i", width=3850000,height=3850000,  projection='aea',\
                   lon_0=34,lat_0=73.8,lat_1=70)
    x, y = m(lons, lats)
    #convert data to Celsius DO NOT DO IF CALC DIFF
    if name == 'Temperature' and not "diff" in image_path:
        data = data - 273.15 
    # Plot data
    import matplotlib as mpl
    cmap = mpl.cm.coolwarm
    cmap = mpl.cm.RdBu_r
    print("min and max of data {} {}".format(min(data.flatten()),max(data.flatten())))
    import math
    minVal = math.floor(min(data.flatten()))
    maxVal = math.ceil(max(data.flatten()))
    #print("Making diffs symmetric")
    #if abs(minVal) > abs(maxVal): maxVal = abs(minVal)
    #if abs(maxVal) > abs(minVal): minVal = -maxVal
    print(f"min and max are now {minVal} {maxVal}")


    norm = mpl.colors.Normalize(vmin=minVal, vmax=maxVal)
    cmap = mpl.cm.coolwarm
    #clev = np.arange(minVal-2,maxVal+2,level) #0.001)
    clev = np.arange(minVal,maxVal,level_step) #0.001)
    #print("Plotting in levels {}".format(clev))
    CS_tmp = m.contourf(x,y,data,cmap=plt.cm.coolwarm) #,levels=level)
    #CS_tmp = m.contourf(x,y,data,clev,cmap=plt.cm.coolwarm) #,levels=level)
    #CS_tmp = m.contourf(x,y,data,cmap=plt.cm.coolwarm) #,levels=level)
    clb = plt.colorbar(CS_tmp,fraction=0.03 )#,ticks=use_ticks)
    #clb.ax.set_title(unit,labelpad=-1)
    clb.set_label(unit, labelpad=2)
    #clb.set_label("m/s", rotation=270)
    #cb.ax.set_title("Test 2")

    #clb = plt.colorbar(CS_tmp,fraction=0.042, pad=0.04,ticks=[-50,-40,-30,-20,-10,0,10,20])
    #from mpl_toolkits.axes_grid1 import make_axes_locatable
    #axes = plt.gca()
    #divider = make_axes_locatable(axes)
    #cax = divider.append_axes("right", size="5%", pad=0.05)
    #cax = plt.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height])
    #clb=plt.colorbar(CS_tmp, cax=cax,ticks=[-50,-40,-30,-20,-10,0,10,20])
    
    # Countries and coasts lines
    m.drawcountries(linewidth=0.4, color='k', zorder=4)
    m.drawcoastlines(linewidth=0.4, color='k', zorder=4)

    # Grid
    parallels = np.arange(0.,81,5.)
    m.drawparallels(parallels,labels=[True,False,False,False], fontsize=15, labelstyle='+/-', linewidth=0.2)
    meridians = np.arange(0.,360.,5.)
    m.drawmeridians(meridians,labels=[False,False,False,True], fontsize=15, labelstyle='+/-', linewidth=0.2)

    # fig.axes.get_xaxis().set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Title and labels
    #plt.title(name, fontsize=20) #,position=(1208090,1585877))
    if dom == 'West':
        plt_title=name
    else:
        plt_title=""
    plt.text(0.5,0.8,plt_title,fontsize=20,transform=ax.transAxes,
       horizontalalignment='center', verticalalignment='center')
    plt.ylabel(u'latitude', fontsize=20, labelpad=45)
    plt.xlabel(u'longitude', fontsize=20, labelpad=25)
    #clb.ax.set_title('['+ unit + ']', fontdict = {'fontsize': 15}, pad=5)
    
    # Save figure
    plt.tight_layout()
    plt.savefig(image_path)
    #print(f">>>>>> Using {root_fig}")
    #print(f"Output in {image_path}")
    plt.close('all')
    #return image_path

if __name__ == '__main__':
    #root_grib='/scratch/ms/dk/nhd/SISAWS/IGB/data/'

    print("Plotting rain diffs")
    grib1 = os.path.join(root_grib,'IGB_S3_'+testcase,TIME,'PRECIP+'+HOUR1+'_IGB_S3_'+testcase+'.grib')
    grib2 = os.path.join(root_grib,'IGB_S3_'+testcase,TIME,'PRECIP+'+HOUR2+'_IGB_S3_'+testcase+'.grib')
    print(f"Doing difference between {grib1} and {grib2}")
    grbs1 = pygrib.open(grib1)
    grbs2 = pygrib.open(grib2)
    vlevel = 0
    for grb in grbs1:
       print(grb.level)
       if grb.name == variable and grb.level==vlevel:
           data1 = grb.values
           lats, lons = grb.latlons()
           name = variable # +"_"+ TIME.replace("/","")#grb.name # + " 01/01/2019 06:00 AM"
           color = 'RdBu_r'
           break
    
    for grb in grbs2:
       if grb.name == variable and grb.level==vlevel:
           data2 = grb.values
           break
    data=data2-data1
    image_path = os.path.join(outpath,root_fig + '.png') 
    plotting(lons, lats, data, name, unit, level_step, color,dom,image_path)
    #chmod_fig(image_path)
    crop_image(image_path,coords=(220,160,1000,1000))
