import psutil
import time

def log_resources(interval=1, duration=10):
    start_time = time.time()
    end_time = start_time + duration
    
    with open("resource_log.txt", "w") as logfile:
        logfile.write("Timestamp, CPU(%), Memory(%), Disk Read(Bytes/s), Disk Write(Bytes/s), Network Sent(Bytes/s), Network Received(Bytes/s)\n")
        
        while time.time() < end_time:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            cpu_percent = psutil.cpu_percent(interval=interval)
            memory_percent = psutil.virtual_memory().percent
            disk_io = psutil.disk_io_counters()
            network_io = psutil.net_io_counters()
            
            logfile.write(f"{timestamp}, {cpu_percent}, {memory_percent}, {disk_io.read_bytes}, {disk_io.write_bytes}, {network_io.bytes_sent}, {network_io.bytes_recv}\n")
            print(f"{timestamp}, {cpu_percent}, {memory_percent}, {disk_io.read_bytes}, {disk_io.write_bytes}, {network_io.bytes_sent}, {network_io.bytes_recv}")
            time.sleep(interval)

if __name__ == "__main__":
    log_resources(interval=1, duration=60)