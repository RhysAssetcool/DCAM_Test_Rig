#include <Arduino.h>
#include <AccelStepper.h>

// Motor setup: DRIVER mode, STEP and DIR pins
AccelStepper stepperZ(AccelStepper::DRIVER, 4, 3);  // Z-axis (zoom)
AccelStepper stepperY(AccelStepper::DRIVER, 7, 6);  // Y-axis (tilt)
AccelStepper stepperX(AccelStepper::DRIVER, 10, 9);  // X-axis (pan)

void setup() {
  Serial.begin(115200);

  // Configure X-axis motor
  stepperX.setEnablePin(2);  // Enable pin for X-axis
  stepperX.setMaxSpeed(1000);     // Max steps/sec
  stepperX.setAcceleration(300);  // Smoother movement

  // Configure Y-axis motor
  stepperY.setEnablePin(5);  // Enable pin for Y-axis
  stepperY.setMaxSpeed(800);      // Less speed if lower microstepping
  stepperY.setAcceleration(250);

  // Configure Z-axis motor
  stepperZ.setEnablePin(8);  // Enable pin for Z-axis
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
// #include <Arduino.h>
// #include <AccelStepper.h>

// const int MICROSTEPS_PER_REV = 3200;

// // Helper to convert revolutions to microsteps
// long revToMicrosteps(float revolutions) {
//   return (long)(revolutions * MICROSTEPS_PER_REV);
// }

// // Define stepper motor connections and interface type
// #define X_STEP_PIN 10
// #define X_DIR_PIN 9
// #define Y_STEP_PIN 7
// #define Y_DIR_PIN 6
// #define Z_STEP_PIN 4
// #define Z_DIR_PIN 3

// AccelStepper stepperX(AccelStepper::DRIVER, X_STEP_PIN, X_DIR_PIN);
// AccelStepper stepperY(AccelStepper::DRIVER, Y_STEP_PIN, Y_DIR_PIN);
// AccelStepper stepperZ(AccelStepper::DRIVER, Z_STEP_PIN, Z_DIR_PIN);

// void setup() {
//   Serial.begin(9600);

//   stepperX.setMaxSpeed(8000);
//   stepperX.setAcceleration(4000);
//   stepperX.moveTo(revToMicrosteps(2)); // Move X 2 revolutions

//   stepperY.setMaxSpeed(8000);
//   stepperY.setAcceleration(4000);
//   stepperY.moveTo(revToMicrosteps(3)); // Move Y 3 revolutions

//   stepperZ.setMaxSpeed(8000);
//   stepperZ.setAcceleration(4000);
//   stepperZ.moveTo(revToMicrosteps(1)); // Move Z 1 revolution
// }

// void loop() {
//   if (stepperX.distanceToGo() == 0) {
//     stepperX.moveTo(-stepperX.currentPosition());
//   }
//   if (stepperY.distanceToGo() == 0) {
//     stepperY.moveTo(-stepperY.currentPosition());
//   }
//   if (stepperZ.distanceToGo() == 0) {
//     stepperZ.moveTo(-stepperZ.currentPosition());
//   }

//   stepperX.run();
//   stepperY.run();
//   stepperZ.run();
// }