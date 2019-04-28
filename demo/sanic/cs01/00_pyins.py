# import sys
# # from distutils.core import setup
# #
# # sys.argv = ['pyinstaller.py', 'build']
# #
# # # setup(name='at86', version='0.1', description='at86', options=options, executables=executables)
# # setup(name='at86')


import shutil
import os

# os.system("C:/python3/python -OO -m PyInstaller -w -y -n 0watsen --onefile main.py")
os.system("C:/python3/python -OO -m PyInstaller main.py")

shutil.copyfile('i.html', 'dist/i.html')
shutil.copyfile('cs_sqlite.db', 'dist/cs_sqlite.db')


# import sys
# # import pyinstaller_setuptools
# from pyinstaller_setuptools import setup
# sys.argv = ['pyinstaller.py', 'build']
# setup(
#     scripts=['main.py'],
# )
