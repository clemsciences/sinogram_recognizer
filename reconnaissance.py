


def trouver_bord(nom_image_hough, n):
    im = Image.open("C:/Users/Clément-B/Desktop/ny/"+nom_image_hough)
    im.save("C:/Users/Clément-B/Desktop/ny/utile_"+nom_image_hough)
    im = Image.open("C:/Users/Clément-B/Desktop/ny/utile_"+nom_image_hough)
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
                if max <= pixels[(theta, rho)]:
                    max = pixels[(theta, rho)]
                    l[t] = (theta, rho, max)
        za.point((l[t][0], l[t][1]), fill = 0)
        im.save("C:/Users/Clément-B/Desktop/ny/utile_"+nom_image_hough)
        time.sleep(3)
        im = Image.open("C:/Users/Clément-B/Desktop/ny/utile_"+nom_image_hough)
        pixels = im.load()
        za = ImageDraw.Draw(im)
    return l