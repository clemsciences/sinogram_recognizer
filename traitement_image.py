# -*- coding: cp1252 -*-
from PIL import Image, ImageDraw, ImageOps
from math import atan, sqrt, pi
import time
"""
import Image
import ImageDraw
import ImageOps
"""
from numpy import *
import random

"""



Les images renvoyées ne sont jamais sauvegardées dans le programme



"""

# Algorithmes principaux

def creer_matrice(t_x, t_y, val_defaut):
    l = []
    for i in range(t_x):
        l.append([])
        for j in range(t_y):
            l[i].append(val_defaut)
    return l
def convertir_image(image):
    pix = image.load()
    longueur, hauteur = image.size
    matr = zeros(hauteur, longueur)
    for i in range(longueur):
        for j in range(hauteur):
            matr[j][i] = pixels[i,j]
    return matr
def produit_scalaire(i, j, filtre, pix):
    #Ancien nom : coordonnees_autour
    #exemple : coordonnees_autour(i, j, filtre, matrice_im):
    taille_m = len(filtre)# matrice_m doit être une matrice carré)
    diff = taille_m/2
    somme = 0
    for a in range(len(filtre)):
        for b in range(len(filtre)):
            somme = (pix[i+a - diff ,j+b - diff]* filtre[a][b]) + somme
    return somme

def produit_scalaire_mat(i, j, filtre, matrice):
    taille_m = len(filtre)# matrice_m doit être une matrice carré)
    diff = taille_m/2
    somme = 0
    for a in range(len(filtre)):
        for b in range(len(filtre)):
            somme = (matrice[j+b - diff][i+a - diff ]* filtre[a][b]) + somme
    return somme
def convolution_matr(matrice, filtre):
    diff = len(filtre)
    longueur, hauteur = len(matrice[0]),len(matrice)
    mat2 = creer_matrice(longueur - 2,hauteur - 2, 0)
    map( lambda y : map( lambda x : produit_scalaire_mat(x,y, filtre, matrice), range(diff,longueur-diff)), range(diff,hauteur - diff))
    return mat2
m = [[0,0,0,0,0,0,0,0,0],
    [2,3,8,288,109,38,23,112,98],
     [2,3,8,288,109,38,23,112,98],
     [2,3,8,288,0,0,0,112,98],
     [2,3,8,288,0,0,0,112,98],
     [78,3,8,45,0,0,0,112,98],
     [2,3,8,288,0,0,0,112,98],
     [2,3,8,288,109,38,23,112,98],
     [2,89,8,288,109,38,23,112,98]]
#print [[1,1,1],[1,1,1],[1,1,1]]
#print  convolution_matr(m, [[1,2,1],[0,0,0],[-1,-2,-1]])
def convolution(image, filtre):
    longueur, hauteur = image.size
    pixels = image.load()
    ny = Image.new("L", (longueur - 2, hauteur - 2))
    diff = len(filtre)/2
    za = ImageDraw.Draw(ny)
    pixels = image.load()
    for i in range(diff,longueur-diff ):
        for j in range(diff,hauteur-diff):
            za.point((i -diff ,j - diff), fill = (produit_scalaire(i, j, filtre , pixels)))
    return ny
def double_convolution(image, filtrex, filtrey):
    diff_x = len(filtrex)
    longueur, hauteur = image.size
    pixels = image.load()
    diff_y = len(filtrey)
    ny = Image.new("L", (longueur - 2, hauteur - 2))
    za = ImageDraw.Draw(ny)
    #print (len(l_dif_pix)/2) #C'est la moitié de la taille de la différence de position entre le pixel
    for i in range(diff_x,longueur - diff_x ):
        for j in range(diff_y,hauteur - diff_y):
            sommex = produit_scalaire(i, j, filtrex , pixels)
            sommey = produit_scalaire(i, j, filtrey , pixels)
            #print i,j
            #print i-diff_x, j - diff_y
            za.point((i - diff_x ,j - diff_y), fill = (sqrt(sommex**2+sommey**2)))
    return ny
def moyenne(matrice, taille):
    # prend en argument une matrice du type : pixels[(i,j)]
    somme = 0
    for i in range(taille[0]):
        for j in range(taille[1]):
            somme = somme + matrice[(i,j)]
    moyenne = somme/float(taille[0]*taille[1])
    return moyenne
def densifie_probabiliste(image, seuil, n_x, n_y, n):
	#n_x et n_y sont les nombres approximatifs de cases  que l'image contiendra
	longueur, hauteur = image.size
	#seuil fixe la tolérance à la reconnaissance d'une case comme étant noir
	pixels = image.load()
	t_x = longueur / n_x
	t_y = hauteur /n_y
	pix_x_plus = longueur % n_x
	pix_y_plus = hauteur % n_y
	
	ny = Image.new("L", (n_x , n_y ))
	za = ImageDraw.Draw(ny)
	for i in range(n_x):
		for j in range(n_y):
			k = 0
			while k < n:
				if i >pix_x_plus:	
					x = random.choice(range(i*t_x, i*t_x+2))
				else:
					x = random.choice(range(i*t_x, i*t_x+1))
				if j > pix_y_plus:
					y = random.choice(range(j*t_y, j*t_y+2))
				else:
					y = random.choice(range(j*t_y, j*t_y+1))
				if pixels[x,y] > seuil:
					za.point((i ,j ), fill = 255)
					break
				elif k == n-1:
					za.point((i ,j ), fill = 0)
				else:
					k +=1
	return ny
