void setup() {
  Serial.begin(115200);  // Baud rate for PC communication
}

void loop() {
  int ch1 = analogRead(A0);
  int ch2 = analogRead(A1);
  int ch3 = analogRead(A2);
  int ch4 = analogRead(A3);

  // Send EEG data as CSV over Serial
  Serial.print(ch1);
  Serial.print(",");
  Serial.print(ch2);
  Serial.print(",");
  Serial.print(ch3);
  Serial.print(",");
  Serial.print(ch4);
  Serial.println();

  delay(10);  // Sampling rate adjustment (can be changed)
}