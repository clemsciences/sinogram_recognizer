# FILTRES
dico = dict()

# Filtre de flou gaussien
FLOU_GAUSSIEN   =   [[2,3,5,4,2],[4, 9, 12, 9, 4],[5, 12, 15, 12, 5],[4, 9, 12, 9, 4],[2,3,5,4,2]]
dico["flou_gaussien"] = FLOU_GAUSSIEN
#Filtre de Flou
FLOU = [[1, 2, 1], [2, 4, 2], [1, 2, 1]]
dico["flou"] = FLOU
# Filtre de coin

COIN_X = [[-4, -4, -4],[-4,5,-4],[5,5,5]]
COIN_Y = [[5,5,5],[-4,5,-4],[-4,-4,-4]]
dico["coin_x"] = COIN_X
dico["coin_y"] = COIN_Y

#Filtre de Sobel

SOBEL_X = [[-1, -2, -1],[0,0,0],[1,2,1]]
SOBEL_Y = [[-1,0,1],[-2,0,2],[-1,0,1]]
dico["sobel_x"] = SOBEL_X
dico["sobel_y"] = SOBEL_Y 
