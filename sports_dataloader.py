import os
import cv2 
from varname.helpers import debug
import numpy as np

def read_gt_txt(gt_txt_path):   
    with open(gt_txt_path, 'r') as f: # открываем  gt.txt
        markup_lines = f.readlines()
    match_frames = {}
    # print(markup_lines[0])
    for player_position_str in markup_lines:
        # print('=' * 50)
        # print(player_position_str)
        player_position = player_position_str.split(', ')
        player_position = player_position[:-3]
        for i in range(len(player_position)):
            player_position[i] = int(player_position[i])
        frame_number, player_id, x, y, width , height = player_position
        # print(player_id, x, y)
        if frame_number not in match_frames.keys():
            match_frames[frame_number] = {}
        player_position_xywh = (x, y, width, height)
        player_position_x1y1x2y2 = box_xywh_to_x1y1x2y2(box_xywh=player_position_xywh)  
        match_frames[frame_number][player_id] = player_position_x1y1x2y2
    return match_frames

def box_xywh_to_x1y1x2y2(box_xywh):
    box_x1y1x2y2 = (
        box_xywh[0],
        box_xywh[1],
        box_xywh[0]+box_xywh[2], #  х плюс ширина 
        box_xywh[1]+box_xywh[3] # у плюс высота
    )
    return box_x1y1x2y2

def box_width(box_x1y1x2y2):
    width = box_x1y1x2y2[2]-box_x1y1x2y2[0]
    return width

def box_height(box_x1y1x2y2):
    height = box_x1y1x2y2[3]-box_x1y1x2y2[1]
    return height

def box_center(box_x1y1x2y2):
    player_center_xy = (
        player_position_x1y1x2y2[0]+round(box_width(box_x1y1x2y2)/2),
        player_position_x1y1x2y2[1]+round(box_height(box_x1y1x2y2)/2),
    )
    return player_center_xy

def read_image_path(match_path):   
    match_path = {}
    for current_dir, dirs, files in os.walk(match_path):
        # debug(current_dir)
        # debug(dirs)
        # debug(files)
        for file_name in files:
            if len(file_name) == 10 and os.path.splitext(file_name)[1] == '.jpg':
                frame_number = int(os.path.splitext(file_name)[0])
                # debug(frame_number,file_name)
                file_path = os.path.join(current_dir, file_name)
                match_path[frame_number] = file_path
    return match_path
    
players_colors_bgr = {
    0: (3,252,223),
    1: (3,107,252),
    2: (252,3,157),
    3: (207,3,252),
    4: (252,3,48),
    5: (252,123,3),
    6: (252,198,3),
    7: (248,252,3),
    8: (165,252,3),
    9: (3,252,57),
    10: (22,120,61),
    11: (0,0,0),
}

match_path = '/Users/ila/sasha_the_coder/datasets/sportsMOT_volley_starter_pack.002/sportsMOT_volley_light_dataset/match_001_short'
markup_path = '/Users/ila/sasha_the_coder/datasets/sportsMOT_volley_starter_pack.002/sportsMOT_volley_light_dataset/match_001_short/gt/gt.txt'
match_name = os.path.basename(match_path)
outdir = 'out'
os.makedirs(outdir, exist_ok=True)
match_frames = read_gt_txt(gt_txt_path=markup_path)
# дз: вынести слудующие строки(74-85) которые читают пути до изображений из папки в новую функцию read_image_path(match_path)

