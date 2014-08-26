# -*- coding: utf-8 -*-
__author__="Romualdo Andre da Costa"

from sys import argv
from optparse import OptionParser
import logging

if __name__ == "__main__":
    if(len(argv)!=3):
        print "usage: python test.py fileOmr fileOpscan"
    #colocar conteudo dos arquivos num dicionario
    answersOmr={}
    answersOpscan={}
    LOG_FILENAME = 'test.log'#arquivo de log
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
    logger=logging.getLogger(__name__)
    with open(argv[1],'r') as fileOmr:
        for line in fileOmr:
            answersOmr[line[:6]]=line[7:]
        fileOmr.close()
    with open(argv[2],'r') as fileOpscan:
        for line in fileOpscan:
            answersOpscan[line[:6]]=line[7:]
        fileOpscan.close()
    errors=0
    for inscricao, answers in answersOmr.iteritems():
        if inscricao in answersOpscan:
            answersOp=answersOpscan[inscricao]
            #print inscricao, answersOp
            for i in range(len(answers)):
                #print inscricao,answers[i],answersOp[i]
                if answers[i]!=answersOp[i]:
                    logger.info('dif insc: %s, pos: %d',inscricao,i)
                    errors+=1
    print 'erros: ',errors
