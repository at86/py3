import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        import wx

        app = wx.App()

        hideF = wx.Frame(parent=None, id=wx.ID_ANY, title='ssss')
        hideF.Show()

        app.MainLoop()
        wx.Exit()


# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

thread1.daemon=True
thread2.daemon=True

# 开启新线程
thread1.start()
thread2.start()

thread1.join()
thread2.join()
print ("退出主线程")
