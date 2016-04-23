# -*- coding: cp1252 -*-
from PIL import Image
from FILTRES import *
from numpy import *
from traitement_image import *
from transformee_de_hough import*
from trouver_brillant import *
from dessiner_dans_image import *
import os
import pickle


def algo_sobel(image):
    a = image
    a = double_convolution(a, SOBEL_X, SOBEL_Y)
    pix = a.load()
    a = seuillage(a, moyenne(pix, a.size)+75)
    a = amincir_beaucoup(a)
    # a = amincir_beaucoup(amincir_beaucoup(amincir_beaucoup(a)))
    #
    # a = convolution(a, FLOU)
    return a


def image_de_hough(im, seuil):
    hou = transformer(im, seuil, 2*180)
    return hou
a = Image.open("C:/Users/Clément-B/Desktop/TIPE/3_points.jpg")
# b = image_de_hough(a, 100)
# b.save("C:/Users/Clément-B/Desktop/3_points_hough.jpg")
"""
b = Image.open("C:/Users/Clément-B/Desktop/3_points_hough.jpg")
a = ImageOps.grayscale(a)
a = inverser(a)
b = inverser(b)
a.save("C:/Users/Clément-B/Desktop/TIPE/3_points.jpg")
b.save("C:/Users/Clément-B/Desktop/3_points_hough.jpg")
"""


def analyse(im):
    pass


def marche(nom_image):
    """
    C'est un script qui à partir d'une image normale dessine les traits représentatifs de l'image.
    :param nom_image:
    :return:
    """
    # C'est la seule fonction qui est autorisée à enregistrer des photos
    im = Image.open("C:/Users/Clément-B/Desktop/ny/collection/"+nom_image)
    imag = ImageOps.grayscale(im)
    imag = algo_sobel(imag)
    print "OOOOOH ETTTT"
    # imag = amincir_beaucoup(amincir_beaucoup(amincir_beaucoup(amincir_beaucoup(imag))))
    imag = inverser(imag)
    imag.save("C:/Users/Clément-B/Desktop/ny/traitees/aaatraitee_"+nom_image)
    imag = image_de_hough(imag, 240)
    imag.save("C:/Users/Clément-B/Desktop/ny/donnees_hough/aaahough_"+nom_image)
    liste = point_plus_brillant(imag, 20, (20, 20))
    imag = dessiner_bord(im, liste)
    print liste
    imag.save("C:/Users/Clément-B/Desktop/ny/matiere_a_apprendre/aaa"+nom_image)
    print "fini"
#marche("shen_2.jpg")


def obtenir_donnee(nom_image):
    im = Image.open("C:/Users/Clément-B/Desktop/ny/donnees_hough/"+nom_image)
    liste = point_plus_brillant(im, 20, (10, 10))
    return liste


def enregistrer_donnees():
    donnees = []
    for nom_image in os.listdir("C:/Users/Clément-B/Desktop/ny/donnees_hough/"):
        donnees.append(obtenir_donnee(nom_image))
    enregistrer_fichier(array(donnees), "l")


def enregistrer_fichier(objet, nom):
    with open("C:/Users/Clément-B/Desktop/ny/donnees_liste_hough/"+nom,"wb") as f:
        mon_pickler = pickle.Pickler(f)
        mon_pickler.dump((objet))


def distance_minimale(l):
    d_min = distance(l[0], l[1])
    for i in range(len(l)-1):
        for j in range(i+1, len(l)):
            if d_min > distance(l[i], l[j]):
                d_min = distance(l[i], l[j])
    return d_min


def quadriller():
    with open("C:/Users/Clément-B/Desktop/ny/donnees_liste_hough/l", "rb") as f:
        z = pickle.Unpickler(f)
        l = z.load()
    liste_des_minima = []
    n = shape(l)

    for i in range(n[0]):
        liste_des_minima.append(distance_minimale(l[i]))
    d_min = min(liste_des_minima)
    longueur, hauteur = (180, 415)
    #longueur, hauteur = (300,300)
    a = zeros((n[0], int(longueur/d_min), int(hauteur/d_min)))
    for j in range(n[0]):
        for i in l[j]:
            try:
                a[j,int(i[0]/d_min),int(i[1]/d_min)] = 1
            except IndexError:
                print j,int(i[0]/d_min),int(i[1]/d_min)
    # a est une liste composées des listes venant de chaque photo et ces listes sont des listes 
    return a


def distance_hamming(m1,m2):
    # m1 et m2 sont des matrices
    d = 0
    longueur, hauteur = shape(m1)
    for i in range(longueur):
        for j in range(hauteur):
            d += (m1[i, j] + m2[i, j]) % 2
    return d


