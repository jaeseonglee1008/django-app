from django.conf import settings
import numpy as np
import cv2

def opencv_dface(path):
    img = cv2.imread(path, 1)

    if (type(img) is np.ndarray):
# check img size
        print(img.shape)

# resize width and height
        factor = 1
        if img.shape[1] > 640:
            factor = 640.0 / img.shape[1]
        elif img.shape[0] > 480:
            factor = 480.0 / img.shape[0]

        if factor != 1:
            w = img.shape[1] * factor
            h = img.shape[0] * factor
            img = cv2.resize(img, (int(w), int(h)))

        baseUrl = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
        # xml file as result of face and eye learned. data located in base URL(.media)
        face_cascade = cv2.CascadeClassifier(baseUrl+'haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(baseUrl+'haarcascade_eye.xml')

        # input img converted to gray
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # face detection with the adaboost cascade algorithm
        # scale factor 1.2, minNeighbor
        faces = face_cascade.detectMultiScale(gray, 1.4, 5)
        # draw the face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (94, 73, 52), 2)
            # set the frame again for eyes
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (219, 152, 52), 2)
        # overwrite result
        cv2.imwrite(path, img)

    else:
        print('Invalid input')
        print(path)
