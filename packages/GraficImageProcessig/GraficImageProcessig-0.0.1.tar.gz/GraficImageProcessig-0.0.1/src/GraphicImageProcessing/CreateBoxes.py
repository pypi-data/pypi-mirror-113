import xml.etree.ElementTree as Et
import cv2
import imageio
from skimage.io import imshow, imread,imread_collection
import csv
import argparse
import numpy as np


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
