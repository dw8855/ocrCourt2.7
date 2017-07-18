# -*- coding: UTF-8 -*-
from pytesseract import *
from jpype import *
import os


from PIL import Image


def Ocr(imageFile, type):
    if type == 'Abbyy':
        imagePath = r'D:\page.jpg'
        imageFile.save(imagePath)
        imageFile = imagePath
        if not isJVMStarted():
            javaPath = getDefaultJVMPath()
            classPath = '-Djava.class.path=%s;%s;%s' % ('D:\ocr\webapps\ROOT\WEB-INF\lib\FREngine-1.0.jar', 'D:\Abbyy\CADF\Inc\Java\com.abbyy.FREngine.jar', 'D:\ocr\webapps\ROOT\WEB-INF\classes');
            # listocr = os.listdir(classPath)
            startJVM(javaPath, classPath)
        if isJVMStarted():
            Abbyy = JClass('Abbyy')
            name = imageFile.split(os.path.sep)[-1]
            txtname = imageFile.split(os.path.sep)[0] + os.path.sep + name.split('.')[0] + '.txt'
            Abbyy.main([imageFile, txtname])
            Txt = open(txtname, 'r')
            txt = Txt.read()
            return txt
    elif type == 'Tesseract':
        try:
            txt = image_to_string(imageFile, 'chi_sim')
        except():
            tessdata_dir_config = '--tessdata-dir "<replace_with_your_tessdata_dir_path>"'
            txt = image_to_string(imageFile, lang='chi_sim', config=tessdata_dir_config)
        return txt


if __name__ == '__main__':
    imageFile = 'D:\page_12.jpg'
    type = 'Tesseract'
    imageFile = Image.open(imageFile)
    txt = Ocr(imageFile, type)
    print txt
