import socket
import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define Motor Pins
STEER_IN1 = 17  # Left
STEER_IN2 = 18  # Right
MOVE_IN3 = 22  # Forward
MOVE_IN4 = 23  # Backward
PWM_ENA = 12  # Speed control for steering
PWM_ENB = 13  # Speed control for movement

# Setup Pins
GPIO.setup([STEER_IN1, STEER_IN2, MOVE_IN3, MOVE_IN4], GPIO.OUT)
GPIO.setup([PWM_ENA, PWM_ENB], GPIO.OUT)

# PWM Setup
pwm_steering = GPIO.PWM(PWM_ENA, 1000)  # 1kHz frequency
pwm_movement = GPIO.PWM(PWM_ENB, 1000)

pwm_steering.start(0)  # Start with 0 duty cycle
pwm_movement.start(0)

# Function to Control Motors
def move_car(command):
    if command == "L":  # Turn Left
        GPIO.output(STEER_IN1, GPIO.HIGH)
        GPIO.output(STEER_IN2, GPIO.LOW)
        pwm_steering.ChangeDutyCycle(80)  # Adjust speed
    
    elif command == "R":  # Turn Right
        GPIO.output(STEER_IN1, GPIO.LOW)
        GPIO.output(STEER_IN2, GPIO.HIGH)
        pwm_steering.ChangeDutyCycle(80)
    
    elif command == "M":  # Move Forward
        GPIO.output(MOVE_IN3, GPIO.HIGH)
        GPIO.output(MOVE_IN4, GPIO.LOW)
        pwm_movement.ChangeDutyCycle(90)
    
    elif command == "S":  # Stop
        GPIO.output(STEER_IN1, GPIO.LOW)
        GPIO.output(STEER_IN2, GPIO.LOW)
        GPIO.output(MOVE_IN3, GPIO.LOW)
        GPIO.output(MOVE_IN4, GPIO.LOW)
        pwm_steering.ChangeDutyCycle(0)
        pwm_movement.ChangeDutyCycle(0)

# TCP Server Setup
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5005

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"Listening on {HOST}:{PORT}")

    conn, addr = server.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            command = data.decode().strip()
            print(f"Received Command: {command}")
            move_car(command)

# Cleanup
GPIO.cleanup()