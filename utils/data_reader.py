#!/usr/bin/python3
import csv
import git
import time
from simple_term_menu import TerminalMenu
import matplotlib.pyplot as plt
import numpy as np

seconds_per_day = 86400

def get_git_root(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return git_root


def readRecords(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        allRows = []
        for row in reader:
            allRows.append(row)
        return allRows


def getAnalytics(userID, allRows, duration = None, start_hour = None, end_hour = None):
    # Get the list of filtered_rows based on start_time and end_time
    start_time = 0
    end_time = time.time()
    filteredRows = []
    if duration is None:
        filteredRows = allRows
    else:
        if duration.lower() == "a":
            start_time = end_time - seconds_per_day
        elif duration.lower() == "b":
            start_time = end_time - 7*seconds_per_day
        elif duration.lower() == "c":
            start_time = end_time - 30*seconds_per_day
        elif duration.lower() == "d":
            start_time = end_time - 365*seconds_per_day
    
        for row in allRows:
            cond1 = int(row['start_time']) >= start_time and int(row['end_time']) <= end_time
            cond2 = int(row['start_time']) <= start_time and int(row['end_time']) >= start_time
            cond3 = int(row['start_time']) <= end_time and int(row['end_time']) >= end_time
            if cond1 or cond2 or cond3:
                filteredRows.append(row)
    
    desired_rows = []
    for row in filteredRows:
        if row["user_id"] == userID:
            if start_hour is not None and end_hour is not None:
                cond1 = start_hour >= int(row['start_time']) % seconds_per_day and start_hour <= int(row['end_time']) % seconds_per_day
                cond2 = end_hour >= int(row['start_time']) % seconds_per_day and end_hour <= int(row['end_time']) % seconds_per_day
                cond3 = start_hour < int(row['start_time']) % seconds_per_day and end_hour > int(row['end_time']) % seconds_per_day
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


def getOption():
    options = ["[a] Previous Day", "[b] Previous Week", "[c] Previous Month", "[d] Previous Year", "[e] All time", "[x] Exit"]
    terminal_menu = TerminalMenu(options, title="Select a time range for metrics")
    menu_entry_index = terminal_menu.show()
    return options[menu_entry_index]


def createGraph(text, filteredTimeRows):
    print(text)
    short = []
    medium = []
    long = []
    count = []
    for iteration, thisTime in enumerate(filteredTimeRows):
        print("Hour: ", iteration)
        for row in thisTime:
            print (row["user_id"], row["name"], row["start_time"], row["end_time"], row["num_short"], row["num_medium"], row["num_long"])
        (totalShort, totalMedium, totalLong) = analyzeResults(thisTime)
        print("Short:", totalShort, "\nMedium:", totalMedium, "\nLong:", totalLong)
        short.append(totalShort)
        medium.append(totalMedium)
        long.append(totalLong)
        count.append(iteration)

    y_short = short
    y_medium = medium
    y_long = long
    x = count
    X_axis = np.arange(len(x))
    plt.figure(figsize=(15, 10))
    plt.bar(X_axis-0.4, y_short, 0.4, label = 'Short')
    plt.bar(X_axis, y_medium, 0.4, label = 'Medium')
    plt.bar(X_axis+0.4, y_long, 0.4, label = 'Long')
    plt.xticks(X_axis, x)
    plt.xlabel("Hour")
    plt.ylabel("Detection")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # Read the records
    filename = get_git_root('.') + "/data/driver_data.csv"
    rows = readRecords(filename)

    # Analytics across all time
    filteredAllRows = getAnalytics("shuvam_sinha", rows)
    print("All Data")
    for row in filteredAllRows:
        print (row["user_id"], row["name"], row["start_time"], row["end_time"], row["num_short"], row["num_medium"], row["num_long"])
    (totalShort, totalMedium, totalLong) = analyzeResults(filteredAllRows)
    print("Short:", totalShort, "\nMedium:", totalMedium, "\nLong:", totalLong)

    # Analytics within a time range    
    isRun = True
    text = ""
    letter = ""
    while isRun:
        filteredTimeRows = []
        myOption = getOption()
        print(f"You have selected {myOption}!")
        if myOption == "[a] Previous Day":
            for i in range(0, 24):
                filteredTimeRows.append(getAnalytics("shuvam_sinha", rows, "a", i*3600, (i+1)*3600-1))
            createGraph(myOption, filteredTimeRows)
        elif myOption == "[b] Previous Week":
            for i in range(0, 24):
                filteredTimeRows.append(getAnalytics("shuvam_sinha", rows, "b", i*3600, (i+1)*3600-1))
            createGraph(myOption, filteredTimeRows)
        elif myOption == "[c] Previous Month":
            for i in range(0, 24):
                filteredTimeRows.append(getAnalytics("shuvam_sinha", rows, "c", i*3600, (i+1)*3600-1))
            createGraph(myOption, filteredTimeRows)
        elif myOption == "[d] Previous Year":
            for i in range(0, 24):
                filteredTimeRows.append(getAnalytics("shuvam_sinha", rows, "d", i*3600, (i+1)*3600-1))
            createGraph(myOption, filteredTimeRows)
        elif myOption == "[e] All time":
            for i in range(0, 24):
                filteredTimeRows.append(getAnalytics("shuvam_sinha", rows, "e", i*3600, (i+1)*3600-1))
            createGraph(myOption, filteredTimeRows)
        elif myOption == "[x] Exit":
            isRun = False
