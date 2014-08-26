#!/usr/bin/python
import sys
# import the necessary things for OpenCV
import cv2.cv as cv
import cv2
import numpy as np
import matplotlib.pyplot as pyplt

if __name__ == "__main__":

    #filename = "teste0003.jpg"
    hist=None
    hist_size = 256
    range_0=[0,256]
    ranges = [ range_0 ]
    #gray = cv.LoadImage( filename,0)
    #if not gray:
    #    print "Failed to load %s" % filename
    #    sys.exit(-1)
    # create the output image
    #edge = cv.CreateImage ((gray.width, gray.height), 8, 1)
    #cv.cvSmooth (gray, edge,cv.CV_BLUR, 3, 3, 0)
    #cv.Threshold(gray,edge,250,255,cv.CV_THRESH_BINARY)
    #seleciona duas regioes
    #subimage1 = cv.GetSubRect( edge, ( 185, 1109, 35, 35 ))
    subimage1=cv.LoadImage("9t.jpg",0)
    thre1=cv.CreateImage ((subimage1.width, subimage1.height), 8, 1)
    cv.Threshold(subimage1,thre1,100,255,cv.CV_THRESH_BINARY)
    
    subimage2=cv.LoadImage("9f.jpg",0)
    thre2=cv.CreateImage ((subimage2.width, subimage2.height), 8, 1)
    cv.Threshold(subimage2,thre2,100,255,cv.CV_THRESH_BINARY)
    #subimage2 = cv.GetSubRect( edge, ( 285, 1109, 35, 35 ))
    #cria histogramas
    hist1 = cv.CreateHist([hist_size], cv.CV_HIST_ARRAY, ranges, 1);
    hist2 = cv.CreateHist([hist_size], cv.CV_HIST_ARRAY, ranges, 1);
    #calcula histogramas
    cv.CalcArrHist([thre1],hist1)
    cv.CalcArrHist([thre2],hist2)
    
    [min_val1, max_val1, min_idx1, max_idx1] = cv.GetMinMaxHistValue(hist1)
    print("imagem 1")
    print cv.Get1D(hist1.bins,255)
    print([min_val1, max_val1, min_idx1, max_idx1])
    valor1= cv.Get1D(hist1.bins,0)
    [min_val2, max_val2, min_idx2, max_idx2] = cv.GetMinMaxHistValue(hist2)
    print("imagem 2")
    print([min_val2, max_val2, min_idx2, max_idx2])
    valor2= cv.Get1D(hist2.bins,0)
    print(valor1)
    print(valor2)
    print valor1[0] < valor2[0]    
    cv.NamedWindow("imagem 1", cv.CV_WINDOW_AUTOSIZE)
    # show the image	
    cv.ShowImage ("imagem 1", thre1)

    cv.NamedWindow("imagem 2", cv.CV_WINDOW_AUTOSIZE)
    cv.ShowImage ("imagem 2", thre2)
    
    # Wait for a key stroke; the same function arranges events processing
    cv.WaitKey(0);

    
    '''size = 256
    histo = np.zeros(size, dtype = np.int32)
     
    for x in range(0, subimage1.height):
      for y in range(0, subimage1.width):
        tuple = cv.Get2D(subimage1, x, y)
        histo[(tuple[0] + tuple[1] + tuple[2])/3] += 1
     
    pyplt.bar(left = np.arange(histo.size), height = histo)
    pyplt.figure()
    for x in range(0, subimage2.height):
      for y in range(0, subimage2.width):
        tuple = cv.Get2D(subimage2, x, y)
        histo[(tuple[0] + tuple[1] + tuple[2])/3] += 1
     
    pyplt.bar(left = np.arange(histo.size), height = histo)
    pyplt.show()'''
    
