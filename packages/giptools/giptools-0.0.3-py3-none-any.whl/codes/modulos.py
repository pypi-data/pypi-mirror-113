import xml.etree.ElementTree as Et
import cv2
import imageio
from skimage.io import imshow, imread, imread_collection
import csv
import argparse
import numpy as np
import matplotlib.pyplot as plt
from skimage import color, exposure
from glob import glob
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
import os



def xmlExtractCoord(path=None, item=None, child=None):
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


def csvExtractCoord(path, begin=0):
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

    with open(path, encoding='utf-8') as csvfile:
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
    

def ImageBox(path_file=None,item=None,child=None,imagem=None,file='csv'):


    """
    this method takes a path to the image and an xml or csv file 
    containing coordinates for creating it returns bounding boxes in an image.

    PARAMETERS
    ==========
    coords : list
        list with object's coordinates.
    img : np.array
        image base.
     path : str
        XML file directory.

    item : str
        searched xml tag.

    child : str
        searched object.
    file: str
        chosen file type
    """
    
    args = argparse.ArgumentParser(description='Criacação de boxes')
    args.add_argument('--imagem', help='dataset para plot', type=str, default=None)
    args.add_argument('--path_file', help='dataset para plot', type=str, default=None)
    args.add_argument('--child', help='dataset para plot', type=str, default=None)
    args.add_argument('--item', help='dataset para plot', type=str, default=None)
    args.add_argument('--file', help='dataset para plot', type=str, default='csv')

    args = args.parse_args(["--imagem", imagem,
                            "--path_file", path_file,
                            "--child",child,
                            "--item",item,
                           "--file",file])
    coords = []
    if args.file =='csv':
        coords = csvExtractCoord(args.path_file,args.item)
        
    if args.file =='xml':
        coords = xmlExtractCoord(args.path_file,args.item,args.child)
    
    image_orig = imread(args.imagem)
 
    for dot in coords:
        x1 = dot['xmin']
        y1 = dot['ymin']
        x2 = dot['xmax']
        y2 = dot['ymax']

    
        cv2.rectangle(image_orig, (x1, y1), (x2, y2), color=(0, 0, 0), thickness=2)
    
   
    imageio.imwrite("boxes_"+args.imagem, image_orig) 


