# -*- coding: cp1252 -*-
from FILTRES import *
from traitement_image import *
from transformee_de_hough import*
from trouver_brillant import *
from dessiner_dans_image import *
import os
import pickle
def algo_sobel(image) :
    a = image
    #a = convolution(a, FLOU)
    a = double_convolution(a, SOBEL_X, SOBEL_Y)
    #a = convolution(a, FLOU_GAUSSIEN)
    pix = a.load()
    a = seuillage(a, moyenne(pix, a.size)+75)
    a = amincir_beaucoup(a)
    #a = amincir_beaucoup(amincir_beaucoup(amincir_beaucoup(a)))
    #
    #a = convolution(a, FLOU)
    return a

def image_de_hough(im, seuil):
    hou = transformer(im, seuil)
    return hou

def analyse(im):
    pass

def marche(nom_image):
    #C'est la seule fonction qui est autorisée à enregistrer des photos
    im = Image.open("C:/Users/Clément-B/Desktop/ny/collection/"+nom_image)
    imag = ImageOps.grayscale(im)
    imag = algo_sobel(imag)
    print "OOOOOH ETTTT"
    #imag = amincir_beaucoup(amincir_beaucoup(amincir_beaucoup(amincir_beaucoup(imag))))
    imag = inverser(imag)
    imag.save("C:/Users/Clément-B/Desktop/ny/traitees/traitee_"+nom_image)
    imag = image_de_hough(imag, 240)
    imag.save("C:/Users/Clément-B/Desktop/ny/donnees_hough/hough_"+nom_image)
    liste = point_plus_brillant(imag, 20, (10, 10))
    imag = dessiner_bord(im, liste)
    print liste
    imag.save("C:/Users/Clément-B/Desktop/ny/matiere_a_apprendre/"+nom_image)
    print "fini"
    
def obtenir_donnee(nom_image):
    im = Image.open("C:/Users/Clément-B/Desktop/ny/donnees_hough/"+nom_image)
    liste = point_plus_brillant(im, 20,(10,10))
    return liste
def enregistrer_donnees():
    donnees = []
    for nom_image in os.listdir("C:/Users/Clément-B/Desktop/ny/donnees_hough/"):
        donnees.append(obtenir_donnee(nom_image))
    enregistrer_fichier(array(donnees), "l")
"""
def enregistrer_donnees():
    donnees_entrainement = []
    donnees_validation = []
    donnees_test = []
    l_valid = []
    l_test = []
    nom = ""
    for i in range(20,30):
        l_valid.append("hough_xue_"+str(i)+".jpg")
        l_valid.append("hough_shen_"+str(i)+".jpg")
    for i in range(20,36):
        l_test.append("hough_xue_"+str(i)+".jpg")
        l_test.append("hough_shen_"+str(i)+".jpg")
    for nom_image in os.listdir("C:/Users/Clément-B/Desktop/ny/donnees_hough/"):
        if nom_image in l_valid:
            donnees_validation.append(obtenir_donnee(nom_image))
        elif nom_image in l_test:
            donnees_test.append(obtenir_donnee(nom_image))
        else:
            #marche(nom_image)
            donnees_entrainement.append(obtenir_donnee(nom_image))
    enregistrer_fichier(array(donnees_entrainement),"entrainement")
    enregistrer_fichier(array(donnees_test),"test")
    enregistrer_fichier(array(donnees_validation),"validation")
    """
def enregistrer_fichier(objet, nom):
    with open("C:/Users/Clément-B/Desktop/ny/donnees_liste_hough/"+nom,"wb") as f:
        mon_pickler = pickle.Pickler(f)
        mon_pickler.dump((objet))
