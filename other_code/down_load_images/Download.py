'''运行程序，输入关键字，即可下载。
仅用于百度图片下载
'''






#-*- coding:utf-8 -*-

#下载搜索的图片  
import re
import requests
import os  
#抓取网页图片  
#创建保存图片的文件夹  
def mkdir(path):  
    path = path.strip()  
    # 判断路径是否存在   
    isExists = os.path.exists(path)  
    if not isExists:  
        print( u'新建了名字叫做',path,u'的文件夹' ) 
        # 创建目录操作函数  
        os.makedirs(path)  
        return True  
    else:  
        # 如果目录存在则不创建，并提示目录已经存在  17型手枪
        print( u'名为',path,u'的文件夹已经创建成功' ) 
        return False  
  
def dowmloadPic(html,keyword):

    pic_url = re.findall('"objURL":"(.*?)",',html,re.S)
    i = 0
    print( '找到关键词:'+keyword+'的图片，现在开始下载图片...')
    for each in pic_url:
        print( '正在下载第'+str(i+1)+'张图片，图片地址:'+str(each))
        try:
            pic= requests.get(each, timeout=10)
        except requests.exceptions.ConnectionError:
            print( '【错误】当前图片无法下载')
            continue
         #download to different files
#        string =  keyword+ "/"  +'pictures' + keyword +'_' + str(i) + '.jpg'   #download to different files     
       #download to some file
        filename = keyword
        string_1 =  filename + "/" + 'pictures'+keyword+'_'+str(i) + '.jpg'       
        
        fp = open(string_1,'wb+')
        fp.write(pic.content)
        fp.close()
        i += 1

if __name__ == '__main__':
    word = input("Input key word: ")
    path = word  
    mkdir(path) #创建本地文件夹  
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='+word+'&ct=201326592&v=flip'
    result = requests.get(url)
    dowmloadPic(result.text,word)













#python create_pascal_tf_record.py 
#--data_dir='D:/Learning/python/Object-Detector-App-master-leanring/train/TF-OD-Test/picture/' \
# 
#--year=VOC2012 
#--set=train 
#--output_path='D:/Learning/python/Object-Detector-App-master-leanring/train/TF-OD-Test/data/pascal_train.record'
# 
#
#python create_pascal_tf_record.py --data_dir='D:/Learning/python/Object-Detector-App-master-leanring/train/TF-OD-Test/picture/' \
# 
#--year=VOC2007 --set=val --output_path='D:/Learning/python/Object-Detector-App-master-leanring/train/TF-OD-Test/data/pascal_val.record'
#
#
#
#python object_detection/create_pascal_tf_record.py \
#--data_dir='D:\\Learning\\python\\Object-Detector-App-master-leanring\\train\\TF-OD-Test\\picture\\' \
#--year=VOC2012 \
#--set=train \
#--output_path='D:\\Learning\\python\\Object-Detector-App-master-leanring\\train\\TF-OD-Test\\data\\pascal_train.record'
#
#



#import re
#import requests
#
#
#def dowmloadPic(html,keyword):
#

#    pic_url = re.findall('"objURL":"(.*?)",',html,re.S)
#    i = 0
#    print( '找到关键词:'+keyword+'的图片，现在开始下载图片...')
#    for each in pic_url:
#        print( '正在下载第'+str(i+1)+'张图片，图片地址:'+str(each))
#        try:
#            pic= requests.get(each, timeout=10)
#        except requests.exceptions.ConnectionError:
#            print( '【错误】当前图片无法下载')
#            continue
#        string = 'pictures'+keyword+'_'+str(i) + '.jpg'
#        #resolve the problem of encode, make sure that chinese name could be store
#        fp = open(string,'wb+')
#        fp.write(pic.content)
#        fp.close()
#        i += 1
#
#
#
#if __name__ == '__main__':
#    word = input("Input key word: ")
#    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='+word+'&ct=201326592&v=flip'
#    result = requests.get(url)
#    dowmloadPic(result.text,word)