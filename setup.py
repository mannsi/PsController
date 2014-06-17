from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages


setup(
    name="ps_controller"
    , version="0.1"
    , description="ps_controller"
    , packages=find_packages()
    , install_requires=[
        "APScheduler == 2.1.1",
        "crcmod == 1.7",
        "pyserial == 2.7",
        "cherrypy == 3.2.4"
    ]
    , scripts=["psControllerMain.py"]
    , entry_points={
        "console_scripts": [
            "ps_controller = psControllerMain:run"

        ]
    }
)
