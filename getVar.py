# -*- coding: UTF-8 -*-

import os

def getVar(opts):
        if opts[1] == 'on':
                imagePath = opts[0]
                saveImagePath = opts[3]
                switch = opts[1]
                type = opts[2]
                return imagePath, switch, type, saveImagePath
        elif opts[1] == 'off':
                imagePath = opts[0]
                switch = opts[1]
                type = opts[2]
                return imagePath, switch, type

if __name__ == '__main__':
    getVar([r'D:\no-down\25.jpg', r'D:\down', 'on', 'off'])
