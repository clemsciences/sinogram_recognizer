# -*- coding: cp1252 -*-
import math
from traitement_image import *
NOIR = 0


def distance(coup1, coup2):
    n = len(coup1)
    somme = 0
    for i in range(n):
        somme += (coup1[i] - coup2[i])**2
    return math.sqrt(somme)
"""
def convertir(im):
    longueur, hauteur = im.size
    pixels = im.load()
    m = creer_matrice(longueur, hauteur, 0)
    for i in range(longueur):
        for j in range(hauteur):
            m[j][i] = pixels[i,j]
    return m
"""


def point_plus_brillant(im, n, rayon):
    """
    # matrice : pixels[i,j]
    Fonction qui cherche les droites qui sont les plus déterminants pour identifier un idéogramme
    """
    longueur, hauteur = im.size
    pixels = im.load()
    l = []
    max = 0      
    for t in range(n):
        max = 0
        l.append([0])
        for theta in range(longueur):
            for rho in range(hauteur):
                if max <= pixels[(theta, rho)] :
                    max = pixels[(theta, rho)]
                    l[t] = (theta, rho)  # (theta, rho, max) anciennement
        colorer(im, rayon, NOIR, l[t])
    o = []
    # print o
    for i in l:
        o.extend([i])
        # print o
    return o


def assez_loin(couple, liste, rayon):
    """
    Fonction qui a un couple de coordonnées, renvoie une valeur de vérité 
    qui affirme si l'ensemble des points de la liste l est assez loin (de l'ordre de rayon) du couple
    """
    taille = len(liste)
    valeur = True
    for i in range(taille):
        if distance(couple, liste[i]) < rayon:
            valeur = False
            break
    return valeur


def colorer(im, rayon, couleur, point):
    pix = im.load()
    za = ImageDraw.Draw(im)
    longueur, hauteur = im.size
    for i in range(-rayon[0],rayon[0]+1):
        for j in range(-rayon[1], rayon[1]+1):
            if i == 0 and j == 0 and longueur <= i+point[0] and 0 > i+point[0] and 0 > j+point[1] and hauteur <= j+point[1]:
                pass
            else:
                za.point((point[0]+i, point[1] +j), fill=couleur)
