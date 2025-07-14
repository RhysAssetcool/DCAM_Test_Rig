import pygame
import time

# Initialize Pygame
pygame.init()

# Initialize the joystick
pygame.joystick.init()

# Check for joystick
if pygame.joystick.get_count() == 0:
    print("No joystick connected")
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick name: {joystick.get_name()}")
    print(f"Joystick ID: {joystick.get_id()}")

    try:
        while True:
            # Process Pygame events
            pygame.event.pump()



            # Get axis values
            axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]
            print(f"Axes: {axes}")

            # Get button values
            buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
            print(f"Buttons: {buttons}")

            # Get hat values
            hats = [joystick.get_hat(i) for i in range(joystick.get_numhats())]
            print(f"Hats: {hats}")

            # Wait for a short period to avoid flooding the console
            time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting...")

# Quit Pygame
pygame.quit()