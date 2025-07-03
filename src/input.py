
class ControllerInput:

    def __init__(self):
        import pygame
        self.pygame = pygame
        self.pygame.init()
        self.pygame.joystick.init()
        if self.pygame.joystick.get_count() == 0:
            print("No joystick connected")
            self.joystick = None
        else:
            self.joystick = self.pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Joystick name: {self.joystick.get_name()}")
            print(f"Joystick ID: {self.joystick.get_id()}")

    def poll(self):
        if not self.joystick:
            return None
        self.pygame.event.pump()
        axes = [self.joystick.get_axis(i) for i in range(self.joystick.get_numaxes())]
        buttons = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
        hats = [self.joystick.get_hat(i) for i in range(self.joystick.get_numhats())]
        return {'axes': axes, 'buttons': buttons, 'hats': hats}

    def close(self):
        self.pygame.quit()