import sys
import struct
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QLineEdit, QLabel, QMessageBox
)
import can

# Configuration
CAN_INTERFACE = 'can0'
CAN_ID_BASE = 0x05080000  # Extended frame base
ENABLE_CMD = 0x01
DISABLE_CMD = 0x02
SPEED_CMD = 0x07

class StepperControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.bus = can.interface.Bus(channel=CAN_INTERFACE, bustype='socketcan')

    def initUI(self):
        self.setWindowTitle("Pump CAN Control")

        layout = QVBoxLayout()

        self.speed_label = QLabel("Enter Speed (-800 to 800 RPM):")
        layout.addWidget(self.speed_label)

        self.speed_input = QLineEdit()
        layout.addWidget(self.speed_input)

        self.set_button = QPushButton("Set Speed")
        self.set_button.clicked.connect(self.send_speed)
        layout.addWidget(self.set_button)

        self.on_button = QPushButton("ON")
        self.on_button.clicked.connect(self.send_enable)
        layout.addWidget(self.on_button)

        self.off_button = QPushButton("OFF")
        self.off_button.clicked.connect(self.send_disable)
        layout.addWidget(self.off_button)

        self.setLayout(layout)

    def send_enable(self):
        self.send_can_message(ENABLE_CMD)

    def send_disable(self):
        self.send_can_message(DISABLE_CMD)

    def send_speed(self):
        try:
            rpm = int(self.speed_input.text())
            if not -800 <= rpm <= 800:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid integer between -800 and 800.")
            return

        # Convert RPM to pulse/sec (UIM242 uses pulses/sec, but manual testing assumes RPM direct)
        speed_value = int(-rpm * 3200/60)  # Scale as needed, assumed 10 pulses per RPM
        hex_speed = struct.pack("<i", speed_value)  # 4-byte little-endian signed int
        self.send_can_message(SPEED_CMD, hex_speed)

    def send_can_message(self, cmd_byte, data=b''):
        can_id = CAN_ID_BASE | cmd_byte  # Extend CAN ID with command
        msg = can.Message(
            arbitration_id=can_id,
            data=data,
            is_extended_id=True
        )
        try:
            self.bus.send(msg)
            print(f"Sent: ID={hex(can_id)} DATA={data.hex()}")
        except can.CanError as e:
            QMessageBox.critical(self, "CAN Error", f"Failed to send message: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StepperControlApp()
    window.show()
    sys.exit(app.exec_())