import b
import wx
import time

if __name__ == '__main__':

    app = wx.App()
    fr = wx.Frame(parent=None, id=wx.ID_ANY, title="ssss")
    sz = wx.BoxSizer()

    def click(self):
        # import b
        reload(b)
        b.b()
        print 'click '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    btn = wx.Button(fr,label='btn')
    btn.Bind(wx.EVT_BUTTON,click)
    sz.Add(btn)

    fr.Show()
    app.MainLoop()

