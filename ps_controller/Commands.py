__author__ = 'mannsi'

_WRITE_OUTPUT_VOLTAGE = int('0xd0', 16)
_WRITE_OUTPUT_CURRENT = int('0xd1', 16)
_WRITE_INPUT_VOLTAGE = int('0xd2', 16)
_WRITE_PRE_REGULATOR_VOLTAGE = int('0xd3', 16)
_WRITE_ALL_VALUE = int('0xa5', 16)
_WRITE_IS_OUTPUT_ON = int('0xc4', 16)
_WRITE_TARGET_VOLTAGE = int('0xe0', 16)
_WRITE_TARGET_CURRENT = int('0xe1', 16)
_READ_TARGET_VOLTAGE = int('0xc0', 16)
_READ_TARGET_CURRENT = int('0xc1', 16)
_TURN_ON_OUTPUT = int('0xc2', 16)
_TURN_OFF_OUTPUT = int('0xc3', 16)
_ACKNOWLEDGE = int('0x06', 16)
_NOT_ACKNOWLEDGE = int('0x15', 16)
_HANDSHAKE = int('0xa0', 16)


class BaseCommand:
    """
    A command given to the PS201 device.
    A command is always interpreted from the device point of view (i.e. a WriteX command means device writes)
    """
    def int_value(self) -> int:
        raise NotImplementedError()

    def readable(self) -> str:
        raise NotImplementedError()

    def __eq__(self, other):
        return self.int_value() == other.int_value()


class WriteAllValuesCommand(BaseCommand):
    def int_value(self):
        return _WRITE_ALL_VALUE

    def readable(self):
        return "Write all values"


class WriteInputVoltageCommand(BaseCommand):
    def int_value(self):
        return _WRITE_INPUT_VOLTAGE

    def readable(self):
        return "Write input voltage"


class WriteIsOutputOnCommand(BaseCommand):
    def int_value(self):
        return _WRITE_IS_OUTPUT_ON

    def readable(self):
        return "Write is output on"


class WriteOutputCurrentCommand(BaseCommand):
    def int_value(self):
        return _WRITE_OUTPUT_CURRENT

    def readable(self):
        return "Write output current"


class WriteOutputVoltageCommand(BaseCommand):
    def int_value(self):
        return _WRITE_OUTPUT_VOLTAGE

    def readable(self):
        return "Write output voltage"


class WritePreRegVoltageCommand(BaseCommand):
    def int_value(self):
        return _WRITE_PRE_REGULATOR_VOLTAGE

    def readable(self):
        return "Write pre reg voltage"


class WriteTargetVoltageCommand(BaseCommand):
    def int_value(self):
        return _WRITE_TARGET_VOLTAGE

    def readable(self):
        return "Write target voltage"


class WriteTargetCurrentCommand(BaseCommand):
    def int_value(self):
        return _WRITE_TARGET_CURRENT

    def readable(self):
        return "Write target current"


class ReadTargetVoltageCommand(BaseCommand):
    def int_value(self):
        return _READ_TARGET_VOLTAGE

    def readable(self):
        return "Read target voltage"


class ReadTargetCurrentCommand(BaseCommand):
    def int_value(self):
        return _READ_TARGET_CURRENT

    def readable(self):
        return "Read target current"


class TurnOnOutputCommand(BaseCommand):
    def int_value(self):
        return _TURN_ON_OUTPUT

    def readable(self):
        return "Turn on output"


class TurnOffOutputCommand(BaseCommand):
    def int_value(self):
        return _TURN_OFF_OUTPUT

    def readable(self):
        return "Turn off output"


class AcknowledgementCommand(BaseCommand):
    """
    PS201 responds with this command when it acknowledges the command given to it
    """
    def int_value(self):
        return _ACKNOWLEDGE

    def readable(self):
        return "Acknowledgement"


class NotAcknowledgementCommand(BaseCommand):
    """
    PS201 responds with this command when it does not acknowledges the command given to it
    """
    def int_value(self):
        return _NOT_ACKNOWLEDGE

    def readable(self):
        return "Not acknowledgement"


class HandshakeCommand(BaseCommand):
    """
    Command sent to PS201 to establish connection. PS201 will respond with AcknowledgementCommand
    """
    def int_value(self):
        return _HANDSHAKE

    def readable(self):
        return "Handshake"


def get_command(command_int_value: int) -> BaseCommand:
    if command_int_value == _WRITE_OUTPUT_VOLTAGE:
        return WriteOutputVoltageCommand()
    elif command_int_value == _WRITE_OUTPUT_CURRENT:
        return WriteOutputCurrentCommand()
    elif command_int_value == _WRITE_INPUT_VOLTAGE:
        return WriteInputVoltageCommand()
    elif command_int_value == _WRITE_PRE_REGULATOR_VOLTAGE:
        return WritePreRegVoltageCommand()
    elif command_int_value == _WRITE_ALL_VALUE:
        return WriteAllValuesCommand()
    elif command_int_value == _WRITE_IS_OUTPUT_ON:
        return WriteIsOutputOnCommand()
    elif command_int_value == _WRITE_TARGET_VOLTAGE:
        return WriteTargetVoltageCommand()
    elif command_int_value == _WRITE_TARGET_CURRENT:
        return WriteTargetCurrentCommand()
    elif command_int_value == _READ_TARGET_VOLTAGE:
        return ReadTargetVoltageCommand()
    elif command_int_value == _READ_TARGET_CURRENT:
        return ReadTargetCurrentCommand()
    elif command_int_value == _TURN_ON_OUTPUT:
        return TurnOnOutputCommand()
    elif command_int_value == _TURN_OFF_OUTPUT:
        return TurnOffOutputCommand()
    elif command_int_value == _ACKNOWLEDGE:
        return AcknowledgementCommand()
    elif command_int_value == _NOT_ACKNOWLEDGE:
        return NotAcknowledgementCommand()