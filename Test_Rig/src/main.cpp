#include <Arduino.h>
#include <AccelStepper.h>

// Motor setup: DRIVER mode, STEP and DIR pins
AccelStepper stepperX(AccelStepper::DRIVER, 3, 2);  // X-axis (pan)
AccelStepper stepperY(AccelStepper::DRIVER, 6, 5);  // Y-axis (tilt)
AccelStepper stepperZ(AccelStepper::DRIVER, 9, 8);  // Z-axis (zoom)

void setup() {
  Serial.begin(115200);

  // Configure X-axis motor
  stepperX.setEnablePin(4);  // Enable pin for X-axis
  stepperX.setMaxSpeed(1000);     // Max steps/sec
  stepperX.setAcceleration(300);  // Smoother movement

  // Configure Y-axis motor
  stepperY.setEnablePin(7);  // Enable pin for Y-axis
  stepperY.setMaxSpeed(800);      // Less speed if lower microstepping
  stepperY.setAcceleration(250);

  // Configure Z-axis motor
  stepperZ.setEnablePin(10);  // Enable pin for Z-axis
  stepperZ.setMaxSpeed(600);
  stepperZ.setAcceleration(200);

  // Enable all motors
  stepperX.enableOutputs();
  stepperY.enableOutputs();
  stepperZ.enableOutputs();

}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    int first = input.indexOf(',');
    int second = input.indexOf(',', first + 1);

    if (first > 0 && second > first) {
      int xSpeed = input.substring(0, first).toInt();
      int ySpeed = input.substring(first + 1, second).toInt();
      int zSpeed = input.substring(second + 1).toInt();

      stepperX.setSpeed(xSpeed);
      stepperY.setSpeed(ySpeed);
      stepperZ.setSpeed(zSpeed);
    }
  }

  stepperX.runSpeed();
  stepperY.runSpeed();
  stepperZ.runSpeed();
}
