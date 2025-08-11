class SharedData:
    def __init__(self):
        self.x_axe = 0
        self.y_axe = 0
        self.z_axe = 0
        self.dcam_open_toggle = 0

    def to_dict(self):
        return {
            "x_axe": float(self.x_axe),
            "y_axe": float(self.y_axe),
            "z_axe": float(self.z_axe),
            "dcam_open_toggle": int(self.dcam_open_toggle),
        }

    def update_from_dict(self, d: dict):
        self.x_axe = float(d.get("x_axe", 0))
        self.y_axe = float(d.get("y_axe", 0))
        self.z_axe = float(d.get("z_axe", 0))
        self.dcam_open_toggle = int(d.get("dcam_open_toggle", 0))
        return self
