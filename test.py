import cv2
import config
import utils


ball_color = config.get_color_range("ball")
basket_color = config.get_color_range("purple")

cap = cv2.VideoCapture(0)

while cap.isOpened():
    _, frame = cap.read()

    cv2.imshow("frame", frame)
    cv2.imshow("balls", utils.apply_color_mask(frame, ball_color))
    cv2.imshow("baskets", utils.apply_color_mask(frame, basket_color))

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
