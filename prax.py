import cv2

try: 
    f = open("config.txt", "r")
    line = f.readline()
    values = [int(item) for item in line.split(":")[1].split(",")]
    hsv_min = values[:3]
    hsv_max = values[3:]
    f.close()

except FileNotFoundError:
    hsv_min = [0, 0, 0]
    hsv_max = [179, 255, 255]

def set_h_min(value):
    hsv_min[0] = value
def set_h_max(value):
    hsv_max[0] = value

def set_s_min(value):
    hsv_min[1] = value
def set_s_max(value):
    hsv_max[1] = value

def set_v_min(value):
    hsv_min[2] = value
def set_v_max(value):
    hsv_max[2] = value

cv2.namedWindow("hsv")
cv2.createTrackbar("h_min", "hsv", hsv_min[0], 179, set_h_min)
cv2.createTrackbar("h_max", "hsv", hsv_max[0], 179, set_h_max)
cv2.createTrackbar("s_min", "hsv", hsv_min[1], 255, set_s_min)
cv2.createTrackbar("s_max", "hsv", hsv_max[1], 255, set_s_max)
cv2.createTrackbar("v_min", "hsv", hsv_min[2], 255, set_v_min)
cv2.createTrackbar("v_max", "hsv", hsv_max[2], 255, set_v_max)


cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Get BGR frame from camera
    _, frame = cap.read()
    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("hsv", hsv)
    # Apply color mask
    mask = cv2.inRange(hsv, tuple(hsv_min), tuple(hsv_max))
    cv2.imshow("mask", mask)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

f = open("config.txt", "w")
f.write("Ball: ")
f.write(",".join([str(item) for item in (hsv_min + hsv_max)]))
f.write("\n")
f.close()











