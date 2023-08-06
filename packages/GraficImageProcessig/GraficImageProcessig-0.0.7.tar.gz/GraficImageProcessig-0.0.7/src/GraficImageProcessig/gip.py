import xml.etree.ElementTree as Et
import cv2
import imageio
from skimage.io import imshow, imread,imread_collection
from sklearn.model_selection import train_test_split
from skimage import color,exposure
import csv
import argparse
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import numpy as np
import os


class GraficPlot():


    def __init__(self, width=10,height=30):

        '''
        This module aims to simplify the plot of graphics in order to make it more 
        intuitive and practical, plotting several images in user-defined axis,
        PARAMETERS
        ==========
        width:int
            specifies the width of the images

        heigth: int
            specifies the height of the images

        '''
        self.width = width
        self.height = height



    def MultiPlot(self,rows=0, columns=0,  dataset=None, formatImg="jpg",read=False):
        
        '''
        This function will receive an image dataset where it will plot them, 
        based on the number of rows and columns passed as parameter

        PARAMETERS
        ==========
        rows: int
            determines how many lines the plot will have

        columsn:int
            determines how many columns the plot will have


        dataset: str
            image dataset

        formatImg:
            the format of the images

        read:bool
            determine if images will be read

        '''
        args = argparse.ArgumentParser(description='multiple image plot')
        args.add_argument('--rows', help='linhas do grafico', type=int, default=None)
        args.add_argument('--columns', help='colunas do grafico', type=int, default=None)
        args.add_argument('--formatImg', help='formato das imagens', type=str, default="jpg")

        args = args.parse_args(["--rows", str(rows),
                               '--columns',str(columns),
                               "--formatImg", formatImg])

        fig, ax = plt.subplots(args.rows, args.columns,figsize=(self.width,self.height))

        if read:

            dataset = glob(dataset + '/*.' + args.formatImg)
            dataset = imread_collection(dataset)


        
        k = 0
        imshow(dataset[0])
        for i in range(args.rows):
            for j in range(args.columns):
                ax[i,j].imshow(dataset[k])
                if k < len(dataset):
                    k+=1

        plt.show()


    def MultiHistPlot(self,rows=0, columns=0, dataset=None, formatImg='jpg',read=False):


        '''
        This function will receive an image dataset where it will 
        perform the histogram graph for all images,
        based on the number of rows and columns passed as a parameter

        PARAMETERS
        ==========
        rows: int
            determines how many lines the plot will have

        columsn:int
            determines how many columns the plot will have

        dataset: str
            image dataset

        formatImg:
            the format of the images

        read:bool
            determine if images will be read

        '''
        args = argparse.ArgumentParser(description='multiple image plot')
        args.add_argument('--rows', help='linhas do grafico', type=int, default=None)
        args.add_argument('--columns', help='colunas do grafico', type=int, default=None)
        args.add_argument('--formatImg', help='formato das imagens', type=str, default="jpg")


        args = args.parse_args(["--rows", str(rows),
                               '--columns',str(columns),
                               "--formatImg", formatImg])

        fig, ax = plt.subplots(args.rows, args.columns,figsize=(self.width,self.height))
        imagens = dataset
    
        if read:
    
            imagens = glob(dataset + '/*.' + args.formatImg)
            imagens = imread_collection(imagens)

        k = 0
        for i in range(args.rows):
            for j in range(args.columns):
                #criando matriz de uns, usando as dimensoes e tamanho da imagem
                weights = np.ones(imagens[k].ravel().shape) / float(imagens[k].size)
                #criando grafico de histogramas
                ax[i,j].hist(imagens[k].flatten(), bins=256,weights=weights)
                if k < len(imagens):
                    k+=1

        plt.show()    


    def LearnPlot(self,Epochs=1,Dataset=None,MetricsName=None,Title="Grafico de Metricas",Eixo_x="Eixo X",Eixo_y="Eixo_Y",Height=8,Width=15, Save=False):

        '''
        This function will receive a dataframe with the learning metrics and will 
        return a line graph containing the performance of those same metrics

        PARAMETERS
        ==========
        Epochs: int
            number of epochs whose metrics were obtained

        Dataset:dataframe
            metrics dataset

        MetricsName:list
            name of the metrics contained in the dataset

        Title: str
            graphic title

        Dataset: str
            image dataset

        Eixo_x:str
            x-axis name

        Eixo_y:str
            y-axis name

        Save:bool
            Specify whether to save the graphic

        '''
        Epochs = [x for x in range(Epochs)]
        plt.figure(figsize=(Width,Height))
        for i in MetricsName:
            
            plt.plot(Epochs,Dataset[i],label=i)
            plt.grid(True)
            plt.legend()
            
        plt.ylabel(Eixo_y)
        plt.xlabel(Eixo_x)

        if Save:
            plt.savefig(Title+'.svg')

        plt.show()




    def MultiImage(self,imagem=None,  norm=True,gray=True,equa=True,equaGray=True,adap=True,adapGray=True):


        '''
        This function will apply different filters over
        an image and plot each one of them

        PARAMETERS
        ==========
        imagem:str
            path to image

        norm: bool
            normal image plot

        gay: bool
            gray image plot

        equa:bool
            image plot with histogram equalization

        equaGray:bool
            image plot with histogram and gray equalization

        adap:bool
            image plot with adapthist equalization

        adapGray:bool
            image plot with adapthist and gray equalization



        '''

       
        args = argparse.ArgumentParser(description='multiple-image histogram plot')
        args.add_argument('--imagem', help='dataset para plot', type=str, default=None)
        args.add_argument('--norm', help='linhas do grafico', type=bool, default=False)
        args.add_argument('--gray', help='colunas do grafico', type=bool, default=False)
        args.add_argument('--equa', help='colunas do grafico', type=bool, default=False)
        args.add_argument('--equaGray', help='colunas do grafico', type=bool, default=False)
        args.add_argument('--adap', help='colunas do grafico', type=bool, default=False)
        args.add_argument('--adapGray', help='colunas do grafico', type=bool, default=False)

        args = args.parse_args(["--norm",str( norm),
                               '--gray',str(gray),
                               "--equa", str(equa),
                               "--equaGray", str(equaGray),
                                "--adap", str(adap),
                               "--adapGray", str(adapGray),
                                "--imagem", imagem,])

        
        args.imagem = imread(args.imagem)
        plt.figure(figsize=(self.width,self.height))
        
        if args.norm:
            plt.subplot(421), plt.imshow(args.imagem)
            weights = np.ones(args.imagem.ravel().shape) / float(args.imagem.size)
            plt.subplot(422),  plt.hist(args.imagem.flatten(), bins=256,weights=weights)
        if args.gray:
            img_gray = color.rgb2gray(args.imagem)
            plt.subplot(423), plt.imshow(img_gray,plt.cm.gray)
            weights = np.ones(img_gray.ravel().shape) / float(img_gray.size)
            plt.subplot(424),  plt.hist(img_gray.flatten(), bins=256,weights=weights)
            
        if args.equa:
            img_gray = exposure.equalize_hist(args.imagem)
            plt.subplot(425), plt.imshow(img_gray,plt.cm.gray)
            weights = np.ones(img_gray.ravel().shape) / float(img_gray.size)
            plt.subplot(426),  plt.hist(img_gray.flatten(), bins=256,weights=weights)
            
        if args.equaGray:
            img_gray = exposure.equalize_hist(color.rgb2gray(args.imagem))
            plt.subplot(427), plt.imshow(img_gray,plt.cm.gray)
            weights = np.ones(img_gray.ravel().shape) / float(img_gray.size)
            plt.subplot(428),  plt.hist(img_gray.flatten(), bins=256,weights=weights)




