from pypinyin import pinyin, lazy_pinyin, Style
import urllib
import requests
import os
import re
import numpy as np


def read_txt(txt_path):
    names = []
    with open(txt_path,"r") as f:
        for line in f.readlines()[0:]:
            pair = line.strip().split()
            names.append(pair)
        f.close()
    return np.array(names)


def translat_into_pinyin(names):
    new_name =  []
    for i in range (len(names)):
        new_names = lazy_pinyin(names[i])
        new_name_1 = ""
        for j in range (len(new_names)):
            new_name_1 = new_name_1 +new_names[j]
        new_name.append(new_name_1)
    return np.array(new_name)

def build_txt(save_path,names,new_name):
    fp = open("new_name.txt","a")
    for i in range (len(names)):
        fp.write(str(names[i])[2:(len(str(names[i]))-2)])
        fp.write("\t" + new_name[i] + "\n")
    fp.close()
    
        

if __name__ == '__main__':
    txt_path = "D:/X/facenet/Generate_AFDB/name.txt"
    save_path = "D:/X/facenet/Generate_AFDB"
    names = read_txt(txt_path)
    print("成功读取TXT文件, 正在生成新的文件！")
    new_name = translat_into_pinyin(names)
    build_txt(save_path,names,new_name)
    print("成功生成新的文件！")
    
    



