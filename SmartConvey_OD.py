# -*- coding: utf-8 -*-
"""
Created on Thu May  9 11:01:55 2019

@author: Sunny
"""

import cv2
import numpy as np
import os
import sys
import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
root = 'D:/'
#root = 'D:/'
#def main(frame= cv2.imread('/0926_1_detect.jpg'), j='0927', det=45):
import time

def capture_write(filename="image.jpeg", port=1, ramp_frames=30, x=640, y=480):
    vc = cv2.VideoCapture(port)
        
    # Adjust camera lighting
    for i in range(ramp_frames):
        temp = vc.read()
    retval, im = vc.read()
        #    cv2.imwrite(filename,im)
    del(vc)
    return im

def main():
    os.chdir('D:/SC')
    sys.path.append("..")

    # Object detection imports
    MODEL_NAME = 'egg1119'
    PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
    PATH_TO_LABELS = os.path.join('label', 'egg_12345.pbtxt')
    NUM_CLASSES = 5

    #Load a (frozen) Tensorflow model into memory. 
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        
    #Loading label map
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
        
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            
            while True:
                
                det = yield
                j=time.strftime("%y%m%d_%H%M%S" , time.localtime())
                if det ==1235 or det==45:
                    
                    image_np = capture_write()
                    cv2.imwrite(root + '/{}_0_start.jpg'.format(j), image_np)
        #            image_np = image_np.astype('uint8')
                    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
                    image_np_expanded = np.expand_dims(image_bgr, axis=0)
        
                    (boxes, scores, classes, num) = sess.run(
                            [detection_boxes, detection_scores, detection_classes, num_detections],
                            feed_dict={image_tensor: image_np_expanded})
        
                    if det==1 or det==2 or det==3 or det==4 or det==5:
                        boxes = np.squeeze(boxes)
                        scores = np.squeeze(scores)
                        classes = np.squeeze(classes)
                        indices = np.argwhere(classes == det)
                        boxes = np.squeeze(boxes[indices])
                        scores = np.squeeze(scores[indices])
                        classes = np.squeeze(classes[indices])
        
                    elif det ==1235:
                        boxes = np.squeeze(boxes)
                        scores = np.squeeze(scores)
                        classes = np.squeeze(classes)
                        indices = np.concatenate((np.argwhere(classes == 5),np.argwhere(classes == 3),np.argwhere(classes == 2),np.argwhere(classes == 1)),0)
                        boxes = np.squeeze(boxes[indices])
                        scores = np.squeeze(scores[indices])
                        classes = np.squeeze(classes[indices])
                        
                    elif det ==45:
                        boxes = np.squeeze(boxes)
                        scores = np.squeeze(scores)
                        classes = np.squeeze(classes)
                        indices = np.concatenate((np.argwhere(classes == 5),np.argwhere(classes == 4)),0)
                        if indices.shape==(1,1):
                            indices=np.array([[0],[1],[2],[3]])
                        boxes = np.squeeze(boxes[indices])
                        scores = np.squeeze(scores[indices])
                        classes = np.squeeze(classes[indices])
                        
                    vis_util.visualize_boxes_and_labels_on_image_array(
                            image_np,
                            np.squeeze(boxes),
                            np.squeeze(classes).astype(np.int32),
                            np.squeeze(scores),
                            category_index,
                            use_normalized_coordinates=True,
                            line_thickness=1,
                            min_score_thresh=0.8)   # ref: visualization_utils.py#L594
            
                    cv2.imwrite(root + '/{}_1_detect.jpg'.format(j), image_np)
                    print('##   Object detection done   ##')

                    
                    # cut target object
                    box = boxes
                    pic = cv2.imread(root + '/{}_0_start.jpg'.format(j))
                #    pic = cv2.imread(root + '/0926_1_detect.jpg'.format(j))
                    
                    bbox_num = int(np.count_nonzero(boxes!=0)/4)
                    print('##  bbox_num: ', bbox_num, '            ##')
                         
                    box_num = int(np.count_nonzero(classes==5))
                    print('##  box_num: ', box_num, '             ##')
                    empty_num = int(np.count_nonzero(classes==4))
                    print('##  empty_num: ', empty_num, '           ##')
                    d_num = int(np.count_nonzero(classes==3))
                    print('##  d_num: ', d_num, '               ##')
                #    egg_num = bbox_num - box_num - empty_num - d_num
                    defect_list = list(range(box_num + empty_num, d_num)) # [0,1,2]
                    egg_list = list(range(d_num, bbox_num)) # total num of egg
                    d_egg=[]  # len(set(d_egg))
                    ymin0 = 190
                    xmin0 = 270
                    ymax0 = 290
                    xmax0 = 370
                
                    if box_num == 0 and bbox_num != 0:
                        if det==1235:
                            for i in egg_list:
                                for q in defect_list:
                                    if box[i,0]<=box[q,0]and box[i,1]<=box[q,1]and box[i,2]>=box[q,2]and box[i,3]>=box[q,3]:  # No. q defect in egg
                                    
                                        ymin0 = int(box[i,0]*480*0.98)
                                        xmin0 = int(box[i,1]*640*0.98)
                                        ymax0 = int(box[i,2]*480*(1/0.98))
                                        xmax0 = int(box[i,3]*640*(1/0.98))
#                                        roi0 = pic[ymin0:ymax0,xmin0:xmax0].copy()
#                                        cv2.imwrite(root + '/{}_2_cut0_{}.jpg'.format(j,i), roi0)
                                        d_egg.append(i)
#                                        print('d_egg: ', d_egg)
#                            print('box2:',box)
                            ymin = int(box[0,0]*480*0.98)
                            xmin = int(box[0,1]*640*0.98)
                            ymax = int(box[0,2]*480*(1/0.98))
                            xmax = int(box[0,3]*640*(1/0.98))
                            
                            x_p=int((xmax0 + xmin0)*0.5)
                            y_p=int((ymax0 + ymin0)*0.5)
                        else:
                            ymin = int(box[0,0]*480*0.98)
                            xmin = int(box[0,1]*640*0.98)
                            ymax = int(box[0,2]*480*(1/0.98))
                            xmax = int(box[0,3]*640*(1/0.98))
                
                            x_p=int((xmax + xmin)*0.5)
                            y_p=int((ymax + ymin)*0.5)
#                        roi = pic[ymin:ymax,xmin:xmax].copy()
#                        cv2.imwrite(root + '/{}_2_cut.jpg'.format(j), roi)
                        
                        print('##  defect egg numbers: ',len(set(d_egg)), '  ##')
                        yield cv2.circle(pic,(x_p, y_p), 10, (0, 0, 255), 3), x_p, y_p, len(set(d_egg)), j, empty_num#, box, boxes, classes
                    else:
                        print('pass the box')
                        yield 'box', None, None, len(set(d_egg)), j, empty_num
if __name__=='__main__':
    main()


    
 
    



