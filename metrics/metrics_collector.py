import csv
import time
import docker
import mysql.connector
from datetime import datetime

def get_sql_metrics(host, user, password, database):
    try:
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = connection.cursor()
        cursor.execute("SHOW STATUS LIKE 'Threads_connected';")
        threads = cursor.fetchone()[1]
        cursor.execute("SHOW STATUS LIKE 'Queries';")
        queries = cursor.fetchone()[1]
        return threads, queries
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None

def get_docker_stats(container_name):
    client = docker.from_env()
    container = client.containers.get(container_name)
    stats = container.stats(stream=False)
    cpu_usage = stats["cpu_stats"]["cpu_usage"]["total_usage"]
    mem_usage = stats["memory_stats"]["usage"]
    return cpu_usage, mem_usage

def collect_metrics():
    fieldnames = ['timestamp', 'sql1_threads', 'sql1_queries', 'sql2_threads', 'sql2_queries', 'sql1_cpu', 'sql1_mem', 'sql2_cpu', 'sql2_mem']
    with open('/metrics_data/metrics.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql1_metrics = get_sql_metrics('sql1', 'user', 'password', 'testdb')
            sql2_metrics = get_sql_metrics('sql2', 'user', 'password', 'testdb')
            sql1_stats = get_docker_stats('sql1')
            sql2_stats = get_docker_stats('sql2')

            writer.writerow({
                'timestamp': timestamp,
                'sql1_threads': sql1_metrics[0],
                'sql1_queries': sql1_metrics[1],
                'sql2_threads': sql2_metrics[0],
                'sql2_queries': sql2_metrics[1],
                'sql1_cpu': sql1_stats[0],
                'sql1_mem': sql1_stats[1],
                'sql2_cpu': sql2_stats[0],
                'sql2_mem': sql2_stats[1],
            })
            time.sleep(5)  # Collect metrics every 5 seconds

if __name__ == "__main__":
    collect_metrics()
