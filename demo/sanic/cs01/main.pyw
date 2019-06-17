import os
import sys

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), "lib"))

import wat


import threading
import time


# exitFlag = 0
#
# class myThread (threading.Thread):
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#     def run(self):
#         print ("开始线程：" + self.name)
#
#         if self.threadID==1:
#             print_time(self.name, self.counter, 1)
#         else:
#             print_time(self.name, self.counter, 1)
#         print ("退出线程：" + self.name)
#
# def print_time(threadName, delay, counter):
#     while counter:
#         if exitFlag:
#             threadName.exit()
#         time.sleep(delay)
#         print ("%s: %s" % (threadName, time.ctime(time.time())))
#         counter -= 1
#
# # 创建新线程
# thread1 = myThread(1, "Thread-1", 0.2)
# thread2 = myThread(2, "Thread-2", 0.2)
#
# # 开启新线程
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
#


# import wx
# app = wx.App()
# frame = wx.Frame(parent=None, title='Hello World')
# frame.Show()
# app.MainLoop()


import wx
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Hello World')
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        my_btn = wx.Button(panel, label='Press Me')
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(my_sizer)
        self.Show()

    def on_press(self, event):
        value = self.text_ctrl.GetValue()
        if not value:
            print("You didn't enter anything!")
        else:
            print(f'You typed: "{value}"')
        # useThread()
        # useProcess()
        unseProcess2()


def useThread():

    def run_thread(n):
        import main
        main.run()

    t1 = threading.Thread(target=run_thread, args=(5,))
    t1.setDaemon(True)
    t1.start()
    # t1.join()


from multiprocessing import Process
import os
import time
class MyProcess(Process):
    #重新init方法
    def __init__(self,interval):
        #下面一句是调用父类init方法，这一本尽量不要少，因为父类还有很多事情需要在init方法内处理
        Process.__init__(self)
        self.interval=interval

    #重写run方法
    def run(self):
        print("子进程运行中，pid=%d，父进程：%d" % (os.getpid(), os.getppid()))
        t_start=time.time()
        time.sleep(self.interval)
        t_end=time.time()
        print("子进程运行结束，耗时：%0.2f秒"%(t_end-t_start))


def useProcess():

    t_start=time.time()
    print("父进程开始执行")
    p=MyProcess(2)
    p.start()
    # p.join()
    # p.setDaemon(True) # no setDaemon()
    t_end=time.time()
    print("父进程运行结束，耗时：%0.2f秒" % (t_end - t_start))


def unseProcess2():
    import subprocess

    # # 子进程的标准输出默认为当前控制台
    # p = subprocess.Popen("dir", shell=True)
    # p.wait()  # 阻塞当前线程直到子进程 p 执行结束

    p = subprocess.Popen("C:\python3\pythonw.exe D:/wat/py/py3/demo/sanic/cs01/main.pyw", shell=False)


def run():
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()

# if __name__ == '__main__':
#     run()

run()
# print(2323)

# print ("退出主线程")
