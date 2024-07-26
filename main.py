import cv2
import os

img = cv2.imread('./data/road-signs/footpath.jpg')
img2 = cv2.imread('./data/road-signs/left-turn.jpg')

if img is None:
    print('ФАЙЛ НЕ НАЙДЕН')
    os._exit(1)

#img[50:, 150:] = [0, 0, 255]

#x_max, y_max, _ = img.shape

#x = x_max // 3
#y = y_max // 3

#img[x, y] = [0, 0, 255]
#tpl = (img.item(x, y, 0), img.item(x, y, 1), img.item(x, y, 2))

#print(tpl)

#roi = img[50:150, 20:200]

#print(roi)
x, x_max, y, y_max = map(int, input('Введите координаты: ').split())

roi = img[x:x_max, y:y_max]

cv2.imshow('roi', roi)
#cv2.imshow('img', img)
while True:
    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()











