# Прога получает и обрабатывает изображение
import pyautogui
import time
import numpy as np
import cv2
import imutils

# Ждем три секунды, успеваем переключиться на окно:
print('waiting for 2 seconds...')
time.sleep(2)

#ВНИМАНИЕ! PyAutoGUI НЕ ЧИТАЕТ В JPG!
title = 'title.png'

nfs_window_location = None
searching_attempt = 1
while searching_attempt <= 5:
    nfs_window_location = pyautogui.locateOnScreen(title)

    if nfs_window_location is not None:
        print('nfs_window_location = ', nfs_window_location)
        break
    else:
        searching_attempt += 1
        time.sleep(1)
        print("attempt %d..." % searching_attempt)

if nfs_window_location is None:
    print('NFS Window not found')
    exit(1)

# Извлекаем из картинки-скриншота только данные окна NFS.
# Наша target-картинка - это заголовочная полоска окна.
# Для получения скриншота, мы берем ее левую точку (0),
# а к верхней (1) прибавляем высоту (3)
left = nfs_window_location[0]
top = nfs_window_location[1]+nfs_window_location[3]

# ВНИМАНИЕ!  У вас, скорее всего, будет другое разрешение, т.к. у меня 4К-монитор!
# Здесь надо выставить те параметры, которые вы задали в игре.
window_resolution = (640, 480)

window = (left, top, left+window_resolution[0], top+window_resolution[1])

cv2.namedWindow('result')

while True:

    pix = pyautogui.screenshot(region=(int(left), int(top), window_resolution[0], window_resolution[1]))
    numpix = cv2.cvtColor(np.array(pix), cv2.COLOR_RGB2BGR)


    frame_hsv = cv2.cvtColor(numpix, cv2.COLOR_BGR2HSV)

    frame_h = frame_hsv[:, :, 0]
    frame_s = frame_hsv[:, :, 1]
    frame_v = frame_hsv[:, :, 2]

    #Зеленый
    min_ = (50, 120, 90)
    max_ = (69, 220, 220)
    mask = cv2.inRange(frame_hsv, min_, max_)
    result1 = cv2.bitwise_and(numpix, numpix, mask=mask)

    #Желтый
    min_ = (20, 100, 100)
    max_ = (30, 255, 255)
    mask = cv2.inRange(frame_hsv, min_, max_)
    result2 = cv2.bitwise_and(numpix, numpix, mask=mask)


    result_all = cv2.bitwise_or(result1, result2)
    result_rgb = cv2.cvtColor(result_all, cv2.COLOR_RGB2GRAY)
    contours = cv2.findContours(result_rgb, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # Сами структуры контуров хранятся в начальном элементе возвращаемого значения:
    contours = contours[0]

    # Их, кстати, может и не быть:
    if contours:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Третий аргумент — это индекс контура, который мы хотим вывести. Мы хотим самый большой.
        # Вывести все можно, передав -1 вместо 0:
        cv2.drawContours(numpix, contours, -1, (255, 0, 0), 2)

        # Получаем прямоугольник, обрамляющий наш контур:
        (x, y, w, h) = cv2.boundingRect(contours[0])

        # И выводим его:
        cv2.rectangle(result_rgb, (x, y), (x + w, y + h), (0, 255, 0), 1)


    cv2.imshow('mask', result_rgb)
    cv2.imshow('result', numpix)
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()