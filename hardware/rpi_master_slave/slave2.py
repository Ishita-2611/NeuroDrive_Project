import socket
import serial
import time

# Set up serial communication with Arduino
try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Adjust port if needed
    ser.flush()
    print("Serial connection to Arduino established!")
except serial.SerialException as e:
    print(f"Error: Could not open serial port: {e}")
    exit(1)

# Network configuration
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 5005       # Port for communication with master RPi

# Create and bind the server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse socket
    try:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Listening for connections on {HOST}:{PORT}")
    except socket.error as e:
        print(f"Error: Unable to bind socket: {e}")
        exit(1)

    while True:
        print("Waiting for a connection from master RPi...")
        conn, addr = server.accept()  # Accept a connection
        print(f"Connected by {addr}")

        with conn:
            while True:
                try:
                    data = conn.recv(1024).decode().strip()  # Receive command
                    if not data:
                        print("Connection lost. Waiting for new connection...")
                        break
                    
                    print(f"Received command: {data}")

                    # Send command to Arduino
                    ser.write((data + "\n").encode())  
                    print("Command sent to Arduino!")

                except (socket.error, serial.SerialException) as e:
                    print(f"Error: {e}")
                    break
