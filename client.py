import time
from src.net import Net
from src.utils import SharedData
import asyncio
from src.input import ControllerInput

HOST, PORT = "192.168.107.160", 5000  # change HOST to your server IP
SEND_INTERVAL = 0.05            # ~20 Hz
DEBOUNCE = 0.30                 # seconds for toggle button


async def main():
    # Connect network
    controller = ControllerInput()
    sd = SharedData()
    net = Net()
    net.connect(HOST, PORT)
    print(f"[CLIENT] Connected to {HOST}:{PORT}")

    prev_dcam_button = 0
    last_dcam_toggle = 0

    try:
        while True:
            state = controller.poll()
            if state:
                axes = state['axes']
                buttons = state['buttons']
                hats = state['hats']

                # Update shared data based on joystick input
                sd.x_axe = axes[0] if len(axes) > 0 else 0
                sd.y_axe = axes[1] if len(axes) > 1 else 0
                sd.z_axe = axes[3] if len(axes) > 3 else 0

                # Debounce for DCAM open toggle button
                current_dcam_button = buttons[0] if len(buttons) > 0 else 0
                now = time.time()

                # Toggle DCAM open state with debounce
                if current_dcam_button and not prev_dcam_button and (now - last_dcam_toggle) > DEBOUNCE:
                    sd.dcam_open_toggle = current_dcam_button
                    last_dcam_toggle = now
                else:
                    sd.dcam_open_toggle = 0
                prev_dcam_button = current_dcam_button

                print(prev_dcam_button, current_dcam_button, sd.dcam_open_toggle)
                net.send_json(sd.to_dict())

            await asyncio.sleep(SEND_INTERVAL)
            

    except KeyboardInterrupt:
        print("\n[CLIENT] Stopping.")
    finally:
        net.close()
        controller.close()
if __name__ == "__main__":
    asyncio.run(main())
