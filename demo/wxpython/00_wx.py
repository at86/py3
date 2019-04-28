# coding:utf-8

#
import os
# os.system("C:/python3/python -OO -m PyInstaller -w --onefile -y wxmain.py")
# os.system("C:/python3/python -OO -m PyInstaller -w -y wxmain.py")
os.system("C:/python3/python -OO -m PyInstaller -p ./lib -w -y wxmain.py")


# pyinstaller --onedir --windowed --runtime-hook='.\_pyinstaller_hooks\runtime_hooks\use_lib.py'
