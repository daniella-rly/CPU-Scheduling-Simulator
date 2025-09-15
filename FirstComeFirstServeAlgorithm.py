import csv
import heapq
import textwrap
import argparse

# initialize variables
clock = 0
jobQueue = [] # List for queueing up jobs that have already arrived ahead of time
jobIndex = 0
totalResponseTime = 0.0 # for storing the total response time of the jobs
totalTurnAroundTime = 0.0 # for storing the total turn-around time of the jobs

# input the file name for the job population
parser = argparse.ArgumentParser()
parser.add_argument("--data", help="Path to input CSV", default="job1.csv")
parser.add_argument("--out", default=None, help="Optional output file")
args = parser.parse_args()

input_file_name = args.data
# Set the name for the processed output file
output_file_name = args.out or input_file_name.split('.')[0] + "_fcfs.csv"

# determine how many jobs are in the CSV to size arrays correctly
with open(input_file_name, 'r') as _f:
    _r = csv.reader(_f)
    next(_r, None)  # skip header if present
    numJobs = sum(1 for _ in _r)
    if numJobs == 0:
        raise ValueError("The input CSV has no data rows")

# Size arrays dynamically based on the actual number of jobs
endTime        = [0] * numJobs
startJob       = [0] * numJobs
responseTime   = [0] * numJobs
turnAroundTime = [0] * numJobs
clockInitial   = [0] * numJobs
clockFinal     = [0] * numJobs
jobStateList   = [0] * numJobs 


# read the input file
with open(input_file_name, 'r') as file:
    csvreader = csv.reader(file)
    next(csvreader, None) # skip the header row

    pending = next(csvreader, None) 
    # iterate through the rows of values in the .csv file
    while True:
        # check if there are any jobs in the queue or in the input file
        if jobQueue or jobIndex < len(endTime):
            # if there are jobs in the queue, get the one with the least arrival time
            if jobQueue:
                job = heapq.heappop(jobQueue)
                arrivalTime = job[0]
                jobSize = job[1]
                jobState = 1 # to track the status of each job, currently processing the job
            else:
                row = pending
                if row is None:
                # no more rows to read and nothing queued → break out
                    break
                pending = next(csvreader, None)

                arrivalTime = int(row[1])
                jobSize = int(row[2])
            
            # calculate the system time when the job arrives and store the initial clock value for the job
            clock = max(clock, arrivalTime)
            clockInitial[jobIndex] = clock
            
            # update the job status and calculate the values for the current job
            if jobIndex == 0:
                jobState = 1 # currently processing the job
                endTime[jobIndex] = arrivalTime + jobSize
                startJob[jobIndex] = arrivalTime
                responseTime[jobIndex] = startJob[jobIndex] - arrivalTime
                turnAroundTime[jobIndex] = endTime[jobIndex] - arrivalTime
                totalResponseTime = totalResponseTime + responseTime[jobIndex]
                totalTurnAroundTime = totalTurnAroundTime + turnAroundTime[jobIndex]

            else:
                jobState = 1 # currently processing the job
                startJob[jobIndex] = max(endTime[jobIndex - 1], arrivalTime)
                endTime[jobIndex]  = startJob[jobIndex] + jobSize
                responseTime[jobIndex] = startJob[jobIndex] - arrivalTime
                turnAroundTime[jobIndex] = endTime[jobIndex] - arrivalTime
                totalResponseTime = totalResponseTime + responseTime[jobIndex]
                totalTurnAroundTime = totalTurnAroundTime + turnAroundTime[jobIndex]
            
            # update the job status, clock and job index and store the final clock value for the job
            jobStateList[jobIndex] =  2 # job has been processed
            clock = endTime[jobIndex]
            clockFinal[jobIndex] = clock
            jobIndex += 1
            
            # check if there are any other jobs in the input file that have arrived
            # push any arrivals that have arrived by current clock from the pending buffer
            while pending is not None and int(pending[1]) <= clock:
                heapq.heappush(jobQueue, (int(pending[1]), int(pending[2]), 0))
                pending = next(csvreader, None)  # advance the lookahead

        # if there are no more jobs in the queue or in the input file, break out of the loop
        else:
            break


# open the new output CSV file for writing
with open(output_file_name, 'w', newline='') as file:
    csvwriter = csv.writer(file)

    # write the header row for the new columns
    csvwriter.writerow(['Index', 'Arrival Time', 'Job Size', 'Start Job',  'Initial Clock Time', 'End Time', 'Response Time', 'Turnaround Time', 'Final Clock Time', 'Job State'])

    # write the data rows, with the new columns
    with open(input_file_name, 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader, None) # skip the header row

        for index, row in enumerate(csvreader):
            # extract the original values from the input file
            arrivalTime = int(row[1])
            jobSize = int(row[2])

            # write the new values to the output file
            csvwriter.writerow([index, arrivalTime, jobSize, startJob[index],  clockInitial[index], endTime[index], responseTime[index], turnAroundTime[index], clockFinal[index], jobStateList[index]])

    # write the aaverage responsee time and turn around time
    csvwriter.writerow(['', '', '', '','', '', textwrap.fill('Average Response Time: ' + str(round((totalResponseTime / numJobs))), 10), textwrap.fill('Average Turnaround Time: ' + str(round((totalTurnAroundTime / numJobs))), 10), '', ''])
print("CSV file processed successfully.")
