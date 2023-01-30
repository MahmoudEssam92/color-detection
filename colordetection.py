import cv2                                              # We use this to import opencv package
import numpy as np
def empty(a):
    pass

#----------------------------------------------- This a function to join images together ---------------------------------------------------- #

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


#----------------------------------------------- This a function to join images together ---------------------------------------------------- #


path = 'remote.jpg.jpg'

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Hue min", "TrackBars", 0, 179, empty)
cv2.createTrackbar("Hue max", "TrackBars", 34, 179, empty)
cv2.createTrackbar("Sat min", "TrackBars", 96, 255, empty)
cv2.createTrackbar("Sat max", "TrackBars", 250, 255, empty)
cv2.createTrackbar("Value min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Value max", "TrackBars", 255, 255, empty)
while True:
    img = cv2.imread(path)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue max", "TrackBars")
    S_min = cv2.getTrackbarPos("Sat min", "TrackBars")
    S_max = cv2.getTrackbarPos("Sat max", "TrackBars")
    v_min = cv2.getTrackbarPos("Value min", "TrackBars")
    v_max = cv2.getTrackbarPos("Value max", "TrackBars")
    print(h_min,h_max,S_min,S_max,v_min,v_max)
    lower = np.array([h_min,S_min,v_min])
    upper = np.array(([h_max,S_max,v_max]))
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResults = cv2.bitwise_and(img, img, mask=mask)


    imgStack = stackImages(0.8, ([img,imgHSV], [mask,imgResults]))
    cv2.imshow("StackedImages", imgStack)
    cv2.waitKey(1)

