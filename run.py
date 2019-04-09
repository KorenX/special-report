#!/usr/bin/env python

from threading import Thread
from special_report.telegram.telegramBot import start_bot
from special_report.sensors.cameraHandler import IP_cam_get_image
from special_report.app.app import app
from special_report.db.SpecialReport import FillDB, CreateDB

HOST = "localhost"
PORT = 8080

CAMERAS = [("192.168.43.1", 8080)]

threads = []

def start_sensors():
        # ImgRcv.video2frame()

        for camera in CAMERAS:
                t = Thread(target=IP_cam_get_image, kwargs={
                        'url': "https://{ip}:{port}/shot.jpg".format(
                                ip=camera[0], port=camera[1]
                        )})

                t.start()
                threads.append(t)


def main():
    start_sensors()

    t = Thread(target=start_bot, daemon=True)
    t.start()
#     threads.append(t)

    print("Out first project!")
    app.run(host=HOST, port=PORT, debug=True, use_reloader=False)

    while True:
        pass


if __name__ == '__main__':
    CreateDB()
    FillDB()
    main()