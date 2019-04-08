import os
import face_recognition
import image_loader

RELATIVE_PATH_TO_IMAGES = "../assets/images/"

class image_handler:
    def init(self):
        self.members = {}
        self.load_members()

    def handle_data(self, image):
        ''' brief handles the data from the camera and updates DB spaces

            :image: the image from the camera
        '''
        personIDs = self.find_persons_in_image(image)
        for personid in personIDs:
            self.send_data(personid)

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

    def send_data(self, personID):
        ''' brief updates the data in the DB with arrivals

            :personID: the person who has arrived
        '''
        pass #TODO : send the datarow to the occurrences DB

    def load_members(self):
        ''' brief initalization helper function for loading the members from the individual images
        '''
        for filename in os.listdir(RELATIVE_PATH_TO_IMAGES):
            if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
                image = face_recognition.load_image_file(RELATIVE_PATH_TO_IMAGES + filename)
                encoding = face_recognition.face_encodings(image)[0]
                name = filename.split('.')[0]
                self.members[name] = encoding

