#/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
import numpy as np
import cv2
from glob import glob

if __name__ == '__main__':
	print len(argv)
	if(len(argv)<2):
		print "usage: python threshold.py threshold_value regex"
		exit(0)
	threshold= int(argv[1])
	for filename in glob(argv[-1]):
		print filename
		img = cv2.imread(filename)
		imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		retval, bin = cv2.threshold(imgray, threshold, 255, cv2.THRESH_BINARY)
		cv2.imwrite(str(threshold)+'gray.png', bin)
