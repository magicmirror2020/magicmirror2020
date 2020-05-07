import cv2
import math
import webbrowser

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
zero_array = []
one_array = []
two_array = []
three_array = []
four_array = []
five_array = []
font = cv2.FONT_HERSHEY_SIMPLEX
line = cv2.LINE_AA

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
        if arearatio < 2:
            cv2.putText(frame, 'Waiting', (0, 50), font, 2, (255, 255, 255), 3, cv2.LINE_AA)
            #print(arearatio)
        else:
            if arearatio < 17.5:
                l == 0
                cv2.putText(frame, '0', (0, 50), font, 2, (255, 255, 255), 3, line)
                zero_array.append(0)
                print(zero_array)
                if len(zero_array) == 30:
                    #webbrowser.open('http://google.com')
                    zero_array.clear()  # clears array so it can be used again
            else:
                cv2.putText(frame, '1', (0, 50), font, 2, (255, 255, 255), 3, line)
                one_array.append(l)
                print(one_array)
                if len(one_array) == 30:
                    #webbrowser.open('http://google.com')
                    one_array.clear()  # clears array so it can be used again
    if l == 2:
        cv2.putText(frame, '2', (0, 50), font, 2, (255, 255, 255), 3, line)
        two_array.append(l)
        print(two_array)
        if len(two_array) == 30:
            #webbrowser.open(http://192.168.0.16:8080/magicmirror/module/newsfeed/articlemoredetails)
            two_array.clear()  # clears array so it can be used again
    elif l == 3:
        cv2.putText(frame, '3', (0, 50), font, 2, (255, 255, 255), 3, line)
        three_array.append(l)
        print(three_array)
        if len(three_array) == 30:
            #webbrowser.open('http://google.com')
            three_array.clear()  # clears array so it can be used again
    elif l == 4:
        cv2.putText(frame, '4', (0, 50), font, 2, (255, 255, 255), 3, line)
        four_array.append(l)
        print(four_array)
        if len(four_array) == 30:
            #webbrowser.open('http://spotify.com')
            four_array.clear()  # clears array so it can be used again
    elif l == 5:
        cv2.putText(frame, '5', (0, 50), font, 2, (255, 255, 255), 3, line)
        five_array.append(l)
        print(five_array)
        if len(five_array) == 30:
            #webbrowser.open('http://google.com')
            five_array.clear()  # clears array so it can be used again
    # else:
    #     cv2.putText(frame, 'Waiting', (10, 50), font, 2, (255, 255, 255), 3, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    cv2.imshow('Mask', mask)
    if cv2.waitKey(2) & 0xFF == 27:
        break
### Pull
import json
import requests
import time
requests.adapters.DEFAULT_RETRIES=10

# -- newsfeed stuff
url_newsfeed = "http://192.168.0.16:8080/api/module/newsfeed/?apiKey=magic"

# -- newsfeed get list of commands
r = requests.get(url_newsfeed, timeout=30)
newsfeed_commands = json.loads(r.text)
print(newsfeed_commands)

print('\nNEWSFEED COMMANDS\n')
print("MODULE: {}".format(newsfeed_commands['module']))
for action in newsfeed_commands['actions']:
    print("\tCOMMAND: {}".format(action))

# -- newsfeed articlenext command
url_newsfeed_articlenext = "http://192.168.0.16:8080/api/module/newsfeed/articlenext/?apiKey=magic"
r = requests.get(url_newsfeed_articlenext, timeout=30)
response = json.loads(r.text)
print(response)

# -- ALERT TEST
# -- show alert
url_alert_showalert = "http://192.168.0.16:8080/api/module/alert/showalert?title=title&message=message&apiKey=magic"
r = requests.get(url_alert_showalert, timeout=30)
response = json.loads(r.text)
print(response)

# -- wait 10 seconds
time.sleep(10)

# -- hide alert
url_alert_hidealert = "http://192.168.0.16:8080/api/module/alert/hidealert?apiKey=magic"
r = requests.get(url_alert_hidealert, timeout=30)
response = json.loads(r.text)
print(response)

screen_refresh = "http://192.168.0.16:8080/api/refresh"
screen_brightness = "http://192.168.0.16:8080/api/brightness/100" # 10-200
toggle_fullscreen = "http://192.168.0.16:8080/api/togglefullscreen" # switches between windowed and fullscreen views
hide_module = "http://192.168.0.16:8080/api/modules/clock/hide" # replace 'clock' with module names
show_module = "http://192.168.0.16:8080/api/modules/clock/show"
hide_all = "http://192.168.0.16:8080/api/modules/all/hide" # mirror mode
show_all = "http://192.168.0.16:8080/api/modules/all/show" # module mode

# module located here https://github.com/eouia/MMM-Spotify
spotify_pause = "http://192.168.0.16:8080/api/notification/SPOTIFY_PAUSE"
spotify_play = "http://192.168.0.16:8080/api/notification/SPOTIFY_PLAY"
spotify_toggle = "http://192.168.0.16:8080/api/notification/SPOTIFY_TOGGLE" # toggles pause/play
spotify_next = "http://192.168.0.16:8080/api/notification/SPOTIFY_NEXT"
spotify_previous = "http://192.168.0.16:8080/api/notification/SPOTIFY_PREVIOUS"
spotify_shuffle = "http://192.168.0.16:8080/api/notification/SPOTIFY_NEXT"
spotify_repeat = "http://192.168.0.16:8080/api/notification/SPOTIFY_PREVIOUS"
# spotify_search = curl -X POST http://192.168.0.16:8080/api/notification/SPOTIFY_SEARCH -H 'content-type: application/json' -d '{"type": "artist,playlist", "query": "michael+jackson", "random": "false"}'
