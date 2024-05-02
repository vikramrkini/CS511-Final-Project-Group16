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