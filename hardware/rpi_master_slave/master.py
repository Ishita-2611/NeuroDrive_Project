import socket
import time
import random

SLAVE_IP = "192.168.8.126"  # Replace with your slave RPi's IP
PORT = 5005

COMMANDS = ['L', 'R', 'M', 'S']

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((192.168.8.126, PORT))
    print(f"Connected to {SLAVE_IP}:{PORT}")

    while True:
        cmd = random.choice(COMMANDS)  # Send a random command
        client.sendall(cmd.encode())
        print(f"Sent: {cmd}")
        time.sleep(2)  # Adjust the delay as needed
