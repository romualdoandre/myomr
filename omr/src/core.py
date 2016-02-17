<<<<<<< .mine
# -*- coding: utf-8 -*-

__author__="Romualdo Andre da Costa"
__date__ ="$04/04/2011 10:26:25$"
import os
import csv
import logging
import datetime
import cv2.cv as cv
import cv2
import numpy as np

class Core:
    '''
    Módulo de processamento de imagens
    '''
    def __init__(self,filenames=[],appfilename=None,datafilename=None,threshold=95):
        '''
        Construtor do módulo
        @param filenames : arquivos para processamento
        @param appfilename : arquivo de configuração
        @param datafilename: arquivo de saída
        @para mode: modo de gravação (sobrescrever ou adicionar)
        '''
        LOG_FILENAME = 'omr.log'#arquivo de log
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
        self.logger=logging.getLogger(__name__)
        self.reader=None #leitor de arquivo CSV
        self.appfile=None #arquivo de configuração
        self.datafile=None #arquivo de saída
        self.threshold=threshold#valor de filtro para binarizar a imagem e deixar apenas as marcações
        self.id='' #id da folha
        self.filenames=filenames
        self.croppedindex=0
        self.logger.info('Arquivo de saída:'+datafilename)
        self.logger.info('Arquivo de aplicação:'+appfilename)
        if datafilename!=None:
            self.datafile=open(datafilename,'w')
        if appfilename!=None:
            self.appfile=open(appfilename, 'rb')
            reader = csv.DictReader(self.appfile)
            self.conf = [row for row in reader]
            

    def run(self):
        '''
        método principal
        '''
        self.logger.info('Iniciando processamento:'+datetime.datetime.now().ctime())
        i=1
        for filename in self.filenames:
            filename=filename.replace('\\','/')
            filename=filename.encode('ascii','ignore')
            #para cada imagem de entrada, aplique o processamento
            if not self.process_image(filename):
                self.logger.error("Failed to process %s" % filename)
                print("Failed to process %s" % filename)
            print(str(i)+'/'+str(len(self.filenames)))
            i+=1            
        if self.appfile!=None:
            self.appfile.close()
        if self.datafile!=None:
            self.datafile.close()
        self.logger.info('Termino de processamento:'+datetime.datetime.now().ctime())

    def process_image(self,filename):
        '''
        processa a imagem, reconhecendo as marcações determinadas pelo arquivo de configuração
        @param filename : nome do arquivo contendo a imagem
        '''
        self.logger.info('Processando arquivo:'+filename)
        self.pre_process_image(filename, self.threshold)
        hist_size = 64 #tamanho do histograma
        ranges = [ 256 ] #variedade de valores analisados
                
        gray = cv2.imread(filename,0)
        if not gray:
            print( "Falha ao carregar %s" % filename)
            self.logger.error("Falha ao carregar %s" % filename)
            return False
        
        nameparts=filename.split('.')
        extension=nameparts[1]
        nameandpath=nameparts[0].split('/')
        self.id=''
        for row in self.conf:
            self.process_row(gray,row,hist_size,ranges,nameandpath,filename)
        
        self.datafile.write('\n')
        #muda o nome do arquivo original baseado no id da folha
        #newname=self.id+'.'+extension
        nameandpath[-1]=self.id+nameandpath[-1]+'.'+extension
        destname='/'.join(nameandpath)
        cv2.imwrite(filename,gray)
        if self.id!='':
            try:
                os.rename(filename,destname)
            except OSError:
                self.logger.info("arquivo existente: %s",destname)
        #processamento da folha finalizado
        
        return True
    def crop_cell(self,gray,i,x,y,width,height,hor,vert,space):
        '''
        recorta apenas uma marcação do campo
        @param gray : imagem original
        @param i : número da célula. Exemplo: 0 a 4 para a,b,c,d,e.
        @param x : coordenada no eixo X em pixels a partir do canto superior esquerdo
        @param y : coordenada no eixo Y em pixels a partir do canto superior esquerdo.
        @param width :  largura da célula
        @param height : altura da célula
        @param hor : 1 se for horizontal
        @param vert : 1 se for vertical
        @param space : espaço entre células
        '''
        inicio=0 if i==0 else 1
        ptx=x+width*i*hor+hor*space*inicio*i
        pty=y+height*i*vert+vert*space*inicio*i
        rect=(ptx,pty,width,height)
        src_region=gray[pty:pty+height,ptx:ptx+width] # cv.GetSubRect( gray, rect)
        #cropped=cv.CreateImage((width,height),8,1)
        #cv.Copy(src_region,cropped)
        #pt1=(ptx,pty)
        #pt2=(pt1[0]+width,pt1[1]+height)
        #cv.Rectangle(gray,pt1,pt2,(0,0,0))
        return np.copy(src_region)
    
    def calc_hist(self,subimages,hists,hist_size,ranges):
        '''
        Calcula o histograma de cada célula do campo
        @param subimages : imagens recortadas de cada célula
        @param hists : lista de histogramas para armazenas os resultados
        @param hist_size : tamanho dos histogramas
        @param ranges : faixas de valores dos histogramas
        '''
        #cria histogramas
        #hists.append( cv.CreateHist([hist_size], cv.CV_HIST_ARRAY, ranges, 1) );
        #calcula histogramas
        #cv.CalcHist([subimages[-1]],hists[-1])
        hist=cv2.calcHist([subimages[-1]],[0],None,[hist_size],ranges)
        hists.append(hist)
        #temp=cv.Get1D(hists[-1].bins,0)
        #temp2=cv.Get1D(hists[-1].bins,63)
        return [hist[0],hist[-1]]
    
    def process_row(self,gray,row,hist_size,ranges,nameandpath,filename):
        '''
        Processa uma linha do arquivo de configuração representando um campo ou questão da folha de respostas
        @param gray : imagem original da folha de respostas
        @param row : dicionário contendo as informações de uma linha do arquivo de configuração
        @param hist_size : tamanho dos histogramas
        @param ranges : faixas de valores dos histogramas
        @param nameandpath : nome e caminho do arquivo da imagem para salvar no log
        @param filename : nome do arquivo para operações de log
        '''
        #seleciona as regioes
        x=int(row['x'].split('.')[0])
        y=int(row['y'].split('.')[0])
        width=int(row['width'])
        height=int(row['height'])
        num_cell=int(row['num_cell'])
        space=int(row['space'])
        direction=row['direction']
        vert=0
        hor=0
        area=width*height
        hists=[] #histogramas para as imagens
        subimages=[]#partes da imagem para calcular o histograma
    
        if direction=='horizontal':
            hor=1
        else:
            vert=1
        answer=None
        duplicate=0

        histx=[]
        histy=[]
        for i in range(num_cell):
            cropped=self.crop_cell(gray,i,x,y,width,height,hor,vert,space)
            subimages.append( cropped )
            cell_hist=self.calc_hist(subimages,hists,hist_size,ranges)
            histx.append(cell_hist[0])
            histy.append(cell_hist[1])
            self.logger.info( 'black/area: %s',cell_hist[0]/area)
        
        
        for i in range(num_cell):
            self.logger.info('O valor do hist: %s,hist2: %s, tag: %s.i: %s ',x,y,row['tag'],i)
            if histx[i]/area>=0.15:#pelo menos 15% da área amostrada preenchida com preto
                duplicate+=1
                answer=i
        nullanswer=0    
        if duplicate>1:
            for cropped in subimages:
                cv2.imwrite("log/"+nameandpath[-1]+"_"+str(self.croppedindex)+".jpg", cropped)
                self.croppedindex+=1
            self.logger.warning('O arquivo %s possui marcacoes duplicadas no campo %s.duplicate: %s',filename,row['tag'],duplicate)
            nullanswer=1
        if duplicate==0:
            self.logger.warning('O arquivo %s sem marcacoes no campo %s.duplicate: %s',filename,row['tag'],duplicate)
            nullanswer=2
        if nullanswer==1:
            if row['type']=='num':
                answer=-6
            else:
                answer=-55
        if nullanswer==2:
            if row['type']=='num':
                answer=-16
            else:
                answer=-65
        if row['type']=='num':
            answer=chr(48+answer)
        else:
            answer=chr(97+answer).upper()
        if row['imid']=='1':
            self.id=self.id+answer

        self.datafile.write(answer)#escreve o resultado no arquivo

    def pre_process_image(self,filename,treshold):
        '''
        pré-processamento da imagem para remover ruídos
        @param filename : caminho completo do arquivo da imagem
        @param threshold : limiar para filtragem da imagem
        '''
        self.logger.info('Pré-Processando arquivo:'+filename)
        im = cv2.imread(filename ,0)

        if not im:
            print "Failed to load %s" % filename
            sys.exit(-1)
            
        retval, im = cv2.threshold(im, threshold, 255, cv2.THRESH_BINARY)
        cv2.imwrite(filename, im)
        
        

        
