import os  
  

path = "D:\\Learning\\python\\Object-Detector-App-master-leanring\\Create_TFrecords\\data\\VOC2012\\JPEGImages\\"
a=[]

def listdir(path, list_name):  
    for file in os.listdir(path):  
        file_path = os.path.join(path, file)  
        if os.path.isdir(file_path):  
            listdir(file_path, list_name)  
        elif os.path.splitext(file_path)[1]=='.jpg':    #文件名类型
            list_name.append(file_path)  
            
            
            
            
  
listdir(path,a)           
            
            