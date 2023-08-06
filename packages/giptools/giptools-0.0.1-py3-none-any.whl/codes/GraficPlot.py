import matplotlib.pyplot as plt
from skimage.io import imshow, imread,imread_collection
from skimage import color,exposure
from glob import glob
import numpy as np
import argparse
import pandas as pd


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

    '''
    if args.adap:
        print("entrou")
        img_gray = exposure.equalize_adapthist((args.imagem))
        #plt.subplot(620), plt.imshow(img_gray,plt.cm.gray)
        weights = np.ones(img_gray.ravel().shape) / float(img_gray.size)
        #plt.subplot(629),  plt.hist(img_gray.flatten(), bins=256,weights=weights)

 
    if args.adapGray:
        img_gray = exposure.equalize_adapthist(color.rgb2gray(args.imagem))
        plt.subplot(831), plt.imshow(img_gray,plt.cm.gray)
        weights = np.ones(img_gray.ravel().shape) / float(img_gray.size)

        plt.subplot(832),  plt.hist(img_gray.flatten(), bins=256,weights=weights)

    '''