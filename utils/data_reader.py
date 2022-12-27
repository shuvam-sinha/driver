#!/usr/bin/python3
import csv
import os
#read file, put all 7 compenents into different variables, print the variables


def readRecord1(filename):
    with open(filename, 'r') as csvfile:
        all_lines = csvfile.readlines()
        print(all_lines)
        for this_line in all_lines:
            print(this_line)
            tokens = this_line.split(',')

            user_name = tokens[0]
            name = tokens[1]
            start_time = tokens[2]
            end_time = tokens[3]
            num_short = tokens[4]
            num_medium = tokens[5]
            num_long = tokens[6]

            print ("User Name: ", user_name)
            print ("Name: ", name)
            print ("Start Time: ", start_time)
            print ("End Time: ", end_time)
            print ("Short: ", num_short)
            print ("Medium: ", num_medium)
            print ("Long: ", num_long)


def readRecord2(filename1):
    with open(filename1) as csvfile:
        reader = csv.DictReader(csvfile)
        allRows = []
        for row in reader:
            allRows.append(row)
        return allRows


def getAnalytics1(userID, desiredID):
    if userID == desiredID:
        print (row["user_id"], row["name"], row["start_time"], row["end_time"], row["num_short"], row["num_medium"], row["num_long"])


def getAnalytics(userID, allRows):
    # Subset of rows that match userID
    desired_rows = []
    for row in allRows:
        if row["user_id"] == userID:
            desired_rows.append(row)
    return desired_rows

if __name__ == "__main__":
    filename = os.environ['HOME'] + "/data/driver_data.csv"
    #readRecord1(filename)
    rows = readRecord2(filename)
    filteredRows = getAnalytics("shuvam_sinha", rows)
    for row in filteredRows:
        print (row["user_id"], row["name"], row["start_time"], row["end_time"], row["num_short"], row["num_medium"], row["num_long"])
    