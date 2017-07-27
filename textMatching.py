#-*- coding: UTF-8 -*-
from ConfigParser import *
import re

def textMatching(txt, caseType):
    if not txt:
        return ''
    cf = ConfigParser()
    path = r'C:\Users\Administrator\Desktop\textMatching.ini'
    fileOpen = open(path)
    cf.readfp(fileOpen)
    section = cf.sections()
    realySection = []
    realyItems = []
    # cf.items(caseType)
    for i in xrange(len(section)):
        realySection.append(section[i].decode('gbk'))
        if caseType == realySection[-1]:
            items = cf.items(section[i])
            for words in items:
                realyItems.append(words[1].decode('gbk'))
                if re.match(realyItems[-1], txt):
                    return words[0].decode('gbk')
            return ''
    print '请输入正确事件分类'

def pagesProcess(txt, caseType):
    if not txt:
        return False
    cf = ConfigParser()
    path = r'C:\Users\Administrator\Desktop\textMatching.ini'
    fileOpen = open(path)
    cf.readfp(fileOpen)
    section = cf.sections()
    realySection = []
    for i in xrange(len(section)):
        realySection.append(section[i].decode('gbk'))
        if caseType == realySection[-1]:





if __name__ == '__main__':
    txt = textMatching(u'起诉书', u'民事')
    print txt