def seuillage(image, seuil):
    #une image et un nombre naturel compris entre 0 et 255
    pixels = image.load()
    longueur, hauteur = image.size
    za = ImageDraw.Draw(image)
    for i in range(longueur):
        for j in range(hauteur):
            if seuil < pixels[i,j]:
                za.point((i,j), fill = 0)
            else:
                za.point((i,j), fill = 255)
    return image

def inverser(image):
    pixels = image.load()
    ny = Image.new("L", image.size)
    za = ImageDraw.Draw(ny)
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            za.point((x,y), fill = 255 - pixels[x,y])
    return ny

def amincir_peu(image):
    pixels = image.load()
    longueur, hauteur = image.size
    somme = 0
    ny = Image.new("L", (longueur - 2, hauteur - 2))
    za = ImageDraw.Draw(ny)
    for x in range(1, longueur - 1):
        for y in range(1, hauteur - 1):
            somme = pixels[x, y-1]+pixels[x, y+1]+pixels[x - 1, y]+pixels[x+1, y]+pixels[x-1,y-1]+pixels[x-1,y+1]+pixels[x+1,y-1]+pixels[x+1,y+1]
            if somme >= 2*255:
                somme = 255
            elif somme  < 2*255:
                somme = 0
            else:
                somme = pixels[x,y]
            za.point((x,y), fill = somme)
    return ny

def amincir_beaucoup(image):
    pixels = image.load()
    longueur, hauteur = image.size
    somme = 0
    ny = Image.new("L", (longueur - 2, hauteur - 2))
    za = ImageDraw.Draw(ny)
    for x in range(1, longueur - 1):
        for y in range(1, hauteur - 1):
            somme = pixels[x, y-1]+pixels[x, y+1]+pixels[x - 1, y]+pixels[x+1, y]+pixels[x-1,y-1]+pixels[x-1,y+1]+pixels[x+1,y-1]+pixels[x+1,y+1]
            if somme >= 6*255:
                somme = 255
            else :
                somme = 0
            za.point((x,y), fill = somme)
    return ny 
    chi = ""
    pass

    
"""
im = Image.open("C:/Users/Clément-B/Desktop/ny/traitees/traitee_xue_1.jpg")
a = (amincir_beaucoup(amincir_beaucoup(amincir_beaucoup(amincir_beaucoup(amincir_beaucoup(im))))))
a.save( "C:/Users/Clément-B/Desktop/voyons.jpg")
"""
# Algorithmes de flou
def getCannyBlur(image):
    #argument : une image et ça renvoie l'image floutée
    mat =  [[2,3,5,4,2],
				[4, 9, 12, 9, 4],
				[5, 12, 15, 12, 5],
				[4, 9, 12, 9, 4],
				[2,3,5,4,2]]
    mat_div = 1/115.
    somme = 0
    longueur, hauteur = image.size
    pixels = image.load()
    ny = Image.new("L", image.size)
    l_1 = range(2, longueur - 2)
    l_1.reverse()
    l_2 = range(2, hauteur - 2)
    l_2.reverse()
    for i in l_1:
       for j in l_2:
            somme = 0
            for k in range(-2, 3):
                for l in range(-2, 3):
                    somme += pixels[i+k,j+l]*mat[l+2][k+2]
            somme *= mat_div
            if somme > 255:
                somme = 255
            elif somme <0 :
                somme = 0
            za = ImageDraw.Draw(ny)
            za.point((i,j), fill = somme)
    return ny
def flou_gaussien(image):
    mat =  [[2,3,5,4,2],
				[4, 9, 12, 9, 4],
				[5, 12, 15, 12, 5],
				[4, 9, 12, 9, 4],
				[2,3,5,4,2]]
    mat_div = 1/115.
    somme = 0
    ny = Image.new("L", image.size)
    l_1 = range(2, longueur - 2)
    l_1.reverse()
    l_2 = range(2, hauteur - 2)
    l_2.reverse()
    za = ImageDraw.Draw(ny)
    for i in l_1:
        for j in l_2:
            somme = 0
            for k in range(-2, 3):
                for l in range(-2, 3):
                    somme += pixels[i+k,j+l]*mat[l+2][k+2]
            somme *= mat_div
            if somme > 255:
                somme = 255
            elif somme <0 :
                somme = 0
            za.point((i,j), fill = somme)
    return ny
    
