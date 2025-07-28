import os
import sys
import struct
import can

# Configuration
CAN_INTERFACE = 'can1'
CAN_ID_BASE = 0x05080000  # Extended frame base
ENABLE_CMD = 0x01
DISABLE_CMD = 0x02
SPEED_CMD = 0x07

def send_can_message(bus, cmd_byte, data=b''):
    can_id = CAN_ID_BASE | cmd_byte
    msg = can.Message(
        arbitration_id=can_id,
        data=data,
        is_extended_id=True
    )
    try:
        bus.send(msg)
        print(f"[INFO] Sent: ID={hex(can_id)} DATA={data.hex()}")
    except can.CanError as e:
        print(f"[ERROR] CAN send failed: {e}")

def send_enable(bus):
    send_can_message(bus, ENABLE_CMD)

def send_disable(bus):
    send_can_message(bus, DISABLE_CMD)

def send_speed(bus, rpm):
    if not -800 <= rpm <= 800:
        print("[ERROR] RPM out of range (-800 to 800)")
        return
    speed_value = int(-rpm * 3200 / 60)
    hex_speed = struct.pack("<i", speed_value)
    send_can_message(bus, SPEED_CMD, hex_speed)

def main():

    bus = can.interface.Bus(channel=CAN_INTERFACE, bustype='socketcan')

    print("Pump CAN CLI Controller")
    print("Commands:")
    print("  on         - Enable the motor")
    print("  off        - Disable the motor")
    print("  speed NUM  - Set speed in RPM (-800 to 800)")
    print("  quit       - Exit")

    while True:
        try:
            cmd = input(">> ").strip().lower()
            if cmd == "on":
                send_enable(bus)
            elif cmd == "off":
                send_disable(bus)
            elif cmd.startswith("speed"):
                try:
                    _, value = cmd.split()
                    rpm = int(value)
                    send_speed(bus, rpm)
                except (ValueError, IndexError):
                    print("[ERROR] Usage: speed <RPM>")
            elif cmd == "quit":
                print("Exiting.")
                break
            else:
                print("[ERROR] Unknown command.")
        except KeyboardInterrupt:
            print("\n[INFO] Interrupted. Exiting.")
            break

if __name__ == "__main__":
    os.system('sudo ifconfig can0 down')
    os.system('sudo ip link set can0 type can bitrate 500000')
    os.system('sudo ifconfig can0 up')
    os.system('sudo ifconfig can1 down')
    os.system('sudo ip link set can1 type can bitrate 500000')
    os.system('sudo ifconfig can1 up')
    main()
