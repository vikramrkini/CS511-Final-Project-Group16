import sqlite3
import pandas as pd
import s3fs
import psutil
import time

# Function to get current CPU and Memory usage
def get_resource_usage():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    return cpu_usage, memory_usage

# Function to load and return a DataFrame from a Parquet file in S3
def load_parquet_from_s3(s3_path):
    with fs.open(s3_path, mode='rb') as f:
        df = pd.read_parquet(f)
    return df

fs = s3fs.S3FileSystem(anon=True)

base_directory_path = 'aws-public-blockchain/v1.0/eth/blocks'
date_range = pd.date_range(start='2020-01-04', end='2020-01-06')
date_directories_filtered = [f"{base_directory_path}/date={date.strftime('%Y-%m-%d')}" for date in date_range]

db_file = 'block-3.db' 

conn = sqlite3.connect(db_file)
conn.load_extension("crsqlite")

c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS blocks (
    difficulty REAL,
    hash TEXT,
    miner TEXT,
    nonce TEXT,
    number INTEGER,
    size INTEGER,
    timestamp TEXT,
    total_difficulty REAL,
    base_fee_per_gas REAL,
    gas_limit INTEGER,
    gas_used INTEGER,
    extra_data TEXT,
    logs_bloom TEXT,
    parent_hash TEXT,
    state_root TEXT,
    receipts_root TEXT,
    transactions_root TEXT,
    sha3_uncles TEXT,
    transaction_count INTEGER,
    date TEXT,
    last_modified TEXT,
    PRIMARY KEY (hash)
    .load crsqlite
    .mode column
);''')

rows_inserted = 0
start_time = time.time()
start_cpu_usage, start_memory_usage = get_resource_usage()

for date_dir in date_directories_filtered:
    files_in_date_dir = fs.ls(date_dir)
    parquet_files = [file for file in files_in_date_dir if file.endswith('.parquet')]
    
    for file_path in parquet_files:
        df = load_parquet_from_s3(f's3://{file_path}')
        if 'timestamp' in df.columns:
            df['timestamp'] = df['timestamp'].astype(str)
        
        df.to_sql('blocks', conn, if_exists='append', index=False)
        rows_inserted += len(df)

conn.commit()
conn.close()

end_cpu_usage, end_memory_usage = get_resource_usage()
end_time = time.time()

print(f"Data from S3 loaded successfully into the SQLite database. Rows inserted: {rows_inserted}")
print(f"Insertion took {end_time - start_time:.2f} seconds.")
print(f"CPU Usage: From {start_cpu_usage}% to {end_cpu_usage}%. Memory Usage: From {start_memory_usage}% to {end_memory_usage}%.")
