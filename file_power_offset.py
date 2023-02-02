from smart_meter.smart_meter import SmartMeter


class FilePowerOffset:
    def __init__(self, file_name: str, smart_meter: SmartMeter):
        self.file_name = file_name

        smart_meter.modifiers.append(self.get_power_offset)

    def get_power_offset(self):
        f = open(self.file_name, 'r')
        offset = float(f.readline())
        return offset
