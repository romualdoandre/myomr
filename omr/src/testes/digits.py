#/usr/bin/env python

import numpy as np
import cv2


if __name__ == '__main__':
    img=cv2.imread('teste0062.jpg',0)
    '''h, w = img.shape[:2]
    m=cv2.moments(img)
    if abs(m['mu02']) < 1e-2:
        print 'girou'
        skew = m['mu11']/m['mu02']
        M = np.float32([[1, skew, -0.5*h*skew], [0, 1, 0]])
        img = cv2.warpAffine(img, M, (w, h), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)'''
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    x,y,w,h = cv2.boundingRect(contours[0])
    cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow('test', img)
    cv2.waitKey(0)
