使用matlab 手动标记 


下载图片数据时，一定要验证图片的可读性！
使用
import cv2 
cv2.imread() 验证图片的可读性
  
pick_images.py


确定照片的原始格式@@！！！！！！！！！！


步骤资料 里面有一些工具
、



create_pascal_tf_record.py
pascal_label_map.pbtxt


验证！！有的图片无法读取，




Step 1： matlab命令行敲入 trainingImageLabeler 进入APP打开你自己的图像文件进行交互式标注。

Step 2：标注完成后，点击APP右上角Export ROIs导出到工作空间中，变量名自己取，这里我取名mylabel，
双击mylabel可以清楚直观查看标记内容，

Step 3：使用 struct2table() 函数，把输出的Struct结构改为table类型

Matlab  标记的四个点是  左上角坐标（num1，num2）   框框大小（num3，num4） 
需要额外操作使用exal  num3= num3+num1    num4= num4+num2


Step 4：接下来就是正式把mylabel复制到  txt or word ，去掉没有用的信息，格式为： 地址 坐标1 坐标2 坐标3 坐标4
例如：D:\Learning\python\Download_Image\gun\100\000007.jpg	20	100	467	217


Step 5：使用txt_xml.py 制作XML格式文件  

注意XML文件        xml.write('\t<folder>images</folder>\n')  #代表目录images需要和Step6 中文件对应
XML文件中需要修改类别名字@@@@@@@@@@

data文件在   D:\Learning\python\Object-Detector-App-master-leanring\Create_TFrecords\
Step 6：建一个名为Data的文件夹（DATA文件夹.png）
        data文件下需要 pascal_label_map.pbtxt 里面存放类，需要对应。
        Annotation放XML文件，  main中放 train.txt（做为训练图片的图片名,无需后缀） Val.txt做为测试？
        JPEGImages存放图片，其余可不管。  注意XML文件和图片要一一对应
        
        
Step：7把create_pascal_tf_record.py放到\Object-Detector-App-master目录下
（目录中需要object_detection文件，保证import顺利）

Step8：打开CMD命令窗口 进入 cd D:\Learning\python\Object-Detector-App-master
输入 python create_pascal_tf_record.py --data_dir=D:\Learning\python\Object-Detector-App-master-leanring\Create_TFrecords\data\ --year=VOC2012 --set=train --output_path=D:\Learning\python\Object-Detector-App-master-leanring\Create_TFrecords\pascal.record
得到pascal.record

输入 python create_pascal_tf_record.py --data_dir=D:\Learning\python\Object-Detector-App-master-leanring\Create_TFrecords\data\ --year=VOC2012 --set=val --output_path=D:\Learning\python\Object-Detector-App-master-leanring\Create_TFrecords\pascal_val.record
得到pascal_val.record

#--data_dir 为Step6中 data目录
#--output_path为创建 *.Tfrecords

Step9:得到Tfrecords！






设置路径      开始训练
新建文件夹  A ，在A下面建立子目录models，data  
把模型对应的.config文件放到models下
把class文件pascal_label_map.pbtxt，以及2个record问价放到data下          
        config文件  
            1）num_classes:修改为自己的classes num 
            2）将所有PATH_TO_BE_CONFIGURED的地方修改为自己之前设置的路径（共5处）
        label_map.pbtxt
            1）修改里面的class与要训练的图片种类对应
           
            
            
            
训练输入格式、
nvidia-smi 查看GPU
先制定训练使用的GPU  CUDA_VISIBLE_DEVICES = NUM + python +代码
CUDA_VISIBLE_DEVICES=3 

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0" #使用0号GPU 







python train.py 
--train_dir=D:\X\Obeject_training\TF-OD-Test\train 
--pipeline_config_path=D:\X\Obeject_training\TF-OD-Test\model\ssd_mobilenet_v1_pets.config

python train.py 
--train_dir=D:\Learning\python\Object-Detector-App-master-leanring\train\TF-OD-Test\train 
--pipeline_config_path=D:\Learning\python\Object-Detector-App-master-leanring\train\TF-OD-Test\model\ssd_mobilenet_v1_pets.config

CMD命令窗口 进入D:\Learning\python\Object-Detector-App-master
输入：记得根据实际情况，修改class数量

