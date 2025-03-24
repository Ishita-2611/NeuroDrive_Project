import socket
import serial
import time

# Set up serial communication with Arduino
try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Check port!
    time.sleep(2)  # Allow Arduino time to reset
    ser.flush()
    print("Serial connection to Arduino established!")
except serial.SerialException as e:
    print(f"Error: Could not open serial port: {e}")
    exit(1)

# Network configuration
HOST = '0.0.0.0'
PORT = 5005

# Create and bind the server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
    try:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Listening for connections on {HOST}:{PORT}")
    except socket.error as e:
        print(f"Error: Unable to bind socket: {e}")
        exit(1)

    while True:
        print("Waiting for a connection from master RPi...")
        conn, addr = server.accept()
        print(f"Connected by {addr}")

        with conn:
            while True:
                try:
                    data = conn.recv(1024).decode().strip()
                    if not data:
                        print("Connection lost. Waiting for new connection...")
                        break
                    
                    print(f"Received command: {data}")

                    # Send command to Arduino
                    ser.write((data + "\n").encode())
                    time.sleep(0.1)  # Small delay for processing

                    # Read response from Arduino (optional)
                    response = ser.readline().decode().strip()
                    if response:
                        print(f"Arduino response: {response}")
                    else:
                        print("No response from Arduino.")

                except (socket.error, serial.SerialException) as e:
                    print(f"Error: {e}")
                    break
