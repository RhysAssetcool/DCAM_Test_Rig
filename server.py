#!/usr/bin/env python3

import asyncio
from src.utils import SharedData
from src.motor_contol import MotorControl
from src.dcam import DCAMController
from src.net import Net
import os

ser_motor_port = '/dev/ttyACM0'  # Adjust this to your motor control serial port
use_serial = True  # Set to True if you want to use serial communication
HOST, PORT = "0.0.0.0", 5000

os.system('sudo ip link set can1 type can bitrate 500000')
os.system('sudo ifconfig can1 up')

async def main():

    shared_data = SharedData()

    server = Net()
    server.bind_and_listen(HOST, PORT)
    print(f"[SERVER] Listening on {HOST}:{PORT}")

    conn, addr = server.accept()
    print(f"[SERVER] Client connected: {addr}")
    motor_control = MotorControl(port=ser_motor_port, use_serial=False)  # Set to True if you want to use serial communication
    motor_control.set_sensitivity(x_sensitivity=1, y_sensitivity=0.5, z_sensitivity=0.3)
    motor_control.set_deadzone(deadzone=0.1)
    motor_control.set_acceleration(accel_rate=100, max_speed=5000)
    motor_control.invert_control(invert_x=True, invert_y=True, invert_z=False)


    dcam_controller = DCAMController(use_can=True,
                                     can_config={
                                         'channel': 'can1',
                                         'bustype': 'socketcan',
                                         'arbitration_id': 0x123
                                     })
    
    dcam_controller.set_position_range(min_position=0, max_position=30)  # Set your desired range
    dcam_controller.set_dcam_open_state(True)  # Initialize the state

    # Start the motor control handler as a background task
    motor_task = asyncio.create_task(motor_control.handle(shared_data))
    dcam_task = asyncio.create_task(dcam_controller.handle(shared_data))

    try:
        while True:
            data = conn.recv_json()
            if data:
                # Update shared data from received JSON
                shared_data.update_from_dict(data)

                # Process motor control
                motor_control.x_speed = shared_data.x_axe
                motor_control.y_speed = shared_data.y_axe
                motor_control.z_speed = shared_data.z_axe

                print(f"[SERVER] Received: {shared_data.to_dict()}")

            await asyncio.sleep(0.05)
    except KeyboardInterrupt:
        print("\n[SERVER] Stopping.")
    finally:
        conn.close()
        server.close()
        motor_control.close()
        dcam_controller.close()


if __name__ == "__main__":
    asyncio.run(main())