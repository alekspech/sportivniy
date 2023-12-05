import os
import cv2
from datetime import datetime
from varname.helpers import debug
import json

def curDateTime():
    now = datetime.now()
    return now.strftime("%Y.%m.%d.%H.%M.%S")

start_time = curDateTime()
video_path = '/Users/ila/sasha_the_coder/datasets/videos/chekanka_001.mp4'
# images_path = '/Users/ila/sasha_the_coder/datasets/images/test'
images_path = '/Users/ila/sasha_the_coder/datasets/images/chekanka_001'
# os.makedirs(images_path, exist_ok=True)
debug(start_time)
images_names = sorted(os.listdir(images_path))
print(images_names)
images_count = len(images_names)
labels = {
    'T': 'trash',
    'b': 'with_ball',
    'c': 'chekanka',
}
frames_labels = {}
for i in range(images_count):
    image_path = images_names[i]
    frames_labels[image_path] = 'unwatched'
current_image_id = 0 
labels_path = images_path + '_labels.json'
if os.path.isfile(labels_path):
    with open(labels_path, 'r') as f:
        frames_labels = json.load(f)
        print('labels loaded from file',labels_path)
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

    lastast_x_text_position = 10 
    last_y_text_position = 25
    label_info  = '{} = {}'.format(image_name, frames_labels[image_name])
    cv2.putText(
        img2draw,
        label_info,
        org=(lastast_x_text_position , last_y_text_position ),
        fontFace=cv2.FONT_HERSHEY_COMPLEX,
        fontScale=1,
        color=(248,252,3),
        thickness=5
    )
    last_y_text_position += 50

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
    with_ball = False    
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
    elif last_pressed == 'H': #  left
        current_image_id -= 100
        continue 
    elif last_pressed == 'L': #  right
        current_image_id += 100
        continue 
    elif last_pressed in labels.keys():
        frames_labels[image_name] = labels[last_pressed]
        with open(labels_path, 'w') as f:
            json.dump(frames_labels, f, indent=4)
            print('labels saved to', labels_path)