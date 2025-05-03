import socket
import json
import time

UDP_PORT = 6000
BROADCAST_IP = '255.255.255.255'

# Get local IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))  # Connect to Google's DNS server
local_ip = s.getsockname()[0]
s.close()

username = input("Enter your username: ")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
msg = json.dumps({"username": username, "ip": local_ip}).encode()

print(f"[Service Announcer] Broadcasting... (Your IP: {local_ip})")
while True:
    s.sendto(msg, (BROADCAST_IP, UDP_PORT))
    time.sleep(8)

