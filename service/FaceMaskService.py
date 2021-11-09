import os
import cv2
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model


class FaceMaskService:
    @staticmethod
    def detect(photo):
        prototxtPath = os.path.sep.join(["Face-Mask-Detection", "face_detector", "deploy.prototxt"])
        weightsPath = os.path.sep.join(["Face-Mask-Detection", "face_detector",
                                        "res10_300x300_ssd_iter_140000.caffemodel"])
        net = cv2.dnn.readNet(prototxtPath, weightsPath)
        model = load_model(os.path.sep.join(["Face-Mask-Detection","mask_detector.model"]))
        blob = cv2.dnn.blobFromImage(photo, 1.0, (300, 300),
                                     (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the detection
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the confidence is
            # greater than the minimum confidence
            if confidence > 0.5:
                (h, w) = photo.shape[:2]
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # ensure the bounding boxes fall within the dimensions of
                # the frame
                (startX, startY) = (max(0, startX), max(0, startY))
                (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

                # extract the face ROI, convert it from BGR to RGB channel
                # ordering, resize it to 224x224, and preprocess it
                face = photo[startY:endY, startX:endX]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face = cv2.resize(face, (224, 224))
                face = img_to_array(face)
                face = preprocess_input(face)
                face = np.expand_dims(face, axis=0)

                # pass the face through the model to determine if the face
                # has a mask or not
                (mask, withoutMask) = model.predict(face)[0]
                return mask > withoutMask
        return False
