
class Constants:
    """
    Special device function constants
    """
    START = int('0x7e', 16)  # This is the first and last part of the device serial response
    #ACKNOWLEDGE = int('0x06', 16)  # Device send this as command if it acknowledged the last command
    #NOT_ACKNOWLEDGE = int('0x15', 16)  # Device send this as command if it did not acknowledged the last command
    ESCAPE = int('0x7d', 16)  # Indicates that the next char is an escaped char
    FLIP = int('0x20', 16)  # Used to escape chars
    NEW_LINE = int('0x0a', 16)
    RETURN = int('0x0d', 16)

    LOGGER_NAME = "PS201Logger"

    """
    connection states
    """
    CONNECTED = "Connected"
    DISCONNECTED = "Disconnected"
    NO_DEVICE_FOUND = "No device found"