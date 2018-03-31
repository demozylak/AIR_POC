from PIL import Image
import PIL
import os


size = 256, 256
FOLDER_IN = 'in'
FOLDER_OUT = 'thummbnails'



if not os.path.exists(FOLDER_OUT):
    os.mkdir(FOLDER_OUT)


filenames_in = os.listdir(FOLDER_IN)


for infile in filenames_in:
    outfile = infile +".png"
    if infile != outfile:
        try:
            im = Image.open(os.path.join(FOLDER_IN, infile))
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(os.path.join(FOLDER_OUT, outfile), "PNG")
        except IOError:
            print ("cannot create thumbnail for '%s'" % infile)

