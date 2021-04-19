#================================================================
#
#   File name   : detection_custom.py
#   Author      : PyLessons
#   Created date: 2020-09-17
#   Website     : https://pylessons.com/
#   GitHub      : https://github.com/pythonlessons/TensorFlow-2.x-YOLOv3
#   Description : object detection image and video example
#
#================================================================
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import cv2
import numpy as np
import tensorflow as tf
from yolov3.utils import detect_image, detect_realtime, detect_video, Load_Yolo_model, detect_video_realtime_mp
from yolov3.configs import *
from yolov3.dataset import Dataset
from yolov3.yolov4 import Create_Yolo
from evaluate_mAP import get_mAP


image_path   = "D:/YoloV4/TensorFlow-2.x-YOLOv3-master/IMAGES/image2084.png"
video_path   = "/content/Realtime_Animal_Tracking/Yolo/primate_clip_744.mp4"

yolo = Load_Yolo_model()
#detect_image(yolo, image_path, "D:/YoloV4/TensorFlow-2.x-YOLOv3-master/IMAGES/detect.jpg", input_size=YOLO_INPUT_SIZE, show=False, CLASSES=TRAIN_CLASSES, rectangle_colors=(255,0,0))
detect_video(yolo, video_path, '/content/Realtime_Animal_Tracking/Yolo/IMAGES/detected2.mp4', input_size=YOLO_INPUT_SIZE, show=False, CLASSES=TRAIN_CLASSES, rectangle_colors=(255,0,0))
#detect_realtime(yolo, '', input_size=YOLO_INPUT_SIZE, show=True, CLASSES=TRAIN_CLASSES, rectangle_colors=(255, 0, 0))

#detect_video_realtime_mp(video_path, "Output.mp4", input_size=YOLO_INPUT_SIZE, show=True, CLASSES=TRAIN_CLASSES, rectangle_colors=(255,0,0), realtime=False)

testset = Dataset('test')
mAP_model = Create_Yolo(input_size=YOLO_INPUT_SIZE, CLASSES=TRAIN_CLASSES)
mAP_model.load_weights("/content/checkpoints/yolov4_custom") # use keras weights
get_mAP(mAP_model, testset, score_threshold=TEST_SCORE_THRESHOLD, iou_threshold=TEST_IOU_THRESHOLD)
