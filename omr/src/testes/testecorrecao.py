#!/usr/bin/python
import sys
# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

if __name__ == "__main__":

    filename = "teste2.png"
    hists=[]
    subimages=[]
    x=772
    y=410
    width=25
    height=25
    hist_size = 64
    num_cell=10
    answer=None
    max=0
    range_0=[0,256]
    ranges = [ range_0 ]
    gray = highgui.cvLoadImage( filename,0)
    if not gray:
        print "Failed to load %s" % filename
        sys.exit(-1)
    # create the output image
    edge = cv.cvCreateImage (cv.cvSize (gray.width, gray.height), 8, 1)
    
    cv.cvThreshold(gray,edge,150,255,cv.CV_THRESH_BINARY)

    #seleciona duas regioes
    for i in range(num_cell):
        subimages.append( cv.cvGetSubRect( edge, cv.cvRect( x, y+height*i, width, height )) )
        #cria histogramas
        hists.append( cv.cvCreateHist([hist_size], cv.CV_HIST_ARRAY, ranges, 1) );
        #calcula histogramas
        cv.cvCalcHist(subimages[-1],hists[-1])
        temp=cv.cvGet1D(hists[-1].bins,0)
        if max < temp[0]:
            max=temp
            answer=i
        #highgui.cvNamedWindow("imagem"+str(i), highgui.CV_WINDOW_AUTOSIZE)
        #highgui.cvShowImage ("imagem"+str(i), subimages[-1])

    '''[min_val1, max_val1, min_idx1, max_idx1] = cv.cvGetMinMaxHistValue(hist1)
    print("imagem 1")
    print([min_val1, max_val1, min_idx1, max_idx1])
    valor1= cv.cvGet1D(hist1.bins,0)
    [min_val2, max_val2, min_idx2, max_idx2] = cv.cvGetMinMaxHistValue(hist2)
    print("imagem 2")
    print([min_val2, max_val2, min_idx2, max_idx2])
    valor2= cv.cvGet1D(hist2.bins,0)
    print(valor1)
    print(valor2)
    print valor1[0] < valor2[0]    
    highgui.cvNamedWindow("imagem 1", highgui.CV_WINDOW_AUTOSIZE)
    # show the image	
    highgui.cvShowImage ("imagem 1", subimage1)

    
    
    # Wait for a key stroke; the same function arranges events processing
    '''
    #orde=sorted(hists,key=lambda hist: cv.cvGet1D(hist.bins,0))
    #print(cv.cvGet1D(orde[0].bins,0))
    resized = cv.cvCreateImage (cv.cvSize (1024, 768), 8, 1)
    highgui.cvNamedWindow("imagem", highgui.CV_WINDOW_AUTOSIZE)
    cv.cvResize(edge,resized)
    highgui.cvShowImage ("imagem", resized)
    #print(chr(97+answer))
    print(answer)
    highgui.cvWaitKey(0);
    
    