def MaskBox(path_file=None,item=None,child=None,imagem=None,file='csv'):
    
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
     path : str
        XML file directory.

    item : str
        searched xml tag.

    child : str
        searched object.
    file: str
        chosen file type
    """
    args = argparse.ArgumentParser(description='Criacação de boxes')
    args.add_argument('--imagem', help='dataset para plot', type=str, default=None)
    args.add_argument('--path_file', help='dataset para plot', type=str, default=None)
    args.add_argument('--child', help='dataset para plot', type=str, default=None)
    args.add_argument('--item', help='dataset para plot', type=str, default=None)
    args.add_argument('--file', help='dataset para plot', type=str, default='csv')
    
    args = args.parse_args(["--imagem", imagem,
                            "--path_file", path_file,
                            "--child",child,
                            "--item",item,
                           "--file",file])
    coords = []
    if args.file =='csv':
        coords = csvExtractCoord(args.path_file,args.item)
        
    if args.file =='xml':
        coords = xmlExtractCoord(args.path_file,args.item,args.child)
    
    img = imread(args.imagem)
    shape = img.shape

    mask = np.zero([shape[0], shape[1], shape[2]], dtype=int).astype(np.uint8)
    
    for dot in coords:
        x1 = dot['xmin']
        y1 = dot['ymin']
        x2 = dot['xmax']
        y2 = dot['ymax']
          
        mask[y1: y2 + 1, x1:x2 + 1, :] = 255
    
    imageio.imwrite("boxes_"+args.imagem, mask) 
   
    return Mask


def MultiPlot(rows=0, columns=0, width=10, height=30, dataset=None, formatImg="jpg"):
    
    '''
    This function will receive an image dataset where it will plot them, 
    based on the number of rows and columns passed as parameter

    PARAMETERS
    ==========
    rows: int
        determines how many lines the plot will have

    columsn:int
        determines how many columns the plot will have

    width:int
        specifies the width of the images

    heigth: int
        specifies the height of the images

    dataset: str
        image dataset

    formatImg:
        the format of the images

    '''
    args = argparse.ArgumentParser(description='multiple image plot')
    args.add_argument('--dataset', help='dataset para plot', type=str, default=None)
    args.add_argument('--rows', help='linhas do grafico', type=int, default=None)
    args.add_argument('--columns', help='colunas do grafico', type=int, default=None)
    args.add_argument('--height', help='altura da imagem', type=int, default=10)
    args.add_argument('--width', help='largura imagem', type=int, default=10)
    args.add_argument('--formatImg', help='formato das imagens', type=str, default="jpg")
    args = args.parse_args(["--dataset", dataset,
                           "--rows", str(rows),
                           '--columns',str(columns),
                           "--height", str(height),
                           "--width", str(width),
                           "--formatImg", formatImg])

    fig, ax = plt.subplots(args.rows, args.columns,figsize=(args.height,args.width))

    imagens = glob(args.dataset + '/*.' + args.formatImg)
    imagens = imread_collection(imagens)
    
    k = 0
    imshow(imagens[0])
    for i in range(args.rows):
        for j in range(args.columns):
            ax[i,j].imshow(imagens[k])
            if k < len(imagens):
                k+=1

    plt.show()


def MultiHistPlot(rows=0, columns=0, width=10, height=30, dataset=None, formatImg='jpg'):


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

    width:int
        specifies the width of the images

    heigth: int
        specifies the height of the images

    dataset: str
        image dataset

    formatImg:
        the format of the images

    '''

    args = argparse.ArgumentParser(description='multiple-image histogram plot')
    args.add_argument('--dataset', help='dataset para plot', type=str, default=None)
    args.add_argument('--rows', help='linhas do grafico', type=int, default=None)
    args.add_argument('--columns', help='colunas do grafico', type=int, default=None)
    args.add_argument('--height', help='altura da imagem', type=int, default=30)
    args.add_argument('--width', help='largura imagem', type=int, default=10)
    args.add_argument('--formatImg', help='formato das imagens', type=str, default="jpg")
    args = args.parse_args(["--dataset", dataset,
                           "--rows", str(rows),
                           '--columns',str(columns),
                           "--height", str(height),
                           "--width", str(width),
                           "--formatImg", formatImg])

    fig, ax = plt.subplots(args.rows, args.columns,figsize=(args.height,args.width))

    imagens = glob(args.dataset + '/*.' + args.formatImg)
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


def LearnPlot(Epochs=1,Dataset=None,MetricsName=None,Title="Grafico de Metricas",Eixo_x="Eixo X",Eixo_y="Eixo_Y",Height=8,Width=15, Save=False):

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

    Width:int
        specifies the width of the images

    Heigth: int
        specifies the height of the images

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



def MultiImage(imagem=None, width=20, height=10, norm=True,gray=True,equa=True,equaGray=True,adap=True,adapGray=True):


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

    width:int
        specifies the width of the images

    heigth: int
        specifies the height of the images
    '''

   
    args = argparse.ArgumentParser(description='multiple-image histogram plot')
    args.add_argument('--imagem', help='dataset para plot', type=str, default=None)
    args.add_argument('--norm', help='linhas do grafico', type=bool, default=False)
    args.add_argument('--gray', help='colunas do grafico', type=bool, default=False)
    args.add_argument('--equa', help='colunas do grafico', type=bool, default=False)
    args.add_argument('--equaGray', help='colunas do grafico', type=bool, default=False)
    args.add_argument('--adap', help='colunas do grafico', type=bool, default=False)
    args.add_argument('--adapGray', help='colunas do grafico', type=bool, default=False)
    args.add_argument('--height', help='altura da imagem', type=int, default=10)
    args.add_argument('--width', help='largura imagem', type=int, default=30)

    args = args.parse_args(["--norm",str( norm),
                           '--gray',str(gray),
                           "--equa", str(equa),
                           "--equaGray", str(equaGray),
                            "--adap", str(adap),
                           "--adapGray", str(adapGray),
                           "--height", str(height),
                           "--width", str(width),
                            "--imagem", imagem,])

    
    args.imagem = imread(args.imagem)
    plt.figure(figsize=(args.width,args.height))
    
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
