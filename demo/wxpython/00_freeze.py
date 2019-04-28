import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    # "packages": ["os"],
    "excludes": ["tkinter"],
    "include_msvcr": True
}

base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

# sys.argv = ['setup.py', 'build_ext', '--inplace']
sys.argv = ['setup.py', 'build']

setup(name="Hello World",
      version="1.0",
      description="cx_Freeze PyQt Hello World",
      options={"build_exe": build_exe_options},
      executables=[Executable("wxmain.py", base=base, targetName="wxmain_cx.exe")])
