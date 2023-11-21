import os
import cv2
from datetime import datetime
from varname.helpers import debug

def curDateTime():
    now = datetime.now()
    return now.strftime("%Y.%m.%d.%H.%M.%S")

start_time = curDateTime()
video_path = '/Users/ila/sasha_the_coder/datasets/videos/chekanka_001.mp4'
images_path = '/Users/ila/sasha_the_coder/datasets/images/chekanka_001'
# os.makedirs(images_path, exist_ok=True)
debug(start_time)
images_names = sorted(os.listdir(images_path))
print(images_names)
images_count = len(images_names)
current_image_id = 0
is_programme_finished = False
last_pressed = None
while is_programme_finished == False:
    if current_image_id < 0:
        current_image_id = images_count - 1
    elif current_image_id >= images_count - 1:
        current_image_id  = 0 
    image_name = images_names[current_image_id]
    image_path = os.path.join(images_path, image_name)
    img  = cv2.imread(image_path)
    img2draw = img.copy()

    frame_info = 'frame {} of {}'.format(current_image_id, images_count-1)

    lastast_x_text_position = 50 
    last_y_text_position = 100

    cv2.putText(
        img2draw,
        frame_info,
        org=(lastast_x_text_position , last_y_text_position ),
        fontFace=cv2.FONT_HERSHEY_COMPLEX,
        fontScale=1,
        color=(248,252,3),
        thickness=5
    )
    if last_pressed != None:
        last_y_text_position += 50

        cv2.putText(
            img2draw,
            last_pressed,
            org=(lastast_x_text_position , last_y_text_position ),
            fontFace=cv2.FONT_HERSHEY_COMPLEX,
            fontScale=1,
            color=(248,252,3),
            thickness=5
        )
    cv2.imshow('разметчик',img2draw)
    last_pressed_key = cv2.waitKeyEx(-1)
    debug(last_pressed_key)
    last_pressed = chr(last_pressed_key)
    if last_pressed == 'q':
        is_programme_finished = True
        break
    elif last_pressed == 'h': #  left
        current_image_id -= 1
        continue 
    elif last_pressed == 'l': #  right
        current_image_id += 1
        continue 