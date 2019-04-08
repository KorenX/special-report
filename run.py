#!/usr/bin/env python

from special_report.app.app import app

HOST = "localhost"
PORT = 8080


def main():
    print("Out first project!")
    app.run(host=HOST, port=PORT, debug=True)

    while True:
        pass


if __name__ == '__main__':
    main()