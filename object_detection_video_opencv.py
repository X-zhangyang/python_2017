import os
import cv2
import time
import argparse
import multiprocessing
import numpy as np
import tensorflow as tf




import imageio
imageio.plugins.ffmpeg.download()

from moviepy.editor import *
from IPython.display import HTML

from utils import FPS, WebcamVideoStream

from multiprocessing import Queue, Pool


from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

CWD_PATH = os.getcwd()

# Path to frozen detection graph. This is the actual model that is used for the object detection.
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
#PATH_TO_CKPT = os.path.join(CWD_PATH, 'object_detection', MODEL_NAME, 'frozen_inference_graph.pb')

# List of the strings that is used to add correct label for each box.
#PATH_TO_LABELS = os.path.join(CWD_PATH, 'object_detection', 'data', 'mscoco_label_map.pbtxt')



#训练模型2017.08.30
#模型的位置和标签 
PATH_TO_CKPT = os.path.join('D:\\Learning\\python\\Object-Detector-App-master\\object_detection\\ssd_mobilenet_v1_coco_11_06_2017\\frozen_inference_graph.pb')
PATH_TO_LABELS = os.path.join(CWD_PATH, 'object_detection', 'data', 'mscoco_label_map.pbtxt')


#视频位置
Video_path = "D:\\Learning\\python\\test\\boat\\15s-20s.mp4"

NUM_CLASSES = 90

# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)



#
#import numpy as np
#import cv2






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
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
            
        with tf.Session(graph=detection_graph) as sess:
            image_process = detect_objects(image, sess, detection_graph)
            return image_process
        

#

cap = cv2.VideoCapture(Video_path)



##获得码率及尺寸
fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
num_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

videoWriter = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)

#while(cap.isOpened()):
#    ret, frame = cap.read()
#
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#    frame = process_image(gray)
#    cv2.imshow('frame',frame)
#    
#    videoWriter.write(frame)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break
#
#cap.release()
#cv2.destroyAllWindows()




success, frame = cap.read()
while success:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = process_image(gray)
    videoWriter.write(frame)
    success, frame = cap.read()


cap.release()
cv2.destroyAllWindows()












#
#videoCapture = cv2.VideoCapture(Video_path)
#
###获得码率及尺寸
#fps = videoCapture.get(cv2.CAP_PROP_FPS)
#size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), 
#        int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#num_frame = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))

#指定写视频的格式, I420-avi, MJPG-mp4
#videoWriter = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)
#
#num_begin=1 

#将图片 / 视频帧写为视频
#
#fps = 24   #视频帧率
#fourcc = cv2.cv.CV_FOURCC('M','J','P','G')  
#videoWriter = cv2.VideoWriter('D:/testResults/match/flower2.avi', fourcc, fps, (1360,480))   #(1360,480)为视频大小
#for i in range(1,300):
#    p1=0
#    p2=i
#    img12 = cv2.imread('D:/testResults/img_'+str(p1)+'_'+str(p2)+'.jpg')
##    cv2.imshow('img', img12)
##    cv2.waitKey(1000/int(fps))
#    videoWriter.write(img12)
#videoWriter.release()
#
#
#抽取视频帧并存储为图像
#cap = cv2.VideoCapture(Video_path)  
#c = 1  
#  
#while(cap.isOpened()):  
#    ret, frame = cap.read()  
#  
#    new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
#  
#    cv2.imshow('frame',new_frame)  
#    cv2.imwrite('image/'+str(c) + '.jpg',new_frame) #存储为图像  
#    c = c+1  
#    if cv2.waitKey(1) & 0xFF == ord('q'):  
#        break  
#  
#cap.release()  
#cv2.destroyAllWindows()  
#





detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
        
    with tf.Session(graph=detection_graph) as sess:
        success, frame = videoCapture.read()
        while success:
            new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
            
            frame = detect_objects(new_frame, detection_graph, sess)
#            cv2.imshow('frame', frame) #显示
#            cv2.waitKey(1000/int(fps))
            videoWriter.write(frame)
            success, frame = videoCapture.read()

videoCapture.release()
cv2.destroyAllWindows()




#





##
#def process_image(image):
#    # NOTE: The output you return should be a color image (3 channel) for processing video below
#    # you should return the final output (image with lines are drawn on lanes)
#    detection_graph = tf.Graph()
#    with detection_graph.as_default():
#        od_graph_def = tf.GraphDef()
#        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
#            serialized_graph = fid.read()
#            od_graph_def.ParseFromString(serialized_graph)
#            tf.import_graph_def(od_graph_def, name='')
#            
#        with tf.Session(graph=detection_graph) as sess:
#            image_process = detect_objects(image, sess, detection_graph)
#            return image_process
#        
#        
#        
#white_output = 'video1_out.mp4'
##subclip(0,40)代表识别视频中 0-40S这一个时间段
#clip1 = VideoFileClip(Video_path).subclip(19,20)
##clip1 = clip1_1.VideoClip.subclip(0,40)
#white_clip = clip1.fl_image(process_image).to_RGB() #NOTE: this function expects color images!!s
#white_clip.write_videofile(white_output, audio=False)
#        
#        
#
#HTML("""
#<video width="960" height="540" controls>
#  <source src="{0}">
#</video>
#""".format(white_output))
#
###
##clip1 = VideoFileClip("video1_out.mp4")
##clip1.write_gif("final.gif")
##        
        
        
        
        
        
        
        
        
        
        
        