# -*- coding: utf-8 -*-  
# feimengjuan  
import re  
import urllib  

import os  
#抓取网页图片  
  
  
#根据给定的网址来获取网页详细信息，得到的html就是网页的源代码  
def getHtml(url):  
    page = urllib.request.urlopen(url)  
    html = page.read()  
    return html  
  
#创建保存图片的文件夹  
def mkdir(path):  
    path = path.strip()  
    # 判断路径是否存在  
    # 存在    True  
    # 不存在  Flase  
    isExists = os.path.exists(path)  
    if not isExists:  
        print( u'新建了名字叫做',path,u'的文件夹' ) 
        # 创建目录操作函数  
        os.makedirs(path)  
        return True  
    else:  
        # 如果目录存在则不创建，并提示目录已经存在  
        print( u'名为',path,u'的文件夹已经创建成功' ) 
        return False  
  
# 输入文件名，保存多张图片  
def saveImages(imglist,name):  
    number = 1  
    for imageURL in imglist:  
        splitPath = imageURL.split('.')  
        fTail = splitPath.pop()  
        if len(fTail) > 3:  
            fTail = 'jpg'  
        fileName = name + "/" + str(number) + "." + fTail  
        # 对于每张图片地址，进行保存  
        try:  
            u = urllib.request.urlopen(imageURL)  
            data = u.read()  
            f = open(fileName,'wb+')  
            f.write(data)  
            print (u'正在保存的一张图片为',fileName )
            f.close()  
        except urllib.error.URLError as e:  
            print (e.reason)  
        number += 1  
  
  
#获取网页中所有图片的地址  
def getAllImg(html):  
    #利用正则表达式把源代码中的图片地址过滤出来  
    reg = r'src="(.+?\.jpg)" pic_ext'  
    imgre = re.compile(reg)  
    html=html.decode('utf-8')  #python3
    imglist = imgre.findall(html) #表示在整个网页中过滤出所有图片的地址，放在imglist中  
    return imglist  
  
  
#创建本地保存文件夹，并下载保存图片  
if __name__ == '__main__':  
    html = getHtml("https://www.zhihu.com/question/39107568")#获取该网址网页详细信息，得到的html就是网页的源代码  
    #示例网站  http://tieba.baidu.com/p/2460150866
    path = u'图片'  
    mkdir(path) #创建本地文件夹  
    imglist = getAllImg(html) #获取图片的地址列表  
    saveImages(imglist,path) # 保存图片  
    
    
    
    
import re  
import urllib  

  
#抓取网页图片  
  
  
#根据给定的网址来获取网页详细信息，得到的html就是网页的源代码  
def getHtml(url):  
    page = urllib.request.urlopen(url)  
    html = page.read()  
    return html  
  
def getImg(html):  
    #利用正则表达式把源代码中的图片地址过滤出来  
    reg = r'src="(.+?\.jpg)" pic_ext'  
    imgre = re.compile(reg)  
    html=html.decode('utf-8')  #python3
    imglist = imgre.findall(html) #表示在整个网页中过滤出所有图片的地址，放在imglist中  
    x = 0  
    for imgurl in imglist:  
        urllib.request.urlretrieve(imgurl,'%s.jpg' %x) #打开imglist中保存的图片网址，并下载图片保存在本地  
        x = x + 1  
  
html = getHtml("http://weapon.huanqiu.com/lar_grizzly_win_mag")#获取该网址网页详细信息，得到的html就是网页的源代码  

#示例网站  http://tieba.baidu.com/p/2460150866

getImg(html)#从网页源代码中分析并下载保存图片  
