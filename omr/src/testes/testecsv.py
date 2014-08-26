#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import csv
# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

if __name__ == "__main__":

    filenames =['teste3.png','teste2.png']
    hists=[]
    subimages=[]
    hist_size = 64
    range_0=[0,256]
    ranges = [ range_0 ]
    out=open('answers.txt','a')

    for filename in filenames:
        gray = highgui.cvLoadImage( filename,0)
        if not gray:
            print "Failed to load %s" % filename
            sys.exit(-1)
        # create the output image
        edge = cv.cvCreateImage (cv.cvSize (gray.width, gray.height), 8, 1)

        cv.cvThreshold(gray,edge,150,255,cv.CV_THRESH_BINARY)

        with open('config.csv', 'rb') as f:
            reader = csv.DictReader(f)
            for row in reader:
                #seleciona as regioes
                x=int(row['x'])
                y=int(row['y'])
                width=int(row['width'])
                height=int(row['height'])
                num_cell=int(row['num_cell'])
                direction=row['direction']
                vert=0
                hor=0
                if direction=='horizontal':
                    hor=1
                else:
                    vert=1
                answer=None
                max=0
                for i in range(num_cell):
                    subimages.append( cv.cvGetSubRect( edge, cv.cvRect( x+width*i*hor, y+height*i*vert, width, height )) )
                    #cria histogramas
                    hists.append( cv.cvCreateHist([hist_size], cv.CV_HIST_ARRAY, ranges, 1) );
                    #calcula histogramas
                    cv.cvCalcHist(subimages[-1],hists[-1])
                    temp=cv.cvGet1D(hists[-1].bins,0)
                    if max < temp[0]:
                        max=temp[0]
                        answer=i
                if row['type']=='numeric':
                    answer=str(answer)
                else:
                    answer=chr(97+answer).upper()
                out.write(answer)
            f.close()
        out.write('\n')
        '''resized = cv.cvCreateImage (cv.cvSize (1024, 768), 8, 1)
        highgui.cvNamedWindow("imagem", highgui.CV_WINDOW_AUTOSIZE)
        cv.cvResize(edge,resized)
        highgui.cvShowImage ("imagem", resized)'''    
    
    # Wait for a key stroke; the same function arranges events processing
    '''resized = cv.cvCreateImage (cv.cvSize (1024, 768), 8, 1)
    highgui.cvNamedWindow("imagem", highgui.CV_WINDOW_AUTOSIZE)
    cv.cvResize(edge,resized)
    highgui.cvShowImage ("imagem", resized)'''
    #print(chr(97+answer))
    out.close()
    print file('answers.txt').read()
    #highgui.cvWaitKey(0);
    
    
