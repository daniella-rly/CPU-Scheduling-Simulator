import random as rand
import numpy as np
import matplotlib.pyplot as plt
import csv

numJobs = 1500
randNum=0
jobTime = [0]*1500
jobSize = [0]*1500

for x in range(numJobs):
    arrTime = int (rand.gauss(75,20))
    jobTime[x] = arrTime
    if (x>=1):
        jobTime[x] = jobTime[x-1] + jobTime[x]
    randNum = int (100*(rand.random()))
    if (randNum > 80): # large jobs, mean runtime of 250 std dev 15
        jobSize[x] = int (rand.gauss(50,10))
    if (randNum < 80):
        jobSize[x] = int (rand.gauss(250,15))

with open('Job2.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # Write header row
    writer.writerow(["Index", "Arrival Time", "Job Size"])

    # Write data rows
    for x in range(numJobs):
        writer.writerow([x, jobTime[x], jobSize[x]])

print("CSV file processed successfully.")
