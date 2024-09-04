import csv
import time
import os
import subprocess

# Thresholds for switching traffic
THRESHOLD_CPU = 80 * 1e9  # CPU usage in nanoseconds (adjust based on observations)
THRESHOLD_MEM = 1.5 * 1e9  # Memory usage in bytes (1.5GB)
THRESHOLD_THREADS = 50  # Number of active threads/connections (lowered to 50)
THRESHOLD_QUERIES = 5000  # Total number of queries processed

def check_load_and_update_nginx():
    # Wait for the file to exist before continuing
    while not os.path.exists('/metrics_data/metrics.csv'):
        print("Waiting for metrics.csv to be generated...")
        time.sleep(5)  # Wait 5 seconds before checking again

    # Now the file exists, open and read it
    with open('/metrics_data/metrics.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (float(row['sql1_cpu']) > THRESHOLD_CPU or
                float(row['sql1_mem']) > THRESHOLD_MEM or
                int(row['sql1_threads']) > THRESHOLD_THREADS or
                int(row['sql1_queries']) > THRESHOLD_QUERIES):
                switch_to_sql2()
                break

def switch_to_sql2():
    print("Switching traffic to SQL2 due to high load on SQL1")
    os.environ['SQL_SERVER_HOST'] = 'sql2'
    subprocess.run(['docker', 'exec', 'nginx', 'nginx', '-s', 'reload'])

if __name__ == "__main__":
    while True:
        check_load_and_update_nginx()
        time.sleep(10)  # Check every 10 seconds
