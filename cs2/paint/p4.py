# -*- encoding: utf-8 -*
import wx
import os

""" this version use class 'BufferedPaintDC' and 'BufferedDC' """


class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "画图板 - 芒果布丁", (0, 0), (800, 500))
        self.Center(wx.BOTH)  # 窗口居中显示
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 0, 0
        self.iscaptured = -1
        self.p1 = (0, 0)
        self.p2 = (0, 0)
        self.st = 'line'
        self.pos = (0, 0)
        self.pen = wx.Pen("green", 1, wx.SOLID)
        self.img = None
        self.brush = wx.Brush('', wx.TRANSPARENT)  # 透明填充
        self.shapes = []

        self.SetBackgroundColour("black")
        self.b1 = wx.Button(self, -1, label="矩形", pos=(10, 10), size=(50, 30))
        self.b2 = wx.Button(self, -1, label="圆形", pos=(10, 50), size=(50, 30))
        self.b3 = wx.Button(self, -1, label="直线", pos=(10, 90), size=(50, 30))

        self.b1.SetDefault()

        self.InitBuffer()

        self.Bind(wx.EVT_BUTTON, self.ToRect, self.b1)
        self.Bind(wx.EVT_BUTTON, self.ToOval, self.b2)
        self.Bind(wx.EVT_BUTTON, self.ToLine, self.b3)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.OnMotion)

        self.SetMenuBar(self.getMenu())

    def InitBuffer(self):
        size = self.GetClientSize()
        mm = wx.DisplaySize()  # 获取屏幕大小
        self.buffer = wx.Bitmap(mm[0], mm[1])
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetPen(self.pen)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.SetBrush(self.brush)
        dc.Clear()
        self.Draw(dc)

    def ToRect(self, event):
        self.st = 'rect'

    def ToOval(self, event):
        self.st = 'oval'

    def ToLine(self, event):
        self.st = 'line'

    def OnLeftDown(self, event):
        # self.p1 = event.GetEventObject().GetPosition()
        # print
        self.p1 = event.GetPosition()
        self.x1, self.y1 = self.p1
        self.CaptureMouse()  # 6 捕获鼠标
        self.iscaptured = 1

    def OnLeftUp(self, event):
        if self.iscaptured == 1:
            self.ReleaseMouse()  # 7 释放鼠标
            # self.p2 = event.GetEventObject().GetPosition()
            self.p2 = event.GetPosition()
            # self.shapes.append((self.st, self.p1 + self.p2))
            self.shapes.append((self.st, self.p1.x, self.p1.y, self.p2.x, self.p2.y))
            self.InitBuffer()
            self.iscaptured = 0

    def OnMotion(self, event):
        if event.Dragging() and event.LeftIsDown():  # 8 确定是否在拖动
            dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)  # 9 创建另一个缓存的上下文
            self.drawMotion(dc, event)
        event.Skip()

    def drawMotion(self, dc, event):
        if self.iscaptured == 1:
            # self.p2 = event.GetEventObject().GetPosition()
            self.p2 = event.GetPosition()
            # self.shapes.append((self.st, self.p1 + self.p2))
            self.shapes.append((self.st, self.p1.x, self.p1.y, self.p2.x, self.p2.y))
            self.InitBuffer()
            self.shapes.pop(len(self.shapes) - 1)

    def OnPaint(self, event):
        wx.BufferedPaintDC(self, self.buffer)  # 处理一个paint（描绘）请求

    def Draw(self, dc):

        if self.img != None:
            dc.DrawBitmap(self.img, 0, 0, False)
        print len(self.shapes)
        # for st,(x1,y1,x2,y2) in self.shapes:
        for st, x1,y1,x2,y2  in self.shapes:
        # for st, x1, x2, y1, y2 in self.shapes:
            print x1, y1, x2, y2
            if st == 'line':
                dc.DrawLine(x1, y1, x2, y2)
            elif st == 'oval':
                dc.DrawEllipse(x1, y1, x2 - x1, y2 - y1)
            elif st == 'rect':
                dc.DrawRectangle(x1, y1, x2 - x1, y2 - y1)

    def getMenu(self):
        menuBar = wx.MenuBar()

        menu = wx.Menu()
        m11 = menu.Append(-1, "新建")
        self.Bind(wx.EVT_MENU, self.newFile, m11)
        m12 = menu.Append(-1, "打开")
        self.Bind(wx.EVT_MENU, self.openFile, m12)
        m13 = menu.Append(-1, "保存")

        menu.AppendSeparator()
        exit = menu.Append(-1, "退出")
        menuBar.Append(menu, "文件")

        menu2 = wx.Menu()
        menu2.Append(-1, "撤销")
        menu2.Append(-1, "清除")
        menuBar.Append(menu2, "编辑")

        menu3 = wx.Menu()
        menuBar.Append(menu3, "图像")

        menu4 = wx.Menu()
        menuBar.Append(menu4, "帮助")
        return menuBar

    def newFile(self, event):
        pass

    def openFile(self, event):
        wildcard = "JPEG 图片 (*.jpg)|*.jpg|" \
                   "PNG 图片 (*.png)|*.png|" \
                   "BMP 图片 (*.bmp)|*.bmp|" \
                   "All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "选择一个文件", os.getcwd(), "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            name = dialog.GetPath()
            print dialog.GetPath()
            jpg = wx.Image(name, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.img = jpg
            dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
            dc.DrawBitmap(jpg, 0, 0, False)


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()

# 画图板 version4
