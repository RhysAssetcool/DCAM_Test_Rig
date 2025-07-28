import asyncio
import can
import serial
import logging
from src.utils import SharedData

# --- Configure Logger ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Adjust as needed

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)  # Set to DEBUG, INFO, etc.

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(ch)


class DCAMController:
    def __init__(self,
                 use_serial=True,
                 use_can=False,
                 serial_config=None,
                 can_config=None):

        # Validate interface choice
        if use_serial and use_can:
            raise ValueError("Cannot use both serial and CAN simultaneously.")

        self.use_serial = use_serial
        self.use_can = use_can

        self.dcam_current_position = 0
        self.dcam_new_position = 0
        self._dcam_max_position = 30
        self._dcam_min_position = 0
        self._dcam_open_state: bool = False

        self.serial_config = serial_config or {
            'port': '/dev/ttyACM1',
            'baudrate': 115200,
            'timeout': 1
        }

        self.can_config = can_config or {
            'channel': 'can0',
            'bustype': 'socketcan',
            'arbitration_id': 0x123
        }

        self.ser = None
        self.bus = None

        if self.use_serial:
            try:
                self.ser = serial.Serial(**self.serial_config)
                logger.info(f"Serial connection opened on {self.serial_config['port']}")
            except serial.SerialException as e:
                logger.error(f"Failed to open serial port: {e}")
                raise

        elif self.use_can:
            try:
                self.bus = can.interface.Bus(channel=self.can_config['channel'],
                                             bustype=self.can_config['bustype'])
                logger.info(f"CAN bus initialized on {self.can_config['channel']}")
            except can.CanError as e:
                logger.error(f"Failed to initialize CAN bus: {e}")
                raise

        self._send_command(self.dcam_current_position, 0, 0)

    # --- Accessors ---
    def get_dcam_open_state(self):
        return self._dcam_open_state

    def set_dcam_open_state(self, state: bool):
        self._dcam_open_state = state

    def get_position(self):
        return self.dcam_current_position

    def set_position_range(self, min_position=0, max_position=100):
        self._dcam_min_position = min_position
        self._dcam_max_position = max_position

    def get_position_range(self):
        return self._dcam_min_position, self._dcam_max_position

    # --- Internal Logic ---
    def _handle_position(self):
        self.dcam_new_position = self._dcam_max_position if self._dcam_open_state else self._dcam_min_position

    def _send_command(self, pos: int, aux1: int = 0, aux2: int = 0):
        if self.use_serial and self.ser and self.ser.is_open:
            command = f"{pos},{aux1},{aux2}\n"
            self.ser.write(command.encode('utf-8'))
            logger.debug(f"[Serial] Sent: {command.strip()}")

        elif self.use_can and self.bus:
            data = [pos & 0xFF, pos & 0xFF] + [0] * 6
            msg = can.Message(arbitration_id=self.can_config['arbitration_id'],
                              data=data,
                              is_extended_id=False)
            try:
                self.bus.send(msg)
                logger.debug(f"[CAN] Sent: {msg}")
            except can.CanError as e:
                logger.error(f"[CAN] Send failed: {e}")

    # --- Main Loop ---
    async def handle(self, shared_data: SharedData):
        while True:
            if shared_data.dcam_open_toggle:
                logger.info("DCAM open toggle pressed")
                self._dcam_open_state = not self._dcam_open_state
                self._handle_position()
                shared_data.dcam_open_toggle = False

            if self.dcam_current_position != self.dcam_new_position:
                self._send_command(self.dcam_new_position, 0, 0)
                self.dcam_current_position = self.dcam_new_position
                logger.info(f"DCAM position set to: {self.dcam_current_position}")

            await asyncio.sleep(0.1)

    # --- Cleanup ---
    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            logger.info("Serial port closed.")
        if self.bus:
            self.bus.shutdown()
            logger.info("CAN bus shut down.")
