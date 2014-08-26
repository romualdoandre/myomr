#/usr/bin/env python

'''
Simple "Square Detector" program.

Loads several images sequentially and tries to find squares in each image.
'''

import numpy as np
import cv2


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in xrange(0, 255, 30):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                area=cv2.contourArea(cnt)
                if len(cnt) == 4 and  area < 2000 and area> 300 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares

if __name__ == '__main__':
    from glob import glob
    for fn in glob('teste0062.jpg'):
        img = cv2.imread(fn)
        
        squares = find_squares(img)
        print len(squares)
        cv2.drawContours( img, squares, -1, (0, 255, 0), 3 )
        #cv2.imshow('squares', img)
        cv2.imwrite('squares.jpg',img)
        ch = 0xFF & cv2.waitKey()
        if ch == 27:
            break
    cv2.destroyAllWindows()
