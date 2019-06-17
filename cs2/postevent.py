#encoding:utf-8
import wx
import threading
class frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title='ssss')  # , size=(480, 320)
        self.btn = wx.Button(self, id=wx.ID_ANY, label="queue")
        self.Bind(wx.EVT_BUTTON, self.ddd, self.btn)


    def ddd(self,event):
        print 'Frame >> clicked'

    def PrintMain(self):
        print 'Frame >> PostEvent() >>'
        iRet = wx.PostEvent(self,wx.CommandEvent(wx.EVT_BUTTON.typeId,self.btn.GetId()))
        return iRet


app = wx.App()

f=frame()
f.Show()
f.PrintMain()

class TestThread(threading.Thread):
    def __init__(self,f):
        # 线程实例化时立即启动
        threading.Thread.__init__(self)
        self.f=f
    def run(self):
        print 'TestThread >> run()'
        self.f.PrintMain()

th = TestThread(f)
th.start()


app.MainLoop()
wx.Exit()
