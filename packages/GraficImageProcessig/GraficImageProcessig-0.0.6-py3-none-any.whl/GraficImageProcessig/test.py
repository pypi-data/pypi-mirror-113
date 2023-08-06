from gip import GraficPlot as GP
import matplotlib.pyplot as plt
from skimage.io import imshow, imread,imread_collection
from sklearn.model_selection import train_test_split
from skimage import color,exposure
from glob import glob
dataset = glob("imagem/*.jpeg")
datat = imread_collection(dataset)

pl = GP(15,15)

pl.MultiPlot(2,5,dataset= datat,read=False)