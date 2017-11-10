import os
import cv2
import time
import argparse
import multiprocessing
import numpy as np
import tensorflow as tf

import imageio
#需要联网，切会下载一个 file:///C:/Users/Administrator/AppData/Local/imageio/ffmpeg/ffmpeg.win32.exe  
#假如未联网，可以松动放置，已放到目录下
imageio.plugins.ffmpeg.download()

from moviepy.editor import *
from IPython.display import HTML

from utils import FPS, WebcamVideoStream

from multiprocessing import Queue, Pool

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

#使用2号GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "2" 


CWD_PATH = "D:\\X\\Obeject_training\\tensorflow_ob_detection\\"
# Path to frozen detection graph. This is the actual model that is used for the object detection.
MODEL_NAME = 'faster_rcnn_resnet101_coco_11_06_2017'
#PATH_TO_CKPT = os.path.join(CWD_PATH, 'object_detection', MODEL_NAME, 'frozen_inference_graph.pb')




#训练模型2017.08.30
#模型的位置和标签 
PATH_TO_CKPT = os.path.join(CWD_PATH, 'model', MODEL_NAME , 'frozen_inference_graph.pb')
PATH_TO_LABELS = os.path.join(CWD_PATH, 'label_data','commen', 'mscoco_label_map.pbtxt')


#视频位置
Video_path = "D:\\X\\Obeject_training\\tensorflow_ob_detection\\imput_data\\video20170105081000.mkv"

NUM_CLASSES = 90

# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)


#检测图片，并返回操作之后的图片
def detect_objects(image_np, sess, detection_graph):
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    
    #以下五组变量为保存的节点 
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Actual detection.
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})

    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8)
    return image_np


def process_image(image):
     # NOTE: The output you return should be a color image (3 channel) for processing video below
    # you should return the final output (image with lines are drawn on lanes)

    image_process = detect_objects(image, sess, detection_graph)
    return image_process
        
#定义graph，读取模型及数据，之后不用重复读取，提高效率。        
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')        

#启动图，  
with tf.Session(graph=detection_graph) as sess:
    white_output = 'video1_out.mp4'
#subclip(0,40)代表识别视频中 0-40S这一个时间段
    clip1 = VideoFileClip(Video_path).subclip(20,48)

    white_clip = clip1.fl_image(process_image).to_RGB() #NOTE: this function expects color images!!s
    white_clip.write_videofile(white_output, audio=False)
        
sess.close()        
#
#HTML("""
#<video width="960" height="540" controls>
#  <source src="{0}">
#</video>
#""".format(white_output))
#
##
#clip1 = VideoFileClip("video1_out.mp4")
#clip1.write_gif("final.gif")
#        
#        
        
        
        
        
        
        
        
        
        
        