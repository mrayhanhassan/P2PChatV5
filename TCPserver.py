from socket import *
import json
import time
from datetime import datetime
import random
import base64
import sys
from os.path import exists

# Diffie-Hellman parameters
P = 19  # As specified in requirements
G = 2   # As specified in requirements

TCP_PORT = 6001
LOG_FILE = "chat_history.log"

def generate_private_key():
    return random.randint(1, P-1)

def calculate_public_key(private_key):
    return pow(G, private_key, P)

def calculate_shared_key(peer_public_key, private_key):
    return pow(peer_public_key, private_key, P)

def log_message(addr, message, is_sent=True):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    direction = "SENT"  # Per requirement, mark as SENT for responder
    ip = addr[0]
    username = ip  # Default to IP if username not found
    # Try to get username from peers.json
    if exists("peers.json"):
        try:
            with open("peers.json", "r") as f:
                peers = json.load(f)
                if ip in peers and 'username' in peers[ip]:
                    username = peers[ip]['username']
        except:
            pass
    log_entry = f"{timestamp} | {username} | {ip} | {message} | {direction}\n"
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry)
    except:
        print("[Chat Responder] Warning: Could not write to log file")

try:
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Allow address reuse
    serverSocket.bind(('', TCP_PORT))
    serverSocket.listen()
    print("[Chat Responder] Listening for incoming chats...")
except OSError as e:
    if e.errno == 48:  # Address already in use
        print(f"[Chat Responder] Error: Port {TCP_PORT} is already in use.")
        print("Please make sure no other instance of the server is running.")
        print("If you're sure no other instance is running, try waiting a few minutes or restarting your computer.")
        sys.exit(1)
    else:
        print(f"[Chat Responder] Error: {str(e)}")
        sys.exit(1)

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"[Chat Responder] New connection from {addr[0]}")
    
    try:
        # Handle secure chat setup if needed
        data = connectionSocket.recv(1024).decode()
        msg = json.loads(data)
        
        if 'key' in msg:  # Secure chat initialization
            # Receive client's public key
            client_public = int(msg['key'])
            log_message(addr, f"Received public key: {client_public}", True)
            
            # Generate our keys and send public key
            private_key = generate_private_key()
            public_key = calculate_public_key(private_key)
            response = json.dumps({"key": str(public_key)})
            connectionSocket.send(response.encode())
            log_message(addr, f"Sent public key: {public_key}", False)
            
            # Calculate shared key
            shared_key = calculate_shared_key(client_public, private_key)
            
            # Continue with encrypted communication
            while True:
                data = connectionSocket.recv(1024).decode()
                if not data:
                    break
                    
                msg = json.loads(data)
                if 'encrypted_message' in msg:
                    # In real implementation, use proper encryption/decryption with shared_key
                    b64_encrypted = msg['encrypted_message']
                    encrypted_bytes = base64.b64decode(b64_encrypted)
                    encrypted_text = encrypted_bytes.decode()
                    # Simple XOR with shared key for demonstration
                    decrypted = ''.join(chr(ord(c) ^ (shared_key % 256)) for c in encrypted_text)
                    print(f"Decrypted message from {addr[0]}: {decrypted}")
                    log_message(addr, f"Encrypted: {b64_encrypted} (Decrypted: {decrypted})", True)
                    
        else:  # Unsecure chat
            while True:
                if 'unencrypted_message' in msg:
                    message = msg['unencrypted_message']
                    print(f"Message from {addr[0]}: {message}")
                    log_message(addr, message, True)
                
                data = connectionSocket.recv(1024).decode()
                if not data:
                    break
                msg = json.loads(data)
                
    except Exception as e:
        print(f"[Chat Responder] Error: {str(e)}")
    finally:
        print(f"[Chat Responder] Connection from {addr[0]} closed")
        connectionSocket.close()
