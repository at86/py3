# encoding:utf-8

import psutil
import os
import demjson
import setproctitle

PROCNAME = "devNginx"
#
# pids=[]
# for proc in psutil.process_iter():
#     if proc.name() == PROCNAME:
#         print(proc)
#     if proc.name().find(PROCNAME)!=-1:
#         print(proc)
#         pids.append(proc.pid)
# pids.sort()
# print pids

cfg = open('../wx/watsen/pages/devtools.js').read()
# print cfg
setproctitle.setproctitle('Hello, world!')
print 22,setproctitle.getproctitle()
cfg = cfg[cfg.find('['):]
cfg = demjson.decode(cfg)

cfgExes = []
for dev in cfg:
    exe = dev['dir'] + dev['path']
    cfgExes.append(exe.replace('/', '\\'))
print cfgExes[0]
# print cfgExes
# print cfg

# f='D:\\hack\\devTools\\nginx\\devNginx.exe'.replace('.exe','')
# print f
# print f in cfgExes

pids = []
for proc in psutil.process_iter():
    if proc.name().find(PROCNAME) != -1:
        # print proc.as_dict()
        # print proc.pid,proc.children()[0].pid
        # print(proc.exe()[:-4])
        if proc.exe()[:-4] in cfgExes:
            proc
            print proc.cwd(), proc.name()
            print 'ok find'
        pids.append(proc.pid)
pids.sort()
for pid in pids:
    # print psutil.Process(pid).parent().pid
    par = psutil.Process(pid).parent()
    if par is None or par is not None and par.pid not in pids:
        print psutil.Process(pid).as_dict()
        print 'find parent'
print pids
# os.system("pause")