# coding:utf-8
"""
拷贝到目标/pages/目录
"""
import sys
# sys.path.append("/Volumes/py/tool")

# import setuptools  # important
from distutils.core import setup

from Cython.Build import cythonize
from Cython.Compiler import Options

Options.docstrings = False
Options.emit_code_comments = False

import os
import wat
import shutil

# setup(
#     name='Hello world app',
#     # ext_modules = cythonize("watcef.py"),
#     ext_modules=cythonize(
#         [
#             "watcef.py",
#             # "watcef2.py",
#             # "s/cscef.py",
#         ],
#         compiler_directives={
#             # # 'embedsignature': True,
#             # 'docstrings': False,#3.0, but stable is 0.29.2
#             # 'emit_code_comments ': False,
#         }),
# )

# buildFiles = [
#     # "../wx/lib/watcef.py",
#     # "../wx/watpage/cscef.py",
#     "../wx/lib/*.py",
#     "../wx/watpage/*.py",
# ]
# excludeFiles = [
#     # "*/__init__.py",
#     "../wx/watpage/__init__.py",
#     "../wx/lib/__init__.py",
# ]


"""
a __init__.py will make pyd in it's dir,
or the pyd will be in build out dir
"""

def fileRecPy(dirname, pyfile):
    """get *.py but exclude __init__.py, give cython compile to pyd"""
    files = os.listdir(dirname)
    for f in files:
        dirnew = dirname + '/' + f  # os.path.sep
        if os.path.isdir(dirnew):
            print('dir: ', dirnew)
            fileRecPy(dirnew, pyfile)
        else:
            if os.path.splitext(dirnew)[1] == '.py':
                if os.path.basename(dirnew) != '__init__.py':
                    pyfile.append(dirnew)
            print('file: ', dirnew)


# fileRec(os.getcwd())

builds = [
    "../pages",
]
buildFiles = []
for dir1 in builds:
    # dir1 = os.path.abspath(dir1)
    print(dir1)
    fileRecPy(dir1, buildFiles)
print(buildFiles)

buildDir = 'build'
# print buildDir

# python setup.py build_ext --inplace
# print sys.argv
# change to below, run this settu.py from ide run
sys.argv = ['setup.py', 'build_ext', '--inplace']

setup(
    name='watsen',
    ext_modules=cythonize(
        buildFiles,
        language_level=2,
        # exclude=excludeFiles,
        build_dir=buildDir,
        # compiler_directives={
        #     # 'embedsignature': True,
        #     'docstrings': False,#3.0, but stable is 0.29.2
        #     # 'emit_code_comments ': False,
        # },
    ),
)

def fileRecPyd(dirname, pyfile):
    """get *.pyd files"""
    dirname = dirname.replace("../", "", 1)
    files = os.listdir(dirname)
    for f in files:
        dirnew = dirname + '/' + f  # os.path.sep
        if os.path.isdir(dirnew):
            print('dir: ', dirnew)
            fileRecPyd(dirnew, pyfile)
        else:
            fend = os.path.splitext(dirnew)[1]
            if fend == '.pyd' or fend == '.so':
                pyfile.append(dirnew)
            print('file: ', dirnew, fend)

pydFiles = []
for dir1 in builds:
    wat.d(dir1)
    fileRecPyd(dir1, pydFiles)

# PYC_FILE_REOBJ = re.compile('^(.*?)(\..*)?(\.pyc)$')

print(pydFiles)
for f in pydFiles:
    dst = '../' + f
    f2 = os.path.splitext(dst)[0]
    fend = os.path.splitext(dst)[1]
    f2 = os.path.splitext(f2)[0]
    dstPyd = f2 + fend  # mac .so  ; win .pyd;
    wat.d(dstPyd)
    shutil.copyfile(f, dstPyd)
    # # atdo pyc exist then copy pyd replace the pyc
    # if os.path.isfile(dstPyc):
    #     pass
    #     # os.remove(dstPyc)
    #     # shutil.copyfile(f, dst)
    # # elif f.find('wat.pyd')>=0:
    # #     shutil.copyfile(f, dst)