=======
# -*- coding: utf-8 -*-

__author__="Romualdo Andre da Costa"
__date__ ="$04/04/2011 10:26:25$"
import os,sys
import csv
import logging
import datetime
#import cv2.cv as cv
import cv2
import numpy as np

class Core:
    '''
    Módulo de processamento de imagens
    '''
    def __init__(self,filenames=[],appfilename=None,datafilename=None,threshold=95):
        '''
        Construtor do módulo
        @param filenames : arquivos para processamento
        @param appfilename : arquivo de configuração
        @param datafilename: arquivo de saída
        @para mode: modo de gravação (sobrescrever ou adicionar)
        '''
        LOG_FILENAME = 'omr.log'#arquivo de log
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
        self.logger=logging.getLogger(__name__)
        self.reader=None #leitor de arquivo CSV
        self.appfile=None #arquivo de configuração
        self.datafile=None #arquivo de saída
        self.threshold=threshold#valor de filtro para binarizar a imagem e deixar apenas as marcações
        self.id='' #id da folha
        self.filenames=filenames
        self.croppedindex=0
        self.logger.info('Arquivo de saída:'+datafilename)
        self.logger.info('Arquivo de aplicação:'+appfilename)
        if datafilename!=None:
            self.datafile=open(datafilename,'w')
        if appfilename!=None:
            self.appfile=open(appfilename, 'rb')
            reader = csv.DictReader(self.appfile)
            self.conf = [row for row in reader]
            

    def run(self):
        '''
        método principal
        '''
        self.logger.info('Iniciando processamento:'+datetime.datetime.now().ctime())
        i=1
        for filename in self.filenames:
            filename=filename.replace('\\','/')
            filename=filename.encode('ascii','ignore')
            #para cada imagem de entrada, aplique o processamento
            if not self.process_image(filename):
                self.logger.error("Failed to process %s" % filename)
                print("Failed to process %s" % filename)
            print(str(i)+'/'+str(len(self.filenames)))
            i+=1            
        if self.appfile!=None:
            self.appfile.close()
        if self.datafile!=None:
            self.datafile.close()
        self.logger.info('Termino de processamento:'+datetime.datetime.now().ctime())

    def process_image(self,filename):
        '''
        processa a imagem, reconhecendo as marcações determinadas pelo arquivo de configuração
        @param filename : nome do arquivo contendo a imagem
        '''
        self.logger.info('Processando arquivo:'+filename)
        self.pre_process_image(filename, self.threshold)
        hist_size = 64 #tamanho do histograma
        ranges = [0, 256 ] #variedade de valores analisados
                
        gray = cv2.imread(filename,0)
        if gray == None:
            print( "Falha ao carregar %s" % filename)
            self.logger.error("Falha ao carregar %s" % filename)
            return False
        
        nameparts=filename.split('.')
        extension=nameparts[1]
        nameandpath=nameparts[0].split('/')
        self.id=''
        for row in self.conf:
            self.process_row(gray,row,hist_size,ranges,nameandpath,filename)
        
        self.datafile.write('\n')
        #muda o nome do arquivo original baseado no id da folha
        #newname=self.id+'.'+extension
        nameandpath[-1]=self.id+nameandpath[-1]+'.'+extension
        destname='/'.join(nameandpath)
        cv2.imwrite(filename,gray)
        if self.id!='':
            try:
                os.rename(filename,destname)
            except OSError:
                self.logger.info("arquivo existente: %s",destname)
        #processamento da folha finalizado
        
        return True
    def crop_cell(self,gray,i,x,y,width,height,hor,vert,space):
        '''
        recorta apenas uma marcação do campo
        @param gray : imagem original
        @param i : número da célula. Exemplo: 0 a 4 para a,b,c,d,e.
        @param x : coordenada no eixo X em pixels a partir do canto superior esquerdo
        @param y : coordenada no eixo Y em pixels a partir do canto superior esquerdo.
        @param width :  largura da célula
        @param height : altura da célula
        @param hor : 1 se for horizontal
        @param vert : 1 se for vertical
        @param space : espaço entre células
        '''
        inicio=0 if i==0 else 1
        ptx=x+width*i*hor+hor*space*inicio*i
        pty=y+height*i*vert+vert*space*inicio*i
        rect=(ptx,pty,width,height)
        src_region=gray[pty:pty+height,ptx:ptx+width] # cv.GetSubRect( gray, rect)
        #cropped=cv.CreateImage((width,height),8,1)
        #cv.Copy(src_region,cropped)
        #pt1=(ptx,pty)
        #pt2=(pt1[0]+width,pt1[1]+height)
        #cv.Rectangle(gray,pt1,pt2,(0,0,0))
        return np.copy(src_region)
    
    def calc_hist(self,subimages,hists,hist_size,ranges):
        '''
        Calcula o histograma de cada célula do campo
        @param subimages : imagens recortadas de cada célula
        @param hists : lista de histogramas para armazenas os resultados
        @param hist_size : tamanho dos histogramas
        @param ranges : faixas de valores dos histogramas
        '''
        #cria histogramas
        #hists.append( cv.CreateHist([hist_size], cv.CV_HIST_ARRAY, ranges, 1) );
        #calcula histogramas
        #cv.CalcHist([subimages[-1]],hists[-1])
        hist=cv2.calcHist([subimages[-1]],[0],None,[hist_size],ranges)
        hists.append(hist)
        #temp=cv.Get1D(hists[-1].bins,0)
        #temp2=cv.Get1D(hists[-1].bins,63)
        return [hist[0],hist[-1]]
    
    def process_row(self,gray,row,hist_size,ranges,nameandpath,filename):
        '''
        Processa uma linha do arquivo de configuração representando um campo ou questão da folha de respostas
        @param gray : imagem original da folha de respostas
        @param row : dicionário contendo as informações de uma linha do arquivo de configuração
        @param hist_size : tamanho dos histogramas
        @param ranges : faixas de valores dos histogramas
        @param nameandpath : nome e caminho do arquivo da imagem para salvar no log
        @param filename : nome do arquivo para operações de log
        '''
        #seleciona as regioes
        x=int(row['x'].split('.')[0])
        y=int(row['y'].split('.')[0])
        width=int(row['width'])
        height=int(row['height'])
        num_cell=int(row['num_cell'])
        space=int(row['space'])
        direction=row['direction']
        vert=0
        hor=0
        area=width*height
        hists=[] #histogramas para as imagens
        subimages=[]#partes da imagem para calcular o histograma
    
        if direction=='horizontal':
            hor=1
        else:
            vert=1
        answer=None
        duplicate=0

        histx=[]
        histy=[]
        for i in range(num_cell):
            cropped=self.crop_cell(gray,i,x,y,width,height,hor,vert,space)
            subimages.append( cropped )
            cell_hist=self.calc_hist(subimages,hists,hist_size,ranges)
            histx.append(cell_hist[0])
            histy.append(cell_hist[1])
            self.logger.info( 'black/area: %s',cell_hist[0]/area)
        
        
        for i in range(num_cell):
            self.logger.info('O valor do hist: %s,hist2: %s, tag: %s.i: %s ',x,y,row['tag'],i)
            if histx[i]/area>=0.15:#pelo menos 15% da área amostrada preenchida com preto
                duplicate+=1
                answer=i
        nullanswer=0    
        if duplicate>1:
            for cropped in subimages:
                cv2.imwrite("log/"+nameandpath[-1]+"_"+str(self.croppedindex)+".jpg", cropped)
                self.croppedindex+=1
            self.logger.warning('O arquivo %s possui marcacoes duplicadas no campo %s.duplicate: %s',filename,row['tag'],duplicate)
            nullanswer=1
        if duplicate==0:
            self.logger.warning('O arquivo %s sem marcacoes no campo %s.duplicate: %s',filename,row['tag'],duplicate)
            nullanswer=2
        if nullanswer==1:
            if row['type']=='num':
                answer=-6
            else:
                answer=-55
        if nullanswer==2:
            if row['type']=='num':
                answer=-16
            else:
                answer=-65
        if row['type']=='num':
            answer=chr(48+answer)
        else:
            answer=chr(97+answer).upper()
        if row['imid']=='1':
            self.id=self.id+answer

        self.datafile.write(answer)#escreve o resultado no arquivo

    def pre_process_image(self,filename,threshold):
        '''
        pré-processamento da imagem para remover ruídos
        @param filename : caminho completo do arquivo da imagem
        @param threshold : limiar para filtragem da imagem
        '''
        self.logger.info('Pré-Processando arquivo:'+filename)
        im = cv2.imread(filename ,0)
        if im == None:
            print "Failed to load %s" % filename
            sys.exit(-1)
            
        retval, im = cv2.threshold(im, threshold, 255, cv2.THRESH_BINARY)
        cv2.imwrite(filename, im)
        
        

        

>>>>>>> .theirs
