import os
import face_recognition

RELATIVE_PATH_TO_IMAGES = "../assets/images/"

def load():
    members = {}
    for filename in os.listdir(RELATIVE_PATH_TO_IMAGES):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            image = face_recognition.load_image_file(RELATIVE_PATH_TO_IMAGES + filename)
            encoding = face_recognition.face_encodings(image)[0]
            name = filename.split('.')[0]
            members[name] = encoding
    send_members(members)

def send_members(members):
    if members:
        for name in members:
            print(name, members[name])
    else:
        print("no data!")

if __name__ == "__main__":
    load()