def flou(image):
    mat = [[1, 2, 1], [2, 4, 2], [1, 2, 1]]
    l = []
    longueur, hauteur = image.size 
    pixels = image.load()
    im = Image.new("L", (longueur - 2,hauteur - 2))
    za = ImageDraw.Draw(im)
    for i in range(1, longueur - 1):
        for j in range(1, hauteur - 1):
            za.point((i - 1,j - 1), fill = coordonnees_autour(i,j,mat, pixels))
    return im
#Algorithmes renvoyant les images avec que les bords
def getCannyBorders(im ,lower = 85, higher  = 170,performGrayScal = True):
	# Prend en arugment une image et renvoir une image avec seulement en noir les bords
    n = getCannyBlur(im)
    longueur, hauteur = im.size
    za = ImageDraw.Draw(n)
    pixels = im.load()
    pi_8 = pi/8.
    _3_pi_8 = 3*pi/8.
    pi_2 = pi/2.
    pi_4 = pi/4.
    _3_pi_4 = 3*pi/4.
    _5_pi_8 = 5*pi/8.
    _7_pi_8 = 7*pi/8.
    gX = [[-1, 0, 1],
				[-2, 0, 2],
				[-1, 0, 1]]
    gY = [[1, 2, 1],
				[0, 0, 0],
                [-1, -2, -1]]
    px = 0
    sommeX = 0
    sommeY = 0
    somme = 0
    direc = 0
    canny = range(hauteur)
    for i in canny:
        canny[i] = range(longueur)
    print "Conversion"
    d4 = time.time()
    l_3 = range(2,longueur - 2)
    l_3.reverse()
    l_4 = range(2, hauteur - 2)
    l_4.reverse()
    for i in l_3:
        for j in l_4:
            sommeX = 0
            sommeY = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    px = pixels[i+k, j+l]
                    sommeX += px * gX[l+1][k+1]
                    sommeY += px * gY[l+1][k+1]
            somme = sqrt((sommeX**2+sommeY**2))
            if somme > 255:
                somme = 255
            elif somme < 0:
                somme = 0
            if sommeX == 0:
                if sommeY == 0:
                    direc = 0
                else:
                    direc = pi_2
            else:
                direc = pi_2 + atan(sommeY / sommeX)
            if (direc >= 0 and direc < pi_8) or (direc >= _7_pi_8 and direc < pi):
                direc = 0
            elif direc >= pi_8 and direc < _3_pi_8:
                direc = pi_4
            elif direc >= _3_pi_8 and direc < _5_pi_8:
                direc = pi_2
            else :
                direc = _3_pi_4
            o = [somme, direc, False]
			#print o 
            canny[j][i] = o
    print "Remplissage"
    d5 = time.time()
    l_5 = range(3, len(canny[0]) - 3)
    l_5.reverse()
    l_6 = range(3, len(canny) - 3)
    l_6.reverse()
    for i in l_5:
        for j in l_6:
            px = canny[j][i][0]
            direc = canny[j][i][1]
            aucun_bord = False
            if direc == 0:
				#print j+1
				#print canny[j-1][i],canny[j+1][i]
                if px < canny[j-1][i][0] or px < canny[j+1][i][0]:
                    aucun_bord = True
            elif direc == pi_4:
                if px <canny[j - 1][i-1][0] or px < canny[j + 1][i + 1][0]:
                    aucun_bord = True
            elif direc == pi_2:
                if px < canny[j - 1][i + 1][0] or px < canny[j+1][i - 1][0]:
                    aucun_bord = True
            elif direc == _3_pi_4:
				#print "ok : :::::: ", canny[j-1][i+1], canny [j+1][i- 1]
                if px < canny[j-1][i+1][0] or px < canny [j+1][i- 1][0]:
                    aucun_bord = True
            if aucun_bord or px < lower:
                za.point((i,j), fill = "black")
            elif px > higher:
                za.point((i,j), fill = "white")
                canny[j][i][2] = True
            else:
                if canny[j-1][i- 1][2] or canny[j-1][i][2] or canny[j-1][i+1][2] or canny[j][i+1][2] or canny[j+1][i-1][2] or canny[j+1][i][2] or canny[j+1][i+1][2]:
                    za.point((i,j), fill = "white")
                    canny[j][i][2] = True
                else:
                    za.point((i,j), fill = "black")
    #n.save("C:/Users/Clément-B/Desktop/ny/"+"canny_"+nom_image)
    return n
def trouver_squelette(image):
    pass
def utilisation_densifie_probabiliste():
	a = Image.open("C:\Users\Clément\Desktop\\ny\collection\shen_1.jpg")
	a = ImageOps.grayscale(a)

	#a = algo_complexes.algo_sobel(a)
	a = densifie_probabiliste(a, 200, 50, 50, 50)
	a.save("C:\Users\Clément\Desktop\oo.jpg")
if __name__ == "__main__":
	utilisation_densifie_probabiliste()