"""
def entrainer():
    import mlp
    n_xue = 34
    n_shen = 35
    n_entrainement = 20
    n_validation = 10
    n_test = 6
    
    
    with open("C:/Users/Clément-B/Desktop/ny/donnees_liste_hough/entrainement", "rb") as f:
        z = pickle.Unpickler(f)
        entrainement = z.load()
    print shape(entrainement)
    traint = zeros((shape(entrainement)[0],2))
    print shape(entrainement)
    #print traint
    for i in range(shape(entrainement)[0]):
        if i <=n_entrainement :
            traint[i] = [1,0]
        else:
            traint[i] = [0,1]
    with open("C:/Users/Clément-B/Desktop/ny/donnees_liste_hough/test", "rb") as f:
        z = pickle.Unpickler(f)
        test = z.load()
    testt = zeros((shape(test)[0],2))
    for i in range(shape(test)[0]):
        if i <= n_test:
            testt[i] = [1,0]
        else:
            testt[i] = [0,1]
    with open("C:/Users/Clément-B/Desktop/ny/donnees_liste_hough/validation","rb") as f:
        z = pickle.Unpickler(f)
        validation = z.load()
    validt = zeros((shape(validation)[0],2))
    for i in range(shape(test)[0]):
        if i <= n_validation:
            validt[i] = [1,0]
        else:
            validt[i] = [0,1]
    
    #print entrainement
    #print concatenate((ravel(ttt[::20,:]), ravel(ttt[36::56,:])))
    #print shape(entrainement)
    #print shape(entrainement[0])
    
    
    #print ttt[0::20,:,2]
    #print ttt[36::56,:,2]
    
    
    #print shape((ravel(entrainement[0::20,:]))), shape(ravel(ttt[36::56,:]))
    #print shape(ttt)
    
    traint = reshape(concatenate((ravel(buts[::n_entrainement]), ravel(buts[n_shen::n_shen+n_entrainement]))),(n_entrainement*2,20,2))
    validt = reshape(concatenate((ravel(buts[n_entrainement::n_entrainement+n_validation]), ravel(buts[n_shen+n_entrainement::n_shen+n_entrainement+n_validation]))),(n_validation*2,20,2))
    testt = reshape(concatenate((ravel(buts[n_entrainement+n_validation::n_shen]), ravel(buts[n_shen+n_entrainement+n_validation:n_shen+n_xue - 1]))),(n_test*2,20,2))

    
    net = mlp.mlp(entrainement,traint,5,outtype='softmax')
    net.earlystopping(entrainement,traint,validation,validt,0.1)
    net.confmat(test,testt)
    """
def distance_minimale(l):
    d_min = distance(l[0],l[1])
    for i in range(len(l)-1):
        for j in range(i+1, len(l)):
            if d_min > distance(l[i],l[j]):
                d_min = distance(l[i],l[j])
    return d_min
def quadriller():
    with open("C:/Users/Clément-B/Desktop/ny/donnees_liste_hough/l","rb") as f:
        z = pickle.Unpickler(f)
        l = z.load()
    liste_des_minima = []
    n = shape(l)

    for i in range(n[0]):
        liste_des_minima.append(distance_minimale(l[i]))
    d_min =  min(liste_des_minima)
    longueur, hauteur = (180,415)
    #longueur, hauteur = (300,300)
    print
    a = zeros((n[0],int(longueur/d_min), int(hauteur/d_min)))
    for j in range(n[0]):
        for i in l[j]:
            try:
                a[j,int(i[0]/d_min),int(i[1]/d_min)] = 1
            except IndexError:
                print j,int(i[0]/d_min),int(i[1]/d_min)
    # a est une liste composées des listes venant de chaque photo et ces listes sont des listes 
    return a
def distance_hamming(m1,m2):
    #m1 et m2 sont des matrices
    d = 0
    longueur, hauteur = shape(m1)
    for i in range(longueur):
        for j in range(hauteur):
            d = (m1[i,j]+m2[i,j])%2 + d
    return d
def ma_distance(m):
    with open("C:/Users/Clément-B/Desktop/ny/donnees_liste_hough/carte_id_xue","rb") as f:
        mon_pickler = pickle.Unpickler(f)
        m_xue = mon_pickler.load()
    with open("C:/Users/Clément-B/Desktop/ny/donnees_liste_hough/carte_id_sheng","rb") as f:
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
            somme_xue = (m[i,j]%2)*m_xue[i,j] + somme_xue
            somme_shen = somme_shen + (m[i,j]%2)*m_shen[i,j]
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
def tester(m):
    for i in range(shape(l)[0]):
        print ma_distance(l[i]),i+1
def quadriller_1_image(nom_image, bla = []):
    if nom_image != "non":
        l = obtenir_donnee (nom_image)
    else:
        l = bla
    n = len(l)
    print l
    d_min =  distance_minimale(l)
    longueur, hauteur = (180,415)
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
    
def array_en_image (a):
    ny = Image.new("L", shape(a))
    za = ImageDraw.Draw(ny)
    print a
    m = a.max()
    pas = 255/m
    for i in range(shape(a)[0]):
        for j in range(shape(a)[1]):
            za.point((i,j), fill = a[i,j]*pas)
    return ny
if __name__ == "__main__":
    
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