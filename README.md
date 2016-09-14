#myomr
=====

An [Optical Mark Recognizer Software](https://en.wikipedia.org/wiki/Optical_mark_recognition "OMR") made by me using OpenCV and Python.

This software has two parts: a GUI configurer and a CLI OMR.

## Requirements:
* Python 2.7.x
* OpenCV 2.4.x
* Numpy
* PIL and ImageTk
* Tix 

## License:
* [GPL V2](LICENSE)

Preprocessing
-----

You might preprocessing the image to ensure that there is not problems with the sheet image alignment. 

First you might use scripts to ensure the image alignment. Enter the _/omr/src/cropped_ folder and use the *align.py* script as follow:

> python align.py x1 y1 x2 y2 regex

Where *x1* and *y1* is the beginning of the rightest superior mark, *x2* and *y2* is the beginning of the rightest inferior mark and *regex* is a regular expression refering the image files. All the result files will have a *rot_* prefix.

After you might crop the image with the _/omr/src/cropped/crop.py_ script as follow:

> python crop.py x1 y1 x2 y2 regex

Where *x1* and *y1* is the beginning of the rightest superior mark, *x2* and *y2* is the beginning of the rightest inferior mark and *regex* is a regular expression refering the image files. All the result files will have a *crop_* prefix.

GUI configurer tool
-----

