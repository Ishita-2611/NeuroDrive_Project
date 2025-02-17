import serial
import time

# Connect to the HC-05 Bluetooth Module via RFCOMM
bluetooth = serial.Serial('/dev/rfcomm0', baudrate=9600, timeout=1)

def send_command(command):
    bluetooth.write(command.encode())
    print(f"Sent: {command}")

try:
    while True:
        command = input("Enter Command (f=Forward, s=Stop, l=Left, r=Right): ")
        if command in ['f', 's', 'l', 'r']:
            send_command(command)
        else:
            print("Invalid Command! Use: f, s, l, r")
except KeyboardInterrupt:
    print("Disconnected")
    bluetooth.close()
