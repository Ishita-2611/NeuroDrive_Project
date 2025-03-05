import socket
import serial

# Set up serial communication with Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Adjust port as needed
ser.flush()

HOST = '0.0.0.0'
PORT = 5005

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f"Listening on {HOST}:{PORT}")

    conn, addr = server.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break
            print(f"Received: {data}")

            # Send command to Arduino
            ser.write((data + "\n").encode())
