# -*- coding: utf-8 -*-
#! /usr/bin/python
import sys
import math
# import the necessary things for OpenCV
import cv2.cv as cv
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Dev03"
__date__ ="$05/09/2011 11:47:12$"

if __name__ == "__main__":
    #se encontrou o ponto
    found=False
    #as ancoras
    anchors=[]
    #a linha (soh acesso a primeira posicao, que eh o elemento atual)
    row=0
    treshold=113
    filename = "teste.png"
    gray = cv.LoadImage( filename,0)
    
    #gray1 = cv.LoadImage( filename,0)
    #gray = cv.cvCreateImage(cv.cvGetSize(gray1), cv.IPL_DEPTH_16S, 3)
    #gray = cv.cvGetSubRect(gray1,cv.cvRect( 0,0, gray1.width-10, gray1.height-10))
    
    if not gray:
        print "Failed to load %s" % filename
        sys.exit(-1)    
    

    #edge = cv.cvCreateImage (cv.cvSize (gray.width, gray.height), cv.IPL_DEPTH_16S, 3)
    #edge=cv.cvCloneImage(gray)
    #cv.cvThreshold(gray,edge,treshold,255,cv.CV_THRESH_BINARY)
    #gray=edge
    cv.SaveImage("foo-laplace.png", gray)
    #varrer ateh um terco vertical da imagem
    max_x_sweep = gray.width * 0.666
    #max_x_sweep = 1100
    #varredura diagonal a partir do canto superior direito
    #em direcao ao ponto superior esquerdo
    y, current_y = 0,0
    x = gray.width-1
    subimage=cv.cvCloneImage(gray)
    #varredura diagonal a partir do canto inferior direito
    #em direcao ao ponto superior direito
    current_x = gray.width-1
    y = gray.height-1
    found = False
    while x != max_x_sweep and not found:
        y = gray.height-1;
        if current_x <= max_x_sweep:
            x = max_x_sweep
        else:
            current_x-=1
            x=current_x

        while x < gray.width and not found:
            row = gray[y][x]
            if row <= treshold:
                found = True
                point= cv.cvPoint(x,y)
                print(point)
                print(row)
                anchors.append(point)
            x+=1;
            y-=1;

    y, current_y = 0,0
    x = gray.width-1
    while x !=max_x_sweep and not found:
        x = gray.width-1
        if current_y > gray.height-1:
            y =  current_y
        else:
            current_y+=1
            y= current_y

        while y >=0 and not found:
            row = gray[x][y]
            #print(row)
            if row <= treshold:
                found = True;
                point= cv.cvPoint(x,y)
                print(point)
                print(row)
                anchors.append(point)
            x-=1
            y-=1
    '''x = gray.width
    row=255
    while x > max_x_sweep and not found:
        y=0
        #if row!=255 :
        
        while y < 600 and not found:
            row = gray[x][y]
            if row != 255:
                found = True
                point= cv.cvPoint(x,y)
                print(point)
                #print(row)
                anchors.append(point)
            y=y+1
            cv.cvDrawLine(subimage,cv.cvPoint(gray.width,0),cv.cvPoint(x,y),cv.cvScalar(78,x,x))
            #print(str(row)+' x:'+str(x)+' y:'+str(y))
        x=x-1'''
    #anchors.append(cv.cvPoint(1191,193))
    #print(gray[1176][195])
    cv.SaveImage("out.png", subimage)
    #sys.exit(-1)
    

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
        
        

    print("Corrigir em " +str(angulo_correcao) + "graus")

    #usando a anchors superior
    center = cv.cvPoint2D32f(anchors[0].x, anchors[0].y)
    print(center)

    #copia da imagem original
    destination = cv.CloneImage(gray )

    #matriz de rotacao
    rot_mat = cv.CreateMat(2,3,cv.CV_32FC1)

    #definicao de rot_mat
    #angulo_correcao
    scale=1
    cv.cv2DRotationMatrix( center,angulo_correcao, scale, rot_mat )

    #realizacao da transformacao
    cv.WarpAffine( gray, destination, rot_mat )

    #house keeping

    #gray = destination;

    print("Rotacionado")
    cv.ShowImage('rotationado',destination)
    cv.ShowImage('original',gray)
    #cv.WaitKey(0)
    
    #subimage=cv.GetSubRect(gray,cv.cvRect( anchors[0].x-1180, anchors[0].y - 80, 1200, 1600))
    #subimage=cv.GetSubRect(destination,cv.cvRect( 0,32, anchors[0].x, anchors[1].y))
    #subimage=cv.GetSubRect(destination,cv.cvRect(anchors[0].x ,anchors[0].y-80, 80, anchors[1].y-10))
    #subimage=cv.CloneImage(gray)
    #cv.DrawLine(subimage,anchors[0],anchors[1],cv.cvScalar(78,47,47))
    #cv.DrawLine(subimage,cv.cvPoint(gray.width,0),anchors[0],cv.cvScalar(78,47,47))
    print("Recortado")
    #cv.SaveImage("out.png", subimage)
    print('Salvo')
    cv.ShowImage('recortado',subimage)
    cv.WaitKey(0)