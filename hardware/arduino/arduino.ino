#define LEFT  'L'
#define RIGHT 'R'
#define MOVE  'M'
#define STOP  'S'

int motor1A = 5;  
int motor1B = 6;  
int motor2A = 9;  
int motor2B = 10;
int ENA = 3;  // PWM Speed Control Motor 1
int ENB = 11; // PWM Speed Control Motor 2

void setup() {
    Serial.begin(9600); // Start Serial Communication

    // Set motor control pins as outputs
    pinMode(motor1A, OUTPUT);
    pinMode(motor1B, OUTPUT);
    pinMode(motor2A, OUTPUT);
    pinMode(motor2B, OUTPUT);
    pinMode(ENA, OUTPUT);
    pinMode(ENB, OUTPUT);
    
    // Set initial motor speed (0-255)
    analogWrite(ENA, 180);
    analogWrite(ENB, 180);
}

void loop() {
    if (Serial.available() > 0) {
        char command = Serial.read();
        Serial.println(command); // Print received command
        
        switch (command) {
            case LEFT:
                turnLeft();
                break;
            case RIGHT:
                turnRight();
                break;
            case MOVE:
                moveForward();
                break;
            case STOP:
                stopMotors();
                break;
            default:
                Serial.println("Invalid Command!");
                stopMotors();
        }
    }
}

void moveForward() {
    digitalWrite(motor1A, HIGH);
    digitalWrite(motor1B, LOW);
    digitalWrite(motor2A, HIGH);
    digitalWrite(motor2B, LOW);
}

void turnLeft() {
    digitalWrite(motor1A, LOW);
    digitalWrite(motor1B, HIGH);
    digitalWrite(motor2A, HIGH);
    digitalWrite(motor2B, LOW);
}

void turnRight() {
    digitalWrite(motor1A, HIGH);
    digitalWrite(motor1B, LOW);
    digitalWrite(motor2A, LOW);
    digitalWrite(motor2B, HIGH);
}

void stopMotors() {
    digitalWrite(motor1A, LOW);
    digitalWrite(motor1B, LOW);
    digitalWrite(motor2A, LOW);
    digitalWrite(motor2B, LOW);
}
