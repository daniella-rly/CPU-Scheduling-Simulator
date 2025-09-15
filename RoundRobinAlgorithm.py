##This code simulates a round-robin scheduling algorithm for a set of jobs. It reads job information from
##a CSV file provided by the user, initializes several lists to store job-related data, and then iterates through each job in the input file.
##For each job, it determines if it can be executed within the quantum time specified and updates the clock time, end time, start time,
##response time, and turnaround time. If the job cannot be completed within the quantum time, it adds the job to a job queue for later execution.
##The code then processes the job queue and executes each job in a round-robin fashion until all jobs have been completed.
##After all jobs have been processed, the code writes the output to a new CSV file, including information about
##each job's index, arrival time, job size, end time, start time, response time, turnaround time, job state, and context switches.

# import required libraries
import csv
import pandas as pd
import queue
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--data", help="Path to input CSV", default="Job2.csv")
parser.add_argument("--out",  help="Path to output CSV", default="job2_rr.csv")
parser.add_argument("--quantum", type=int, default=50, help="Time quantum")
args = parser.parse_args()

input_file_name  = args.data
output_file_name = args.out
quantumTime = args.quantum

# read data
df = pd.read_csv(input_file_name)
df["Job State"]       = 0
df["Context Switch"]  = 0

# dynamic sizes
numJobs = len(df)
arrivalTime   = df["Arrival Time"].tolist()
jobSize       = df["Job Size"].tolist()         # keep original sizes for output
remainingTime = jobSize.copy()                  # track remaining work here

# arrays
endTime        = [0] * numJobs
startJob       = [0] * numJobs                  # will hold the last start
responseTime   = [None] * numJobs               # set only at first CPU start
turnAroundTime = [0] * numJobs
jobState       = [0] * numJobs                  # 0=new, 1=ready/running again, 2=done
contextSwitch  = [0] * numJobs

# scheduling state
clock = 0
jobQueue = queue.Queue()
queued_jobs = set()

# a function to add jobs to the queue
def processJobs():
    # Enqueue any jobs that have arrived (arrival <= clock), are not finished, and not already queued
    for i in range(numJobs):
        if jobState[i] != 2 and i not in queued_jobs and arrivalTime[i] <= clock:
            jobQueue.put(i)
            queued_jobs.add(i)

# iterate over the dataframe rows
for index, row in df.iterrows():
    if index == 0:
        # start when it arrives (or at current clock if clock is changed elsewhere)
        start = max(clock, arrivalTime[index])
        slice_amt = min(quantumTime, remainingTime[index])

        startJob[index] = start
        endTime[index]  = start + slice_amt
        if responseTime[index] is None:
            responseTime[index] = start - arrivalTime[index]

        remainingTime[index] -= slice_amt
        clock = endTime[index]

        if remainingTime[index] > 0:
            jobState[index] = 1
            contextSwitch[index] += 1
            jobQueue.put(index)
            queued_jobs.add(index)       # will be re-queued below
        else:
            jobState[index] = 2
            
    processJobs()		
    while not jobQueue.empty():
        j = jobQueue.get()
        # If this job hasn't arrived yet (possible if queue became empty and clock jumped), wait
        start = max(clock, arrivalTime[j])
        slice_amt = min(quantumTime, remainingTime[j])

        startJob[j] = start
        endTime[j]  = start + slice_amt
        if responseTime[j] is None:
            responseTime[j] = start - arrivalTime[j]

        remainingTime[j] -= slice_amt
        clock = endTime[j]

        # New arrivals may have come while running this quantum
        processJobs()

        if remainingTime[j] > 0:
            jobState[j] = 1
            contextSwitch[j] += 1
            jobQueue.put(j)       # round-robin: back of the queue
        else:
            jobState[j] = 2

        turnAroundTime[j] = endTime[j] - arrivalTime[j]

# After iterating rows, continue until all jobs are finished
while any(rt > 0 for rt in remainingTime if rt is not None) and not all(state == 2 for state in jobState):
    # If queue is empty but jobs remain, jump clock to the next arrival and enqueue
    if jobQueue.empty():
        next_arrivals = [arrivalTime[i] for i in range(numJobs) if jobState[i] != 2 and i not in queued_jobs]
        if next_arrivals:
            clock = max(clock, min(next_arrivals))
        processJobs()
        if jobQueue.empty():
            break  # no more work
    # Process one quantum
    j = jobQueue.get()
    start = max(clock, arrivalTime[j])
    slice_amt = min(quantumTime, remainingTime[j])
    startJob[j] = start
    endTime[j]  = start + slice_amt
    if responseTime[j] is None:
        responseTime[j] = start - arrivalTime[j]
    remainingTime[j] -= slice_amt
    clock = endTime[j]
    processJobs()
    if remainingTime[j] > 0:
        jobState[j] = 1
        contextSwitch[j] += 1
        jobQueue.put(j)
    else:
        jobState[j] = 2
    turnAroundTime[j] = endTime[j] - arrivalTime[j]

                       
# Fill any never-started jobs (shouldn’t happen if loop completes) with 0s
responseTime = [rt if rt is not None else 0 for rt in responseTime]

# write the output to a new CSV file
with open(output_file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Index', 'Arrival Time', 'Job Size', 'End Time', 'Start Job', 'Response Time', 'Turnaround Time', 'Job State', 'Context Switches'])
    for i in range(numJobs):
        writer.writerow([i, arrivalTime[i], jobSize[i], endTime[i], startJob[i], responseTime[i], turnAroundTime[i], jobState[i], contextSwitch[i]])

print(f"CSV file processed successfully. Output saved to {output_file_name}")
                     
                        
                        
