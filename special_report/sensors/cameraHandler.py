import cv2
import requests
import numpy as np
import base64
# receive
# global_variables
delay = 100
# server_url = "http://specialreport.pythonanywhere.com/add"
server_url = "http://localhost:8080/photo"


def video2frame():
    video = cv2.VideoCapture(0)

    while True:
        success, image = video.read()
        cv2.imwrite("frame.jpg", image)  # save frame as JPEG file
        with open("frame.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            requests.post(server_url, encoded_string)
        key = cv2.waitKey(delay)
        if key == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()


def IP_cam_get_image(url):
    while True:
        image_resp = requests.get(url, verify=False)
        image_arr = np.array(bytearray(image_resp.content), dtype=np.uint8)
        image = cv2.imdecode(image_arr, -1)
        cv2.imwrite("frame.jpg", image)  # save frame as JPEG file
        with open("frame.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            requests.post(server_url, encoded_string)
        # cv2.imshow("Adva's cam", image)
        key = cv2.waitKey(delay)
        if key == ord('q'):
            break
