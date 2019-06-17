# encoding:utf-8
from multiprocessing import Process, Queue
import time

import wx
import threading

class TestThread(threading.Thread):
    def __init__(self,queue):
        #线程实例化时立即启动
        threading.Thread.__init__(self)
        self.queue=queue

    def run(self):
        while True:
            print self.queue.get()
            btn = self.btn
            print btn.GetLabel()
            evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, btn.GetId())
            wx.PostEvent(self.frame, evt)

def btnclick(evt,p):
    print 'btnclick'

class MyApp(wx.App):
    def __init__(self, redirect, queue=None):
        print "dddddddddddddddddd"
        super(MyApp, self).__init__(redirect=redirect)

        frame = wx.Frame(parent=None, id=wx.ID_ANY,
                         title='process', size=(240, 120))
        # self.SetTopWindow(frame)
        frame.Center(wx.BOTH)
        frame.Show()


        btn1 = wx.Button(frame, id=wx.ID_ANY, label="sssss", style=wx.BU_EXACTFIT|wx.BU_EXACTFIT)
        btn1.Bind(wx.EVT_BUTTON, lambda evt, p=2: btnclick(evt, p))

        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, btn1.GetId())
        wx.PostEvent(self, evt)

        sizer = wx.BoxSizer()
        sizer.Add(btn1)

        frame.SetSizer(sizer)


        th = TestThread(queue)
        th.btn = btn1
        th.frame = frame
        th.start()

        self.queue = queue

        # frame.ftimer = wx.Timer(frame)
        # frame.Bind(wx.EVT_TIMER, self.newProcessTimer, frame.ftimer)
        # frame.ftimer.Start(1000)

    def newProcessTimer(self, event):
        self.queue.get()
        # self.queue.put([42, None, 'hello', time.time()])
        # print 'sub', self.queue.get(False)

# app = MyApp(False)
# app.MainLoop()

def f(q):
    # while True:
    #     q.put([42, None, 'hello', time.time()])
    #     time.sleep(1)

    # app = MyApp(False)
    # this codes make gui freeze
    # while True:
    #     q.put([42, None, 'hello', time.time()])
    #     time.sleep(1)
    # app.MainLoop()

    app = MyApp(False, q)
    app.MainLoop()

def doqueue(event,q):
    q.put([42, None, 'hello', time.time()])

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()

    # while True:
    #     time.sleep(1)
    #     # print q.get()
    #     q.put([42, None, 'hello', time.time()])
    #     print 'parent'

    app = wx.App()

    frame = wx.Frame(parent=None, id=wx.ID_ANY,
                     title='main', size=(140, 280))
    # self.SetTopWindow(frame)
    frame.SetSize(0, 0, 500, 268)
    frame.Center(wx.BOTH)

    btn1 = wx.Button(frame, id=wx.ID_ANY, label="queue.put", style=wx.BU_EXACTFIT|wx.BU_EXACTFIT)
    btn1.Bind(wx.EVT_BUTTON, lambda evt, p=q: doqueue(evt, p))

    sizer = wx.BoxSizer()
    sizer.Add(btn1)

    frame.SetSizer(sizer)
    frame.Show()

    app.MainLoop()

    # p.join()
