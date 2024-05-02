import threading
import time
import pyrqlite.dbapi2 as dbapi2
import pandas as pd
import psutil

def log_resources(interval=1, duration=10):
    """Logs system resources to a file."""
    with open("resource_log_1.txt", "w") as logfile:
        logfile.write("Timestamp, CPU(%), Memory(%), Disk Read(Bytes/s), Disk Write(Bytes/s), Network Sent(Bytes/s), Network Received(Bytes/s)\n")
        
        end_time = time.time() + duration
        while time.time() < end_time:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            cpu_percent = psutil.cpu_percent(interval=interval)
            memory_percent = psutil.virtual_memory().percent
            disk_io = psutil.disk_io_counters()
            network_io = psutil.net_io_counters()
            
            logfile.write(f"{timestamp}, {cpu_percent}, {memory_percent}, {disk_io.read_bytes}, {disk_io.write_bytes}, {network_io.bytes_sent}, {network_io.bytes_recv}\n")

def query_and_log_resources(token_address):
    """Performs a specified database query and logs system resources."""
    resource_log_duration = 5  # Duration for resource logging
    resource_thread = threading.Thread(target=log_resources, args=(1, resource_log_duration))
    resource_thread.start()

    query_start_time = time.time()

    connection = dbapi2.connect(host='localhost', port=4001)
    connection.load_extension("crsqlite")


    try:
        with connection.cursor() as cursor:
            query = f"""
            SELECT from_address, to_address, SUM(value) AS total_value, AVG(value) AS average_value, date, block_timestamp
            FROM contracts
            WHERE token_address = '{token_address}'
            GROUP BY from_address, to_address
            ORDER BY total_value DESC;
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            for result in results:
                print(result)
    finally:
        connection.close()
    
    query_end_time = time.time()

    resource_thread.join()

    compute_resource_usage(query_start_time, query_end_time)

def compute_resource_usage(start_time, end_time):
    """Reads the resource_log.txt file and computes the average CPU and Memory usage during the query."""
    df = pd.read_csv("resource_log_1.txt", delimiter=',')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    query_df = df[(df['Timestamp'] >= pd.to_datetime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))) & 
                  (df['Timestamp'] <= pd.to_datetime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))))]

    average_cpu_usage = query_df[' CPU(%)'].mean()  # Adjust column names as necessary
    average_memory_usage = query_df[' Memory(%)'].mean()

    execution_time = end_time - start_time

    print(f"Query Execution Time: {execution_time} seconds")
    print(f"Average CPU Usage During Query: {average_cpu_usage}%, Average Memory Usage: {average_memory_usage}%")


token_address = '0x94f27b5141e17dd8816242d752c7be8e6764bd22'

# Execute the function with a specific token address
query_and_log_resources(token_address)
