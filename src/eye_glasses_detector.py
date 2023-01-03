#!/usr/bin/python3
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pygame
import git
import argparse
import csv
import os
from picamera2 import Picamera2, Preview, MappedArray

timestamp = [0]
detection = [0]

def get_git_root(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return git_root


def draw_eyes(request):
    global detect_time
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
            
            
def addRecord(userId, startTime, endTime, numShort, numMedium, numLong):
    if userId is None:
        return None
    
    filename = get_git_root('.') + "/data/driver_data.csv"
    with open(filename, 'a') as csvFile:
        fieldnames = ['user_id', 'start_time', 'end_time', 'num_short', 'num_medium', 'num_long']
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        if os.path.getsize(filename) == 0:
            writer.writeheader()

        data = {
            "user_id": userId,
            "start_time": int(startTime),
            "end_time": int(endTime),
            "num_short": numShort,
            "num_medium": numMedium,
            "num_long": numLong
        }

        writer.writerow(data)


def runEyeDetector(eye_detector, userId):
    global times_not_detected
    global detect_time
    global original_detect_time
    global w0
    global h0
    global w1
    global h1
    global eyes
    
    picam2 = Picamera2()
    picam2.start_preview(Preview.QTGL)
    config = picam2.create_preview_configuration(
        main={"size": (640, 480)},
        lores={"size": (320, 240), "format": "YUV420"}
    )
    picam2.configure(config)
    (w0, h0) = picam2.stream_configuration("main")["size"]
    (w1, h1) = picam2.stream_configuration("lores")["size"]
    s1 = picam2.stream_configuration("lores")["stride"]
    eyes = []

    pygame.mixer.init()
    speaker_volume = 1
    pygame.mixer.music.set_volume(speaker_volume)

    times_not_detected = 0
    original_detect_time = time.time()
    detect_time = original_detect_time
    
    picam2.post_callback = draw_eyes
    picam2.start()
    flag = True

    start_time = time.monotonic()
    
    numShort = 0
    numMedium = 0
    numLong = 0
    while time.monotonic() - start_time < 30:
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
                    pygame.mixer.music.load(root_location + "/resources/Alarm_sound_effect.mp3")
                    pygame.mixer.music.play()
                    numShort+=1
                elif times_not_detected == 1:
                    pygame.mixer.music.load(root_location + "/resources/Car_Honk_Sound_Effect.mp3")
                    pygame.mixer.music.play()
                    numMedium+=1
                elif times_not_detected >= 2:
                    pygame.mixer.music.load(root_location + "/resources/PolicesirenSoundEffect.mp3")
                    pygame.mixer.music.play()
                    numLong+=1

                    
                times_not_detected+=1
        elif int(current_time) % 5 != 0:
            flag = True

    picam2.stop()
    endTime = time.time()        

    addRecord(userId, original_detect_time, endTime, numShort, numMedium, numLong)

    y = detection
    x = timestamp
    print ("Detection: ", y)
    print ("Timestamp: ", x)
    plt.bar(x, y)
    plt.xlabel("Time")
    plt.ylabel("Detection")
    plt.title("Testing")
    plt.show()


if __name__ == "__main__":
        # Initialization
    userId = input("Enter user id: ")
    root_location = get_git_root('.')
    
    type_of_eyes = input("Are you wearing glasses right now? (y/n)")
    if type_of_eyes.lower()=='n':
        eye_detector = cv2.CascadeClassifier(root_location + "/resources/haarcascade_eye.xml")
    else:    
        eye_detector = cv2.CascadeClassifier(root_location + "/resources/haarcascade_eye_tree_eyeglasses.xml")

    runEyeDetector(eye_detector, userId)