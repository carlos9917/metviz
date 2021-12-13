# Combine 3 images in 1
import os
from PIL import Image
import matplotlib.pyplot as plt 
def paste_images(fig1,fig2,fig3,outfig,imgsize=(3000,1000)) -> None:
    coords_fig1 = (0, 0)
    coords_fig2 = (1000,0)
    coords_fig3 = (2000,0)
    # opening up of images
    img1 = Image.open(fig1)
    img2 = Image.open(fig2)
    img3 = Image.open(fig3)
    # creating a new image and pasting the
    # images
    img = Image.new("RGB",imgsize,"white") #Image.new("RGB", (250, 180), "white")
    
    # pasting the first image (image_name,
    # (position))
    img.paste(img1, coords_fig1)
    # pasting the second image (image_name,
    # (position))
    img.paste(img2, coords_fig2)
    img.paste(img3, coords_fig3)
    #plt.imshow(img2)
    img.save(outfig)
if __name__=="__main__":
    import argparse
    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(description='''
            Example usage: python3 combine_images.py -img img1.png,img2.png,img3.png''',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-figs',help="List of images, separated by commas (currently only 3)",
                        type=str,
                        default=None,
                        required=True)
    parser.add_argument('-fout',help="Name of output file",
                        type=str,
                        default=None,
                        required=True)

    args = parser.parse_args()
    fig1,fig2,fig3 = args.figs.split(",")[0],args.figs.split(",")[1], args.figs.split(",")[2]
    fout = args.fout
    #fig1 =os.path.join(figpath,fig1)
    #fig2 = os.path.join(figpath,fig2)
    #fig3 = os.path.join(figpath,fig3)
    paste_images(fig1,fig2,fig3,fout)