python train.py --train_dir=D:\X\Obeject_training\TF-OD-Test\train --pipeline_config_path=D:\X\Obeject_training\TF-OD-Test\model\ssd_mobilenet_v1_pets.config

 python train.py --train_dir=D:\Learning\python\Object-Detector-App-master-leanring\train\TF-OD-Test\train --pipeline_config_path=D:\Learning\python\Object-Detector-App-master-leanring\train\TF-OD-Test\model\ssd_mobilenet_v1_pets.config

D:\X\Obeject_training\TF-OD-Test
D:\X\Obeject_training\Object-Detector-App-master

CUDA_VISIBLE_DEVICES=3 python train.py --train_dir=D:\X\Obeject_training\TF-OD-Test\train --pipeline_config_path=D:\X\Obeject_training\TF-OD-Test\model\ssd_mobilenet_v1_pets.config

python CUDA_VISIBLE_DEVICES=3
根据提示 补充模块  



TEST
python train.py --train_dir=D:\X\Obeject_training\TF-OD-Test\train  --gpu=3 --pipeline_config_path=D:\X\Obeject_training\TF-OD-Test\model\ssd_mobilenet_v1_pets.config







 训练完成  生成  .pb文件
 把训练出来的3的文件放到D:\Learning\python\out_data下
 根据训练的class  修改config文件
 
使用 export_inference_graph.py

修改格式
标准格式
    python export_inference_graph \
    --input_type image_tensor \
    --pipeline_config_path path/to/ssd_inception_v2.config \
    --checkpoint_path path/to/model-ckpt-数字 \
    --inference_graph_path path/to/inference_graph.pb
    
进入 cd D:\Learning\python\Object-Detector-App-master
  输入 python export_inference_graph.py \
    --input_type=image_tensor \
    --pipeline_config_path=D:\Learning\python\Object-Detector-App-master-leanring\train\TF-OD-Test\model\ssd_mobilenet_v1_pets.config \
    --checkpoint_path=D:\Learning\python\out_data\model.ckpt-2087 \
    --inference_graph_path=D:\Learning\python\out_data
    
python export_inference_graph.py  --input_type=image_tensor   --pipeline_config_path=D:\Learning\python\Object-Detector-App-master-leanring\train\TF-OD-Test\model\ssd_mobilenet_v1_pets.config   --checkpoint_path=D:\Learning\python\out_data\model.ckpt-31662   --inference_graph_path=D:\Learning\python\out_data

多类
python export_inference_graph.py  --input_type=image_tensor   --pipeline_config_path=D:\Learning\python\Object-Detector-App-master-leanring\train\TF-OD-Test\model\ssd_mobilenet_v1_raccoon_gun.config   --checkpoint_path=D:\Learning\python\out_data\model.ckpt-181363   --inference_graph_path=D:\Learning\python\out_data
inception  python export_inference_graph.py  --input_type=image_tensor   --pipeline_config_path=D:\Learning\python\Object-Detector-App-master-leanring\train\TF-OD-Test\model\ssd_inception_v2_raccoon_gun.config   --checkpoint_path=D:\Learning\python\out_data\model.ckpt-200000   --inference_graph_path=D:\Learning\python\out_data

```


import tensorflow as tf

# 通过tf.device将运算指定到特定的设备上。
with tf.device('/cpu:0'):
   a = tf.constant([1.0, 2.0, 3.0], shape=[3], name='a')
   b = tf.constant([1.0, 2.0, 3.0], shape=[3], name='b')
with tf.device('/gpu:0'):
    c = a + b

sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
print(sess.run(c))







打开object_detection_app.py
修改 PATH_TO_CKP  和  PATH_TO_LABELS    进行测试
路径要改为 D:\Learning\python\Object-Detector-App-master\object_detection








检测图片，把训练出来的 .PB 文件和对应的 pbtxt 文件放到模块下。



























https://github.com/tensorflow/models/tree/master/object_detection

浣熊列子
https://github.com/datitran/raccoon_dataset

参考
http://blog.csdn.net/cuixing001/article/details/77092627
http://blog.csdn.net/ch_liu23/article/details/53558549
http://blog.csdn.net/zhangjunbob/article/details/52769381