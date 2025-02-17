#define IN1 5  // Forward/Stop Motor Control
#define IN2 6
#define ENA 3  // PWM for forward motor speed

#define IN3 9  // Left/Right Steering Motor Control
#define IN4 10
#define ENB 11 // PWM for steering motor speed

void setup() {
    Serial.begin(9600);

    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(ENA, OUTPUT);

    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    pinMode(ENB, OUTPUT);

    stopCar();  // Ensure everything starts in a stopped position
}

void loop() {
    if (Serial.available()) {
        char command = Serial.read();
        Serial.println(command); // Debugging output

        if (command == 'f') {
            moveForward();
        } 
        else if (command == 's') {
            stopCar();
        } 
        else if (command == 'l') {
            turnLeft();
        } 
        else if (command == 'r') {
            turnRight();
        }
    }
}

// Function to move forward
void moveForward() {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, 180);  // Adjust speed
}

// Function to stop the car
void stopCar() {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, 0);

    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, 0);
}

// Function to turn left
void turnLeft() {
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, 180);  // Adjust steering speed
}

// Function to turn right
void turnRight() {
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENB, 180);  // Adjust steering speed
}