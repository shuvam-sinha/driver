#!/usr/bin/python3
import csv
import os


seconds_per_day = 86400

def readRecords(filename1):
    with open(filename1) as csvfile:
        reader = csv.DictReader(csvfile)
        allRows = []
        for row in reader:
            allRows.append(row)
        return allRows


# def getAnalytics2(userID, allRows):
#     # Subset of rows that match userID
#     desired_rows = []
#     for row in allRows:
#         if row["user_id"] == userID:
#             desired_rows.append(row)
#     return desired_rows


def getAnalytics(userID, allRows, start_time = None, end_time = None):
    desired_rows = []
    for row in allRows:
        if row["user_id"] == userID:
            if start_time is not None and end_time is not None:
                cond1 = start_time >= int(row['start_time']) % seconds_per_day and start_time <= int(row['end_time']) % seconds_per_day
                cond2 = end_time >= int(row['start_time']) % seconds_per_day and end_time <= int(row['end_time']) % seconds_per_day
                cond3 = start_time < int(row['start_time']) % seconds_per_day and end_time > int(row['end_time']) % seconds_per_day
                cond = cond1 or cond2 or cond3
            else:
                cond = True

            if cond:
                desired_rows.append(row)
    return desired_rows

def analyzeResults(allRows):
    short_num = 0
    medium_num = 0
    long_num = 0
    for row in allRows:
        short_num += int(row["num_short"])
        medium_num += int(row["num_medium"])
        long_num += int(row["num_long"])
    return short_num, medium_num, long_num

if __name__ == "__main__":
    # Read the records
    filename = os.environ['HOME'] + "/data/driver_data.csv"
    rows = readRecords(filename)

    # Analytics across all time
    filteredAllRows = getAnalytics("shuvam_sinha", rows)
    for row in filteredAllRows:
        print (row["user_id"], row["name"], row["start_time"], row["end_time"], row["num_short"], row["num_medium"], row["num_long"])
    (totalShort, totalMedium, totalLong) = analyzeResults(filteredAllRows)
    print("Short:", totalShort, "\nMedium:", totalMedium, "\nLong:", totalLong)

    # Analytics within a time range
    filteredTimeRows = []
    for i in range(0, 24):
        filteredTimeRows.append(getAnalytics("shuvam_sinha", rows, i*3600, (i+1)*3600))

    for iteration, thisTime in enumerate(filteredTimeRows):
        print("Data: ", iteration)
        for row in thisTime:
            print (row["user_id"], row["name"], row["start_time"], row["end_time"], row["num_short"], row["num_medium"], row["num_long"])
        (totalShort, totalMedium, totalLong) = analyzeResults(thisTime)
        print("Short:", totalShort, "\nMedium:", totalMedium, "\nLong:", totalLong)

    