class ImageFilters():

    """
    ImageFilters comes to facilitate the application of filters in an entire 
    image dataset, being able to apply a filter to a certain color channel
    PARAMETERS
    ==========
     dataset: str
        image dataset


    formatImg:
        the format of the images


    """

    def __init__(self, dataset=None,formatImg="jpg"):
        self.dataset = dataset
        self.formatImg = formatImg


    def DataFilters(self, Gray=True,equaHist=True,equaAdap=True):


        '''
        apply multiple filters to an image dataset
        PARAMETERS
        ==========
       
        Gray: bool
            gray image filter

        equaHist:bool
            apply histogram equalization filter to the image

        equaAdap:bool
            apply adapthist equalization filter to the image


        '''
 
        args = argparse.ArgumentParser(description='multiple-image histogram plot')
        args.add_argument('--equaHist', help='colunas do grafico', type=bool, default=False)
        args.add_argument('--Gray', help='colunas do grafico', type=bool, default=False)
        args.add_argument('--equaAdap', help='colunas do grafico', type=bool, default=False)
        
        args = args.parse_args(["--equaHist", str(equaHist),
                                "--equaAdap", str(equaAdap),
                                "--Gray", str(Gray)])
        
        self.dataset = glob(self.dataset + '/*.' + self.formatImg)
        self.dataset = imread_collection(self.dataset)
        if Gray:
            self.dataset = [color.rgb2gray(x) for x in self.dataset]
            
        if args.equaHist:
            self.dataset = [exposure.equalize_hist(x) for x in self.dataset]
            
        if args.equaAdap:
            self.dataset = [exposure.equalize_adapthist(x) for x in self.dataset]
 
        return self.dataset

    def EquaAdapthist(self,dataset,canal):
        dataset_canal = []
        for imagem in dataset:
            final_img = imagem
            for i in range(imagem.shape[0]):

                final_img[i][:,canal] = exposure.equalize_hist(imagem[i][:,2])
            dataset_canal.append(final_img)
            
        return dataset_canal


    def EquaHistograma(self,dataset,canal):
        dataset_canal = []
        for imagem in dataset:
            final_img = imagem
            for i in range(imagem.shape[0]):

                final_img[i][:,canal] = exposure.equalize_adapthist(imagem[i][:,2])
            dataset_canal.append(final_img)
            
        return dataset_canal


    def ChannelFilters(self,canal="blue", equaHist=True,equaAdap=True):


        '''
        apply a filter to a certain color channel in the image
        PARAMETERS
        ==========

        canal:int
            chosen color channel


        equaHist:bool
            apply histogram equalization filter to the image

        equaAdap:bool
            apply adapthist equalization filter to the image

        '''
       
        args = argparse.ArgumentParser(description='multiple-image histogram plot')
        args.add_argument('--equaHist', help='colunas do grafico', type=bool, default=False)
        args.add_argument('--canal', help='colunas do grafico', type=str, default=None)
        args.add_argument('--equaAdap', help='colunas do grafico', type=bool, default=False)
        
        args = args.parse_args(["--equaHist", str(equaHist),
                                "--equaAdap", str(equaAdap),
                                "--canal", canal])

        
        self.dataset = glob(self.dataset + '/*.' + self.formatImg)
        self.dataset = imread_collection(self.dataset)
        
        dataset_canal = []
        
        if args.equaHist:
            if args.canal=='blue':
                dataset_canal = self.EquaHistograma(self.dataset,0)
                
            if args.canal=='red':
                dataset_canal = self.EquaHistograma(self.dataset,1)
                
            if args.canal=='green':
                dataset_canal = self.EquaHistograma(self.dataset,2)

        if args.equaAdap:
            
            if args.canal=='blue':
                dataset_canal = self.EquaAdapthist(self.dataset,0)
                
            if args.canal=='red':
                dataset_canal = self.EquaAdapthist(self.dataset,1)
                
            if args.canal=='green':
                dataset_canal = self.EquaAdapthist(self.dataset,2)

          
        return dataset_canal


    def PathSave(self,dataset,path):

        if not os.path.exists(path):
            os.makedirs(path)
        
        for i in dataset:
            img = imread(i)
            if '/' in i:
                aux = 0
                while True:

                    try: 
                         flag = i.index('/',aux+1)

                    except:
                        break

                    aux = flag

                out = i[aux:]
            imageio.imwrite(path + '/' + out, img) 
        

    def DataSplit(self,size_test=0.2, size_validation=0.1,path_train='Train',path_validation='Validation',path_test="Test"):
        
        
        '''
        This function splits the image dataset and saves it in user-determined folders

        PARAMETERS
        ==========

        size_test:float
            the proportion of the division of training and test data

        size_validation:float
            the proportion of the division of training and validation data

        path_train: str
            path to save training images

        path_validation: str
            path to save validation images

        path_test: str
            path to save test images

        '''


        args = argparse.ArgumentParser(description='multiple-image histogram plot')
        args.add_argument('--size_test', help='colunas do grafico', type=float, default=0.2)
        args.add_argument('--size_validation', help='colunas do grafico', type=float, default=0.1)
        args.add_argument('--path_train', help='dataset para plot', type=str, default="Train")
        args.add_argument('--path_test', help='dataset para plot', type=str, default="Test")
        args.add_argument('--path_validation', help='dataset para plot', type=str, default="Validation")

        
        args = args.parse_args([
                               "--size_test", str(size_test),
                                "--size_validation", str(size_validation),
                                "--path_validation",path_validation,
                                "--path_test",path_test,
                                "--path_train",path_train])
        
        args.dataset = glob(self.dataset + '/*.' + self.formatImg)
        
        train,test = train_test_split(args.dataset,test_size=args.size_test,random_state=1)
        train,validation = train_test_split(train,test_size=args.size_validation,random_state=1)

        
        self.PathSave(train,args.path_train)
        
        self.PathSave(validation,args.path_validation)
        
        self.PathSave(test,args.path_test)
        
        train = imread_collection(train)
        test = imread_collection(test)
        validation = imread_collection(validation)
        

        
        return train,validation,test



