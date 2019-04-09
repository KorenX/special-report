#!/usr/bin/env python

from threading import Thread
from special_report.app.app import app
from special_report.sensors.cameraHandler import IP_cam_get_image

HOST = "localhost"
PORT = 8080

CAMERAS = [("192.168.43.1", 8080)]


def start_sensors():
    # cameraHandler.video2frame()

    for camera in CAMERAS:
        t = Thread(target=IP_cam_get_image, 
                   kwargs={'url': "https://{ip}:{port}/shot.jpg".format(
                           ip=camera[0], port=camera[1])})

        t.start()


def main():
    print("Out first project!")
    start_sensors()

    print("Start server")
    app.run(host=HOST, port=PORT, debug=True)

    while True:
        pass


if __name__ == '__main__':
    main()