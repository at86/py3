# coding:utf-8
import os
import signal
import subprocess
import wat
# import json
import demjson

import wx
import wx.dataview

import psutil

import wx.lib.mixins.listctrl as listmix

# def kill_child_processes(parent_pid, sig=signal.SIGTERM):
#     try:
#         parent = psutil.Process(parent_pid)
#     except psutil.NoSuchProcess:
#         return
#     children = parent.children(recursive=True)
#     for process in children:
#         process.send_signal(sig)

# proc = subprocess.Popen('dir')
# proc = subprocess.Popen('D:\hack\devTools\php-7.0.27-nts-Win32-VC14-x86\devPhp-cgi70.exe -i')

# proc1 = subprocess.Popen('D:\hack\devTools\php-7.0.27-nts-Win32-VC14-x86\php.exe -i')

# , listmix.ColumnSorterMixin
class TestListCtrl(wx.ListCtrl, listmix.CheckListCtrlMixin, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        # self.SetDoubleBuffered(True)
        listmix.CheckListCtrlMixin.__init__(self)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        # listmix.ColumnSorterMixin.__init__(self,3)
        self.setResizeColumn(3)

    def OnCheckItem(self, index, flag):
        print(index, flag)

    # def GetListCtrl(self):
    #     return self

# , listmix.ColumnSorterMixin
class TestListCtrl2(wx.dataview.DataViewListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, *args, **kwargs):
        wx.dataview.DataViewListCtrl.__init__(self, *args, **kwargs)
        # self.SetDoubleBuffered(True)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        # listmix.ColumnSorterMixin.__init__(self,3)
        self.setResizeColumn(4)

    def OnCheckItem(self, index, flag):
        print(index, flag)

    # def GetListCtrl(self):
    #     return self

devToolCfg = '''[
    {
        "name": "devNginx",
        "dir": "D:/hack/devTools/nginx/",
        "path": "devNginx",
        "param": [],
        "btn": null,
        "autoRun": true,
    },
    {
        "name": "devApache",
        "dir": "D:/hack/devTools/Apache/",
        "path": "bin/devHttpd",
        "param": [],
        "btn": null,
        "sepBar": true,
    },
    {
        "name": "devMysqld57",
        "dir": "D:/hack/devTools/mysql-5.7.20-win32/",
        "path": "bin/devMysqld57",
        "param": ["--defaults-file=0my1.ini", "--log_syslog=0"],
        "btn": null,
    },
    {
        "name": "devMysqld55",
        "dir": "D:/hack/devTools/Mysql-5.5.53-win32/",
        "path": "bin/devMysqld55",
        "param": ["--defaults-file=my.ini",],
        "btn": null,
        "sepBar": true,
    },
    {
        "name": "devPhp-cgi70",
        "dir": "D:/hack/devTools/php-7.0.27-nts-Win32-VC14-x86/",
        "path": "devPhp-cgi70",
        "param": ["-b", "localhost:9070", "-c", "php.ini",],
        "btn": null,
    },
    {
        "name": "devPhp-cgi71",
        "dir": "D:/hack/devTools/php-7.1.13-nts-Win32-VC14-x86/",
        "path": "devPhp-cgi71",
        "param": ["-b", "localhost:9071", "-c", "php.ini",],
        "btn": null,
        "sepBar": true,
    },
    {
        "name": "devRedis-server",
        "dir": "D:/hack/devTools/redis/",
        "path": "devRedis-server",
        "param": [],
        "btn": null,
    },
    {
        "name": "devMemcached",
        "dir": "D:/hack/devTools/memcached/",
        "path": "devMemcached",
        "param": [],
        "btn": null,
        "sepBar": true,
    },
    {
        "name": "devGitea",
        "dir": "D:/hack/devTools/gitea/",
        "path": "devGitea",
        "param": ["web",],
        "btn": null,
        "need": ["devMysqld55"],
        "retry": 3,
        "retryIntervalTime": 6000,
        "sepBar": true,
    },
]'''
devToolCfg = demjson.decode(devToolCfg)

app = wx.App()

hideF = wx.Frame(parent=None, id=wx.ID_ANY, title='ssss', size=wx.Size(440, 360))
bs = wx.BoxSizer(orient=wx.VERTICAL)

bs_btns = wx.WrapSizer()
bs.Add(bs_btns, 0, wx.EXPAND, 0)

bs_list = wx.BoxSizer(orient=wx.VERTICAL)
bs.Add(bs_list, 1, wx.EXPAND, 0)
# panel = wx.Panel(hideF, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
# panel.SetDoubleBuffered(True)
# panel.SetSizer(bs_list)
# panel.Layout()
# bs_list.Fit(panel)

# # list_ctrl = wx.ListCtrl(hideF, size=(-1, -1), style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES) #wx.LC_VIRTUAL|
# # listmix.CheckListCtrlMixin.__init__(list_ctrl)
# # listmix.ListCtrlAutoWidthMixin.__init__(list_ctrl)
# list_ctrl = TestListCtrl(hideF, size=(-1, -1), style=wx.LC_REPORT) #wx.LC_VIRTUAL||wx.LC_HRULES|wx.LC_VRULES
# list_ctrl.InsertColumn(0, 'Name',width=140)
# list_ctrl.InsertColumn(1, 'Start',width=140)
# list_ctrl.InsertColumn(2, 'Path')
# # list_ctrl.Arrange()

list_ctrl = wx.dataview.DataViewListCtrl(hideF, size=(-1, -1), style=wx.LC_REPORT)  # wx.LC_VIRTUAL||wx.LC_HRULES|wx.LC_VRULES
# list_ctrl = TestListCtrl2(hideF, size=(-1, -1), style=wx.LC_REPORT)  # wx.LC_VIRTUAL||wx.LC_HRULES|wx.LC_VRULES

list_ctrl.AppendToggleColumn("开启", width=40)
list_ctrl.AppendTextColumn('Name', width=wx.COL_WIDTH_AUTOSIZE)
list_ctrl.AppendTextColumn('Start', width=wx.COL_WIDTH_AUTOSIZE)
list_ctrl.AppendTextColumn('Path', width=wx.COL_WIDTH_AUTOSIZE)
# list_ctrl.

bs_list.Add(list_ctrl, 1, wx.EXPAND | wx.ALL, 0)

index = 0
for devTool in devToolCfg:
    # list_ctrl.InsertItem(index,devTool['name'])
    # list_ctrl.SetItem(index, 1, devTool['path'])
    # list_ctrl.SetItem(index, 2, devTool['dir'])
    # atdo listCtrl
    # list_ctrl.Append([devTool['name'], devTool['path'], devTool['dir']])
    # atdo DataViewListCtrl
    list_ctrl.AppendItem([False, devTool['name'], devTool['path'], devTool['dir']])

    # list_ctrl.SetItemData(index, index)
    index += 1
# print devToolCfg
# cols = list_ctrl.GetColumns()

# print list_ctrl.GetSize() # (100, 80) will be real size after frame show()
widthAll = 0
for col in range(0, list_ctrl.GetColumnCount()):
    item = list_ctrl.GetColumn(col)
    if col > 0:
        item.Width = item.Width + 12
    widthAll = widthAll + item.Width
# print list_ctrl.GetSize() # (100, 80) will be real size after frame show()


proc = None
btn1 = wx.Button(hideF, label="nginx start")
def btn1click(event):
    global proc
    if proc is None or proc.returncode is not None:
        print '11', 'proc is None, open new subprocess'
        # proc = subprocess.Popen('D:/hack/devTools/nginx/devNginx.exe',cwd="D:/hack/devTools/nginx/")
        # atdo os.setsid not for windows
        # proc = subprocess.Popen('D:/hack/devTools/nginx/devNginx.exe',cwd="D:/hack/devTools/nginx/",preexec_fn=os.setsid)
        proc = subprocess.Popen('D:/hack/devTools/nginx/devNginx.exe', cwd="D:/hack/devTools/nginx/")
    print '11=>', 'poll:', proc.poll(), '; pid:', proc.pid, ':returncode', proc.returncode
    print proc
    ps1 = psutil.Process(proc.pid)
    # print ps1.as_dict()
    print ps1.exe()

btn1.Bind(wx.EVT_BUTTON, btn1click)
bs_btns.Add(btn1)

btn2 = wx.Button(hideF, label="nginx close")
def btn2click(event):
    global proc
    print proc.returncode
    # if proc is not None :
    if proc.returncode is None:  # atdo means has been terminate
        # proc.terminate()
        # proc.kill() # atdo nginx, only close main process
        # atdo killpg() not for windows
        # os.killpg(os.getpgid(proc.pid), signal.SIGHUP)
        # os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

        print 'kill process'
        try:
            parent = psutil.Process(proc.pid)
        except psutil.NoSuchProcess:
            return
        children = parent.children()  # recursive=True
        for process in children:
            process.send_signal(signal.SIGTERM)
            print process

        # proc.kill() returncode
        proc.terminate()
        proc.wait()  # atdo use wait() block andl make sure process terminate, then poll() is ok
        proc.poll()
    else:
        print 'has been killed'

btn2.Bind(wx.EVT_BUTTON, btn2click)
bs_btns.Add(btn2)

hideF.SetSizer(bs)
hideF.Show()
sz = list_ctrl.GetSize()
w = sz.Width + 20
wat.d(hideF.GetSize())
# hideF.SetSize(w,hideF.GetSize().GetHeight())
hideF.SetSize(widthAll + 30, hideF.GetSize().GetHeight())
wat.d(hideF.GetSize())

# proc = subprocess.Popen('D:/hack/devTools/nginx/devNginx.exe',cwd="D:/hack/devTools/nginx/")
# # proc.wait()
# wat.d( 'parent')


# , stdout=subprocess.PIPE
# process = subprocess.Popen(['D:/hack/devTools/nginx/devNginx.exe', '-t'],cwd="D:/hack/devTools/nginx/")
# process = subprocess.Popen(['D:/hack/devTools/nginx/devNginx.exe', '-t'],cwd="D:/hack/devTools/nginx/", stdout=subprocess.PIPE)
# stdout = process.communicate()[0]
# print 'STDOUT:{}'.format(stdout)

# process = subprocess.Popen(['D:/hack/devTools/nginx/devNginx.exe', '-t'],cwd="D:/hack/devTools/nginx/", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# out,err = process.communicate()
# print 'out',out  # nginx -t output in stderr
# print 'err',err

# output = check_output('nginx -t'.split(), stderr=STDOUT)

app.MainLoop()

# proc.terminate()


wx.Exit()


# a ='''{
#     "name": "devGitea",
#     "dir": "D:/hack/devTools/gitea/",
#     "path": "devGitea",
#     "param": ["web",],
#     "btn": null,
#     "need": ["devMysqld55"],
#     "retry": 3,
#     "retryIntervalTime": 6000,
#     "sepBar": true,
# }'''
#
# print a
# # a=json.loads(a)
# a=demjson.decode(a)
# print a['retry'],a['path']
