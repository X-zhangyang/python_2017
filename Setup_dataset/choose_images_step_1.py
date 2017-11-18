'''Delete error images, revise images's model&format'''


import os
from PIL import Image
import numpy as np

def read_txt(txt_path):
    names = []
    with open(txt_path,"r") as f:
        for line in f.readlines()[0:]:
            pair = line.strip().split()
            names.append(pair)
    return np.array(names)

def loadfiles(filelist):
    paths = []
    classes = os.listdir(filelist)
    for files in classes:
        paths.append(filelist + "/" + files)
        
    return np.array(paths)


#    path_exp = os.path.expanduser(paths)
#    classes = os.listdir(path_exp)
#    classes.sort()
#    nrof_classes = len(classes)
#    
##    for path in paths.split(':'):
##        path_exp = os.path.expanduser(path)
##        classes = os.listdir(path_exp)
##        classes.sort()
##        nrof_classes = len(classes)
#    for i in range(nrof_classes):
#        class_name = classes[i]
##            class_name = classes[1]
#        facedir = os.path.join(path_exp, class_name)
#        image_paths = get_image_paths(facedir)
#        dataset.append(ImageClass(class_name, image_paths))
#  
#    return dataset
    




def readimages(path_in):
    path_in = path_in + "/"
    #path_in = 'D:\\X\\facenet\\Generate_AFDB\\AFDB\\fanglishen\\'   #输入文件路径
    filelist = os.listdir(path_in)  # 该文件夹下所有的文件（包括文件夹）
    # 遍历所有文件
    for files in filelist:
        try:
            img = Image.open(path_in + files)
           # print(img.mode, img.format , files)

            if img.format== "GIF" :
                img.close()
                os.remove(path_in + files)
                continue
            
            if img.format== "MPO" :
                img.close()
                os.remove(path_in + files)
                continue
            
            if (img.size[0]>500)&(img.size[1]>500):
                if img.size[0]>img.size[1]:
                    rate = img.size[0]/500
                else:
                    rate = img.size[1]/500
                img_size_1 = int(img.size[0]/rate)
                img_size_2 = int(img.size[1]/rate)
                img_new = img.resize((img_size_1, img_size_2),Image.ANTIALIAS)
                img.close()
                os.remove(path_in + files)
                img_new.save(path_in + files, format="jpeg")
                img = Image.open(path_in + files)
                
            if (img.mode!="RGB")or(img.format!= "JPEG"):
                img_new = img.convert("RGB")
                img.close()
                os.remove(path_in + files)
                img_new.save(path_in + files, format="jpeg")
                print("Renew %s image" %files)
                img = Image.open(path_in + files)
                print(img.mode, img.format , files)
                img.close()
           # print("ok")

        except Exception as e:
            print("Not an image and delete! ")
            try:
                img.close()
                os.remove(path_in + files)
            except Exception as e:
                os.remove(path_in + files)
        continue
   
def check(path_in):
    i=0
    path_in = path_in + "/"
    filelist = os.listdir(path_in) 
    for files in filelist:
        img = Image.open((path_in + files))
        i=i+1
        
        print("%s %s  %s  %s"%(files, img.mode, img.format,i))
    




if __name__ == '__main__':
    #txt_path = "D:/X/facenet/Generate_AFDB/name.txt"
    input_path = "D:/X/facenet/Generate_AFDB/AFDB"
    names = loadfiles(input_path)
    
    
    
    
    #names = read_txt(txt_path)
    for i in range (len(names)):
        print("Begin to preread %s" %names[i])
        path_in =  names[i]
        readimages(path_in)









#
#
#
##输出文件的模式和编号
#print(img.mode, img.name)
#
#
##返回文件下所有文件名列表
#imgs = os.listdir(path_dir)