for frame_number , frame_players in match_frames.items():# мы ходим по кадрам , для каждого кадра  получаем позиции всех игроков 
    # print('frame number:{:06d}'.format(frame_number))
    # print(frame_players)
    if frame_number not in match_path.keys():
        continue
    img = cv2.imread(match_path[frame_number])
    img2draw = img.copy()
    for player_id, player_position_x1y1x2y2 in frame_players.items():# ходим по игрокам на текущем кадре
        player_id_str = str(player_id)
        width = box_width(box_x1y1x2y2=player_position_x1y1x2y2)
        height = box_height(box_x1y1x2y2=player_position_x1y1x2y2)
        player_center_xy = box_center(box_x1y1x2y2=player_position_x1y1x2y2)
        cv2.circle(
            img2draw,
            center=player_center_xy, # положение центра кружочка по ширине и высоте
            radius=3,
            color=players_colors_rgb[player_id],
            thickness=5
        )
        top_left_xy = (player_position_x1y1x2y2[0],player_position_x1y1x2y2[1])
        bottom_right_xy = (player_position_x1y1x2y2[2],player_position_x1y1x2y2[3])
        top_left_yx = (player_position_x1y1x2y2[1],player_position_x1y1x2y2[0])
        bottom_right_yx = (player_position_x1y1x2y2[3],player_position_x1y1x2y2[2])
        player_img = img[
           top_left_yx[0]:bottom_right_yx[0], 
           top_left_yx[1]:bottom_right_yx[1],
           : 
        ]
        player_img_square = img[
           player_center_xy[1]-round(height/2):player_center_xy[1]+round(height/2), 
           player_center_xy[0]-round(height/2):player_center_xy[0]+round(height/2), 
           : 
        ]
        # cv2.imshow(str(player_id), player_img)
        
        # cv2.waitKey(-1)
        player_outdir = os.path.join(
            outdir,
            match_name
        )
        os.makedirs(player_outdir, exist_ok=True)
        box_str = f'{top_left_xy[0]}_{top_left_xy[1]}_{bottom_right_xy[0]}_{bottom_right_xy[1]}'
        player_outname = f'{frame_number}_{player_id}_{box_str}.jpg'
        player_square_outname = f'{frame_number}_{player_id}_{box_str}_square.jpg'
        player_outpath = os.path.join(player_outdir, player_outname)
        player_square_outpath = os.path.join(player_outdir, player_square_outname)
        cv2.imwrite(player_outpath, player_img)
        if player_img_square.size:
            cv2.imwrite(player_square_outpath, player_img_square)
        print(f'player {player_id} written to {player_outpath} {player_square_outpath} ')
        # player_width = player_position_xy[2] - player_position_xy[0]                 
        player_id_position = (
            top_left_xy[0] + round(width / 4),
            top_left_xy[1] - 25
        )
        player_color = players_colors_rgb[player_id]
        cv2.rectangle(
            img2draw,
            pt1=top_left_xy, 
            pt2=bottom_right_xy,
            color=player_color,
            thickness=5
        )
        top_left_xy_square = (
            player_center_xy[0]-round(height/2),
            player_center_xy[1]-round(height/2)
        ) 
        bottom_right_xy_square = (
            player_center_xy[0]+round(height/2),
            player_center_xy[1]+round(height/2)
        ) 
        cv2.rectangle(
            img2draw,
            pt1=top_left_xy_square, 
            pt2=bottom_right_xy_square,
            color=player_color,
            thickness=5
        )                       
        cv2.putText(
            img2draw,
            player_id_str,
            org=player_id_position,
            fontFace=cv2.FONT_HERSHEY_COMPLEX,
            fontScale=1,
            color=player_color,
            thickness=5
        ) 
    img_menu = np.ones(
        shape=(100,img2draw.shape[1],3), 
        dtype=img2draw.dtype
    )# нулевая (черная) картинка для нанесения информации о матче
    img_menu[:,:,:] = (250,100,75)
    current_position_xy = (10,30)
    frame_number_str = 'frame number::{}'.format(frame_number)
    frame_players_count = len(frame_players)
    players_info = 'players {} of 12'.format(frame_players_count)
    cv2.putText(
        img_menu,
        frame_number_str,
        org=current_position_xy,
        fontFace=cv2.FONT_HERSHEY_COMPLEX,
        fontScale=1,
        color=(0,0,0),
        thickness=3
    )
    current_position_xy = (
        current_position_xy[0],
        current_position_xy[1] + 30
    )  
    cv2.putText(
        img_menu,
        players_info,
        org=current_position_xy,
        fontFace=cv2.FONT_HERSHEY_COMPLEX,
        fontScale=1,
        color=(0,0,0),
        thickness=3
    )
    img2draw = np.vstack([img_menu,img2draw])
    print(img2draw.shape)
    img_outpath = 'out.jpg'
    cv2.imwrite(img_outpath, img2draw)
    # cv2.imshow('frame', img2draw)
    # cv2.waitKey(-1) 
    print('written to', os.path.abspath(img_outpath))

    exit()    
    

