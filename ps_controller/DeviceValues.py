class DeviceValues:
    def __init__(self):
        self.output_is_on = False
        self.target_voltage = 0
        self.target_current = 0
        self.input_voltage = 0
        self.output_voltage = 0
        self.output_current = 0
        self.pre_reg_voltage = 0

    def to_json(self):
        return self.__dict__