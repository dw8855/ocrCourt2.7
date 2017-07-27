# -*- coding: UTF-8 -*-

from imagePretreatmentGuang import *
from ocr import *
import utils
import numpy
from  textMatching import *
from PIL import *
import re
import roughclassification
from time import *


def fineClassifyDocument(imageFile, type, caseType, lastTxt):
    orignImageFile = imageFile.copy()
    count = 0
    lineNum = 0
    image = numpy.array(orignImageFile)
    orignHeight = len(image)
    orignWidth = len(image[0])
    orignImageFile = orignImageFile.crop((int(0.1 * orignWidth), int(0.05 * orignHeight), int(0.8 * orignWidth), int(0.85 * orignHeight)))
    # orignImageFile.show()
    image = numpy.array(orignImageFile)
    orignHeight = len(image)
    orignWidth = len(image[0])
    orignImageFile = orignImageFile.convert('1')
    imageFile = orignImageFile.copy()
    # imageFile.show()
    imageFile = imageFile.resize((orignWidth/10, orignHeight/10), Image.BILINEAR)
    # imageFile.show()
    image = imageFile.load()
    (width, height) = imageFile.size
    lineHeight = float(3)
    total = height * width
    for i in xrange(height):
        for j in xrange(width):
            if image[j, i] > 250:
                count = count + 1
    if float(count) / float(total) < 0.01:
        return 'blank'
    row = utils.tohisto(imageFile, 'row')
    # ce shi
    up = 0
    down = 0
    start = 0
    for y in xrange(height):
        if y < start:
            continue
        for i in xrange(y, height):
            if row[i] > 1:
                y = i + 1
                up = i - 1 if i - 1 > 0 else 0
                break
            if i == height - 1:
                y = height
        for i in xrange(y, height - 2):
            if (row[i] <= 1) & (row[i + 1] <= 1) & (row[i + 2] <= 1):
                y = i
                down = height - 1 if i + 1 > height - 1 else i + 1
                break
            if i == height - 1:
                y = height
        lineNum = lineNum + 1
        if float(lineHeight) < float(down - up) < float(height * 0.35):
            # lineImageNew = imageFile.crop((0, up, width, down))
            # lineImageNew.show()
            lineImage = orignImageFile.crop((0, int(up * 10), int(orignWidth), int(down * 10)))
            if bool(lineImage) == False:
                continue
            txt = Ocr(lineImage, type)
            if txt == '﻿':
                lineImage = utils.repair(lineImage)
                txt = Ocr(lineImage, type)
            # lineImage.show()
            txt = txt.replace('\t', '').replace('\n', '').replace('\t\n', '')
            txt = txt.decode('utf-8')
            image = imageFile
            txtName = textMatching(txt, caseType)
            if txtName:
                return txtName
        if ((lineNum >= 2) & (lastTxt == u'')) | ((lineNum >= 1) & (lastTxt == u'代理词')):
            break
        start = down
    lineNum = 0
    start = height
    up = 0
    down = 0
    for y in range(height - 1)[::-1]:
        if y > start:
            continue
        for i in range(y)[::-1]:
            if int(row[i]) > 1:
                y = i - 1
                down = i + 2 if i + 2 < height - 1 else height - 1
                break
            if i == 0:
                y = 1
        for i in range(y - 1)[::-1]:
            i = i + 1
            if int(row[i]) <= 1 & int(row[i - 1]) <= 1:
                y = i
                up = i - 1 if i - 1 > 0 else 0
                break
            if i == 0:
                y = 0
        lineNum = lineNum + 1
        if float(height * 0.35) > float(down - up) > float(lineHeight):
            lineImage = orignImageFile.crop((0, int(up * 10), int(orignWidth), int(down * 10)))
            # lineImage = lineImage.copy()
            # lineImage.show()
            txt = Ocr(lineImage, type)
            if txt == '﻿':
                lineImage = utils.repair(lineImage)
                txt = Ocr(lineImage, type)
            # lineImage.show()
            txt = txt.replace('\t', '').replace('\n', '').replace('\t\n', '')
            txt = txt.decode('utf-8')
            txtName = textMatching(txt, caseType)
            if txtName:
                return txtName
        if ((lineNum >= 1) & (lastTxt == u'')) | ((lineNum >= 2) & (lastTxt == u'代理词')):
            break
        start = up
    if re.match(u'代理词' ,lastTxt):
        return lastTxt
    else:
        return ''
        # deepClassifiedInformation = 1
        # fineDocumentNum = fineDocumentNum + 1
        # return deepClassifiedInformation, fineDocumentNum



if __name__ == '__main__':
    # filePath = r'C:\Users\Administrator\Desktop\no-down'
    # file = os.listdir(filePath)[1:]
    # imageName = os.listdir(filePath + os.path.sep + file[0])
    # imagePath = filePath + os.path.sep + file[0] + os.path.sep + imageName[0]

    imagePath = r'D:\down\11.jpg'
    imageFile = Image.open(imagePath)
    type = u'Abbyy'
    deepClassifiedInformation = fineClassifyDocument(imageFile, type, u'民事', 1)
    print(deepClassifiedInformation)



