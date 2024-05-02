# CS511-Final-Project-Group16

## BigchainDB Installation and Deployment Guide

This README provides instructions on how to install BigchainDB on your local machine and deploy it on Amazon Elastic Container Service (ECS).

## Prerequisites

Before you begin, make sure you have the following installed:
- Docker
- Docker Compose
- AWS CLI
- ECS CLI (for deployment on ECS)
- Git (optional, for cloning repositories)

## Installation on Localhost

### Step 1: Clone the Repository

If you have Git installed, you can clone the BigchainDB repository. Otherwise, you can download the latest release from GitHub.

```

git clone https://github.com/bigchaindb/bigchaindb.git
cd bigchaindb

```

### Step 2: Configure BigchainDB

Edit the configuration file to suit your local environment. The configuration file can be found at:

```

nano bigchaindb/.bigchaindb
```

### Step 3: Run BigchainDB using Docker Compose

To start BigchainDB on your local machine using Docker Compose, run:

```

docker-compose up
```

This command will start all required services in containers as defined in the docker-compose.yml file.

## Deployment on Amazon ECS

### Step 1: Configure AWS CLI
Configure your AWS CLI with the appropriate credentials and default region:

```

aws configure
```

### Step 2: Create an ECS Cluster

Create a new ECS cluster where your BigchainDB instance will be deployed.
```

ecs-cli up --cluster-config myClusterConfig --ecs-profile myEcsProfile
```
### Step 3: Create Task Definition

Create a task definition for BigchainDB. You can use the AWS Management Console or the ECS CLI to define tasks.

### Step 4: Deploy BigchainDB to ECS

Use the ECS CLI to deploy BigchainDB to your cluster:

```

ecs-cli compose --file docker-compose.yml service up --create-log-groups --cluster-config myClusterConfig --ecs-profile myEcsProfile
```

### Step 5: Verify Deployment

Verify that the BigchainDB service is running correctly:

```
ecs-cli ps --cluster-config myClusterConfig --ecs-profile myEcsProfile
```


## Running Benchmark Scripts

To run simply use the python notebook for loading and testing BigchainDB. Note for ECS deployment we recommend using lambda functions for triggering various codes.

## Additional Resources

- [BigchainDB Documentation](https://docs.bigchaindb.com/)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [CR-sqlite Documentation](https://vlcn.io/docs/)



## Setting up cr-sqlite
- Visit [cr-sqlite installation documentation](https://vlcn.io/docs) for detailed instructions.
- Pull the latest Docker image from [cr-sqlite Docker Hub](https://vlcn.io/docs/cr-sqlite/installation): 
-  Docker Installation
  ```  
  docker pull cr-sqlite/cr-sqlite
  ```
- For a single node:
  ```
  docker run -p <host_port>:<container_port> cr-sqlite/cr-sqlite
  ```
- For a cluster:
  ```
  docker run cr-sqlite/cr-sqlite -join=$RAFT_ADDRESS:<Child_PORT>
  ```


## Setting up rqlite

### Docker Installation

- Visit [rqlite installation documentation](https://rqlite.io/docs/install-rqlite/) for detailed instructions.
- Pull the latest Docker image from [rqlite Docker Hub](https://hub.docker.com/r/rqlite/rqlite/): 
  ```
  docker pull rqlite/rqlite
  ```
- For a single node:
  ```
  docker run -p <host_port>:<container_port> rqlite/rqlite
  ```
- For a cluster:
  ```
  docker run rqlite/rqlite -join=$RAFT_ADDRESS:<Child_PORT>
  ```

### Homebrew Installation (for MacOS)

- Alternatively, you can install via Homebrew. Check the documentation for specific instructions.

Once installed, verify the installation by running `rqlite` in the command line or Docker command line. Adjust ports in your scripts accordingly.

## Sample Queries

### Sorting Transactions by Value

```sql
SELECT 
    SUM(value) AS total_value,
    AVG(value) AS average_value,
    date,
    block_timestamp 
FROM 
    contracts 
WHERE 
    token_address ='0x94f27b5141e17dd8816242d752c7be8e6764bd22' 
GROUP BY 
    from_address, 
    to_address 
ORDER BY 
    total_value DESC;
```

### Most Active Token Address

```sql
SELECT 
    token_address, 
    COUNT(*) AS transaction_count 
FROM 
    contracts 
GROUP BY 
    token_address 
ORDER BY 
    transaction_count DESC 
LIMIT 1;
```

### Detailed Transaction Analysis

```sql
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
    transaction_count DESC, 
    total_transaction_value DESC 
LIMIT 1;
