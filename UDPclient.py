from socket import *
import json
import time

UDP_PORT = 6000
PEERS_FILE = "peers.json"
peers = {}  # IP -> {username, last_seen}

def save_peers():
    try:
        with open(PEERS_FILE, 'w') as f:
            json.dump(peers, f)
    except:
        print("[Peer Discovery] Warning: Could not save peers to file")

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', UDP_PORT))
print("[Peer Discovery] Listening for broadcasts...")

while True:
    data, addr = s.recvfrom(1024)
    try:
        msg = json.loads(data.decode())
        user = msg['username']
        ip = addr[0]
        if ip not in peers:
            print(f"{user} is online")
        peers[ip] = {"username": user, "last_seen": time.time()}
        save_peers()  # Save to file after each update
    except:
        continue
