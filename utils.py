# -*- coding: UTF-8 -*-

import array
import os
from PIL import Image
import numpy
import roughclassification


def isRed(color):
    if color[0] > 180:
        return True
    else:
        return False


def isBlack(color):
    if sum(color) <= 250:
        return True
    else:
        return False


def binarition(imageFile, threshold):
    Bimage = imageFile
    image = numpy.array(imageFile)
    height = len(image)
    width = len(image[0])
    for i in xrange(width):
        for j in xrange(height):
            r, g, b = roughclassification.getRGB(image[j, i])
            if (r + g + b) < threshold:
                Bimage.putpixel((i, j),  (255, 255, 255))
            else:
                Bimage.putpixel((i, j),  (0, 0, 0))
    return Bimage


def tohisto(imageFile, type):
    image = imageFile.load()
    (width, height) = imageFile.size
    histo = numpy.zeros(height)
    if type == 'row':
        for i in xrange(height):
            for j in xrange(width):
                if image[j, i] == 0:
                    histo[i] = histo[i] + 1
    elif type == 'col':
        for j in range(width):
            for i in range(height):
                if image[j, i] < 255:
                    histo[i] = histo[i] + 1
    return histo

def repair(imageFile):
    image = imageFile.load()
    (height, width) = imageFile.size
    for i in xrange(height):
        for j in xrange(width):
            if (i + 4 < height) & (i - 4 > 0) & (j + 4 < width) & (j - 4 > 0):
                if image[i, j] == 0:
                    if (image[i, j - 3] == 0) | (image[i, j - 2] == 0) | (image[i, j - 1] == 0):
                        imageFile.putpixel((i, j - 3), 0)
                        imageFile.putpixel((i, j - 2), 0)
                        imageFile.putpixel((i, j - 1), 0)
                    elif (image[i, j + 3] == 0) | (image[i, j + 2] == 0) | (image[i, j + 1] == 0):
                        imageFile.putpixel((i, j + 3), 0)
                        imageFile.putpixel((i, j + 2), 0)
                        imageFile.putpixel((i, j + 1), 0)
                    elif (image[i - 2, j] == 0) | (image[i - 3, j] == 0) | (image[i - 1, j] == 0):
                        imageFile.putpixel((i - 3, j), 0)
                        imageFile.putpixel((i - 1, j), 0)
                        imageFile.putpixel((i - 2, j), 0)
                    elif (image[i + 2, j] == 0) | (image[i + 3, j] == 0) | (image[i + 1, j] == 0):
                        imageFile.putpixel((i + 3, j), 0)
                        imageFile.putpixel((i + 1, j), 0)
                        imageFile.putpixel((i + 2, j), 0)
    return imageFile



if __name__ == '__main__':
    imagePath = r'D:\down\11.jpg'
    imageFile = Image.open(imagePath)
    imageFile = repair(imageFile)
    imageFile.show()