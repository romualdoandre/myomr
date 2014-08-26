#/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
import numpy as np
import cv2
from glob import glob

if __name__ == '__main__':
    if(len(argv)!=6):
        print "usage: python crop.py x1 y1 x2 y2 regex"
        exit(0)
    x= int(argv[1])
    y=int(argv[2])
    x2= int(argv[3])
    y2=int(argv[4])
    x_padding=150
    threshold=200
    ref_area=2500
    for fn in glob(argv[-1]):
        print fn
        img = cv2.imread(fn)
        img2=img[:y,x:x+x_padding]
        #squares = find_squares(img)
        imgray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        retval, bin = cv2.threshold(imgray, threshold, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        #cnt=sorted(contours,key= lambda cnt: cv2.contourArea(cnt))
        #minrect=cv2.minAreaRect(cnt[0])
        #print cnt[0]
        #squares=[]
        #print len(contours)
        max_area=0
        max_rect=0
        for c in contours:
            area=cv2.contourArea(c)
            ''' cv2.isContourConvex(c) and area<=2500 and area >=1300'''
            if  area<=ref_area:
                #rect=cv2.minAreaRect(c)
                #rect=cv2.boundingRect(c)
                rect=cv2.minEnclosingCircle(c)
                if area > max_area:
                    max_area=area
                    max_rect=rect
                #squares.append(rect)                
                #cv2.ellipse(img,rect,(0, 255, 0))
                #squares.append(c)
        #squares[0].sort()
        #rect=squares[0]
        #la=cv2.boundingRect(img)
        #p1=rect[0]
        #print p1
        #print type( la)
        #cv2.drawContours( img, squares, -1, (0, 255, 0), 3 )
        #cv2.drawContours( img, contours, -1, (0, 255, 0), 3 )
        
        #x1,x2,y1,y2=int(la[0][0]),int([1][0]),int(la[0][1]),int(la[1][1])
        #cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),10)
        #src=img[p1[0]:][p1[1]:]
        #cv2.imshow('squares', img2)
        img3=img[:y2,:x2]
        #cv2.imshow('squares2', img3)
        imgray = cv2.cvtColor(img3,cv2.COLOR_BGR2GRAY)
        retval, bin = cv2.threshold(imgray, threshold, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
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
                    
        if max_rect and max_rect2:
			print max_area
			print max_rect
			print max_rect2
			#pts=max_rect[0]
			#cv2.ellipse(img,max_rect,(0, 255, 0),4)
			#cv2.circle(img,max_rect[0],(0,255,0),3)
			#img=img[pts[1]:]
			img=img[max_rect[0][1]:,max_rect2[0][0]:x+max_rect[0][0]]
			cv2.imwrite('crop_'+fn,img,(cv2.IMWRITE_JPEG_QUALITY,100))
        else:
			print 'marcas de referencia nao encontradas'
        #cv2.imshow('squares', img2)            
        
        '''ch = 0xFF & cv2.waitKey()
        if ch == 27:
            break
    cv2.destroyAllWindows()'''
