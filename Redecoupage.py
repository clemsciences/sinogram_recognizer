# -*- coding: cp1252 -*-
"""D'autres filtres"""
import math
import Image
import ImageDraw
import ImageOps
import time
import ImageFilter



def optimiser_decoupage(n, taille):
    a = 0
    b = 0
    for i in range(n[0], taille[0]):
        if taille[0]%float(i) == 0:
            a = i
            break
    for i in range(n[1], taille[1]):
        if taille[1]%float(i) == 0:
            b = i
            break
    return (a,b)
def moyenne(n, c , image):
    image = ImageOps.grayscale(image)
    pixels = image.load()
    somme = 0
    for i in range(c[0]*n[0], (c[0]+1)*n[0]):
        for j in range(c[1]*n[1], (c[1]+1)*n[1]):
            try:
                somme = pixels[i,j]+somme
            except:
                print c[0], n[0]
                print i,j
    return (somme /float(n[0]*n[1]))

def diminuer_information(image, n):
    """n est un tuple dont les valeurs sont """
    d = {}
    pixels = image.load()
    ny = Image.new("L", image.size)
    za = ImageDraw.Draw(ny)
    for i in range(image.size[0]/n[0]):
        for j in range(image.size[1]/n[1]):
            d[str(i)+str(j)] = moyenne(n,(i,j), image)
    return d
def diminuer_image(image, n):
    n = optimiser_decoupage(n, image.size)
    print n
    d = diminuer_information(image, n)
    ny = Image.new("L", image.size)
    za = ImageDraw.Draw(ny)
    for i in range(image.size[1]):
        for j in range(image.size[0]):
            za.point((i,j), fill = d[str(i/n[0])+str(i/n[0])])
    return ny
def reduire_encadrement(image, a,b):
    """on obtient la restriction de l'image � un rectangle de coin sup�rieur gauche de coordonn�e a et de coin inf�rieur droite de coordonn�e b"""
    pixels = image.load()
    ny = Image.new("L", image.size)
    za = ImageDraw.Draw(ny)
    for x in range(b[0] - a[0]):
        for y in range(a[1] - b[1]):
            za.point((x,y), fill = pixels[x,y])
    return ny