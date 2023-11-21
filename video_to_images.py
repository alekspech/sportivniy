import os
import cv2

video_path = '/Users/ila/sasha_the_coder/datasets/videos/chekanka_001.mp4'
outdir = '/Users/ila/sasha_the_coder/datasets/images/chekanka_001'
os.makedirs(outdir, exist_ok=True)
video_capture = cv2.VideoCapture(video_path)
frames_number =  int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
print(frames_number)
current_frame = 0
while video_capture.isOpened():
    result, img = video_capture.read()
    if result == False:
        continue
    outname = '{:06d}.jpg'.format(current_frame)
    outpath = os.path.join(outdir, outname)
    cv2.imwrite(outpath, img)
    print(outpath)
    current_frame += 1
    if current_frame >= frames_number:
        video_capture.release()
        break