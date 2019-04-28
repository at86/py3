#coding=utf-8

import sys
from cx_Freeze import setup, Executable

base = None
# if sys.platform == 'win32':
#     base = 'Win32GUI'

options = {
    'build_exe': {
        # 'includes': 'json,atexit',
        'includes': 'asyncio,encodings',
    }
}

executables = [
    Executable('main.py', base=base)
]
sys.argv = ['cxfreeze.py', 'build']

setup(name='sanic_cs01',
      version='0.1',
      description='sanic_cs01 desc',
      options=options,
      executables=executables
      )
