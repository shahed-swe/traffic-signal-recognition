int x;
bool pin11Active = false;
unsigned long pin11StartTime = 0;
const long interval = 100; // Blinking interval for pins 8, 9, and 10
const long delayInterval = 4000; // Duration to keep pin 11 HIGH

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  digitalWrite(11, LOW); // Ensure pin 11 is initially LOW
}

void loop() {
  x = Serial.readString().toInt();

  // Blink pins 8, 9, and 10
  unsigned long currentMillis = millis();
  static unsigned long previousBlinkMillis = 0;

  if (currentMillis - previousBlinkMillis >= interval) {
    previousBlinkMillis = currentMillis;

    digitalWrite(8, HIGH);
    delay(100);  
    digitalWrite(8, LOW);
    delay(100); 
    digitalWrite(9, HIGH);
    delay(100); 
    digitalWrite(9, LOW);
    delay(100); 
    digitalWrite(10, HIGH);
    delay(100); 
    digitalWrite(10, LOW);
    delay(100); 
  }

  // Check if x is greater than 0
  if (x > 19) {
    digitalWrite(11, HIGH);
    pin11Active = true;
  }

  if (!pin11Active) {
    // Start the timer for pin 11
    // pin11Active = true;
    pin11StartTime = currentMillis;
    // digitalWrite(11, HIGH); // Turn on pin 11
  } else if (currentMillis - pin11StartTime >= delayInterval) {
    // Turn off pin 11 after 3 seconds
    pin11Active = false;
    digitalWrite(11, LOW); // Turn off pin 11
  }
}
