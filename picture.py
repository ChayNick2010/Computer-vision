import cv2

cap = cv2.VideoCapture(0)

cv2.namedWindow('result')


while True:
    ret, frame = cap.read()

