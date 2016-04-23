# -*- coding: cp1252 -*-

from PIL import Image, ImageOps
import time
from algo_complexes import *


def marche(nom_image):
    #C'est la seule fonction qui est autoris�e � enregistrer des photos
    im = Image.open("C:/Users/Cl�ment-B/Desktop/ny/collection/"+nom_image)
    imag = ImageOps.grayscale(im)
    imag = algo_sobel(imag)
    print "OOOOOH ETTTT"
    #imag = amincir_beaucoup(amincir_beaucoup(amincir_beaucoup(amincir_beaucoup(imag))))
    imag = inverser(imag)
    imag.save("C:/Users/Cl�ment-B/Desktop/ny/traitees/traitee_test_"+nom_image)
    imag = image_de_hough(imag, 240)
    imag.save("C:/Users/Cl�ment-B/Desktop/ny/donnees_hough/hough_test_"+nom_image)
    liste = point_plus_brillant(imag, 20, (10, 10))
    imag = dessiner_bord(im, liste)
    print liste
    imag.save("C:/Users/Cl�ment-B/Desktop/ny/matiere_a_apprendre/test_"+nom_image)
    print "fini"
    for i in range(len(liste)):
        b = Image.open("C:/Users/Cl�ment-B/Desktop/ny/collection/xue_2.jpg")
        chaine = "dessiner_droite(b, liste[i][1], math.radians(liste[i][0])).save(\"C:/Users/Cl�ment-B/Desktop/b\"+str(i)+\".jpg\")"
        eval(chaine)
        time.sleep(3)
#marche("xue_2.jpg")


# avec algo_sobel
im = Image.open("C:/Users/Cl�ment-B/Desktop/ny/blanc.jpg")
z = image_de_hough(im, 200)
z.save("C:/Users/Cl�ment-B/Desktop/hough_blanc.jpg")
liste = point_plus_brillant(z, 10, (20,20))
imag = dessiner_bord(im, liste)
imag.save("C:/Users/Cl�ment-B/Desktop/testtttt.jpg")



# Dans dessiner_image

"""
print "�"
print "�"
b_hough = Image.open("C:/Users/Cl�ment-B/Desktop/ny/donnees_hough/hough_shen_2.jpg")
l = point_plus_brillant(b_hough, 10, (10,10))
print l
for i in range(len(l)):
    b = Image.open("C:/Users/Cl�ment-B/Desktop/ny/collection/shen_2.jpg")
    eval("dessiner_droite(b, l[i][1], l[i][0]).save("C:/Users/Cl�ment-B/Desktop/b"+str(i)+".jpg"))
    
"""