import sys
from cx_Freeze import setup, Executable
# atdo 编译后不能引入pyside2

build_exe_options = {
    # "packages": ["os"],
    "excludes": ["tkinter"],
    "include_msvcr": True,
    'includes': ['shiboken2'],
}

base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

sys.argv = ['setup.py', 'build']

setup(name="Hello World",
      version="1.0",
      description="cx_Freeze PyQt Hello World",
      options={"build_exe": build_exe_options},
      executables=[Executable("cs.py", base=base, targetName="pyside2cs_cx.exe")])
