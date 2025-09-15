# CPU Scheduling Simulator (Python)

This project simulates four classic CPU scheduling algorithms in Python:

- **First Come First Serve (FCFS)**
- **Shortest Job First (SJF, non-preemptive)**
- **Shortest Time to Completion First (STCF, preemptive SJF)**
- **Round Robin (RR)**

Two datasets of 1,500 jobs each are provided to highlight trade-offs between algorithms.

---

## Repo Structure
- Data
  - Input datasets (job1.csv and job2.csv)
    - **Job1.csv**  
  Designed for comparing **FCFS** and **SJF**. Jobs arrive steadily, highlighting the benefit of SJF over FCFS.

    - **Job2.csv**  
  Designed for comparing **STCF** and **Round Robin**. Includes varied job sizes (including small/zero jobs), stressing preemptive scheduling.
- Algorithms
  - All algorithm implementations
- Generators:
  - Generators for the input datasets
- Outputs:
  - CSV files with the processed output

---

### Quick Start

### Setup
```bash
python -m venv .venv
source .venv/bin/activate     # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```
---

## Run Algorithms
### FCFS
```bash
python Algorithms/FirstComeFirstServeAlgorithm.py --data Data/job1.csv --out Outputs/job1_fcfs.csv
```
### SJF
```bash
python Algorithms/ShortestJobFirstAlgorithm.py --data Data/job1.csv --out Outputs/job1_sjf.csv
```
### Round Robin (Quantum Time = 50)
```bash
python Algorithms/RoundRobinAlgorithm.py --data Data/Job2.csv --out Outputs/job2_rr_q50.csv --quantum 50
```
### STCF
```bash
python Algorithms/ShortestTimeToCompletionFirstAlgorithm.py --data Data/Job2.csv --out Outputs/job2_stcf.csv
```

---

## Results

### Job1 — FCFS vs SJF
| Algorithm | Avg Response Time | Avg Turnaround Time | Notes |
|-----------|------------------:|--------------------:|-------|
| FCFS      |       56418       |       56568         | Baseline, order of arrival |
| SJF       |       49789       |       49938         | Improves averages, may delay long jobs |

### Job2 — STCF vs RR
| Algorithm | Parameters | Avg Response Time | Avg Turnaround Time | Notes |
|-----------|------------|------------------:|--------------------:|-------|
| STCF      | —          |     81350         |     81567           | Great for short jobs, starvation of long ones |
| RR        | quantum=50 |     29064         |     162803          | Fair rotation, performance depends on quantum |

---

## Findings
From the experiments on both datasets:

- **SJF outperforms FCFS**  
  On Job1, SJF consistently produced lower average response and turnaround times compared to FCFS. This is expected, since SJF prioritizes short jobs and avoids the “convoy effect” of a long job blocking many small ones.

- **STCF is highly responsive but unfair to long jobs**  
  On Job2, STCF minimized response times for short jobs but caused extremely high turnaround for long ones, leading to inflated averages overall. This demonstrates the starvation risk of preemptive shortest-job scheduling.

- **Round Robin strikes a balance**  
  With a quantum of 50, RR produced much lower average response times than STCF, but at the cost of very high turnaround times due to frequent context switches and slicing of long jobs. This shows how quantum size directly impacts the balance between responsiveness and efficiency.

### Overall
- **FCFS**: Simple, fair in order of arrival, but inefficient for mixed job sizes.  
- **SJF**: Best average times on steady arrivals, but non-preemptive.  
- **STCF**: Excellent responsiveness for short jobs, but unfair to long ones.  
- **Round Robin**: Balances fairness and responsiveness; effectiveness depends on quantum choice.

