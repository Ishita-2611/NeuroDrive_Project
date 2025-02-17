import serial
import time

# Connect to the HC-05 Bluetooth Module via RFCOMM
bluetooth = serial.Serial('/dev/rfcomm0', baudrate=9600, timeout=1)

def send_command(command):
    bluetooth.write(command.encode())
    print(f"Sent: {command}")

try:
    while True:
        command = input("Enter Command (w=Forward, s=Backward, a=Left, d=Right, x=Stop): ")
        if command in ['w', 's', 'a', 'd', 'x']:
            send_command(command)
        else:
            print("Invalid Command! Use: w, s, a, d, x")
except KeyboardInterrupt:
    print("Disconnected")
    bluetooth.close()