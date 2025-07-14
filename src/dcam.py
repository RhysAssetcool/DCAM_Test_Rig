import serial
from src.utils import SharedData
import asyncio

class DCAMController:
    def __init__(self, 
                 port='/dev/ttyACM1', 
                 baudrate=115200, 
                 timeout=1, 
                 use_serial=True):
        
        self.use_serial = use_serial

        self.dcam_current_position = 0
        self.dcam_new_position = 0
        self._dcam_max_position = 100  # Set a default max position
        self._dcam_min_position = 0    # Set a default min position
        self._dcam_open_state : bool = False
        self.ser = None

        if self.use_serial:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
            command = f"{self.dcam_current_position},{0},{0}\n"
            self.ser.write(command.encode('utf-8'))


    def get_dcam_open_state(self):
        return self.dcam_open_state

    def set_dcam_open_state(self, state: bool):
        self.dcam_open_state = state

    def get_position(self):
        return self.dcam_current_position

    def set_position_range(self, min_position=0, max_position=100):
        self._dcam_min_position = min_position
        self._dcam_max_position = max_position

    def get_position_range(self):
        return self._dcam_min_position, self._dcam_max_position

    def _handle_position(self):
        if self._dcam_open_state == True:
            self.dcam_new_position = self._dcam_max_position
        else:   
            self.dcam_new_position = self._dcam_min_position

    async def handle(self, shared_data: SharedData):
        while True:
            if shared_data.dcam_open_toggle:
                print("DCAM open toggle pressed")
                self._dcam_open_state = not self._dcam_open_state
                self._handle_position()
                shared_data.dcam_open_toggle = False

            if self.dcam_current_position != self.dcam_new_position and self.use_serial:
                command = f"{self.dcam_new_position},{0},{0}\n"
                self.ser.write(command.encode('utf-8'))
                self.dcam_current_position = self.dcam_new_position
                print (f"DCAM position set to: {self.dcam_current_position}")

            await asyncio.sleep(0.1)

    def close(self):
        if self.use_serial and self.ser.is_open and self.ser:
            self.ser.close()