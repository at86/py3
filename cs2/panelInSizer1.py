# -*- coding: utf-8 -*-

import wx
import wx.lib.scrolledpanel

class myGridLabel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, style=wx.BORDER_SIMPLE)

        # txtOne = wx.StaticText(self, wx.ID_ANY, "")
        # txtOne.SetLabelText("aljdfals flakdsjfjlasd f")

        txtOne = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY | wx.BORDER_NONE)
        txtOne.SetLabelText("sdsdf")
        # txtOne.Disable()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(txtOne, 0, wx.ALL, 4)

        self.SetSizer(sizer)

class main_frame(wx.Frame):
    """Main Frame holding the main panel."""
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        # p = wx.Panel(self)

        p = wx.lib.scrolledpanel.ScrolledPanel(self, size=(-1, -1))
        p.SetupScrolling()

        sizer = wx.BoxSizer(wx.VERTICAL)
        myp = myGridLabel(p)
        sizer.Add(myp)
        for i in range(10):
            myp = myGridLabel(p)
            sizer.Add(myp, 0, flag=wx.TOP, border=-1)

        p.SetSizerAndFit(sizer)

        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = main_frame(None, -1, size=(440, 300))
    app.MainLoop()
