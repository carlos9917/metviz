# Combine 3 images in 1
import os
from PIL import Image
import matplotlib.pyplot as plt 
def paste_images(fig1,fig2,fig3,imgsize=(2500,1000)): -> None:
    # opening up of images
    img1 = Image.open(fig1)
    img2 = Image.open(fig2)
    img3 = Image.open(fig3)
    # creating a new image and pasting the
    # images
    img = Image.new("RGB",imgsize,"white") #Image.new("RGB", (250, 180), "white")
    
    # pasting the first image (image_name,
    # (position))
    img.paste(img1, (0, 0))
    # pasting the second image (image_name,
    # (position))
    img.paste(img2, (800, 0))
    img.paste(img3, (1600, 0))
    #plt.imshow(img2)
    img.save(outfig)
if __name__=="__main__":
    import argparse
    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(description='''
            Example usage: python3 combine_images.py -img img1.png,img2.png,img3.png''',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-img',help="List of images, separated by commas (currently only 3)",
                        type=str,
                        default=None,
                        required=True)

    args = parser.parse_args()
    fig1,fig2,fig3 = args.img.split()[0],args.img.split()[1], args.img.split()[2]
    #fig1 =os.path.join(figpath,fig1)
    #fig2 = os.path.join(figpath,fig2)
    #fig3 = os.path.join(figpath,fig3)
    paste_images(fig1,fig2,fig3)
