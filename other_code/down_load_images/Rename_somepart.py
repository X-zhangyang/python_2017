import sys  
import os  





def replace_filename(file_path,var1,var2):  
    for root,dirs,files in os.walk(file_path):  
        for file_name in files:  
            if var1 in file_name:  
                os.rename(os.path.join(root,file_name),os.path.join(root,file_name.replace(var1,var2)))  
                print('new file name is {0}'.format(file_name.replace(var1,var2)))  
  
  
  
replace_filename(sys.argv[1],sys.argv[2],sys.argv[3])  