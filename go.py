from PIL import Image
import PIL
import os
from utils.wskazniki import *
testers = []


#************* Paramki i inny shit (tu se pozmieniac pod siebie)
FOLDER_IN = 'in'
FOLDER_OUT = 'out'

# w pixlach , i dla kazdego porownania to samo bo jestem leniwy af
cutout_coords = (200, 200) #x, y lewy gorny rog wycinka
cutout_size = (150, 150) #x, y rozmiar wycinka

class JPG:
    def getNext(self, fnameIn, imageIn):
        for q in [10, 25, 50, 75, 95]:  # iteruj po tych wartosciach kułaliti
            args = {'quality': q}
            name = 'q_%u.jpg' % q  # jak w printf
            yield (name, args)

class JPEG2000:
    def getNext(self, fnameIn, imageIn):
        for q in [1, 2, 4, 8]:  # iteruj po tych wartosciach kułaliti ktos wie jak to sie ma do tego zrypanego programiku ??
            args = {'quality_mode': 'rates', 'quality_layers':[q]}
            name = 'q_%u.jp2' % q  # jak w printf
            yield (name, args)

class GIF:
    def getNext(self, fnameIn, imageIn):
        for q in [3, 15, 50, 100, 200, 255]:  # iteruj po tych ilosciach kolorow
            args = {'Xpaleta': q}
            name = 'kol_%u.gif' % q  # jak w printf
            yield (name, args)

class PNG:
    def getNext(self, fnameIn, imageIn):
        for q in [1, 3, 5, 7, 9]:  # iteruj po tych wartosciach kułaliti
            args = {'compress_level': q}
            name = 'q_%u.png' % q  # jak w printf
            yield (name, args)


testers.append(JPG)
testers.append(JPEG2000)
testers.append(GIF)
testers.append(PNG)



#************* Programik



if not os.path.exists(FOLDER_OUT):
    os.mkdir(FOLDER_OUT)



filenames_in = os.listdir(FOLDER_IN)

pictures_in = []
for x in filenames_in:
    pictures_in.append(Image.open(os.path.join(FOLDER_IN, x)))


def wytnijladniepls(oryginal, nieoryginal, tuzapisz):
    tmp = Image.new('RGB', (cutout_size[0]*2,cutout_size[1]))
    box = (cutout_coords[0], cutout_coords[1], cutout_coords[0] + cutout_size[0], cutout_coords[1] + cutout_size[1])
    region1 = nieoryginal.crop(box)
    region2 = oryginal.crop(box)
    tmp.paste(region1, (0,0,cutout_size[0], cutout_size[1]))
    tmp.paste(region2, (cutout_size[0],0,  cutout_size[0]*2,cutout_size[1] ))
    tmp.save(tuzapisz)
    #print (tuzapisz)

for gen in testers:
    print ("+-------------------- %s --------------------+ " % gen.__name__)
    subpath = os.path.join(FOLDER_OUT, gen.__name__)
    if not os.path.exists(subpath):
        os.mkdir(subpath)
    for i in range(len(filenames_in)):
        fname_in = filenames_in[i]
        pictures_in[i].copy().convert("RGB").save('tmp.bmp')
        size_in = os.stat('tmp.bmp').st_size
        base, ext = os.path.splitext(fname_in)
        if not os.path.exists(os.path.join(subpath, base)):
            os.mkdir(os.path.join(subpath, base))
        print ("+-- Using %s (%.1fkB) --+" % (fname_in, size_in/1024))
        gen_o = gen()

        for name, kwargs in gen_o.getNext(fname_in, pictures_in[i].copy()):
            fname = os.path.join(subpath, base, name)

            pictures_in[i].copy().convert("RGB").save(fname, **kwargs)
            if "Xpaleta" in kwargs:
                pictures_in[i].copy().convert("RGB").quantize(colors=kwargs["Xpaleta"]).save(fname, **kwargs)

            pic_out = Image.open(fname)
            size_out = os.stat(fname).st_size
            wytnijladniepls(pictures_in[i].copy().convert("RGB"), pic_out.copy().convert("RGB"), os.path.join(subpath, base, name + '.comp.png'))

            #wskazniki
            kompresja = 100 - (float(size_out)/float(size_in))*100 #wzur od AnJ
            psnr_v = psnr(pictures_in[i].copy(), pic_out)
            mae_v = mae(pictures_in[i].copy(), pic_out)

            print ("%s | %.1fkB | kompresja: %.1f%% | PSNR: %.3f dB | MAE: %.3f" % (name, size_out/1024, kompresja, psnr_v, mae_v))

