# P2P-CHAT

A peer-to-peer chat application that allows users to discover and communicate with other users on the same network.

## Features

- Automatic peer discovery using UDP broadcasts
- Support for both secure and unsecure chat options
- Secure chat using Diffie-Hellman key exchange
- Message logging for chat history
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

3. **TCP Server (TCPserver.py)**
   - Handles incoming chat connections
   - Runs on port 6001
   - Supports both secure and unsecure chat modes
   - Logs all messages to chat_history.log

4. **TCP Client (TCPclient.py)**
   - Initiates chat connections with other peers
   - Supports both secure and unsecure chat modes
   - Logs all messages to chat_history.log

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
   This will show you other users who are online on the network.

3. **Start the TCP Server**
   ```bash
   python TCPserver.py
   ```
   This will allow other users to connect to you for chat.

4. **Start a Chat**
   ```bash
   python TCPclient.py
   ```
   When prompted:
   - Enter the IP address of the user you want to chat with
   - Choose whether to use secure chat (yes/no)

## Security Features

- **Secure Chat Mode**
  - Uses Diffie-Hellman key exchange (P=19, G=2)
  - Messages are encrypted using a simple XOR cipher with the shared key
  - Both parties must agree to use secure chat

- **Message Logging**
  - All messages are logged to chat_history.log
  - Logs include timestamp, IP address, message content, and direction (sent/received)

## Requirements

- Python 3.x
- Standard Python libraries (socket, json, time, datetime, random)

## Notes

- The application works best on the same local network
- Make sure your firewall allows UDP broadcasts and TCP connections on ports 6000 and 6001
- For secure chat, both parties must agree to use the secure mode