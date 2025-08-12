## Running the Pumps

If you want to run the pumps, open another terminal, SSH into the test rig, navigate to the same `~/DCAM_Test_Rig` directory, and run:

```sh
python run_pumps.py
```

# DCAM Test Rig Control

This program provides a command-line interface to control a test rig using a joystick, motor controller, and DCAM (via CAN or serial). It uses Python's `argparse` module to allow flexible configuration via command-line arguments.

## Requirements
- Python 3.8+
- `pygame` (for joystick input)
- `pyserial` (for serial communication)
- `python-can` (for CAN bus communication)
- Appropriate permissions to bring up CAN interfaces (may require `sudo`)


## Usage

1. SSH into the test rig:

	```sh
	ssh <username>@<test_rig_ip>
	```

2. Navigate to the program directory:

	```sh
	cd ~/DCAM_Test_Rig
	```

3. Run the program from the command line:

	```sh

	# DCAM Test Rig Control

	## Overview
	This program provides a command-line interface to control a test rig using a joystick, motor controller, and DCAM (via CAN or serial). It is designed for flexible configuration and operation via command-line arguments.

	---

	## Table of Contents
	- [Requirements](#requirements)
	- [Setup](#setup)
	- [Usage](#usage)
	- [Command-Line Arguments](#command-line-arguments)
	- [Running the Pumps](#running-the-pumps)
	- [Notes](#notes)
	- [Troubleshooting](#troubleshooting)
	- [License](#license)

	---

	## Requirements
	- Python 3.8+
	- `pygame` (for joystick input)
	- `pyserial` (for serial communication)
	- `python-can` (for CAN bus communication)
	- Appropriate permissions to bring up CAN interfaces (may require `sudo`)

	---

	## Setup
	1. **SSH into the test rig:**
		```sh
		ssh user@kamino
		```
	2. **Navigate to the program directory:**
		```sh
		cd ~/DCAM_Test_Rig
		```
	3. **Dependencies:**
		The required Python packages are already installed on the test rig. You do not need to install them again.

	---

	## Usage
	Run the main control program with:
	```sh
	python Test_Rig_Control.py [OPTIONS]
	```

	### Example
	```sh
	python Test_Rig_Control.py \
	  --motor-port COM3 \
	  --dcam-can-channel can0 \
	  --x-axis-sensitivity 1.2 \
	  --y-axis-sensitivity 0.7 \
	  --z-axis-sensitivity 0.5 \
	  --acceleration 150 \
	  --max-speed 6000
	```

	---

	## Command-Line Arguments

	| Argument                  | Type    | Default      | Description                                      |
	|--------------------------|---------|--------------|--------------------------------------------------|
	| `--phase`                | str     | default      | Phase argument for the test rig                  |
	| `--motor-port`           | str     | /dev/ttyACM0 | Serial port for motor control                    |
	| `--dcam-can-channel`     | str     | can1         | CAN channel for DCAM control                     |
	| `--dcam-can-bustype`     | str     | socketcan    | CAN bus type for DCAM control                    |
	| `--dcam-arbitration-id`  | int     | 0x123        | CAN arbitration ID for DCAM control              |
	| `--x-axis-sensitivity`   | float   | 1.0          | X-axis sensitivity for motor control             |
	| `--y-axis-sensitivity`   | float   | 0.5          | Y-axis sensitivity for motor control             |
	| `--z-axis-sensitivity`   | float   | 0.3          | Z-axis sensitivity for motor control             |
	| `--acceleration`         | float   | 100          | Acceleration for motor control                   |
	| `--max-speed`            | float   | 5000         | Max speed for motor control                      |

	---

	## Running the Pumps

	If you want to run the pumps, open another terminal, SSH into the test rig, navigate to the same `~/DCAM_Test_Rig` directory, and run:

	```sh
	python run_pumps.py
	```

	---

	## Notes
	- Ensure your joystick is connected before running the program.
	- The program will print status and debug information to the console.
	- Use `Ctrl+C` to exit the program safely.

	---

	## Troubleshooting
	- If you see "No joystick connected", check your joystick connection and try again.
	- If serial or CAN initialization fails, ensure the correct port/channel and permissions.

	---

	## License
	MIT License