import requests
import time
import random

NODE_URLS = [
    "<node1 url>",
    "<node2 url>",
    "<node3 url>",
]

NUM_ITERATIONS = 10

WAIT_TIME = 2

def execute_query(node_url, query):
    try:
        response = requests.post(f"{node_url}/db", data=query.encode())
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error executing query on {node_url}: {e}")
        return None

def compare_results(results):
    if len(set(results)) == 1:
        return True
    else:
        return False

if __name__ == "__main__":
    for i in range(NUM_ITERATIONS):
        print(f"Iteration {i + 1}")
        
        insert_query = f"INSERT INTO sync_table (value) VALUES ({random.randint(1, 1000)})"
        execute_query(NODE_URLS[0], insert_query)
        
        start_time = time.time()
        while True:
            results = [execute_query(node_url, "SELECT * FROM sync_table ORDER BY value DESC LIMIT 1") for node_url in NODE_URLS]
            if not all(results):
                print("One or more nodes failed to execute the query.")
                break
            if compare_results(results):
                end_time = time.time()
                sync_time = end_time - start_time
                print(f"Data synchronized across all nodes in {sync_time:.2f} seconds.")
                break
            time.sleep(0.1)
        
        print()
        time.sleep(WAIT_TIME)