def ma_distance(m):
    """
    C'est la fonction qui décide que la carte d'identité de l'image donnée en entrée est un "xue" ou un "shen"
    :param m:
    :return:
    """
    with open("C:/Users/Clément-B/Desktop/ny/donnees_liste_hough/carte_id_xue", "rb") as f:
        mon_pickler = pickle.Unpickler(f)
        m_xue = mon_pickler.load()
    with open("C:/Users/Clément-B/Desktop/ny/donnees_liste_hough/carte_id_sheng", "rb") as f:
        mon_pickler = pickle.Unpickler(f)
        m_shen = mon_pickler.load()
    longueur, hauteur = shape(m)
    somme_xue = 0
    somme_shen = 0
    im_xue = array_en_image(m_xue)
    im_shen = array_en_image(m_shen)
    im_xue.save("C:/Users/Clément-B/Desktop/id_xue.jpg")
    im_shen.save("C:/Users/Clément-B/Desktop/essai.jpg")
    for i in range(longueur):
        for j in range(hauteur):
            somme_xue += (m[i, j] % 2) * m_xue[i, j]
            somme_shen += (m[i, j] % 2) * m_shen[i, j]
    if somme_xue > somme_shen:
        return "xue"
    else:
        return "shen"


def carte_identite(l):
    # l est une liste de matrices qui codent pour un même ideogramme
    somme = zeros((shape(l[0])))
    for i in (l):
        somme = somme + i 
    return somme


def creer_carte_identite():
    with open("C:/Users/Clément-B/Desktop/ny/donnees_liste_hough/l_quadrillage", "rb") as f:
        z = pickle.Unpickler(f)
        l = z.load()
    with open("C:/Users/Clément-B/Desktop/ny/donnees_liste_hough/carte_id_xue","wb") as f:
        mon_pickler = pickle.Pickler(f)
        mon_pickler.dump(carte_identite(l[:20]))
    with open("C:/Users/Clément-B/Desktop/ny/donnees_liste_hough/carte_id_sheng","wb") as f:
        mon_pickler = pickle.Pickler(f)
        mon_pickler.dump(carte_identite(l[36:56]))


def tester(l):
    for i in range(shape(l)[0]):
        print ma_distance(l[i]), i+1


def quadriller_1_image(nom_image, bla=[]):
    if nom_image != "non":
        l = obtenir_donnee(nom_image)
    else:
        l = bla
    n = len(l)
    print l
    d_min = distance_minimale(l)
    longueur, hauteur = (180, 415)
    print "yo"
    print "d_min : ", d_min
    a = zeros((int(longueur/d_min), int(hauteur/d_min)))
    print (int(longueur/d_min), int(hauteur/d_min))
    for i in range(n):
        try:
            a[int(l[i][0]/d_min),int(l[i][1]/d_min)] = 1
        except IndexError:
            print int(l[i][0]/d_min),int(l[i][1]/d_min)
    # a est une liste composées des listes venant de chaque photo et ces listes sont des listes 
    return a


def array_en_image(a):
    ny = Image.new("L", shape(a))
    za = ImageDraw.Draw(ny)
    print a
    m = a.max()
    pas = 255/m
    for i in range(shape(a)[0]):
        for j in range(shape(a)[1]):
            za.point((i, j), fill=a[i, j]*pas)
    return ny


if __name__ == "__main__":
    nom_image = "IMG_6730.jpg"
    im = Image.open("C:/Users/Clément/Desktop/"+nom_image)
    z = algo_sobel(im)
    z.save("C:/Users/Clément/Desktop/transfor.jpg")
    


    """
    z = array_en_image(quadriller_1_image("hough_shen_1.jpg"))
    z.save("C:/Users/Clément-B/Desktop/reduc.jpg")
    """
    #marche()
    #ma_distance(a)
    """
    im = Image.open("C:/Users/Clément-B/Desktop/ny/collection/shen_1.jpg")
    l = obtenir_donnee("hough_shen_1.jpg")
    ny = dessiner_bord(im, l)
    ny.save("C:/Users/Clément-B/Desktop/dessine_shen_1.jpg")
    """
    """
    enregistrer_donnees()
    a =  quadriller()
    enregistrer_fichier(a,"l_quadrillage")
    print shape(a)
    """
    """
    
    i = 2
    sino = "shen"
    a = quadriller_1_image("hough_"+sino+"_"+str(i)+".jpg")
    
    print a
    
    #ma_distance(a)
    ny = array_en_image(a)
    ny.save("C:/Users/Clément-B/Desktop/essai"+sino+str(i)+".jpg")
    """
    """
    #with open("C:/Users/Clément-B/Desktop/ny/donnees_liste_hough/l","rb") as f:
    #    z = pickle.Unpickler(f)
    #    l = z.load()
    #a = quadriller_1_image("non", l[0])
    #print a
    
    
    #print distance_hamming(a[10],a[40])
    #print a[0]
    
    #entrainer()
    """