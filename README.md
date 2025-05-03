# P2P-CHAT

A peer-to-peer chat application that allows users to discover and communicate with other users on the same network.

## Features

- Automatic peer discovery using UDP broadcasts
- View online users with status (Online/Away) based on recent activity
- Initiate chat by selecting a username (case-insensitive)
- Support for both secure and unsecure chat options
- Secure chat using Diffie-Hellman key exchange (user-supplied private key)
- Message logging for chat history (includes username and IP)
- Simple and intuitive command-line interface

## Components

The application consists of four main components:

1. **UDP Server (UDPserver.py)**
   - Broadcasts user presence on the network
   - Runs on port 6000
   - Sends periodic broadcasts containing username and IP address

2. **UDP Client (UDPclient.py)**
   - Listens for peer broadcasts
   - Maintains a list of discovered peers
   - Saves peer information to peers.json
   - Tracks last seen time for each peer

3. **TCP Server (TCPserver.py)**
   - Handles incoming chat connections
   - Runs on port 6001
   - Supports both secure and unsecure chat modes
   - Logs all messages to chat_history.log (with username and IP)
   - Displays decrypted messages for secure chat
   - Service persists after each chat session

4. **TCP Client (TCPclient.py)**
   - Initiates chat connections with other peers
   - Prompts for username (case-insensitive) to select chat partner
   - Supports both secure and unsecure chat modes
   - For secure chat, prompts for a private key (number), public key is calculated automatically
   - Messages are encrypted using a simple XOR cipher with the shared key
   - Logs all messages to chat_history.log (with username and IP)
   - Allows viewing online users and chat history from the main menu
   - Service persists after each chat session

## How to Use

1. **Start the UDP Server**
   ```bash
   python UDPserver.py
   ```
   Enter your username when prompted. This will start broadcasting your presence on the network.

2. **Start the UDP Client**
   ```bash
   python UDPclient.py
   ```
   This will show you other users who are online on the network and maintain the peers list.

3. **Start the TCP Server**
   ```bash
   python TCPserver.py
   ```
   This will allow other users to connect to you for chat. The service will continue running after each chat session.

4. **Start the TCP Client**
   ```bash
   python TCPclient.py
   ```
   When prompted:
   - Choose 'Users' to view online users and their status (Online/Away)
   - Choose 'Chat' to initiate a chat session
     - Enter the username (case-insensitive) of the user you want to chat with
     - Choose whether to use secure chat (yes/no)
     - For secure chat, enter a private key (number between 1 and 18)
   - Choose 'History' to view the chat history (with timestamp, username, IP, message, and direction)
   - The service will persist after each chat session

## Security Features

- **Secure Chat Mode**
  - Uses Diffie-Hellman key exchange (P=19, G=2)
  - User supplies a private key (number), public key is calculated automatically
  - Messages are encrypted using a simple XOR cipher with the shared key
  - Both parties must agree to use secure chat
  - Decrypted messages are displayed on the receiver's console

- **Message Logging**
  - All messages are logged to chat_history.log
  - Logs include timestamp, username, IP address, message content, and direction (SENT/RECEIVED)
  - Both Chat Initiator and Chat Responder write to the same log file

## User Status

- Users are shown as **Online** if their last broadcast was received within the last 10 seconds
- Users are shown as **Away** if their last broadcast was received within the last 15 minutes but not the last 10 seconds
- Only users seen within the last 15 minutes are displayed

## Requirements

- Python 3.x
- Standard Python libraries (socket, json, time, datetime, random, base64)

## Notes

- The application works best on the same local network
- Make sure your firewall allows UDP broadcasts and TCP connections on ports 6000 and 6001
- For secure chat, both parties must agree to use the secure mode and enter their private keys
