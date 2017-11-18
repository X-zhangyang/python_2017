#This code can only download images from baidu
#

import urllib
import requests
import os
import re

import numpy as np


str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}

# str 的translate方法需要用单个字符的十进制unicode编码作为key
# value 中的数字会被当成十进制unicode编码转换成字符
# 也可以直接用字符串作为value
char_table = {ord(key): ord(value) for key, value in char_table.items()}

# 解码图片URL
def decode(url):
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    return url.translate(char_table)

# 生成网址列表
def buildUrls(word):
    word = urllib.parse.quote(word)
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    #urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    urls = (url.format(word=word, pn=x) for x in range (0,360,60))   #设定图片下载数量
    return urls

# 解析JSON获取图片URL
re_url = re.compile(r'"objURL":"(.*?)"')
def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls

def downImg(imgUrl, dirpath, imgName):
    filename = os.path.join(dirpath, imgName)
    #string_1 =  save_path + "/" + spelling_name + "/" + spelling_name +'_'+str(i) + '.jpg'   
    try:
        res = requests.get(imgUrl, timeout=15)
        if str(res.status_code)[0] == "4":
            print(str(res.status_code), ":" , imgUrl)
            return False
    except Exception as e:
        print("抛出异常：", imgUrl)
        print(e)
        return False
    with open(filename, "wb") as f:
        f.write(res.content)
    return True


#def mkDir(dirName):
#    dirpath = os.path.join(sys.path[0], dirName)
#    if not os.path.exists(dirpath):
#        os.mkdir(dirpath)
#    return dirpath

def mkdir(file_name,save_path):  
    save_path = save_path.strip()  
    # 判断路径是否存在   
    isExists = os.path.exists(file_name)  
    if not isExists:  
        print( u'新建了名字叫做',file_name,u'的文件夹' ) 
        # 创建目录操作函数  
        os.makedirs(save_path + "/" +file_name)  
        return True  
    else:  
        # 如果目录存在则不创建，并提示目录已经存在  17型手枪
        print( u'名为',file_name,u'的文件夹已经创建成功' ) 
        return False  


def read_txt(txt_path):
    names = []
    with open(txt_path,"r") as f:
        for line in f.readlines()[0:]:
            pair = line.strip().split()
            names.append(pair)
    return np.array(names)


if __name__ == '__main__':
    txt_path = "D:/X/facenet/Generate_AFDB/new_name3.txt"
    names = read_txt(txt_path)
    print("成功读取TXT文件")
    save_path = "D:/X/facenet/Generate_AFDB/AFDB"
    print("下载文件保存路径为:" + save_path)
    print("=" * 50)
    j = 0
    for k in range (len(names)):
        word = names[k,0]
        mkdir(names[k,1],save_path) 
    #    dirpath = mkDir("results")
        urls = buildUrls(word)
        index = 0
        
        
        for url in urls:
            print("正在请求：", url)
            try:
                
                html = requests.get(url, timeout=20).content.decode('utf-8')
                imgUrls = resolveImgUrl(html)
                if len(imgUrls) == 0:  # 没有图片则结束
                    break
                dirpath = save_path + "/" + names[j,1]
                for url in imgUrls:
                    if downImg(url, dirpath, str(index) + ".jpg"):
                        index += 1
                        print("已下载 %s 张" % index)
            except:
                continue     
        j=j+1
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                #http://lovenight.github.io/2015/11/15/Python-3-%E5%A4%9A%E7%BA%BF%E7%A8%8B%E4%B8%8B%E8%BD%BD%E7%99%BE%E5%BA%A6%E5%9B%BE%E7%89%87%E6%90%9C%E7%B4%A2%E7%BB%93%E6%9E%9C/
