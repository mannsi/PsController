class DeviceValues:
    def __init__(self):
        self.output_is_on = False
        self.target_voltage = 0  # 1V is value 1000
        self.target_current = 0  # 1A is value 1000
        self.output_voltage = 0  # 1V is value 1000
        self.output_current = 0  # 1A is value 1000

    def to_json(self):
        return self.__dict__
