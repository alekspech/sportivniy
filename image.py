import cv2 

image_path = '../datasets/mbappe.jpg'
image = cv2.imread(image_path)
h, w, c = image.shape # высота ширина цветовые каналы
print(image[0, 0])
image[:,:,0] *= 0 # обнуляем синий(нулевой)цветовой канал
image[:,:,1] *= 0
image = image[0:int(h/2),:,:]
cv2.imshow('mbappe', image)
cv2.waitKey(delay=-1)
print('done')