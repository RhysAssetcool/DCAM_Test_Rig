# Joysticks
# 0, 1, 2, 3, 4, 5
# Lx, Ly, Rx, Ry, LT, RT

# Buttons
# 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
# A, B, X, Y, LB, RB, LM, RM, L3, R3

# Hats
# 0, 1 
# X, Y


import asyncio
from input import ControllerInput
from utils import SharedData
from motor_contol import MotorControl
async def main():
    
    shared_data = SharedData()
    controller = ControllerInput()
    motor_control = MotorControl(use_serial=False)  # Set to True if you want to use serial communication

    # Start the motor control handler as a background task
    motor_task = asyncio.create_task(motor_control.handle(shared_data))

    try:
        while True:
            state = controller.poll()
            if state:
                axes = state['axes']
                buttons = state['buttons']
                hats = state['hats']

                # Update shared data based on joystick input
                shared_data.x_axe = axes[0] if len(axes) > 0 else 0
                shared_data.y_axe = axes[1] if len(axes) > 1 else 0
                shared_data.z_axe = axes[2] if len(axes) > 2 else 0
                shared_data.fire = buttons[0] if len(buttons) > 0 else 0

                # print(f"Axes: {shared_data.x_axe}, {shared_data.y_axe}, {shared_data.z_axe}")
                # print(f"Buttons: {shared_data.fire}")

            await asyncio.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        controller.close()
        motor_task.cancel()
        try:
            await motor_task
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    asyncio.run(main())
# This script initializes the controller input and motor control, polls the joystick for input,
# updates the shared data, and handles motor control in a loop.
# It also handles graceful shutdown on keyboard interrupt.
