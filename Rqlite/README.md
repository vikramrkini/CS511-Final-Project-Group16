First of all to set up rqlite

Go to : https://rqlite.io/docs/install-rqlite/

Setup for docker, as it is easy and convinient

You could pull the latest docker image here : https://hub.docker.com/r/rqlite/rqlite/

docker pull rqlite/rqlite

docker run -p<PORT>:<PORT> rqlite/rqlite => single node

docker run rqlite/rqlite -join=$RAFT_ADDRESS:<Child_PORT> => cluster

For MacOS , you can also do it using homebrew

Once you have this set up, check for rqlite in command line or docker command line.

Now change the ports accordingly in the scripts.


Sorting Transactions by Value:For a given token address, calculate the total and average value, and finally sort these contract by their value in descending order. In addition to the total and average, select other fields that might be of interest, such as from_address, to_address, and block_timestamp, to provide a comprehensive view of each transaction.

SELECT SUM(value) AS total_value,AVG(value) AS average_value,date,block_timestamp FROM contracts WHERE token_address ='0x94f27b5141e17dd8816242d752c7be8e6764bd22' GROUP BY from_address, to_address ORDER BY total_value DESC;

Execution Time: Time taken from query start to finish.
Resource Utilization: CPU and memory usage, as well as disk I/O, if applicable.
Accuracy and Relevance: Ensure sorted results match expected outcomes based on the query criteria.

Determine the most frequently occurring token_address in the contract dataset to identify the most active or popular token over the dataset's timeframe. This query aims to count the number of transactions associated with each token_address and then sort these counts to find the most active token. Such analysis is essential for understanding token dynamics

SELECT token_address, COUNT(*) AS transaction_count
FROM contract
GROUP BY token_address
ORDER BY transaction_count DESC
LIMIT 1;

Execution Time: Measure how long it takes to execute the query, as this reflects the database's efficiency in processing aggregation and sorting operations.
Resource Usage: Monitor CPU, memory, and disk I/O during query execution to assess the impact of such queries on system resources.


SELECT SUM(value) AS total_value,AVG(value) AS average_value,date,block_timestamp FROM contracts WHERE token_address ='0x94f27b5141e17dd8816242d752c7be8e6764bd22' GROUP BY from_address, to_address ORDER BY total_value DESC;

SELECT token_address, COUNT(*) AS transaction_count FROM contracts GROUP BY token_address ORDER BY transaction_count DESC LIMIT 1;

SELECT 
    token_address, 
    COUNT(*) AS transaction_count,
    AVG(value) AS average_transaction_value,
    SUM(value) AS total_transaction_value,
    MAX(value) AS highest_transaction_value,
    MIN(block_timestamp) AS earliest_transaction,
    MAX(block_timestamp) AS latest_transaction
FROM 
    contracts
WHERE 
    date BETWEEN '2016-01-01' AND '2016-03-05'
GROUP BY 
    token_address
ORDER BY 
    transaction_count DESC, total_transaction_value DESC
LIMIT 1;