#/usr/bin/env python

'''
Simple "Square Detector" program.

Loads several images sequentially and tries to find squares in each image.
'''

import numpy as np
import cv2

if __name__ == '__main__':
    from glob import glob
    for fn in glob('image*.tif'):
        print fn
        img = cv2.imread(fn)
        img2=img[:600,1900:]
        #squares = find_squares(img)
        imgray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        retval, bin = cv2.threshold(imgray, 200, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        #cnt=sorted(contours,key= lambda cnt: cv2.contourArea(cnt))
        #minrect=cv2.minAreaRect(cnt[0])
        #print cnt[0]
        squares=[]
        #print len(contours)
        max_area=0
        max_rect=0
        for c in contours:
            area=cv2.contourArea(c)
            ''' cv2.isContourConvex(c) and area<=2500 and area >=1300'''
            if  area<=2500:
                #rect=cv2.minAreaRect(c)
                #rect=cv2.boundingRect(c)
                rect=cv2.minEnclosingCircle(c)
                if area > max_area:
                    max_area=area
                    max_rect=rect
                squares.append(rect)                
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
        shape=img.shape
        if max_rect:
            print max_area
            print max_rect
            #pts=max_rect[0]
            #cv2.ellipse(img,max_rect,(0, 255, 0),4)
            #cv2.circle(img,max_rect[0],(0,255,0),3)
            #img=img[pts[1]:]
            img=img[max_rect[0][1]:]
        #cv2.imshow('squares', img2)            
        cv2.imwrite('la'+fn+'.jpg',img)
        ch = 0xFF & cv2.waitKey()
        if ch == 27:
            break
    cv2.destroyAllWindows()
