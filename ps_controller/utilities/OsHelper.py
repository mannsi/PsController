import platform

WINDOWS = 10
LINUX = 20
OSX = 30


def get_current_os():
    """ Gets the running operating system
    :return: int -- Operating system as defined in this file
    """
    system_name = platform.system()
    if system_name == "Windows":
        return WINDOWS
    elif system_name == "Darwin":
        return OSX
    else:
        return LINUX