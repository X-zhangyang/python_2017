"""Performs face alignment and stores face thumbnails in the output directory.

 python choose_images_step_2.py  输入文件路径（D:\X\facenet\datasets\test\0000045）输出文件路径（D:\X\facenet\datasets\test\a） --image_size=250 --gpu_memory_fraction=0.25
 python choose_images_step_2.py  D:\X\facenet\Generate_AFDB\AFDB_step_1  D:\X\facenet\Generate_AFDB\AFDB_step_2  --image_size=250 --gpu_memory_fraction=0.25

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from scipy import misc
import sys	
import os
import argparse
import tensorflow as tf
import numpy as np
import facenet
import align.detect_face
import random
from time import sleep


os.environ["CUDA_VISIBLE_DEVICES"] = "2"


def main(args):
    sleep(random.random())
    output_dir = os.path.expanduser(args.output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Store some git revision info in a text file in the log directory
    src_path,_ = os.path.split(os.path.realpath(__file__))
    
    dataset = facenet.get_dataset(args.input_dir)
    facenet.store_revision_info(src_path, output_dir, ' '.join(sys.argv))
    print('%d' % len(dataset))

    
    print('Creating networks and loading parameters')
    
    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=args.gpu_memory_fraction)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = align.detect_face.create_mtcnn(sess, None)
    
    minsize = 20 # minimum size of face
    threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
    factor = 0.709 # scale factor

    # Add a random key to the filename to allow alignment using multiple processes
    random_key = np.random.randint(0, high=99999)
    bounding_boxes_filename = os.path.join(output_dir, 'bounding_boxes_%05d.txt' % random_key)
    
    with open(bounding_boxes_filename, "w") as text_file:
        nrof_images_total = 0
        nrof_successfully_aligned = 0
        if args.random_order:
            random.shuffle(dataset)
        for cls in dataset:
            output_class_dir = os.path.join(output_dir, cls.name)
            if not os.path.exists(output_class_dir):
                os.makedirs(output_class_dir)
                if args.random_order:
                    random.shuffle(cls.image_paths)
            for image_path in cls.image_paths:
                nrof_images_total += 1
                filename = os.path.splitext(os.path.split(image_path)[1])[0]
                output_filename = os.path.join(output_class_dir, filename+'.jpg')
                #print(image_path)
                if not os.path.exists(output_filename):
                    try:
                        img = misc.imread(image_path)
                    except (IOError, ValueError, IndexError) as e:
                        errorMessage = '{}: {}'.format(image_path, e)
                        print(errorMessage)
                    else:
                        if img.ndim<2:
                            print('Unable to align "%s"' % image_path)
                            text_file.write('%s\n' % (output_filename))
                            continue
                        if img.ndim == 2:
                            img = facenet.to_rgb(img)
                        img = img[:,:,0:3]
    
                        bounding_boxes, _ = align.detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
                        nrof_faces = bounding_boxes.shape[0]
                        if nrof_faces>0:
                            det = bounding_boxes[:,0:4]
                            img_size = np.asarray(img.shape)[0:2]
#                            if nrof_faces>1:
#                                bounding_box_size = (det[:,2]-det[:,0])*(det[:,3]-det[:,1])
#                                img_center = img_size / 2
#                                offsets = np.vstack([ (det[:,0]+det[:,2])/2-img_center[1], (det[:,1]+det[:,3])/2-img_center[0] ])
#                                offset_dist_squared = np.sum(np.power(offsets,2.0),0)
#                                index = np.argmax(bounding_box_size-offset_dist_squared*2.0) # some extra weight on the centering
#                                det = det[index,:]
                            for k in range(len(det)):
                                
                            
                                
                                det_temp = np.squeeze(det[k])
                                bb = np.zeros(4, dtype=np.int32)
                            
                                #人脸在图片中的占比
                                rate = args.size_rate
                                width = (det_temp[2] - det_temp[0])/rate
                                high = (det_temp[3] - det_temp[1])/rate
                                
                            
                                bb[0] = np.maximum(det_temp[0]-width, 0)
                                bb[1] = np.maximum(det_temp[1]-high, 0)
                                bb[2] = np.minimum(det_temp[2]+width, img_size[1])
                                bb[3] = np.minimum(det_temp[3]+high, img_size[0])
                            
                                cropped = img[bb[1]:bb[3],bb[0]:bb[2],:]
                                scaled = misc.imresize(cropped, (args.image_size, args.image_size), interp='bilinear')
                                nrof_successfully_aligned += 1
                                if k>0 :
                                    output_filename_temp = output_class_dir +"/" +filename +'_'+ str(k)+ '.jpg'
                                else:
                                    output_filename_temp = output_class_dir +'/' +filename + '.jpg' 
                               
                                misc.imsave(output_filename_temp , scaled)
                                text_file.write('%s %d %d %d %d\n' % (output_filename_temp , bb[0], bb[1], bb[2], bb[3]))
                        else:
                            print('Unable to align "%s"' % image_path)
                            text_file.write('%s\n' % (output_filename_temp ))
            print('Path:%s has %s images' % (args.input_dir +'/' + cls.name ,len(cls)))                        
            print('Number of successfully aligned images: %d' % nrof_successfully_aligned)
        print('There are %d images.' % nrof_images_total)
#        print('%d' % len(dataset))

            

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    
    parser.add_argument('input_dir', type=str, help='Directory with unaligned images.')
    parser.add_argument('output_dir', type=str, help='Directory with aligned face thumbnails.')
    parser.add_argument('--image_size', type=int,
        help='Image size (height, width) in pixels.', default=182)
    parser.add_argument('--margin', type=int,
        help='Margin for the crop around the bounding box (height, width) in pixels.', default=44)
    parser.add_argument('--random_order', 
        help='Shuffles the order of images to enable alignment using multiple processes.', action='store_true')
    parser.add_argument('--size_rate', type=int, 
        help='The face size rate in an image', default=1.0)
    parser.add_argument('--gpu_memory_fraction', type=float,
        help='Upper bound on the amount of GPU memory that will be used by the process.', default=1.0)
    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
