# -*- encoding: utf8 -*
import wx

""" this version use class 'PaintDC' and 'ClientDC' """


class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "画图板 - 芒果布丁", (0, 0), (800, 500))
        self.Center(wx.BOTH)  # 窗口居中显示
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 0, 0
        self.st = 'line'
        self.pos = (0, 0)
        self.pen = wx.Pen("green", 1, wx.SOLID)
        self.brush = wx.Brush('', wx.TRANSPARENT)  # 透明填充
        self.shapes = []

        # self.SetBackgroundColour("black")
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

    def InitBuffer(self):
        size = self.GetClientSize()
        self.buffer = wx.Bitmap(size.width, size.height)
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

        self.p1 = event.GetEventObject().GetPosition()
        self.x1, self.y1 = self.p1

    def OnLeftUp(self, event):
        self.p2 = event.GetEventObject().GetPosition()
        # print  self.p1, self.p2
        # print type(self.p1)
        # print  self.p1 + self.p2
        # self.shapes.append((self.st, self.p1 + self.p2))
        # atdo
        self.shapes.append((self.st, self.p1.x, self.p1.y, self.p2.x, self.p2.y))
        dc = wx.ClientDC(self)
        self.Draw(dc)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)  # 处理一个paint（描绘）请求
        self.Draw(dc)

    def Draw(self, dc):
        dc.SetPen(self.pen)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.SetBrush(self.brush)
        dc.Clear()
        print self.shapes
        # for st, (x1, y1, x2, y2) in self.shapes:
        for st,  x1, x2, y1, y2  in self.shapes:

            if st == 'line':
                dc.DrawLine(x1, y1, x2, y2)
            elif st == 'oval':
                dc.DrawEllipse(x1, y1, x2 - x1, y2 - y1)
            elif st == 'rect':
                dc.DrawRectangle(x1, y1, x2 - x1, y2 - y1)


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()

# 画图板 version1
