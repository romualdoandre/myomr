# -*- coding: utf-8 -*-
__author__="Romualdo Andre da Costa"

from sys import argv
from optparse import OptionParser
from core import Core
import glob

class Omr:
    '''
    This module parses the options from comand line and starts the process
    '''
    def __init__(self,options):
        '''
        Constructor
        @param options : program options
        '''
        self.core=None
        self.appfilepath=options.appfilepath
        self.datafilepath=options.datafilepath
        self.inputfolder=options.inputfolder
        self.extension=options.extension
        self.threshold=options.threshold
    
    def scan(self):
        '''
        Starts the processing. Supported image formats: all supported by OpenCV and PIL
        '''
        if self.inputfolder!=None and self.appfilepath!=None and self.datafilepath!=None:
            self.core=Core(glob.glob(self.inputfolder+'/*.'+self.extension),self.appfilepath,self.datafilepath,self.threshold)
            self.core.run()
        else:
            print("Por favor, forneÃ§a a pasta de entrada, o arquivo de aplicaÃ§Ã£o e o arquivo de dados")

if __name__ == "__main__":
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage,version="%prog 1.0")
    parser.add_option("-i", "--input",action="store", type="string", dest="inputfolder",help='folder with images')
    parser.add_option("-o", "--output",action="store", type="string", dest="datafilepath",help='output file with sheets data')
    parser.add_option("-a", "--app",action="store", type="string", dest="appfilepath",help='file with sheet fields')
    parser.add_option("-t", "--threshold",action="store", type="int", dest="threshold",help='threshold value')
    parser.add_option("-e", "--extension",action="store", type="string", dest="extension",help='file extension of image files, all supported by OpenCV and PIL')
    (options, args)= parser.parse_args(argv)
    program=Omr(options)
    program.scan()
