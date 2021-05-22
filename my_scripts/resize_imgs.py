from PIL import Image
import os, sys

path = "./"
dirs = os.listdir(path)

def resize():
    for item in dirs:
        fullName = os.path.abspath(path+item)
        f, ext = os.path.splitext(fullName)
        print(fullName)
        if os.path.isfile(fullName) and ext == ".png":
            im = Image.open(fullName)
            w, h = im.size
            newH = int(h * 320.0 / w)
            print(w, h, newH)
            imResize = im.resize((320, newH), Image.ANTIALIAS)
            print(fullName)
            imResize.save(f + '_small.png', 'png', quality=90)

resize()