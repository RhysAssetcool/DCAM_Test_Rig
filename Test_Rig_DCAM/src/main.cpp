#include <Arduino.h>
#include <Servo.h>

#define ACTUATOR_1 5
#define ACTUATOR_2 6

Servo actuator1;
Servo actuator2;

// Define PWM range and corresponding position range
const int PWM_MIN = 1000;  // Minimum pulse width in microseconds
const int PWM_MAX = 2000;  // Maximum pulse width in microseconds
const int POSITION_MIN = -1;
const int POSITION_MAX = 3000;  // in mm

// Define feedback range
const int FEEDBACK_MIN = 640;
const int FEEDBACK_MAX = 70;

int targetPosition = 0;

void moveToPosition(Servo& actuator, int targetPosition) 
{
  int pwmValue = map(targetPosition, POSITION_MIN, POSITION_MAX, PWM_MIN, PWM_MAX);
  actuator.writeMicroseconds(pwmValue);  // Ensure using writeMicroseconds for precise control
}

void setAllActuatorsToPosition(int targetPosition) 
{
  moveToPosition(actuator1, targetPosition);
  moveToPosition(actuator2, targetPosition);
}

void setup() 
{
  Serial.begin(115200);         // Start serial communication at 9600 bps
  actuator1.attach(ACTUATOR_1);
  actuator2.attach(ACTUATOR_2);
  setAllActuatorsToPosition(POSITION_MIN);
}

void loop() 
{
  // Check if new data is available from the serial monitor
  if (Serial.available()) 
  {
    String input = Serial.readStringUntil('\n');
    int first = input.indexOf(',');
    int second = input.indexOf(',', first + 1);

    if (first != -1 && second != -1) 
    {
      int part1 = input.substring(0, first).toInt();
      int part2 = input.substring(first + 1, second).toInt();
      int part3 = input.substring(second + 1).toInt();
      targetPosition = part1;
    }
  }

    if (targetPosition >= POSITION_MIN && targetPosition <= POSITION_MAX) 
    {
      setAllActuatorsToPosition(targetPosition);
    }
}
