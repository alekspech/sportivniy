# https://www.rapidtables.com/web/color/RGB_Color.html - сайт для выбора цветов
import os
import cv2 #  набор функций для обработки изображений (cv - computer vision - компьютерное зрение) 

image_path = 'datasets/mbappe.jpg'
# image_path = '/Users/ila/sasha_the_coder/images/30cc0788d11ed9794d9789b6128b4.jpeg'
# image_path = '/Users/ila/sasha_the_coder/images/30cc0788d11ed9794d9789b6128b4.jpeg'
image_name = os.path.basename(image_path) # вырезать имя файла из полного пути до файла 
out_image_name = 'geometry_' + image_name

image_dir = os.path.dirname(image_path)# вырезать путь до папки с файлом из полного пути до файла
out_image_path = os.path.join(image_dir, out_image_name)

image = cv2.imread(image_path)
height, width, channels  = image.shape # высота ширина цветовые каналы
image2draw = image.copy() # картинка для рисования - копия оригинальной картинки
# image2draw *= 0 # мы умножаем все пиксели на ноль и получаем черную картинку
print(height, width, channels)
green_color = (0,200,0)# палитра из цветов синий зеленый красный
red_color = (0,0,200)# палитра из цветов синий зеленый красный
white_color = (255,255,255)# палитра из цветов синий зеленый красный
black_color = (0,0,0)# палитра из цветов синий зеленый красный
yellow_color = (0,190,210)# палитра из цветов синий зеленый красный
blue_color = (255,255,102)# палитра из цветов синий зеленый красный
pink_color = (255,0,255)# палитра из цветов синий зеленый красный

color = (0,0,0)
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

image_center_xy = (
    round(width/2),
    round(height/2),
)
circle_radius = 150



image2draw = cv2.circle(
    image2draw,
    center=image_center_xy, # положение центра кружочка по ширине и высоте
    radius=circle_radius,
    color=blue_color,
    thickness=5
)
image2draw = cv2.circle(
    image2draw,
    center=image_center_xy, # положение центра кружочка по ширине и высоте
    radius=5,
    color=yellow_color,
    thickness=-1
)
top_left_xy = (
    image_center_xy[0] + circle_radius,
    image_center_xy[1] + circle_radius
)
bottom_right_xy = (
    image_center_xy[0] - circle_radius,
    image_center_xy[1] - circle_radius
)
image2draw = cv2.rectangle(
    image2draw,
    pt1=top_left_xy, 
    pt2=bottom_right_xy,
    color=green_color,
    thickness=5
)
image2draw = cv2.line(
    image2draw,
    pt1=top_left_xy, 
    pt2=bottom_right_xy,
    color=red_color,
    thickness=5
)
# задать четыре переменные - вершины ромба -  top left right bottom
# попарно соединить их через сv2 line, чтобы получился ромб 
top_xy = (
    image_center_xy[0],  
    image_center_xy[1] - circle_radius 
)
left_xy = (
    image_center_xy[0] - circle_radius,  
    image_center_xy[1]
)
right_xy = (
    image_center_xy[0] + circle_radius,  
    image_center_xy[1]
)
bottom_xy = (
    image_center_xy[0],  
    image_center_xy[1] + circle_radius
)



image2draw = cv2.line(
    image2draw,
    pt1=top_xy, 
    pt2=right_xy,
   color=red_color,
    thickness=5
)
image2draw = cv2.line(
    image2draw,
    pt1=top_xy, 
    pt2=left_xy,
   color=red_color,
    thickness=5
)
image2draw = cv2.line(
    image2draw,
    pt1=bottom_xy, 
    pt2=right_xy,
   color=red_color,
    thickness=5
)
image2draw = cv2.line(
    image2draw,
    pt1=bottom_xy, 
    pt2=left_xy,
   color=red_color,
    thickness=5
)


family_position_xy = (
    image_center_xy[0] - 270,  
    image_center_xy[1] - 370 
)

image2draw = cv2.putText(
    image2draw,
    'Ronaldo',
    org=family_position_xy,
    fontFace=cv2.FONT_HERSHEY_COMPLEX,
    fontScale=2,
    color=blue_color,
    thickness=5
)
number_position_xy = (
    image_center_xy[0] - 250,  
    image_center_xy[1] - 120 
)
image2draw = cv2.putText(
    image2draw,
    '7',
    org=number_position_xy,
    fontFace=cv2.FONT_HERSHEY_PLAIN,
    fontScale=12,
    color=blue_color,
    thickness=6
) 

# подобрать настройки сv2.putText чтобы надпись роналду примерно совпало с надписью на футболке написать 7 на футболке это отдельная функция
cv2.imwrite(out_image_path, image2draw)
print('done', out_image_path)
cv2.imshow('mbappe', image2draw)
cv2.waitKey(-1)