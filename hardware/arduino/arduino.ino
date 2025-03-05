#define LEFT  'L'
#define RIGHT 'R'
#define MOVE  'M'
#define STOP  'S'

int motor1A = 5;  
int motor1B = 6;  
int motor2A = 9;  
int motor2B = 10;

void setup() {
    Serial.begin(9600);
    pinMode(motor1A, OUTPUT);
    pinMode(motor1B, OUTPUT);
    pinMode(motor2A, OUTPUT);
    pinMode(motor2B, OUTPUT);
}

void loop() {
    if (Serial.available() > 0) {
        char command = Serial.read();
        Serial.println(command);

        switch (command) {
            case LEFT:
                digitalWrite(motor1A, LOW);
                digitalWrite(motor1B, HIGH);
                digitalWrite(motor2A, HIGH);
                digitalWrite(motor2B, LOW);
                break;
            case RIGHT:
                digitalWrite(motor1A, HIGH);
                digitalWrite(motor1B, LOW);
                digitalWrite(motor2A, LOW);
                digitalWrite(motor2B, HIGH);
                break;
            case MOVE:
                digitalWrite(motor1A, HIGH);
                digitalWrite(motor1B, LOW);
                digitalWrite(motor2A, HIGH);
                digitalWrite(motor2B, LOW);
                break;
            case STOP:
                digitalWrite(motor1A, LOW);
                digitalWrite(motor1B, LOW);
                digitalWrite(motor2A, LOW);
                digitalWrite(motor2B, LOW);
                break;
        }
    }
}
