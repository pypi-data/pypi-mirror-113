
from gip import CreateBoxes as CB 


imagens = CB("../../imagem/_tuberculosis-phone-0088.jpg")

imagens.ImageBox("object","bndbox","../../imagem/tuberculosis-phone-0088.xml","xml")

imagens.MaskBox("object","bndbox","../../imagem/tuberculosis-phone-0088.xml","xml")