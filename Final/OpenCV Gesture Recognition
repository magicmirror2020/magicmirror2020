import cv2
import math
import webbrowser
import json
import requests
import time
requests.adapters.DEFAULT_RETRIES=10

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
font = cv2.FONT_HERSHEY_SIMPLEX
line = cv2.LINE_AA

mode = 10

# Gesture Arrays
zero_array = []
one_array = []
two_array = []
three_array = []
four_array = []
five_array = []

# Mirror Commands
screen_refresh = "http://192.168.0.16:8080/api/refresh"
screen_brightness = "http://192.168.0.16:8080/api/brightness/100" # 10-200
toggle_fullscreen = "http://192.168.0.16:8080/api/togglefullscreen" # switches between windowed and fullscreen views on pi screen
hide_module = "http://192.168.0.16:8080/api/modules/clock/hide" # replace 'clock' with module names
show_module = "http://192.168.0.16:8080/api/modules/clock/show"
hide_all = "http://192.168.0.16:8080/api/modules/all/hide" # mirror mode
show_all = "http://192.168.0.16:8080/api/modules/all/show" # module mode
next_page = "http://192.168.0.16:8080/api/notification/PAGE_INCREMENT" # pages module
previous_page = "http://192.168.0.16:8080/api/notification/PAGE_DECREMENT"

# News module commands - located here https://github.com/bugsounet/MMM-News
news_previous = "http://192.168.0.16:8080/api/notification/NEWS_PREVIOUS"
news_next = "http://192.168.0.16:8080/api/notification/NEWS_NEXT"
news_detail = "http://192.168.0.16:8080/api/notification/NEWS_DETAIL"
news_close = "http://192.168.0.16:8080/api/notification/NEWS_DETAIL_CLOSE"
news_scrolldown = "http://192.168.0.16:8080/api/notification/NEWS_DETAIL_SCROLLDOWN"
# news_scrollup = "http://192.168.0.16:8080/api/notification/NEWS_DETAIL_SCROLLUP"

# Spotify module commands - located here https://github.com/eouia/MMM-Spotify
# spotify_pause = "http://192.168.0.16:8080/api/notification/SPOTIFY_PAUSE"
# spotify_play = "http://192.168.0.16:8080/api/notification/SPOTIFY_PLAY"
spotify_toggle = "http://192.168.0.16:8080/api/notification/SPOTIFY_TOGGLE" # toggles pause/play
spotify_next = "http://192.168.0.16:8080/api/notification/SPOTIFY_NEXT"
spotify_previous = "http://192.168.0.16:8080/api/notification/SPOTIFY_PREVIOUS"
spotify_shuffle = "http://192.168.0.16:8080/api/notification/SPOTIFY_NEXT"
spotify_repeat = "http://192.168.0.16:8080/api/notification/SPOTIFY_PREVIOUS"
# spotify_search = curl -X POST http://192.168.0.16:8080/api/notification/SPOTIFY_SEARCH -H 'content-type: application/json' -d '{"type": "artist,playlist", "query": "michael+jackson", "random": "false"}'

