import serial

car_arduino = serial.Serial('COM4', 9600)  # Change COM port for your car Arduino

def send_command_to_car(command):
    car_arduino.write(command.encode())
    print(f"Sent Command: {command}")

# Example:
send_command_to_car('F')  # Forward
send_command_to_car('S')  # Stop
send_command_to_car('L')  # Left
send_command_to_car('R')  # Right