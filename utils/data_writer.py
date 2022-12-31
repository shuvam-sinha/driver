#!/usr/bin/python3
import argparse
import csv
import git
import time
import os
from random import randrange


def get_git_root(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return git_root


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='detector',
        description='Eye detection'
    )

    parser.add_argument('-u', '--username', required=True)
    args = parser.parse_args()
    # print(args.username)
    # print(args.name)

    startTime = time.time()
    time.sleep(10)
    endTime = time.time()
    numShort = randrange(5)
    numMedium = randrange(5)
    numLong = randrange(5)

    addRecord(args.username, startTime, endTime, numShort, numMedium, numLong)

