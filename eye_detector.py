#!/usr/bin/python3
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pygame
from picamera2 import Picamera2, Preview, MappedArray


eye_detector = cv2.CascadeClassifier("/home/ssinha/Bluestamp_Project/haarcascade_eye.xml")


original_detect_time = time.time()
detect_time = original_detect_time
detection = [0]
timestamp = [0]

times_not_detected = 0

def draw_eyes(request):
    global detect_time
    global detection
    global times_not_detected
    
    this_second = int(time.time() - original_detect_time)
    if len(eyes) > 0:
        if timestamp[-1] != this_second:
            times_not_detected = 0
            detection.append(1)
            timestamp.append(this_second)
        detect_time = time.time()

    else:
        if timestamp[-1] != this_second:
            detection.append(0)
            timestamp.append(this_second)
            
    with MappedArray(request, "main") as m:
        for e in eyes:
            (x, y, w, h) = [c * n // d for c, n, d in zip(e, (w0, h0) * 2, (w1, h1) * 2)]
            cv2.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0, 0))


picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
config = picam2.create_preview_configuration(main={"size": (640, 480)},
                                      lores={"size": (320, 240), "format": "YUV420"})
picam2.configure(config)

(w0, h0) = picam2.stream_configuration("main")["size"]
(w1, h1) = picam2.stream_configuration("lores")["size"]
s1 = picam2.stream_configuration("lores")["stride"]
eyes = []
picam2.post_callback = draw_eyes

picam2.start()
flag = True


sound_file = ("/home/ssinha/Bluestamp_Project/Car_Honk_Sound_Effect.mp3")

pygame.mixer.init()
speaker_volume = 1
pygame.mixer.music.set_volume(speaker_volume)

start_time = time.monotonic()
while time.monotonic() - start_time < 45:
    buffer = picam2.capture_buffer("lores")
    grey = buffer[:s1 * h1].reshape((h1, s1))
    eyes = eye_detector.detectMultiScale(grey, 1.12, 15)
    
    current_time = time.time()
    if int(current_time) % 5 == 0 and flag:
        diff = current_time - detect_time
        if diff > 5:
            print ("Not attentive for,", int(diff), "seconds")
            flag = False
            if times_not_detected == 0:
                pygame.mixer.music.load("/home/ssinha/Bluestamp_Project/Alarm_sound_effect.mp3")
                pygame.mixer.music.play()
            elif times_not_detected == 1:
                pygame.mixer.music.load("/home/ssinha/Bluestamp_Project/Car_Honk_Sound_Effect.mp3")
                pygame.mixer.music.play()
            elif times_not_detected >= 2:
                pygame.mixer.music.load("/home/ssinha/Bluestamp_Project/PolicesirenSoundEffect.mp3")
                pygame.mixer.music.play()

                
            times_not_detected+=1
    elif int(current_time) % 5 != 0:
        flag = True
        
y = detection
x = timestamp
print ("Detection: ", y)
print ("Timestamp: ", x)
plt.bar(x, y)
plt.xlabel("Time")
plt.ylabel("Detection")
plt.title("Testing")
plt.show()