class CreateBoxes():

    """
    This module offers the possibility of creating masks and plotting bounding 
    boxes on this mask, passed through an xml and csv file, being also able to 
    plot the boxes in an image.
    PARAMETERS
    ==========
    image : str
        image directory 
    """

    def __init__(self,image=None):
        self.imagem = image
    


    def xmlExtractCoord(self,path=None, item=None, child=None):
        """
        This method takes as parameter the root element of
        the XML file and returns a list of dictionaries containing
        the coordinates xmax, ymax and xmin, ymin.

        PARAMETERS
        ==========
        path : str
            XML file directory.

        item : str
            searched xml tag.

        child : str
            searched object.

        """
        tree = Et.parse(path)
        root = tree.getroot()

        listBox = []

        for obj in root.iter(item):
            for box in obj.iter(child):
                coordDict = dict({})
                cont = 0
                for coords in box:
                    coordDict[coords.tag] = int(coords.text)
                    cont += 1
                    if cont == 4:
                        listBox.append(coordDict)

        return listBox


    def csvExtractCoord( begin=0):
        """
        This method takes as parameter a path the csv file
        and returns a list of dictionaries containing
        the coordinates xmax, ymax and xmin, ymin.

        PARAMETERS
        ==========
        path : str
            csv file directory.
        
        begin : int
            valou from the first coordinate.

        """

        with open(self.path, encoding='utf-8') as csvfile:
            table = csv.reader(csvfile, delimiter=',')

            listBox = []
            for l in table:
                coordDict = dict({})

                coordDict["xmin"] = int(l[begin])
                coordDict["ymin"] = int(l[begin+1])
                coordDict["xmax"] = int(l[begin+2])
                coordDict["ymax"] = int(l[begin+3])

                listBox.append(coordDict)

        return listBox
        

    def ImageBox(self,item=None,child=None,path=None,file='csv'):


        """
        this method takes a path to the image and an xml or csv file 
        containing coordinates for creating it returns bounding boxes in an image.

        PARAMETERS
        ==========
        coords : list
            list with object's coordinates.
        path : np.array
            CSV OU XML directory.

        item : str
            searched xml tag.

        child : str
            searched object.
        file: str
            chosen file type
        """
        
        args = argparse.ArgumentParser(description='Criacação de boxes')
        args.add_argument('--path', help='dataset para plot', type=str, default=None)
        args.add_argument('--child', help='dataset para plot', type=str, default=None)
        args.add_argument('--item', help='dataset para plot', type=str, default=None)
        args.add_argument('--file', help='dataset para plot', type=str, default='csv')

        args = args.parse_args(["--path", path,
                                "--child",child,
                                "--item",item,
                               "--file",file])
        coords = []
        if args.file =='csv':
            coords = self.csvExtractCoord(args.path,args.item)
            
        if args.file =='xml':
            coords = self.xmlExtractCoord(args.path,args.item,args.child)
        
        image_orig = imread(self.imagem)
     
        for dot in coords:
            x1 = dot['xmin']
            y1 = dot['ymin']
            x2 = dot['xmax']
            y2 = dot['ymax']

        
            cv2.rectangle(image_orig, (x1, y1), (x2, y2), color=(0, 0, 0), thickness=2)

        if "/" in self.imagem:
            aux = 0
            while True:

                try: 
                     flag = self.imagem.index('/',aux+1)

                except:
                    break

                aux = flag
            
            string = self.imagem[aux+1:]
            self.imagem = self.imagem.replace(string,"boxe" + string)

       
        imageio.imwrite(self.imagem, image_orig) 
       
        return image_orig


    def MaskBox(self,item=None,child=None,path=None,file='csv'):
        
        """
         this method takes a path to the image and an xml or csv file containing 
         coordinates for creating it returns bounding boxes in a mask created based
          on the size of the image.

        PARAMETERS
        ==========
        coords : list
            list with object's coordinates.
        img : np.array
            image base.


        item : str
            searched xml tag.

        child : str
            searched object.
        file: str
            chosen file type
        """
        args = argparse.ArgumentParser(description='Criacação de boxes')
        args.add_argument('--path', help='dataset para plot', type=str, default=None)
        args.add_argument('--child', help='dataset para plot', type=str, default=None)
        args.add_argument('--item', help='dataset para plot', type=str, default=None)
        args.add_argument('--file', help='dataset para plot', type=str, default='csv')
        
        args = args.parse_args(["--path", path,
                                "--child",child,
                                "--item",item,
                               "--file",file])
        coords = []
        if args.file =='csv':
            coords = self.csvExtractCoord(args.path,args.item)
            
        if args.file =='xml':
            coords = self.xmlExtractCoord(args.path,args.item,args.child)
        
        img = imread(self.imagem)
        shape = img.shape

        mask = np.ones([shape[0], shape[1], shape[2]], dtype=int).astype(np.uint8)
        
        for dot in coords:
            x1 = dot['xmin']
            y1 = dot['ymin']
            x2 = dot['xmax']
            y2 = dot['ymax']
              
            mask[y1: y2 + 1, x1:x2 + 1, :] = 255

        if "/" in self.imagem:
            aux = 0
            while True:

                try: 
                     flag = self.imagem.index('/',aux+1)

                except:
                    break

                aux = flag
            
            string = self.imagem[aux+1:]
            self.imagem = self.imagem.replace(string,"mask" + string)



        imageio.imwrite(self.imagem, mask) 
       
        return mask
