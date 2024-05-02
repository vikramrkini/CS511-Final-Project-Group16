import sqlite3
import psutil
import time


def print_resource_usage(start_time, start_cpu, start_memory):
    end_time = time.time()
    end_cpu = psutil.cpu_percent()
    end_memory = psutil.virtual_memory().percent
    print(f"Query Time: {end_time - start_time:.2f} seconds")
    print(f"CPU Usage: From {start_cpu}% to {end_cpu}%")
    print(f"Memory Usage: From {start_memory}% to {end_memory}%")

conn = sqlite3.connect(db_file)
c = conn.cursor()

query = '''
        SELECT token_address, COUNT(*) AS transaction_count
        FROM contracts
        GROUP BY token_address
        ORDER BY transaction_count DESC
        LIMIT 10;
        '''

start_time = time.time()
start_cpu = psutil.cpu_percent()
start_memory = psutil.virtual_memory().percent

c.execute(query)
rows = c.fetchall()

print("Top 10 token addresses by transaction count:")
for row in rows:
    print(row)

print_resource_usage(start_time, start_cpu, start_memory)

conn.close()
