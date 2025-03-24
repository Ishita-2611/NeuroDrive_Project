#include <Arduino.h>
#include <string.h>
#include <ctype.h>

#define LEFT  'L'
#define RIGHT 'R'
#define MOVE  'M'
#define STOP  'S'

// Motor A (Left Motor)
const int motor1A = 5;  // IN1
const int motor1B = 6;  // IN2
const int ENA = 3;     // Enable/Speed control for Motor A

// Motor B (Right Motor)
const int motor2A = 9;  // IN3
const int motor2B = 10; // IN4
const int ENB = 11;    // Enable/Speed control for Motor B

// Motor speed settings
const int NORMAL_SPEED = 180;  // Normal running speed (0-255)
const int TURN_SPEED = 160;    // Speed during turns
const int STOP_SPEED = 0;      // Stop speed

// Command processing variables
String inputCommand = "";
boolean commandComplete = false;

void setup() {
    // Initialize serial communication
    Serial.begin(9600);
    inputCommand.reserve(10); // Reserve 10 bytes for incoming commands

    // Configure motor control pins
    pinMode(motor1A, OUTPUT);
    pinMode(motor1B, OUTPUT);
    pinMode(motor2A, OUTPUT);
    pinMode(motor2B, OUTPUT);
    pinMode(ENA, OUTPUT);
    pinMode(ENB, OUTPUT);
    
    // Initial state - motors stopped
    stopMotors();
}

void loop() {
    // Process commands when received
    if (commandComplete) {
        processCommand(inputCommand);
        // Reset for next command
        inputCommand = "";
        commandComplete = false;
    }
}

// Serial event handler - called when new data arrives
void serialEvent() {
    while (Serial.available()) {
        char inChar = (char)Serial.read();
        
        // Process on newline
        if (inChar == '\n') {
            commandComplete = true;
        } else {
            inputCommand += inChar;
        }
    }
}

void processCommand(String command) {
    command.trim();  // Remove any whitespace
    
    if (command.length() != 1) {
        Serial.println("Invalid Command!");
        stopMotors();
        return;
    }

    char cmd = command.charAt(0);
    cmd = toupper(cmd);  // Convert to uppercase

    switch (cmd) {
        case LEFT:
            turnLeft();
            Serial.println(LEFT);  // Echo command
            break;
            
        case RIGHT:
            turnRight();
            Serial.println(RIGHT);  // Echo command
            break;
            
        case MOVE:
            moveForward();
            Serial.println(MOVE);  // Echo command
            break;
            
        case STOP:
            stopMotors();
            Serial.println(STOP);  // Echo command
            break;
            
        default:
            Serial.println("Invalid Command!");
            stopMotors();
            break;
    }
}

void moveForward() {
    // Set motor directions
    digitalWrite(motor1A, HIGH);
    digitalWrite(motor1B, LOW);
    digitalWrite(motor2A, HIGH);
    digitalWrite(motor2B, LOW);
    
    // Set motor speeds
    analogWrite(ENA, NORMAL_SPEED);
    analogWrite(ENB, NORMAL_SPEED);
}

void turnLeft() {
    // Left motor backward, right motor forward
    digitalWrite(motor1A, LOW);
    digitalWrite(motor1B, HIGH);
    digitalWrite(motor2A, HIGH);
    digitalWrite(motor2B, LOW);
    
    // Set turning speeds
    analogWrite(ENA, TURN_SPEED);
    analogWrite(ENB, TURN_SPEED);
}

void turnRight() {
    // Left motor forward, right motor backward
    digitalWrite(motor1A, HIGH);
    digitalWrite(motor1B, LOW);
    digitalWrite(motor2A, LOW);
    digitalWrite(motor2B, HIGH);
    
    // Set turning speeds
    analogWrite(ENA, TURN_SPEED);
    analogWrite(ENB, TURN_SPEED);
}

void stopMotors() {
    // Stop both motors
    digitalWrite(motor1A, LOW);
    digitalWrite(motor1B, LOW);
    digitalWrite(motor2A, LOW);
    digitalWrite(motor2B, LOW);
    
    // Set speeds to zero
    analogWrite(ENA, STOP_SPEED);
    analogWrite(ENB, STOP_SPEED);
}
