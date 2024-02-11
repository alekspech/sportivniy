import os
import cv2
from datetime import datetime
from varname.helpers import debug
import json
import shutil

def mouse(event, x, y):
    if event == cv2.EVENT_RBUTTONDOWN:
        return (x, y)

def curDateTime():
    now = datetime.now()
    return now.strftime("%Y.%m.%d.%H.%M.%S")

start_time = curDateTime()
video_path = '/Users/ila/sasha_the_coder/datasets/videos/chekanka_001.mp4'
# images_path = '/Users/ila/sasha_the_coder/datasets/images/test'
images_path = '/Users/ila/sasha_the_coder/datasets/images/chekanka_001'
ball_images_path = '/Users/ila/sasha_the_coder/datasets/images/chekanka_001_saved/chekanka'
frame_from = 943
frame_to =  1038
for image_name in sorted(os.listdir(ball_images_path)):
    frame_name, extention = os.path.splitext(image_name)
    frame_number = int(frame_name)
    if frame_number < frame_from or frame_number > frame_to:
        continue
    print(frame_number)
    image_path = os.path.join(ball_images_path, image_name)
    img = cv2.imread(image_path, flags=1)
    img2draw = img.copy()
    print(img.shape)
    # cv2.imshow('img chorno-bely', img2draw)
    # cv2.waitKey(200)
    window_name = 'ball drawer'
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, img2draw)
    cv2.waitKey(-1)
    cv2.setMouseCallback(window_name, mouse)