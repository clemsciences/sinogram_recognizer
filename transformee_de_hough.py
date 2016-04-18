# -*- coding: cp1252 -*-
import Image
import math
import ImageDraw
import ImageOps    
import math
import time
#(255, 255, 255) = blanc
#(0,0,0) = noir
"""
#Variante non finie
def transformer(image, seuil, balayage_theta):
    # Prend en paramètres une image pré-traitée (une image don't il ne reste que les contours) et un seuil qui est une entier naturel compris entre 0 et 255
    longueur, hauteur = image.size
    image = ImageOps.grayscale(image)
    pixels = image.load() 
    theta_m = math.atan(hauteur/float(longueur))
    print theta_m
    dim_espace_hough = (balayage_theta,2*int(longueur*math.cos(theta_m)+hauteur*math.sin(theta_m)))
    ampl_rho = int(longueur*math.cos(theta_m)+hauteur*math.sin(theta_m))
    image_hough = Image.new("L", (dim_espace_hough[0],dim_espace_hough[1]))
    pix = image_hough.load()
    za = ImageDraw.Draw(image_hough)
    print dim_espace_hough
    for x in range(longueur):
        for y in range(hauteur):
            if pixels[(x,y)] > seuil:
                for theta in range(dim_espace_hough[0]):
                    rho = x * math.cos(2*math.pi*theta / dim_espace_hough[0])+ y * math.sin(2*math.pi*theta/dim_espace_hough[0])
                    #print rho
                    if pix[theta,(int(rho+ampl_rho))] == 255:
                        pass
                    else:
                        za.point((theta, (int(rho +ampl_rho ))), fill = 1 + pix[theta,int(rho+ampl_rho)])
                    pix = image_hough.load()
    return image_hough
"""


def transformer(image, seuil, ampl_theta=1):
    # Prend en paramètres une image pré-traitée (une image don't il ne reste que les contours) et un seuil qui est une entier naturel compris entre 0 et 255
    longueur, hauteur = image.size
    image = ImageOps.grayscale(image)
    pixels = image.load() 
    theta_m = math.atan(hauteur/float(longueur))
    print theta_m
    dim_espace_hough = (180,int(longueur*math.cos(theta_m)+hauteur*math.sin(theta_m)))
    image_hough = Image.new("L", (dim_espace_hough[0],dim_espace_hough[1]))
    pix = image_hough.load()
    za = ImageDraw.Draw(image_hough)
    print dim_espace_hough
    for x in range(longueur):
        for y in range(hauteur):
            if pixels[(x,y)] > seuil:
                for theta in range(dim_espace_hough[0]):
                    rho = x * math.cos(math.radians(theta))+ y * math.sin(math.radians(theta))
                    # print rho
                    if pix[theta,(int(rho)%dim_espace_hough[1])] == 255:
                        pass
                    else:
                        za.point((theta, (int(rho)%dim_espace_hough[1])), fill = 100 + pix[theta,int(rho)%dim_espace_hough[1]])
                    pix = image_hough.load()
    return image_hough
    """
im = Image.open("C:/Users/Clément-B/Desktop/ny/pour_tipe.jpg")
a = transformer(im, 200)
a.save("C:/Users/Clément-B/Desktop/hough.jpg")
"""


def trouver_bord(image_hough, n, rayon):
    """
    Fonction qui cherche les droites qui sont les plus déterminants pour identifier un idéogramme
    :param image_hough:
    :param n:
    :param rayon:
    :return:
    """
    str(image_hough)  # Truc pas certain
    image_hough.save("C:/Users/Clément-B/Desktop/ny/utile")
    im = Image.open("C:/Users/Clément-B/Desktop/ny/utile")
    pixels = im.load()
    longueur, hauteur = im.size
    za = ImageDraw.Draw(im)
    l = []
    max = 0    
    l.append((0,0,max))
    for t in range(n):
        l.append((0,0,max))
        max = 0
        for theta in range(longueur):
            for rho in range(hauteur):
                if max <= pixels[(theta, rho)] and assez_loin((theta,rho), l, rayon):
                    max = pixels[(theta, rho)]
                    l[t] = (theta, rho, max)
        za.point((l[t][0], l[t][1]), fill = 0)
        im.save("C:/Users/Clément-B/Desktop/ny/utile_"+nom_image_hough)
        time.sleep(3)
        im = Image.open("C:/Users/Clément-B/Desktop/ny/utile_"+nom_image_hough)
        pixels = im.load()
        za = ImageDraw.Draw(im)
    return 

def assez_loin(couple, liste, rayon):
    """
    Fonction qui a un couple de coordonnées, renvoie une valeur de vérité
    qui affirme si l'ensemble des points de la liste l est assez loin (de l'ordre de rayon) du couple
    :param couple:
    :param liste:
    :param rayon:
    :return:
    """
    theta = couple[0]
    rho = couple[1]
    taille = len(liste)
    valeur = True
    for i in range(taille):
        if math.sqrt((theta - liste[i][0])**2+(rho - liste[i][1])**2) < rayon:
            valeur = False
            break
    return valeur
