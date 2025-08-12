# Joysticks
# 0, 1, 2, 3, 4, 5
# Lx, Ly, Rx, Ry, LT, RT

# Buttons
# 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
# A, B, X, Y, LB, RB, LM, RM, L3, R3

# Hats
# 0, 1 
# X, Y



import argparse
import asyncio
from src.input import ControllerInput
from src.utils import SharedData
from src.motor_contol import MotorControl
from src.dcam import DCAMController
import time
import os
import can 


def parse_args():
    parser = argparse.ArgumentParser(description="Test Rig Control Script")
    parser.add_argument('--phase', type=str, default='default', help='Phase argument for the test rig (default: %(default)s)')
    parser.add_argument('--motor-port', type=str, default='/dev/ttyACM0', help='Serial port for motor control (default: %(default)s)')
    parser.add_argument('--dcam-can-channel', type=str, default='can1', help='CAN channel for DCAM control (default: %(default)s)')
    parser.add_argument('--dcam-can-bustype', type=str, default='socketcan', help='CAN bus type for DCAM control (default: %(default)s)')
    parser.add_argument('--dcam-arbitration-id', type=int, default=0x123, help='CAN arbitration ID for DCAM control (default: %(default)s)')
    parser.add_argument('--x-axis-sensitivity', type=float, default=1.0, help='X-axis sensitivity for motor control (default: %(default)s)')
    parser.add_argument('--y-axis-sensitivity', type=float, default=0.5, help='Y-axis sensitivity for motor control (default: %(default)s)')
    parser.add_argument('--z-axis-sensitivity', type=float, default=0.3, help='Z-axis sensitivity for motor control (default: %(default)s)')
    parser.add_argument('--acceleration', type=float, default=100, help='Acceleration for motor control (default: %(default)s)')
    parser.add_argument('--max-speed', type=float, default=5000, help='Max speed for motor control (default: %(default)s)')
    return parser.parse_args()


async def main(args):

    os.system(f"sudo ip link set {args.dcam_can_channel} type can bitrate 500000")
    os.system(f"sudo ifconfig {args.dcam_can_channel} up")

    shared_data = SharedData()
    controller = ControllerInput()
    motor_control = MotorControl(port=args.motor_port)
    motor_control.set_sensitivity(x_sensitivity=args.x_axis_sensitivity, 
                                  y_sensitivity=args.y_axis_sensitivity, 
                                  z_sensitivity=args.z_axis_sensitivity)
    
    motor_control.set_deadzone(deadzone=0.1)
    motor_control.set_acceleration(accel_rate=args.acceleration, 
                                   max_speed=args.max_speed)
    motor_control.invert_control(invert_x=True, invert_y=True, invert_z=True)

    dcam_controller = DCAMController(use_can=True,
                                     can_config={
                                         'channel': args.dcam_can_channel,
                                         'bustype': args.dcam_can_bustype,
                                         'arbitration_id': args.dcam_arbitration_id
                                     })
    dcam_controller.set_position_range(min_position=0, max_position=30)
    dcam_controller.set_dcam_open_state(True)

    motor_task = asyncio.create_task(motor_control.handle(shared_data))
    dcam_task = asyncio.create_task(dcam_controller.handle(shared_data))

    prev_dcam_button = 0
    last_dcam_toggle = 0
    debounce_interval = 0.3

    try:
        while True:
            state = controller.poll()
            if state:
                axes = state['axes']
                buttons = state['buttons']
                hats = state['hats']

                shared_data.x_axe = axes[0] if len(axes) > 0 else 0
                #shared_data.y_axe = axes[1] if len(axes) > 1 else 0
                shared_data.y_axe = axes[4] if len(axes) > 4 else 0
                _, shared_data.z_axe = hats[0] if len(hats) > 0 else (0, 0)

                current_dcam_button = buttons[0] if len(buttons) > 0 else 0
                now = time.time()
                if current_dcam_button and not prev_dcam_button and (now - last_dcam_toggle) > debounce_interval:
                    shared_data.dcam_open_toggle = True
                    last_dcam_toggle = now
                prev_dcam_button = current_dcam_button
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
    
    args = parse_args()
    asyncio.run(main(args))

