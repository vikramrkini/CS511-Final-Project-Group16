import threading
import time
import pyrqlite.dbapi2 as dbapi2
import pandas as pd
import psutil

# Define a global stop event
stop_event = threading.Event()

def log_resources(interval=1, duration=10):
    with open("resource_log_2.txt", "w") as logfile:
        logfile.write("Timestamp, CPU(%), Memory(%), Disk Read(Bytes/s), Disk Write(Bytes/s), Network Sent(Bytes/s), Network Received(Bytes/s)\n")
        
        end_time = time.time() + duration
        while time.time() < end_time:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            cpu_percent = psutil.cpu_percent(interval=interval)
            memory_percent = psutil.virtual_memory().percent
            disk_io = psutil.disk_io_counters()
            network_io = psutil.net_io_counters()
            
            logfile.write(f"{timestamp}, {cpu_percent}, {memory_percent}, {disk_io.read_bytes}, {disk_io.write_bytes}, {network_io.bytes_sent}, {network_io.bytes_recv}\n")


def query_and_log_resources():
    resource_thread = threading.Thread(target=log_resources, args=(1,))
    resource_thread.start()

    query_start_time = time.time()
    
    connection = dbapi2.connect(host='localhost', port=4001)
    connection.load_extension("crsqlite")

    try:
        with connection.cursor() as cursor:
            cursor.execute('''
            SELECT 
    token_address, 
    COUNT(*) AS transaction_count,
    AVG(value) AS average_transaction_value,
    SUM(value) AS total_transaction_value,
    COUNT(DISTINCT from_address) AS unique_senders,
    COUNT(DISTINCT to_address) AS unique_receivers,
    MIN(value) AS min_transaction_value,
    MAX(value) AS max_transaction_value,
    strftime('%Y-%m', date) AS transaction_month,
    MAX(block_number) - MIN(block_number) AS block_range
FROM 
    contracts
WHERE 
    date BETWEEN '2017-01-01' AND '2017-02-01'
    AND value > 1000  -- Considering only transactions with values greater than 1000
GROUP BY 
    token_address, transaction_month
ORDER BY 
    transaction_count DESC, total_transaction_value DESC
LIMIT 10;
            ''')
            most_active_token = cursor.fetchone()
            print("Most Active Token:", most_active_token)
    finally:
        connection.close()

    query_end_time = time.time()
    
    stop_event.set()
    resource_thread.join()

    compute_resource_usage(query_start_time, query_end_time)

def compute_resource_usage(start_time, end_time):
    """Reads the resource_log.txt file and computes the average CPU and Memory usage during the query."""
    df = pd.read_csv("resource_log_3.txt", delimiter=',')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    query_df = df[(df['Timestamp'] >= pd.to_datetime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))) & 
                  (df['Timestamp'] <= pd.to_datetime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))))]

    average_cpu_usage = query_df[' CPU(%)'].mean()
    average_memory_usage = query_df[' Memory(%)'].mean()
    execution_time = end_time - start_time
    print(f"Query Execution Time: {execution_time} seconds")
    print(f"Average CPU Usage During Query: {average_cpu_usage}%, Average Memory Usage: {average_memory_usage}%")

query_and_log_resources()
