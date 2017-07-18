# -*- coding: UTF-8 -*-


import getVar
import roughclassification
import fineclassifycertificate
import fineclassifydocument
import os
import imagePretreatmentGuang
from time import *
import sys


#   User: duanwei
#   Date: 2017/6/19
#   version number: 0.1


def Main():
    opts = sys.argv[1:]
    if opts[1] == 'on':
        imagePath, switch, ocrType, saveImagePath = getVar.getVar(opts)
    elif opts[1] == 'off':
        imagePath, switch, ocrType = getVar.getVar(opts)
    if os.path.isfile(imagePath):
        roughNum = 0
        fineCertificateNum = 0
        fineDocumentNum = 0
        if switch == 'on':
            imageFile = imagePretreatmentGuang.imagePretreatmentGuang(imagePath, saveImagePath)
            if imageFile == '':
                return 'whitePage'
        elif switch =='off':
            pass
        classifiedInformation = roughclassification.roughClassification(imageFile)
        if classifiedInformation == '证件':
            deepClassifiedInformation = fineclassifycertificate.fineClassifyCertificate(imageFile)
            txt = deepClassifiedInformation
            if deepClassifiedInformation:
                fineCertificateNum = fineCertificateNum + 1
            if classifiedInformation == '其它':
                print('文件分类失败，它的路径为' + imagePath)
                roughNum = roughNum + 1
        elif classifiedInformation == '文书':
            deepClassifiedInformation = fineclassifydocument.fineClassifyDocument(imageFile, ocrType)
            print deepClassifiedInformation
            if deepClassifiedInformation:
                fineDocumentNum = fineDocumentNum + 1
            if classifiedInformation == '其它':
                print('文件分类失败，它的路径为' + imagePath)
                roughNum = roughNum + 1
        print(fineCertificateNum, fineDocumentNum, roughNum)
    else:
        file = os.listdir(imagePath)
        imagePathName = imagePath
        roughNum = 0
        fineCertificateNum = 0
        fineDocumentNum = 0
        for fileName in file:
            imagePath = imagePathName + os.path.sep + fileName
            if switch == 'on':
                imageFile = imagePretreatmentGuang.imagePretreatmentGuang(imagePath, saveImagePath)
                if imageFile == '':
                    return 'whitePage'
            elif switch == 'off':
                pass
            classifiedInformation = roughclassification.roughClassification(imageFile)
            if classifiedInformation == '证件':
                deepClassifiedInformation = fineclassifycertificate.fineClassifyCertificate(imageFile)
                txt = deepClassifiedInformation
                if deepClassifiedInformation:
                    fineCertificateNum = fineCertificateNum + 1
                if classifiedInformation == '其它':
                    print('文件分类失败，它的路径为' + imagePath)
                    roughNum = roughNum + 1
            elif classifiedInformation == '文书':
                deepClassifiedInformation = fineclassifydocument.fineClassifyDocument(imageFile, ocrType)
                print deepClassifiedInformation
                if deepClassifiedInformation:
                    fineDocumentNum = fineDocumentNum + 1
                if classifiedInformation == '其它':
                    print('文件分类失败，它的路径为' + imagePath)
                    roughNum = roughNum + 1
            print(fineCertificateNum, fineDocumentNum, roughNum)


if __name__ == "__main__":
    # filePath = r'C:\Users\Administrator\Desktop\桥西卷宗未处理'
    # saveImagePath = r'C:\Users\Administrator\Desktop\已处理'
    # file = os.listdir(filePath)[1:]
    # type = 'Abbyy'
    # for fileName in file:
    #     imageName = os.listdir(filePath + '/' + fileName)
    #     for image in imageName:
    #         imagePath = filePath + '/' + fileName + '/' + image
    #         Main(imagePath, saveImagePath, type)
    Main()