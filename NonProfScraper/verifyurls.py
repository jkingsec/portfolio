import requests
import csv
import sys

with open(sys.argv[1], newline='', mode='r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        try:
            requests.get(row[3])
        except requests.exceptions.ConnectionError:
            print(f"{row[0]} not reachable")
