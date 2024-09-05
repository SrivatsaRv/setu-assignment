
### Files and Directories

- **`docker-compose.yml`**: Defines the Docker services for MySQL containers, load testing, and monitoring.
- **`docker_metrics.csv`**: CSV file where monitoring metrics are recorded. (generated by monitor.py script)
- **`init.sql`**: SQL script for initializing the MySQL databases and creating the `users` table.
- **`load_test/`**: Contains the Dockerfile and Python script for generating load on `sql1 and sql2`. 
- **`monitor/`**: Contains the Dockerfile and Python script for monitoring container metrics and MySQL sessions.

## Services

### MySQL Containers (`sql1` and `sql2`)

- **`sql1`**: MySQL container exposed on port `3306`.
- **`sql2`**: MySQL container exposed on port `3307`.

### Load Testing (`load_test`)

- **Image**: Python 3.9 with MySQL connector.
- **Script**: `load_test.py` inserts random data into the `users` table in the `sql1` database every second.

### Monitoring (`monitor`)

- **Image**: Python 3.9 with Docker SDK and MySQL connector.
- **Script**: `monitor.py` collects and logs metrics such as CPU usage, memory usage, and active MySQL sessions to `docker_metrics.csv` every 5 seconds.

## Getting Started
1- Clone the Repository - `git clone https://github.com/SrivatsaRv/setu-assignment.git`
2- Ensure you have Docker , and Docker Compose Installed - Check with `docker --version` and `docker compose` 
3- Enter the Working Directory - and enter - `docker compose up --build -d` - to bring up the Docker Compose components
4- Verify things are working


## How to Verify? 
1. Verify Containers Are Running: `docker ps -a`  (nothing should be in exited stage)

2. Verify docker_metrics.csv file is created:
- `ls -l /project-dir should see docker_metrics.csv` file generated,  verify its content by cat or wc -latest 

3. Verify the SQL records ingestion - at this point, we should see only SQL1 container taking records , SQL2 should show 0
- `mysql> SHOW databases;`
- `mysql> USE testdb;`
- `mysql> SHOW tabes;`
- `mysql> SELECT COUNT(*) FROM users;`  (SQL-1 container will show records count increasing, SLQ-2 container will show 0 records count)
