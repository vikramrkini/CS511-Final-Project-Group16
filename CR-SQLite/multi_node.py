import sqlite3
import psutil
import time

def get_resource_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    return cpu_usage, memory_usage

def execute_query_on_node(db_file, query, params):
    """
    Executes a given query on a database and returns the results.
    """
    conn = sqlite3.connect(db_file)
    conn.load_extension("crsqlite")
    cur = conn.cursor()
    cur.execute(query, params)
    results = cur.fetchall()
    conn.close()
    return results

def test_multi_node_operation(node_db_files, query, params):
   
    start_cpu_usage, start_memory_usage = get_resource_usage()
    
    start_time = time.time()
    for db_file in node_db_files:
        print(f"Executing query on {db_file}...")
        results = execute_query_on_node(db_file, query, params)
        for result in results:
            print(result)
    end_time = time.time()
    
    end_cpu_usage, end_memory_usage = get_resource_usage()
    
    print(f"\nOperation completed in {end_time - start_time:.2f} seconds.")
    print(f"CPU Usage: From {start_cpu_usage}% to {end_cpu_usage}%. Memory Usage: From {start_memory_usage}% to {end_memory_usage}%.")

if __name__ == "__main__":
    node = ['block-1.so', 'block-2.so', 'block-3.so'] 
    query = """
    SELECT
        miner,
        COUNT(number) AS blocks_mined,
        AVG(difficulty) AS average_difficulty,
        AVG(size) AS average_size
    FROM
        blocks
    WHERE
        number BETWEEN ? AND ?
    GROUP BY
        miner
    ORDER BY
        blocks_mined DESC, average_difficulty DESC
    LIMIT 5;
    """
    params = (9190000, 9200000)  
    
    test_multi_node_operation(node_db_files, query, params)
    