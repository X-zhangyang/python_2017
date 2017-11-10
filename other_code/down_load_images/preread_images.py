import os
from PIL import Image
import numpy as np

def rename():
    count = 0    #文件代码  
    name = ''   #修改后的文件名，可以根据要求修改
    F_type  = '.jpg'  #修改后的文件扩展名，可以根据要求修改
#    img_1 = Image.open("D:\\Learning\\python\\Download_Image\\gun\\picture_with_problem\\0000045.jpg")
    #文件路径
    path_in = 'D:\\Learning\\python\\Download_Image\\gun\\100\\'   #输入文件路径
    path_out = 'D:\\Learning\\python\\Download_Image\\revise_images\\Gun_0\\'   #输出文件路径
    filelist = os.listdir(path_in)  # 该文件夹下所有的文件（包括文件夹）
    # 遍历所有文件
    for files in filelist:
        img = Image.open(path_in + files)
        print(img.mode, img.format , files)
    

#    
#        Olddir = os.path.join(path_in, files) # 原来的文件路径
#        fp = open(path_in + files)
#        img = Image.open(fp)
#  
#        mode_img = img.mode
#        if mode_img == "P":
#            print(mode_img,files)
#            print(img.mode,files)
#            fp.close()
#            os.remove(Olddir)  
#        count += 1
 
rename()









#
#
#
##输出文件的模式和编号
#print(img.mode, img.name)
#
#
##返回文件下所有文件名列表
#imgs = os.listdir(path_dir)
