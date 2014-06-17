
class Constants:
    """
    Special device function constants
    """
    START = int('0x7e', 16)  # This is the first and last part of the device serial response
    ESCAPE = int('0x7d', 16)  # Indicates that the next char is an escaped char
    FLIP = int('0x20', 16)  # Used to escape chars
    NEW_LINE = int('0x0a', 16)
    RETURN = int('0x0d', 16)

    LOGGER_NAME = "PS201Logger"
