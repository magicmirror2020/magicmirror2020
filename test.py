import cv2

# 1= color, 0= grayscale, -1=alphachannels
img = cv2.imread('pic3.png', 1)
# print(img) = creates an array of rgb values

# img, start/end coordinate, color (bgr), thickness
# arrowedLine = arrow at end
# img = cv2.line(img, (0,0), (255,255), (0,0,255), 3)

cv2.imshow('image', img)
# 5000 = 5 seconds | 0 = window not close
k = cv2.waitKey(0)

# if the escape key is pressed close, if s save
if k==27:
    cv2.destroyAllWindows()
elif k==ord('s'):
    cv2.imwrite('pic3_copy.png', img)
    cv2.destroyAllWindows()
