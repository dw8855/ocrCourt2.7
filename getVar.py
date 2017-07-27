# -*- coding: UTF-8 -*-

import os

def getVar(opts):
        if opts[1] == 'on':
                imagePath = opts[0]
                saveImagePath = opts[4]
                caseType = opts[3].decode('gbk')
                switch = opts[1]
                type = opts[2]
                return imagePath, switch, type, caseType, saveImagePath
        elif opts[1] == 'off':
                imagePath = opts[0]
                switch = opts[1]
                type = opts[2]
                caseType = opts[3].decode('gbk')
                return imagePath, switch, type, caseType

if __name__ == '__main__':
    a, b, c, d=  getVar([r'D:\no-down\25.jpg', 'off', 'Abbyy', '民事'])
