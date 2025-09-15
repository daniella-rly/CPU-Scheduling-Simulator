import csv
import heapq
import textwrap
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--data", help="Path to input CSV", default="Job2.csv")
parser.add_argument("--out",  help="Path to output CSV", default=None)
args = parser.parse_args()

input_file_name  = args.data
output_file_name = args.out or input_file_name.split('.')[0] + "_stcf.csv"

# read jobs
rows = []
with open(input_file_name, "r") as f:
    r = csv.reader(f)
    header = next(r)  # ['Index','Arrival Time','Job Size']
    for row in r:
        idx  = int(row[0])
        arr  = int(row[1])
        size = int(row[2])
        rows.append((idx, arr, size))

# sort by arrival to handle out-of-order arrivals cleanly
rows.sort(key=lambda x: x[1])

numJobs = len(rows)
if numJobs == 0:
    raise ValueError("Input CSV has no data rows.")

# Initialize lists and vaariables
endTime        = [0] * numJobs
startJob       = [-1] * numJobs            # first time the job gets CPU
responseTime   = [0] * numJobs
turnAroundTime = [0] * numJobs
clockInitial   = [-1] * numJobs            # clock when job first scheduled
clockFinal     = [0] * numJobs
jobStateList   = [0] * numJobs             # 0=new, 1=running/ready, 2=done
remainingTime  = [rows[i][2] for i in range(numJobs)]

clock = 0

# event-driven: run current job until it finishes, or a new shorter job arrives
i = 0  # pointer into arrival-sorted rows
heap = []  # min-heap of (remaining, index_in_rows)

while i < numJobs or heap:
    # if nothing ready, jump to next arrival
    if not heap and i < numJobs and clock < rows[i][1]:
        clock = rows[i][1]

    # push all arrivals at/ before 'clock' into heap
    while i < numJobs and rows[i][1] <= clock:
        idx_in = i
        rem    = remainingTime[idx_in]
        heapq.heappush(heap, (rem, idx_in))
        jobStateList[idx_in] = 1
        i += 1

    if not heap:
        continue

    # pick job with smallest remaining time
    rem, j = heapq.heappop(heap)
    idx, arr, size = rows[j]

    # on first CPU start, record start/response/initial clock
    if startJob[j] == -1:
        startJob[j] = clock
        responseTime[j] = startJob[j] - arr
        clockInitial[j] = clock

    # how long can we run it?
    # either until it finishes, or until the next arrival happens
    if i < numJobs:
        time_to_next_arrival = rows[i][1] - clock
    else:
        time_to_next_arrival = rem  # no more arrivals

    slice_amt = rem if rem <= time_to_next_arrival else time_to_next_arrival

    # advance time
    clock += slice_amt
    rem   -= slice_amt

    if rem == 0:
        # finished
        remainingTime[j] = 0
        endTime[j] = clock
        turnAroundTime[j] = endTime[j] - arr
        clockFinal[j] = clock
        jobStateList[j] = 2
    else:
        # preempted by an arrival; reinsert with updated remaining
        remainingTime[j] = rem
        heapq.heappush(heap, (rem, j))

# write CSV
with open(output_file_name, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Index','Arrival Time','Job Size','Start Job','Initial Clock Time','End Time','Response Time','Turnaround Time','Final Clock Time','Job State'])
    for j in range(numJobs):
        idx, arr, size = rows[j]
        w.writerow([
            idx, arr, size,
            startJob[j],
            clockInitial[j],
            endTime[j],
            responseTime[j],
            turnAroundTime[j],
            clockFinal[j],
            jobStateList[j]
        ])

    avg_resp = sum(responseTime) / numJobs
    avg_tat  = sum(turnAroundTime) / numJobs
    w.writerow(['', '', '', '', '', '',
                textwrap.fill('Average Response Time: ' + str(round(avg_resp)), 10),
                textwrap.fill('Average Turnaround Time: ' + str(round(avg_tat)), 10),
                '', ''])

print(f"CSV file processed successfully. Output saved to {output_file_name}")
