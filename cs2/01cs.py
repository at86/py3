import os
import sys

# __file__ by cxfreeze.py will error of __file__
# url=os.path.join(os.path.dirname(os.path.abspath(__file__)),"sample1.html")


def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)

path=os.getcwd()
print path
url=os.path.join(os.getcwd(),"/sample1.html") # D:/sample1.html
print url
url= path+"/sample1.html"
print url
sys.exit(0)