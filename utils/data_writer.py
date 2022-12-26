#!/usr/bin/python3
import argparse
import csv
import os
import time
from random import randrange


def addRecord(userId, name, startTime, endTime, numShort, numMedium, numLong):
    if userId is None or name is None:
        return None

    filename = os.environ['HOME'] + "/data/driver_data.csv"
    # print(filename)
    with open(filename, 'a') as csvFile:
        fieldnames = ['user_id', 'name', 'start_time', 'end_time', 'num_short', 'num_medium', 'num_long']
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        if os.path.getsize(filename) == 0:
            writer.writeheader()

        data = {
            "user_id": userId,
            "name": name,
            "start_time": int(startTime),
            "end_time": int(endTime),
            "num_short": numShort,
            "num_medium": numMedium,
            "num_long": numLong
        }

        writer.writerow(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='detector',
        description='Eye detection'
    )

    parser.add_argument('-u', '--username')
    parser.add_argument('-n', '--name')
    args = parser.parse_args()
    # print(args.username)
    # print(args.name)

    startTime = time.time()
    time.sleep(10)
    endTime = time.time()
    numShort = randrange(5)
    numMedium = randrange(5)
    numLong = randrange(5)

    addRecord(args.username, args.name, startTime, endTime, numShort, numMedium, numLong)

