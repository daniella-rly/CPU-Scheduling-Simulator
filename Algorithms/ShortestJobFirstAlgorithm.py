##This code performs a scheduling algorithm called "Shortest Job First" on a list of jobs read from a CSV file.
##The algorithm prioritizes the jobs with the shortest processing time, and calculates various metrics such as
##response time and turn around time. The output is then written to a new CSV file, including the metrics and
##the state of each job after being processed by the algorithm.

import csv
import numpy as np
import pandas as pd
import argparse

# initialize variables
clock = 0
flag = False

# read csv file
parser = argparse.ArgumentParser()
parser.add_argument("--data", help="Path to input CSV", default="job1.csv")
parser.add_argument("--out",  help="Path to output CSV", default="job1_sjf.csv")
args = parser.parse_args()

input_file_name  = args.data
# Set name for output csv file
output_file_name = args.out

# open the input CSV file and read the rows into a pandas dataframe
df = pd.read_csv(input_file_name)

# set the initial job state to 0 for all jobs in the dataframe
df["Job State"] = 0

# Total number of jobs in the csv file
numJobs = len(df)

# dynamic arrays sized to actual job count
endTime        = [0] * numJobs
startJob       = [0] * numJobs
responseTime   = [0] * numJobs
turnAroundTime = [0] * numJobs

# extract columns (lists sized to numJobs)
arrivalTime = df["Arrival Time"].tolist()
jobSize     = df["Job Size"].tolist()
jobState    = df["Job State"].tolist()

# perform the scheduling algorithm on the dataframe
for row in df.itertuples(index=True):
    index = row.Index
    flag = False
    # For the first row (index 0), calculate the clock time and set the 
    # corresponding values in the endTime, startJob, responseTime, and 
    # turnAroundTime lists, and mark the job as completed (jobState=2).
    if index == 0:
        clock = arrivalTime[index]+ jobSize[index] # Calculate the clock time for the current row
        endTime[index] = arrivalTime[index] + jobSize[index] # Set the end time for the job
        startJob[index] = arrivalTime[index] # Set the start time for the job
        responseTime[index] = 0 # Set the response time for the job
        turnAroundTime[index] = endTime[index] - arrivalTime[index] # Set the turnaround time for the job
        jobState[index] = 2 # Mark the job as completed in the jobState list

    for i in range (numJobs):
        # Check if there are any jobs that have arrived and are waiting to be executed
        if jobState[i] != 2 and arrivalTime[i] <= clock:
            # Update the state of the job to indicate that it is ready to be executed
            jobState[i] = 1
            # Set the flag to True to indicate that there is at least one job that is ready to be executed
            flag = True

    if not flag:
        # find next arriving unfinished job globally
        candidates = [i for i in range(numJobs) if jobState[i] != 2]
        if candidates:
            next_i = min(candidates, key=lambda i: arrivalTime[i])
            clock = arrivalTime[next_i]
            # mark any job that has arrived by this time as ready
            for i in candidates:
                if arrivalTime[i] <= clock and jobState[i] != 2:
                    jobState[i] = 1
    # initialize shortest_job_index variable to None  
    shortest_job_index = None

    # iterate over jobState list to find the index of the shortest job in the queue
    for i, state in enumerate(jobState):
        if state == 1:
            # if shortest_job_index is None, set it to the current index
            # otherwise, check if the current job is shorter than the previous shortest job
            if shortest_job_index is None or jobSize[i] < jobSize[shortest_job_index]:
                shortest_job_index = i

    # if there is a shortest job in the queue           
    if shortest_job_index is not None:
        # update the clock by adding the duration of the shortest job
        clock = clock + jobSize[shortest_job_index]
        # update the end time of the shortest job
        endTime[shortest_job_index] = clock
        # calculate the start time of the shortest job
        startJob[shortest_job_index] = endTime[shortest_job_index] - jobSize[shortest_job_index]
        # calculate the response time of the shortest job
        responseTime[shortest_job_index] = startJob[shortest_job_index] - arrivalTime[shortest_job_index]
        # calculate the turnaround time of the shortest job
        turnAroundTime[shortest_job_index] = endTime[shortest_job_index] - arrivalTime[shortest_job_index]
        # set the state of the shortest job to 2 (completed)
        jobState[shortest_job_index] = 2
        # reset shortest_job_index variable to None
        shortest_job_index = None

# calculate the average response time and turn around time
avg_response_time = np.mean(responseTime)
avg_turnaround_time = np.mean(turnAroundTime)

#write the output to a new CSV file
with open(output_file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Index', 'Arrival Time', 'Job Size', 'End Time', 'Start Job', 'Response Time', 'Turnaround Time', 'Job State'])
    for i in range(numJobs):
        writer.writerow([i, arrivalTime[i], jobSize[i], endTime[i], startJob[i], responseTime[i], turnAroundTime[i], jobState[i]])
    writer.writerow(['Average Response Time', avg_response_time])
    writer.writerow(['Average Turnaround Time', avg_turnaround_time])

print(f"CSV file processed successfully. Output saved to {output_file_name}")
