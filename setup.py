from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages
from ps_controller import __version__

setup(
    name="PsController"
    , version=__version__
    , description="Software used to control the DPS201"
    , packages=find_packages()
    , install_requires=[
        "crcmod == 1.7",
        "pyserial == 2.7",
        "cherrypy == 3.2.4"
    ]
    #, data_files=[('/etc/init.d', ['ps_web_server/auto_start_script/ps_web_server'])]
    , package_data={'ps_web_server': ['css/*.css', 'fonts/museo/*', 'js/*.js', 'index.html']}
    , scripts=["psControllerMain.py"]
    , entry_points={
        "console_scripts": [
            "PsController = psControllerMain:run"

        ]
    }
)