from cameraAnalysis.ImageAnalyzer import ImageAnalyzer as IA
import cameraAnalysis.camera as cam
import cv2
import time
from datetime import datetime

RPI_PHOTO_PATH = "RPi-camphoto.jpg"

# Using PiCamera to take a picture
# Image is stored as the 'RPi-camphoto.jpg' file
cam.TakeAShot()

# Using ImageAnalyzer class to calculate average rgb of an image
ia = IA()
ia.PassImage(RPI_PHOTO_PATH)
rgbs = ia.GetAverageRGB()

#Face detection
image = cv2.imread(RPI_PHOTO_PATH)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

# Write calculated average rgb to the text file 'rgbs.txt'
with open("lora-comm/dragino_lora_app/read.txt", "w", encoding="UTF-8") as file:
    for key, val in rgbs.items():
        file.write(f"{key}= {val} ")
        
with open("lora-comm/dragino_lora_app/read2.txt", "w", encoding="UTF-8") as file:
    file.write(f"Data: {datetime.now()}, Liczba twarzy: {len(faces)}\n")
