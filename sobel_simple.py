# -*- coding: cp1252 -*-
import algo_complexes
print "départ"
from PIL import Image, ImageOps
from FILTRES import *
from traitement_image import *
a = Image.open("D:\IMG_6730.jpg")
a = ImageOps.grayscale(a)

#a = algo_complexes.algo_sobel(a)
a = double_convolution(a, COIN_X, COIN_Y)
a.save("C:\Users\Clément-B\Desktop\oo.jpg")
