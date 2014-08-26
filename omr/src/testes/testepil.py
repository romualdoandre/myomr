# -*- coding: utf-8 -*-
#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="racosta"
__date__ ="$20/09/2011 11:49:30$"

from PIL import Image
import sys
import math
# import the necessary things for OpenCV
import cv2.cv as cv
import cv2

if __name__ == "__main__":
    #filename = "fresp_anti_horario.png"
    filename = "fresp_horario.png"
    im = cv.LoadImage(filename,cv2.CV_LOAD_IMAGE_COLOR) ## Read image file
    
    if (im == None):
        print "Failed to load %s" % filename
        sys.exit(-1)
        
    #edge = cv.cvCreateImage (cv.cvSize (im.width, im.height), cv.IPL_DEPTH_16S, 3)
    #cv.cvThreshold(im,im,113,255,cv.CV_THRESH_BINARY)
    cv.SaveImage("treshold.png", im)
    im=Image.open("treshold.png")
    pix=im.load()
    treshold=113
    anchors=[]
    #im.show()
    max_x_sweep = im.size[0]* 0.666
    #max_x_sweep = 1100
    #varredura diagonal a partir do canto superior direito
    #em direcao ao ponto superior esquerdo
    y, current_y = 0,0
    x = im.size[0]-1
    found = False
    y, current_y = 0,0
    x = im.size[0]-1
    while x !=max_x_sweep and not found:
        x = im.size[0]-1
        if current_y > im.size[1]-1:
            y =  current_y
        else:
            current_y+=1
            y= current_y

        while y >=0 and not found:
            row = pix[x,y]
            #print(row)
            if row <= treshold:
                found = True;
                point= cv.cvPoint(x,y)
                print(point)
                print(row)
                anchors.append(point)
            x-=1
            y-=1
    #varredura diagonal a partir do canto inferior direito
    #em direcao ao ponto superior direito
    current_x = im.size[0]-1
    y = im.size[1]-1
    found = False
    
    while x != max_x_sweep and not found:
        y = im.size[1]-1;
        if current_x <= max_x_sweep:
            x = max_x_sweep
        else:
            current_x-=1
            x=current_x

        while x < im.size[0] and not found:
            row = pix[x,y]
            if row <= treshold:
                found = True
                point= cv.cvPoint(x,y)
                print(point)
                print(row)
                anchors.append(point)
            x+=1;
            y-=1;
    
    print(anchors)
    #a reta tem que ter 90 graus, entao eu vou descontar isso depois

    #se o x do top é maior que o x do bottom, rotacionou em sentido anti-horário
    #se o x do top é menor que o x do bottom, rotacionou em sentido horário

    sentido_horario = anchors[1].x > anchors[0].x

    if sentido_horario:
        print("Sentido horario")
    else:
        print("Sentido anti-horario")

    if sentido_horario:
        adjac = anchors[1].x - anchors[0].x
    else:
        adjac= anchors[0].x - anchors[1].x
    oposto = anchors[1].y - anchors[0].y
    try:
        tangente = (oposto/adjac)
        comprimento = math.sqrt( math.pow(adjac, 2)+ math.pow(oposto, 2))

        print("Comprimento:"  + str(comprimento))

        print("cateto oposto = " + str(oposto))
        print("cateto adjac  = " +str(adjac))
        print("tg o " + str(tangente))
        angulo_reta = ((math.atan(tangente))*180)/math.pi

        print("Angulo da reta: " + str(angulo_reta))
        if sentido_horario:
            angulo_correcao = angulo_reta - 90
        else:
            angulo_correcao =90 - angulo_reta
    except:
        print("Imagem alinhada")
        angulo_correcao=0        

    print("Corrigir em " +str(angulo_correcao) + "graus")

    im=im.rotate(angulo_correcao)
    
    #utilizando o algoritmo dos cantos com o x e y alterados para levar em conta o não dimensionamento do canvas em relação à imagem propriamente dita
    
    pix=im.load()
    anchors=[]
    max_x_sweep = im.size[0]* 0.666
    #max_x_sweep = 1100
    #varredura diagonal a partir do canto superior direito
    #em direcao ao ponto superior esquerdo
    found = False
    y, current_y = adjac,adjac
    x = im.size[0]-adjac*2
    while x !=max_x_sweep and not found:
        x = im.size[0]-adjac*2
        if current_y > im.size[1]-1:
            y =  current_y
        else:
            current_y+=1
            y= current_y

        while y >=0 and not found:
            row = pix[x,y]
            #print(row)
            if row <= treshold:
                found = True;
                point= cv.cvPoint(x,y)
                print(point)
                print(row)
                anchors.append(point)
            x-=1
            y-=1
    #varredura diagonal a partir do canto inferior direito
    #em direcao ao ponto superior direito
    current_x = im.size[0]-adjac
    y = im.size[1]-adjac
    found = False
    
    while x != max_x_sweep and not found:
        y = im.size[1]-adjac
        if current_x <= max_x_sweep:
            x = max_x_sweep
        else:
            current_x-=1
            x=current_x

        while x < im.size[0] and not found:
            row = pix[x,y]
            if row <= treshold:
                found = True
                point= cv.cvPoint(x,y)
                print(point)
                print(row)
                anchors.append(point)
            x+=1;
            y-=1;
    
    print(anchors)
    
    
    #utilizando rotação para descobrir onde foi para os pontos das ancoras
    '''x2=anchors[0].x*math.cos(math.radians(angulo_correcao))-anchors[0].y*math.sin(math.radians(angulo_correcao))
    y2=anchors[0].x*math.sin(math.radians(angulo_correcao))+anchors[0].y*math.cos(math.radians(angulo_correcao))
    x3=anchors[1].x*math.cos(math.radians(angulo_correcao))-anchors[1].y*math.sin(math.radians(angulo_correcao))
    y3=anchors[1].x*math.sin(math.radians(angulo_correcao))+anchors[1].y*math.cos(math.radians(angulo_correcao))
    print(x2)
    print(y2)
    print(x3)
    print(y3)'''
    #subimage=im.crop([anchors[0].x-1180, anchors[0].y - 80, 1200, 1600])
    subimage=im.crop([0, anchors[0].y, anchors[1].x, anchors[1].y])
    #subimage=im.crop([0, int(y2)-adjac*2, int(x3)+adjac*2, int(y3)])
    subimage.load()
    #subimage.show()
    #subimage.save("out2.png")
    
    subimage.save("out1.png")
    
    
    #im.save("out4.png")
    
    
    