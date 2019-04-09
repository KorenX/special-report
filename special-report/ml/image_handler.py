import os
import face_recognition
from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np

RELATIVE_PATH_TO_IMAGES = "../assets/images/"
DEFAULT_EMOTION = "neutral"

class image_handler:
    def init(self):
        self.members = {}
        self.load_members()
        detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'
        emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'
        self.face_detection = cv2.CascadeClassifier(detection_model_path)
        self.emotion_classifier = load_model(emotion_model_path, compile=False)
        self.EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

    def handle_data(self, image):
        ''' brief handles the data from the camera and updates DB spaces

            :image: the image from the camera
        '''
        personIDs = self.find_persons_in_image(image)
        emotions = self.get_emotions(image)

        dictionary = {}

        i = 0
        for personid in personIDs:
            if i < len(emotions):
                dictionary[personid] = emotions[i]
            else:
                dictionary[personid] = DEFAULT_EMOTION
            i += 1
        return dictionary


    def find_persons_in_image(self, image):
        ''' brief finds all person ids in the image

            :image: the image which may or may not have people

            :return: a list of the ids of people in the image
        '''
        codes = face_recognition.face_encodings(image)
        ids = []
        for code in codes:
            for member in self.members:
                if face_recognition.compare_faces(self.members[member], code)[0]:
                    ids.append(member)
                    break
        return ids

    def load_members(self):
        ''' brief initalization helper function for loading the members from the individual images
        '''
        for filename in os.listdir(RELATIVE_PATH_TO_IMAGES):
            if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
                image = face_recognition.load_image_file(RELATIVE_PATH_TO_IMAGES + filename)
                encoding = face_recognition.face_encodings(image)[0]
                name = filename.split('.')[0]
                self.members[name] = encoding

    def get_emotions(self, frame):
        ''' brief exports a list of emotions from the image

            :param frame: the image

            :return: the list of emotions
        '''
        frame = imutils.resize(frame, width=300)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                                     flags=cv2.CASCADE_SCALE_IMAGE)
        faces = sorted(faces, reverse=True,
                       key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))
        moods = []
        for face in faces:
            (fX, fY, fW, fH) = face
            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            preds = self.emotion_classifier.predict(roi)[0]

            maxi = 0
            e = DEFAULT_EMOTION
            for (i, (emotion, prob)) in enumerate(zip(self.EMOTIONS, preds)):
                if maxi < prob:
                    maxi = prob
                    e = emotion
            moods.append(e)
        return moods


