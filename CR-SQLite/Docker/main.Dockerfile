
FROM ubuntu:latest

# Install SQLite and any other dependencies you might need
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev && rm -rf /var/lib/apt/lists/*

# Set a working directory
WORKDIR /data

# Assuming you have a version of crsqlite.so compiled for aarch64, copy it into the container
COPY ./crsqlite.so /data/

.load crsqlite
.mode column

ENV LD_LIBRARY_PATH=/data:${LD_LIBRARY_PATH}
