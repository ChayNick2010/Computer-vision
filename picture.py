import pyautogui
import time
import numpy as np
import cv2
import imutils
print('waiting for 2 seconds...')
time.sleep(2)

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

left = nfs_window_location[0]
top = nfs_window_location[1]+nfs_window_location[3]

window_resolution = (640, 480)

window = (left, top, left+window_resolution[0], top+window_resolution[1])
print(type(left), type(top), window_resolution[0], window_resolution[1])
cv2.namedWindow('result')

ranges = {
    'min_h1': {'current': 20, 'max': 180},
    'max_h1': {'current': 40, 'max': 180},
}


def trackbar_handler(name):
    def handler(x):
        global ranges
        ranges[name]['current'] = x

    return handler


for name in ranges:
    cv2.createTrackbar(name,
                       'result',
                       ranges[name]['current'],
                       ranges[name]['max'],
                       trackbar_handler(name)
                       )

while True:

    pix = pyautogui.screenshot(region=(int(left), int(top), window_resolution[0], window_resolution[1]))
    numpix = cv2.cvtColor(np.array(pix), cv2.COLOR_RGB2BGR)
    numpix = numpix[window_resolution[1]//2:, :, :]
    numpix_hsv = cv2.cvtColor(np.array(pix), cv2.COLOR_RGB2HSV)
    numpix_hsv = numpix_hsv[window_resolution[1]//2:, :, :]

    min_g = (58, 50, 0)
    max_g = (63, 255, 255)

    min_y = (25, 50, 50)
    max_y = (30, 255, 255)

    min_r1 = (0, 50, 0)
    max_r1 = (10, 255, 255)
    min_r2 = (170, 50, 0)
    max_r2 = (180, 255, 255)

    mask_g = cv2.inRange(numpix_hsv, min_g, max_g)
    mask_y = cv2.inRange(numpix_hsv, min_y, max_y)
    mask_r1 = cv2.inRange(numpix_hsv, min_r1, max_r1)
    mask_r2 = cv2.inRange(numpix_hsv, min_r2, max_r2)

    mask = cv2.bitwise_or(mask_g, mask_y)
    mask = cv2.bitwise_or(mask, mask_r1)
    mask = cv2.bitwise_or(mask, mask_r2)

    result = cv2.bitwise_and(numpix, numpix, mask=mask)

    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = contours[0]

    if contours:

        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        cv2.drawContours(result, contours, -1, (255, 0, 0), 1)

        for idx, c in enumerate(contours, start=0):
            (x, y, w, h) = cv2.boundingRect(contours[idx])

            cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 1)

            (x1, y1), radius = cv2.minEnclosingCircle(contours[idx])
            center = (int(x1), int(y1))
            radius = int(radius)

            X = result.shape[0]
            Y = result.shape[1]
            startP = (Y//2, X)

            cv2.circle(result, center, radius, (0, 255, 0), 1)
            cv2.line(result, startP, center, (0, 255, 0), 1)

    cv2.imshow('result', result)
    cv2.imshow('mask', mask)
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()