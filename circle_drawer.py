import os
import cv2
from datetime import datetime
from varname.helpers import debug
import json
import shutil

green_color = (0,200,0)# палитра из цветов синий зеленый красный
red_color = (0,0,200)# палитра из цветов синий зеленый красный
white_color = (255,255,255)# палитра из цветов синий зеленый красный
black_color = (0,0,0)# палитра из цветов синий зеленый красный
yellow_color = (0,190,210)# палитра из цветов синий зеленый красный
blue_color = (255,255,102)# палитра из цветов синий зеленый красный
pink_color = (255,0,255)# палитра из цветов синий зеленый красный


current_x = None
current_y = None
def mouse(event, x, y, flags, info):
    global current_x, current_y
    if event == cv2.EVENT_LBUTTONDOWN:
        current_x, current_y = x, y

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
    cv2.setMouseCallback(window_name, mouse)
    last_pressed_key = 0
    while last_pressed_key != 'q':
        cv2.imshow(window_name, img2draw)
        last_pressed_key = cv2.waitKeyEx(-1)
        debug(last_pressed_key)
        last_pressed = chr(last_pressed_key)
        debug(current_x , current_y)
        if current_x is not None:
            cv2.circle(
                img2draw,
                center=(current_x, current_y), # положение центра кружочка по ширине и высоте
                radius=40,
                color=blue_color,
                thickness=5
            )