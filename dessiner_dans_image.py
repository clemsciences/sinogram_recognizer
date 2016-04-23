# -*- coding: cp1252 -*-
from traitement_image import *
from trouver_brillant import *


def dessiner_bord(image, l_points):
    im = image
    t = len(l_points)
    for i in l_points:
        im = dessiner_droite(im, i[1], math.radians(i[0]))
        time.sleep(3)
    return im


def dessiner_droite(image, rho, theta):
    couleur = (30,30,255)
    longueur, hauteur = image.size
    za = ImageDraw.Draw(image)
    pixels = image.load()
    
    if theta % math.pi == 0:
        for y in range(hauteur):
            za.point((int(rho), y), fill=couleur)
    else:
        for x in range(longueur):
            y = int(-math.cos(theta)/math.sin(theta)*x + rho/math.sin(theta))
            if y > hauteur or y < 0:
                pass
            else:
                za.point((x, y), fill=couleur)
    return image
