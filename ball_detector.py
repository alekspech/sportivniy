import os
import cv2
from datetime import datetime
from varname.helpers import debug
import json
import shutil
import numpy as np

background_leg = [943, 944, 945, 946, 955]
background_stadium = [947, 948, 949, 950, 952]
forwardground_leg = [951, 965, 966, 982, 997]

img_path = '/Users/ila/sasha_the_coder/datasets/images/chekanka_001_saved/chekanka/000946.jpg'
out_path = '/Users/ila/sasha_the_coder/datasets/images/chekanka_001_saved/000948_ball.jpg'
img = cv2.imread(img_path)
img = cv2.resize(img, dsize=None, fx=1/2, fy=1/2)
img2draw = img.copy()
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.GaussianBlur(img, (5,13), 0)
_, img = cv2.threshold(
    img, 
    thresh=175, 
    maxval=255,
   type=cv2.THRESH_BINARY
)
contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    area = w * h
    if area < 100 or area > 1000:
        continue
    ratio = w/h
    print(ratio)
    if ratio < 0.8 or ratio>1.5:
        continue
    cv2.rectangle(
        img2draw,
        (x, y),
        (x + w , y + h),
        (0,255,0),
        thickness=2
    )
out_img = np.vstack((
    img2draw,
    cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
)) 
cv2.imwrite(out_path, out_img)
print(out_path)

