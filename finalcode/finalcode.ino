#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x3F, 16, 2);  // 0x3F  

#define en 5
#define in1 6
#define in2 7
#define sensorPin 2
#define potPin A0

#define encoderStep 20
#define measuredTime 1000  // Time in milisecond
#define diameter 0.3048 //12 inch to 0.3048 mm // 66 mm to m 0.066

unsigned long currentMillis = 0, prevMillis = 0;
int steps = 0;
float rps = 0, speed = 0;
int potValue = 0;
float maxSpeed = 0, minSpeed = 0;
float wheelCircumference = 3.1416 * diameter;  // wheelCircumference = 2 * pi * radious or pi * diameter

void setup() {
  Serial.begin(9600);
  lcd.init(); lcd.backlight(); lcd.clear();
  lcd.setCursor(0, 0); lcd.print("Speed Alarm");
  lcd.setCursor(0, 1); lcd.print("  SYSTEM Kit ");

  pinMode(en, OUTPUT); pinMode(in1, OUTPUT); pinMode(in2, OUTPUT);

  pinMode(sensorPin, INPUT); pinMode(potPin, INPUT);

  delay(2000);
  lcd.clear();

  digitalWrite(in1, LOW); digitalWrite(in2, HIGH);
  // analogWrite(en, 127);
  analogWrite(en, 150);

  attachInterrupt(digitalPinToInterrupt(sensorPin), countStape, RISING);

  lcd.setCursor(0, 0); lcd.print("Speed:");
}

void loop() {
  currentMillis = millis();
  if (currentMillis - prevMillis >= measuredTime) {
    rps = steps / encoderStep;
    speed = wheelCircumference * rps *3.6;


    // if(speed > maxSpeed) maxSpeed = speed;
    // Serial.print("  Speed:"); Serial.print(speed); Serial.println("");
    lcd.setCursor(6, 0); lcd.print(speed); lcd.print(" Km/H  ");
    // lcd.setCursor(0, 0); lcd.print("Speed:"); lcd.print(speed); lcd.print(" Km/H  ");
    // lcd.setCursor(0, 1); lcd.print("Max:"); lcd.print(maxSpeed); lcd.print(" Km/H  ");
    
    prevMillis = currentMillis;
    steps = 0;
  }

  potValue = analogRead(potPin);

  // Serial.print(" Raw: "); Serial.print(potValue);
  // Serial.print(" Step: "); Serial.println(steps);

  potValue = map(potValue, 0, 1023, 0, 245);
  analogWrite(en, potValue); //digitalWrite(in1, LOW); digitalWrite(in2, HIGH);

  // Serial.print(" Mapped:");
  // Serial.print(potValue);  
}

void countStape() {
  steps++;
}