ross_play = "http://192.168.0.16:8080/api/notification/ROSS_PLAY_VIDEO"
ross_pause = "http://192.168.0.16:8080/api/notification/ROSS_PAUSE_VIDEO"
show_forecast = "http://192.168.0.16:8080/api/modules/weatherforecast/show" # toggling weather forecast
hide_forecast = "http://192.168.0.16:8080/api/modules/weatherforecast/hide" # toggling weather forecast
r = requests.get(hide_forecast, timeout=30)
response = json.loads(r.text)

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
    # can make concise later hard code for now
    if l == 1:
        if arearatio < 3:
            cv2.putText(frame, 'Waiting', (0, 50), font, 2, (255, 255, 255), 3, cv2.LINE_AA)
            # print(arearatio)
        else:
            if  3 < arearatio < 17.5:
                l == 0
                zero_array.append(0)
                # print(zero_array)
                if len(zero_array) == 30:
                    mode = 0
                    zero_array.clear()
                    time.sleep(1)
            else:
                one_array.append(l)
                #print(one_array)
                if len(one_array) == 30:
                    mode = 1
                    one_array.clear()
                    time.sleep(1)
    if l == 2:
        two_array.append(l)
        #print(two_array)
        if len(two_array) == 30:
            mode = 2
            two_array.clear()
            time.sleep(1)
    if l == 3:
        three_array.append(l)
        #print(three_array)
        if len(three_array) == 30:
            mode = 3
            three_array.clear()
            time.sleep(1)
    if l == 4:
        four_array.append(l)
        #print(four_array)
        if len(four_array) == 30:
            mode = 4
            four_array.clear()
            time.sleep(1)
    if l == 5:
        five_array.append(l)
        #print(five_array)
        if len(five_array) == 30:
            mode = 5
            five_array.clear()
            time.sleep(1)

    if mode == 1:
        # print("WEATHER")
        if len(zero_array) == 29:
            mode = 10
        if len(one_array) == 29:
            r = requests.get(show_forecast, timeout=30)
            response = json.loads(r.text)
            one_array.clear()
        if len(two_array) == 29:
            r = requests.get(hide_forecast, timeout=30)
            response = json.loads(r.text)
            two_array.clear()

    if mode == 2:
        # print("NEWS")
        if len(zero_array) == 100:
            mode = 10
        if len(one_array) == 29:
            r = requests.get(news_detail, timeout=30)
            response = json.loads(r.text)
            one_array.clear()
        if len(two_array) == 29:
            r = requests.get(news_scrolldown, timeout=30)
            response = json.loads(r.text)
            two_array.clear()
        if len(three_array) == 29:
            r = requests.get(news_close, timeout=30)
            response = json.loads(r.text)
            three_array.clear()
        if len(four_array) == 29:
            r = requests.get(news_next, timeout=30)
            response = json.loads(r.text)
            four_array.clear()
        if len(five_array) == 29:
            r = requests.get(news_previous, timeout=30)
            response = json.loads(r.text)
            five_array.clear()

    if mode == 3:
        # print("SPOTIFY")
        if len(zero_array) == 29:
            mode = 10
        if len(one_array) == 29:
            r = requests.get(spotify_toggle, timeout=30)
            response = json.loads(r.text)
            one_array.clear()
        if len(two_array) == 29:
            r = requests.get(spotify_next, timeout=30)
            response = json.loads(r.text)
            two_array.clear()
        if len(three_array) == 29:
            r = requests.get(spotify_previous, timeout=30)
            response = json.loads(r.text)
            three_array.clear()
        if len(four_array) == 29:
            r = requests.get(spotify_shuffle, timeout=30)
            response = json.loads(r.text)
            four_array.clear()
        if len(five_array) == 29:
            r = requests.get(spotify_repeat, timeout=30)
            response = json.loads(r.text)
            five_array.clear()

    if mode == 4:
        # print("2ND PAGE")
        if len(zero_array) == 29:
            mode = 10
        if len(one_array) == 29:
            r = requests.get(next_page, timeout=30)
            response = json.loads(r.text)
            one_array.clear()
        if len(two_array) == 29:
            r = requests.get(previous_page, timeout=30)
            response = json.loads(r.text)
            two_array.clear()
        if len(three_array) == 29:
            r = requests.get(ross_play, timeout=30)
            response = json.loads(r.text)
            three_array.clear()
        if len(four_array) == 29:
            r = requests.get(ross_pause, timeout=30)
            response = json.loads(r.text)
            four_array.clear()

    if mode == 5:
        # print("SCREEN")
        if len(zero_array) == 29:
            mode = 10
        if len(one_array) == 29:
            r = requests.get(hide_all, timeout=30)
            response = json.loads(r.text)
            one_array.clear()
        if len(two_array) == 29:
            r = requests.get(show_all, timeout=30)
            response = json.loads(r.text)
            two_array.clear()

    cv2.imshow('frame', frame)
    cv2.imshow('Mask', mask)
    if cv2.waitKey(2) & 0xFF == 27:
        break
