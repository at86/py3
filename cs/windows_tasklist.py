import os
import subprocess
# import StringIO
from io import BytesIO
import csv
import wat

def taskKill(imageName):
    return runCmd(['taskkill', '/im', imageName])

def runCmd(cmdArgs):
    process = subprocess.Popen(cmdArgs, stdout=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    exitcode = process.wait()

    return (exitcode, stdout, stderr)

# stdoutdata = subprocess.getoutput('tasklist /fo csv /fi "IMAGENAME eq devHttpd.exe"')
# wat.d(stdoutdata)
# reader = stdoutdata.split('\n')
# wat.d(reader)

"""
wmic process where name="devHttpd.exe" or name="python.exe" get processid, executablepath
wmic process get processid, executablepath
"""

# parentprocessid,
# /Format:Textvaluelist   /format:wmiclitableformatnosys
# CSName,Description,processid, parentprocessid, executablepath, CommandLine, name,
s='''wmic process where 'name="devHttpd.exe" or name="python.exe"' get processid, parentprocessid, executablepath'''
stdoutdata = subprocess.getoutput(s)
wat.d(stdoutdata)




# for row in reader:
#     wat.d(row)
#     # wat.d(row)
#     # if len(row) == 5:
#     #     toReturn.append(row[1])
