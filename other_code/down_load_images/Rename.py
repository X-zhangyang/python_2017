#----网上现有的代码，可用
import os
def rename():
    count = 0    #文件代码  
    name = ''   #修改后的文件名，可以根据要求修改
    F_type  = '.jpg'  #修改后的文件扩展名，可以根据要求修改
    
    #文件路径
    path_in = 'D:\\Learning\\python\\Download_Image\\证件照'   #输入文件路径
    path_out = 'D:\\Learning\\python\\Download_Image\\证件照'   #输出文件路径
    filelist = os.listdir(path_in)  # 该文件夹下所有的文件（包括文件夹）
    for files in filelist:  # 遍历所有文件
        Olddir = os.path.join(path_in, files)  # 原来的文件路径
        if os.path.isdir(Olddir):  # 如果是文件夹则跳过
            continue
#        filename = os.path.splitext(files)[0]  # 修改前的文件名
#        filetype = os.path.splitext(files)[1]  # 修改前文件的扩展名 可以修改
#        
        Newdir = os.path.join(path_out, name + str(count+1) + F_type)  # 新的文件路径+文件名+扩展名
        os.rename(Olddir, Newdir)  # 重命名
        count += 1
 
rename()