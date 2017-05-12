#/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
from glob import glob
import numpy as np
import cv2
from math import atan2,degrees

if __name__ == '__main__':
    if(len(argv)!=6):
        print "usage: python align.py x1 y1 x2 y2 regex"
        exit(0)
    x1= int(argv[1])
    y1=int(argv[2])
    x2= int(argv[3])
    y2=int(argv[4])
    ref_area=2500
    threshold=200
    x_padding=150
    for fn in glob(argv[-1]):
        print fn
        img = cv2.imread(fn)
        img2=img[:y1,x1:x_padding+x1]
        imgray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        retval, bin = cv2.threshold(imgray, threshold, 255, cv2.THRESH_BINARY)
        _,contours, _ = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours( img2, contours, -1, (0, 255, 0), 2 )
        
        max_area=0
        max_rect=0
        for c in contours:
            area=cv2.contourArea(c)
            if  area<=ref_area:
                rect=cv2.minEnclosingCircle(c)
                if area > max_area:
                    max_area=area
                    max_rect=rect
        
        img3=img[y2:,x2:x_padding+x2]
        #cv2.imshow('squares2', img3)
        imgray = cv2.cvtColor(img3,cv2.COLOR_BGR2GRAY)
        retval, bin = cv2.threshold(imgray, threshold, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours( img3, contours, -1, (0, 255, 200), 2 )
        max_area2=0
        max_rect2=0
        for c in contours:
            area=cv2.contourArea(c)
            '''cv2.isContourConvex(c) and area<=2500 and area >=1300'''
            if  area<=ref_area:
                rect=cv2.minEnclosingCircle(c)
                if area > max_area2:
                    max_area2=area
                    max_rect2=rect
        print 'up'
        print max_rect
        print max_area
        print 'down'
        print max_rect2
        print max_area2
        
        if max_rect and max_rect2:
            a1=(int(max_rect[0][0]),int(max_rect[0][1]))
            a2=(int(max_rect2[0][0]),int(max_rect2[0][1]))
            
            '''cv2.circle(img2,a1,int(max_rect[1]),(0,255,0),3)
            cv2.circle(img3,a2,int(max_rect2[1]),(255,0,0),3)
            cv2.imshow('squares', img2)
            cv2.imshow('squares2', img3)'''

            #calcula angulo
            xdiff=a1[0]-a2[0]
            ydiff=y2+(a1[1]-a2[1])
            angle=degrees(atan2(ydiff,xdiff))
            print 'xdiff:',xdiff
            print 'ydiff:',ydiff
            print 90-abs(angle)

            #rotacionar imagem
            img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            shape=img.shape
            #image_center = tuple(np.array(shape)/2)
            image_center=(a1[1]+x1,a1[0])
            rot_mat = cv2.getRotationMatrix2D(tuple(np.array(shape)/2),90-angle,1.0)
            result = cv2.warpAffine(img, rot_mat, shape[::-1],flags=cv2.INTER_LANCZOS4)
            fn=fn.replace('\\','/')
            fn=fn.encode('ascii','ignore')
            nameparts=fn.split('.')
            extension=nameparts[1]
            nameandpath=nameparts[0].split('/')
            nameandpath[-1]='rot_'+nameandpath[-1]+'.'+extension
            destname='/'.join(nameandpath)
            print destname
            cv2.imwrite(destname,result,(cv2.IMWRITE_JPEG_QUALITY,100))
        else:
            print 'marcas de referencia nao encontradas'
        
        '''cv2.imshow('result', result)
        ch = 0xFF & cv2.waitKey()
        if ch == 27:
            break
    cv2.destroyAllWindows()'''
