from cx_Freeze import setup, Executable
import ps_controller.utilities.OsHelper as osHelper

platFormBase = "Console"
if osHelper.getCurrentOs() == osHelper.WINDOWS:
    platFormBase = "Win32GUI"  # For windows to hide the console window in the back

buildOptions = dict(include_files=['Icons/'])

setup(
    name="ps_controller"
    , version="0.1"
    , description="ps_controller"
    , options=dict(build_exe=buildOptions)
    , executables=[Executable("psControllerMain.py", base=platFormBase, targetName="ps_controller.exe")]
)
