import cv2
import math
import webbrowser

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
open_array = []
three_array = []

mode = 0

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # flips camera horizontally
    cv2.rectangle(frame, (300, 300), (100, 100), (255, 255, 255), 2)  # roi rectangle
    roi = frame[100:300, 100:300]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (35, 35), 0)
    _, mask = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # mask with otsu's binarization

    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # finds contours
    cnt = max(contours, key=lambda x: cv2.contourArea(x))  # find contours in the max area (hand)
    # approximates the contour
    temp = 0.0005 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, temp, True)

    hull = cv2.convexHull(cnt)  # convex hull around hand
    # define area of hull and area of hand
    areahull = cv2.contourArea(hull)
    areacnt = cv2.contourArea(cnt)
    arearatio = ((areahull - areacnt) / areacnt) * 100  # percentage of area not covered by hand

    # find defects in convex hull
    hull = cv2.convexHull(approx, returnPoints=False)
    defects = cv2.convexityDefects(approx, hull)
    # l = number of defects
    l = 0
    # finding number of defects
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(approx[s][0])
        end = tuple(approx[e][0])
        far = tuple(approx[f][0])
        pt = (100, 180)
        # finds length of sides of triangle
        a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
        c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
        s = (a + b + c) / 2
        ar = math.sqrt(s * (s - a) * (s - b) * (s - c))
        # distance between point and convex hull
        d = (2 * ar) / a
        # cosine rule
        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57
        # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
        if angle <= 90 and d > 30:
            l += 1
            cv2.circle(roi, far, 3, [255, 0, 0], -1)
        # draw lines around hand
        cv2.line(roi, start, end, [0, 255, 0], 2)

    l += 1  # need or else count is down 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    if l == 5:
        open_array.append(l)
        print(open_array)
        if len(open_array) == 26:
            mode = 1
            if mode == 1:
                webbrowser.open('http://spotify.com')
                open_array.clear()  # clears array so it can be used again
                mode = 0  # needs to be last

    else:
        cv2.putText(frame, 'Nothing', (10, 50), font, 2, (255, 255, 255), 3, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    cv2.imshow('Mask', mask)
    k = cv2.waitKey(2) & 0xFF
    if k == 27:
        break

    if l == 1:
        if areacnt < 5000:  # adjust this for how much mask in frame
            cv2.putText(frame, 'Waiting for gesture', (0, 50), font, 2, (255, 255, 255), 3, cv2.LINE_AA)
        else:
            if arearatio < 17.5:
                cv2.putText(frame, '0', (0, 50), font, 2, (255, 255, 255), 3, cv2.LINE_AA)
            else:
                cv2.putText(frame, '1', (0, 50), font, 2, (255, 255, 255), 3, cv2.LINE_AA)
    elif l == 2:
        cv2.putText(frame, '2', (0, 50), font, 2, (255, 255, 255), 3, cv2.LINE_AA)
    elif l == 3:
        cv2.putText(frame, '3', (0, 50), font, 2, (255, 255, 255), 3, cv2.LINE_AA)
    elif l == 4:
        cv2.putText(frame, '4', (0, 50), font, 2, (255, 255, 255), 3, cv2.LINE_AA)
