import psutil


class Battery:
    def __init__(self):
        self.psutil = psutil

    @property
    def battery(self):
        return psutil.sensors_battery()

    @property
    def is_plugged(self):
        is_plugged = self.battery.power_plugged
        if is_plugged is None: 
            print("transitioning between plug in and plug out")
            return False
        else:
            return is_plugged

    @property
    def percent(self):
        return self.battery.percent

    @battery.setter
    def battery(self, value):
        pass

    @is_plugged.setter
    def is_plugged(self, value):
        pass

    @percent.setter
    def percent(self, value):
        pass

    def __call__(self):
        return (self.is_plugged, self.percent)