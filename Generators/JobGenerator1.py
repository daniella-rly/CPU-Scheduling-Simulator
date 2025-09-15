import random as rand
import numpy as num
import matplotlib.pyplot as plt
import csv
import numpy as np

numJobs = 1500
mean = 150
mean2 = 75
stdDev = 20
jobTime = [0]*numJobs
jobSize = [0]*numJobs
for x in range(numJobs):
    jobSize[x] = max(1, int(rand.gauss(mean, stdDev)))
    arrTime = max(0, int(rand.gauss(mean2, stdDev)))
    jobTime[x] = arrTime
    if(x>=1):
        jobTime[x] = jobTime[x-1]+jobTime[x]

with open('job1.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # Write header row
    writer.writerow(["Index", "Arrival Time", "Job Size"])

    # Write data rows
    for x in range(numJobs):
        writer.writerow([x, jobTime[x], jobSize[x]])

print("CSV file processed successfully.")

   
