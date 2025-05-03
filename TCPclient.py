from socket import *
import json
from datetime import datetime
import random
import sys
import base64
import time

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

def log_message(ip, username, message, is_sent=True):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    direction = "SENT" if is_sent else "RECEIVED"
    log_entry = f"{timestamp} | {username} | {ip} | {message} | {direction}\n"
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry)
    except:
        print("[Chat Initiator] Warning: Could not write to log file")

def show_users():
    try:
        with open("peers.json", "r") as f:
            peers = json.load(f)
            now = time.time()
            found = False
            for ip, info in peers.items():
                last_seen = info.get('last_seen', 0)
                if now - last_seen <= 15 * 60:  # 15 minutes
                    found = True
                    status = "Online" if now - last_seen <= 10 else "Away"
                    print(f"{info['username']} ({status})")
            if not found:
                print("No users online in the last 15 minutes.")
    except FileNotFoundError:
        print("peers.json not found. Run UDPclient.py to discover peers.")
    except Exception as e:
        print(f"Error reading peers.json: {e}")

def show_history():
    try:
        with open("chat_history.log", "r") as f:
            history = f.readlines()
            if not history:
                print("No chat history found.")
                return
            print("Chat History:")
            print("Timestamp | Username | IP | Message | Direction")
            for line in history:
                print(line.strip())
    except FileNotFoundError:
        print("chat_history.log not found. No chat history yet.")
    except Exception as e:
        print(f"Error reading chat_history.log: {e}")

def chat_flow():
    # Prompt for username (case-insensitive)
    username = input("Enter username to chat with: ").strip()
    try:
        with open("peers.json", "r") as f:
            peers = json.load(f)
            # Find user by case-insensitive match
            user_ip = None
            for ip, info in peers.items():
                if info['username'].lower() == username.lower():
                    user_ip = ip
                    break
            if not user_ip:
                print(f"User '{username}' not found in peers list.")
                return
    except Exception as e:
        print(f"Could not read peers.json: {e}")
        return

    secure = input("Secure chat? (yes/no): ").strip().lower() == 'yes'

    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((user_ip, TCP_PORT))
        print(f"Connected to {username} at {user_ip}")

        shared_key = None
        if secure:
            # Ask user for a number to use as their private key
            while True:
                try:
                    user_number = int(input("Enter a number to use as your private key (1-18): "))
                    if 1 <= user_number < P:
                        break
                    else:
                        print(f"Number must be between 1 and {P-1}.")
                except ValueError:
                    print("Please enter a valid integer.")
            private_key = user_number
            public_key = calculate_public_key(private_key)
            key_packet = json.dumps({"key": str(public_key)})
            clientSocket.send(key_packet.encode())
            log_message(user_ip, username, f"Sent public key: {public_key}")
            response = clientSocket.recv(1024).decode()
            peer_key_data = json.loads(response)
            if 'key' in peer_key_data:
                peer_public = int(peer_key_data['key'])
                shared_key = calculate_shared_key(peer_public, private_key)
                print("Secure connection established")
            else:
                print("Error: Failed to establish secure connection")
                return

        print("Type your messages (press Enter to send, Ctrl+C to exit):")
        while True:
            message = input("> ")
            if secure:
                encrypted = ''.join(chr(ord(c) ^ (shared_key % 256)) for c in message)
                encrypted_bytes = encrypted.encode()
                b64_encrypted = base64.b64encode(encrypted_bytes).decode()
                packet = json.dumps({"encrypted_message": b64_encrypted})
            else:
                packet = json.dumps({"unencrypted_message": message})
            clientSocket.send(packet.encode())
            log_message(user_ip, username, message)

    except KeyboardInterrupt:
        print("\nClosing chat...")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        clientSocket.close()

def main():
    while True:
        print("\nSelect an option:")
        print("1. Users - View online users")
        print("2. Chat - Initiate chat")
        print("3. History - View chat history")
        choice = input("Enter 'Users', 'Chat', or 'History' (or 'Exit' to quit): ").strip().lower()
        if choice == 'users' or choice == '1':
            show_users()
        elif choice == 'chat' or choice == '2':
            chat_flow()
        elif choice == 'history' or choice == '3':
            show_history()
        elif choice == 'exit':
            print("Exiting Chat Initiator.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
