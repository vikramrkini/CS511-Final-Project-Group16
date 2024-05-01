import concurrent.futures
import time
import requests
import psutil
import datetime

NUM_QUERIES = 5
RQLITE_NODE_URL = "<give your local url>"  

def query_rqlite(query):
    try:
        start_time = datetime.datetime.now()
        response = requests.post(f"{RQLITE_NODE_URL}/db", data=query.encode())
        response.raise_for_status()
        end_time = datetime.datetime.now()
        execution_time = end_time - start_time
        return response.text, execution_time
    except requests.exceptions.RequestException as e:
        print(f"Error executing query: {e}")
        return None, None

if __name__ == "__main__":
    queries = [f"SELECT * FROM blocks WHERE id = {i}" for i in range(NUM_QUERIES)]
    process = psutil.Process()

    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_QUERIES) as executor:
        future_to_query = {executor.submit(query_rqlite, query): query for query in queries}

        for future in concurrent.futures.as_completed(future_to_query):
            query = future_to_query[future]
            try:
                result, execution_time = future.result()
                if result:
                    print(f"Query: {query}\nResult: {result}\nExecution Time: {execution_time}")
                else:
                    print(f"Query {query} failed to execute.")
            except Exception as e:
                print(f"Query {query} generated an exception: {e}")

    cpu_usage = process.cpu_percent()
    memory_usage = process.memory_info().rss / (1024 ** 2)
    print(f"\nCPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_usage:.2f} MB")