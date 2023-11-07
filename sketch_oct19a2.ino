int x;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  digitalWrite(13, LOW); // Ensure pin 11 is initially LOW
}

void loop() {
  x = Serial.readString().toInt();


  Serial.print(x);
  if (x > 29) {
    digitalWrite(13, HIGH);
    delay(2000);
    digitalWrite(13, LOW);
  }
}
