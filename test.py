import cv2
import config
import utils


try:
    ball_color = config.get_color_range("ball")
except KeyError:
    exit("Ball color has not been thresholded, run threshold.py")

try:
    basket_color = config.get_color_range("purple")
except KeyError:
    exit("Purple color has not been thresholded, run threshold.py")

cap = cv2.VideoCapture(0)

while cap.isOpened():
    _, frame = cap.read()

    ball_mask = utils.apply_color_mask(frame, ball_color)
    basket_mask = utils.apply_color_mask(frame, basket_color)

    contours, hierarchy = cv2.findContours(ball_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    circles = map(cv2.minEnclosingCircle, contours)
    circles = sorted(circles, key = lambda circle: circle[1])

    if len(circles):
        biggest_circle = circles[-1]
        (x, y), radius = biggest_circle
        cv2.circle(frame, (int(x), int(y)), int(radius), utils.get_color_range_mean(ball_color), 5)

    cv2.imshow("frame", frame)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
