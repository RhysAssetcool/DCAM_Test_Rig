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
from src.input import ControllerInput
from src.utils import SharedData
from src.motor_contol import MotorControl
from src.dcam import DCAMController
import time 

ser_dcam_port = '/dev/ttyACM1'  # Adjust this to your camera serial port
ser_motor_port = '/dev/ttyACM0'  # Adjust this to your motor control serial port
use_serial = True  # Set to True if you want to use serial communication

async def main():
    
    shared_data = SharedData()
    controller = ControllerInput()
    motor_control = MotorControl(port=ser_motor_port, use_serial=True)  # Set to True if you want to use serial communication
    motor_control.set_sensitivity(x_sensitivity=1, y_sensitivity=0.5, z_sensitivity=0.3)
    motor_control.set_deadzone(deadzone=0.1)
    motor_control.set_acceleration(accel_rate=100, max_speed=5000)
    motor_control.invert_control(invert_x=True, invert_y=True, invert_z=False)

    dcam_controller = DCAMController(port=ser_dcam_port, use_serial=True)  # Set to True if you want to use serial communication
    dcam_controller.set_position_range(min_position=0, max_position=3000)  # Set your desired range
    dcam_controller.set_dcam_open_state(False)  # Initialize the camera state

    # Start the motor control handler as a background task
    motor_task = asyncio.create_task(motor_control.handle(shared_data))
    dcam_task = asyncio.create_task(dcam_controller.handle(shared_data))

    prev_dcam_button = 0
    last_dcam_toggle = 0
    debounce_interval = 0.3  # seconds

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
                shared_data.z_axe = axes[3] if len(axes) > 3 else 0

                # Debounce for DCAM open toggle button
                current_dcam_button = buttons[0] if len(buttons) > 0 else 0
                now = time.time()
                if current_dcam_button and not prev_dcam_button and (now - last_dcam_toggle) > debounce_interval:
                    shared_data.dcam_open_toggle = True
                    last_dcam_toggle = now
          
    
                prev_dcam_button = current_dcam_button
                print(shared_data.dcam_open_toggle)
            await asyncio.sleep(0.05)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        controller.close()
        motor_task.cancel()
        dcam_task.cancel()
        motor_control.close()
        dcam_controller.close()
        try:
            await motor_task
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    asyncio.run(main())
# This script initializes the controller input and motor control, polls the joystick for input,
# updates the shared data, and handles motor control in a loop.
# It also handles graceful shutdown on keyboard interrupt.
