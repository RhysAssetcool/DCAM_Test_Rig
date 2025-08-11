class SharedData:
    def __init__(self):
        self.x_axe = 0
        self.y_axe = 0
        self.z_axe = 0
        self.dcam_open_toggle = 0

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(d):
        return SharedData(**d)