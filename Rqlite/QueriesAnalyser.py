import requests
import time
import json
import psutil
import datetime

NODE_URLS = [
    "node1 url",
    "node2 url",
    "node3 url",
]

QUERY_FILE = "queries.json" # You will need to have queries in this file, to which you want to anaylse the performance

def execute_query(node_url, query):
    try:
        start_time = datetime.datetime.now()
        response = requests.post(f"{node_url}/db", data=query.encode())
        response.raise_for_status()
        end_time = datetime.datetime.now()
        execution_time = end_time - start_time
        return response.text, execution_time
    except requests.exceptions.RequestException as e:
        print(f"Error executing query on {node_url}: {e}")
        return None, None

def compare_results(results):
    if len(set(results)) == 1:
        return True
    else:
        return False

def evaluate_query_performance(query):
    process = psutil.Process()
    start_cpu_usage = process.cpu_percent()
    start_memory_usage = process.memory_info().rss / (1024 ** 2)  # Convert to MB

    results = [execute_query(node_url, query) for node_url in NODE_URLS]
    successful_results = [result for result in results if result[0]]
    
    if not successful_results:
        print("Query failed to execute on all nodes.")
        return

    if compare_results([result[0] for result in successful_results]):
        print("Node results are consistent.")
    else:
        print("Node results are inconsistent.")
        for node_url, (result, execution_time) in zip(NODE_URLS, results):
            if result:
                print(f"{node_url}: {result}")
            else:
                print(f"{node_url}: Query execution failed.")

    end_cpu_usage = process.cpu_percent()
    end_memory_usage = process.memory_info().rss / (1024 ** 2)

    cpu_usage_delta = end_cpu_usage - start_cpu_usage
    memory_usage_delta = end_memory_usage - start_memory_usage

    print(f"\nCPU Usage: {cpu_usage_delta}%")
    print(f"Memory Usage: {memory_usage_delta:.2f} MB")

    for node_url, (result, execution_time) in zip(NODE_URLS, results):
        if result:
            print(f"{node_url} Execution Time: {execution_time}")

if __name__ == "__main__":
    with open(QUERY_FILE, "r") as file:
        query = file.read().strip()

    evaluate_query_performance(query)