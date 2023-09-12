import os
import sys
from PIL import Image
import matplotlib.pyplot as plt

def crop_image(image_path,coords=(220,170,1000,1000)):
    from PIL import Image
    # the coordinates are given as top-left (x,y) and right-bottom (x,y)
    #0,0 is in the upper left corner of the domain!!!
    #things grow from there in "south east" direction
    image = Image.open(image_path)
    width, height = image.size
    print("Width and height: {},{}".format(width,height))
    #left = 400
    #top = 0 #height/2 # height / 4
    #right = 1560
    #bottom = height # 3 * height / 4
    #coords=(left, top, right, bottom)
    #coords=(220,150,900,1000)
    print("Box: left-top, right-bottom {}".format(coords))
    cropped_image = image.crop(coords)
    saved_location=image_path.replace(".png","_cropped.png")
    cropped_image.save(saved_location)
    return saved_location
    #cropped_image.show()


def paste_images(fig1:str, fig2:str,outfig:str ,imgsize=(3200,1000),coord1=(0,-80),coord2=(1600,0)) -> None:
    coords_fig1 = coord1 #(0, -80)
    coords_fig2 = coord2 #(1600,0)
    # opening up of images
    img1 = Image.open(fig1)
    img2 = Image.open(fig2)
    # creating a new image and pasting the
    # images
    img = Image.new("RGB",imgsize,"white") #Image.new("RGB", (250, 180), "white")

    # pasting the first image (image_name,
    # (position))
    img.paste(img1, coords_fig1)
    # pasting the second image (image_name,
    # (position))
    img.paste(img2, coords_fig2)
    #plt.imshow(img2)
    img.save(outfig)
    return outfig

def combine_t2m(fig1,fig2,period):
    fig1=crop_image(fig1,(108,710,1746,1287))
    fig2=crop_image(fig2,(28,289,984,785))
    outfig=paste_images(fig1,fig2,out,(3000,800),(0,-80),(1600,0))
    out_cut=crop_image(outfig,(20,15,2583,580))

def combine_tp(fig1,fig2,period):
    fig1=crop_image(fig1,(81,789,1710,1346))
    fig2=crop_image(fig2,(44,429,1529,1151))
    outfig=paste_images(fig1,fig2,out,(3100,800),(0,80),(1600,0))
    out_cut=crop_image(outfig,(20,15,2583,580))

if __name__=="__main__":
    year = "2013"

    #combine only one day
    period="20230101"
    fig1 = os.path.join("means_gribmean","daily_mx2t_carra_2023-01-01.png")
    fig2 = os.path.join("means_era5","daily_mx2t_era5_2023-01-01.png")
    out = "maps_mx2t_"+period+".png"
    combine_t2m(fig1,fig2,period)
    sys.exit(0)


    for month in range(1,13):
        period = year+str(month).zfill(2)
        period = year + str(month).zfill(2)

        #fig1 = os.path.join("means_gribmean","monthly_t2m_carra_"+period+".png")
        #fig2 = os.path.join("means_era5","monthly_t2m_era5_"+period+".png")
        #out = "maps_t2m_"+period+".png"
        #combine_t2m(fig1,fig2,period)

        fig1 = os.path.join("means_gribmean","monthly_tp_carra_"+period+".png")
        fig2 = os.path.join("means_era5","monthly_tp_era5_"+period+".png")
        out = "maps_tp_"+period+".png"
        combine_tp(fig1,fig2,period)
