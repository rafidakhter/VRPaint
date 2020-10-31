import cv2
import numpy as np
import time


def paintOnAir(cords):
    for cord in cords:
        cv2.circle(imgOutput, (cord[0], cord[1]), 10, (0, 255, 0), cv2.FILLED)


def contourLocation(maskedImg):
    # function returns the coordinates of the green object

    cx, cy = 0, 0  # if not contours found then return 0
    contours, hierarchy = cv2.findContours(maskedImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >= 1000:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)

            cx = (x + (w // 2))
            cy = (y + (h // 2))

    return cx, cy


def maskImg(img):
    # takes the image and converts it to an HSV format
    # using the upper and lower threshold values of specific colour implement the mask
    # returns masked image

    greenMaskLimit = [57, 76, 0, 100, 255, 255]

    lower = np.array(greenMaskLimit[0:3])
    upper = np.array(greenMaskLimit[3:6])
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lower, upper)

    return mask


# fist make webcam object

def createVideoObject():
    cap = cv2.VideoCapture(0)  # webcam called at 0
    cap.set(3, 640)
    cap.set(4, 480)
    cap.set(10, 150)
    return cap


video = createVideoObject()
cords = []
sec = 0
while True:
    sucess, img = video.read()
    img = cv2.flip(img, 1)
    imgOutput = img.copy()
    maskedImg = maskImg(img)
    cx, cy = contourLocation(maskedImg)
    if cx != 0 and cy != 0:
        cords.append([cx, cy])
    paintOnAir(cords)
    print(sec)
    if sec % 10 == 0:
        if not cords:
            pass
        else:
            cords.pop(0)
    sec += 1

    cv2.imshow("Pint", imgOutput)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
