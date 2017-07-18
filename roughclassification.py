# -*- coding: UTF-8 -*-

from PIL import Image
from numpy import *


def roughClassification(imageFile):
    Bcount = 0
    Ocount = 0
    Wcount = 0
    Gcount = 0
    BOcount = 0
    orignImage = array(imageFile)
    orignHeight = len(orignImage)
    orignWidth = len(orignImage[0])
    imageFile = imageFile.resize((orignWidth/10, orignHeight/10), Image.BILINEAR)
    image = array(imageFile)
    height = len(image)
    width = len(image[0])
    total = height * width
    imageColor = image
    for i in range(height):
        for j in range(width):
            r, g, b = getRGB(imageColor[i, j])
            if isBlue(r, g, b):
                Bcount = Bcount + 1
            elif isGreen(r, g, b):
                Gcount = Gcount + 1
            elif isOrange(r, g, b):
                Ocount = Ocount + 1
            elif isBOrange(r, g, b):
                BOcount = BOcount + 1
            elif isWhite(r, g, b):
                Wcount = Wcount + 1
    if (Wcount / total > 0.99) | ((Bcount / total > 0.03) & (BOcount / total >
    0.0012) | (Ocount / total > 0.03)) | (Gcount / total > 0.003):
        return '证书'
    else:
        return '文书'


def getRGB(color):
    red = color[0]
    green = color[1]
    blue = color[2]
    return red, green, blue


def isBlue(r, g, b):
    if (r > 100) & (g > 120) & (g < 200) & (b > 160):
        return True
    else:
        False


def isGreen(r, g, b):
    if (r < 120) & (g > 135) & (g < 230) & (b > 140) & (b < 230):
        return True
    else:
        False


def isOrange(r, g, b):
    if (r > 230) & (g > 150) & (g < 180) & (b > 100) & (b < 130):
        return True
    else:
        False


def isBOrange(r, g, b):
    if (r > 220) & (g > 110) & (g < 230) & (b < 120):
        return True
    else:
        False


def isWhite(r, g, b):
    if int(r) + int(g) + int(b) > 630:
        return True
    else:
        False
