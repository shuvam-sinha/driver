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
        for i in reader:
            print (i["user_id"], i["name"], i["start_time"], i["end_time"], i["num_short"], i["num_medium"], i["num_long"])


if __name__ == "__main__":
    filename = os.environ['HOME'] + "/data/driver_data.csv"
    # readRecord1(filename)
    readRecord2(filename)
