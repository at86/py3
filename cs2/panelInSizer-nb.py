# -*- coding: utf-8 -*-

import wx
import wx.lib.scrolledpanel
import random

class myGridLabel(wx.Panel):
    def __init__(self, parent, text, fsize=(120, 40)):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, style=wx.BORDER_SIMPLE, size=fsize)

        # item = wx.StaticText(self, wx.ID_ANY, "")
        # item.SetLabelText("aljdfals flakdsjfjlasd f")

        item = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY | wx.BORDER_NONE)
        item.SetLabelText(text)
        # item.Disable()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(item, 0, wx.ALL, 4)

        self.SetSizer(sizer)

class myGridBtn(wx.Panel):
    def __init__(self, parent, text, fsize=(120, 40)):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, style=wx.BORDER_SIMPLE, size=fsize)

        item = wx.Button(self, wx.ID_ANY, text)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(item, 0, wx.ALL, 4)

        self.SetSizer(sizer)

class main_frame(wx.Frame):
    """Main Frame holding the main panel."""
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        # p = wx.Panel(self)

        p = wx.lib.scrolledpanel.ScrolledPanel(self, size=(-1, -1))
        p.SetupScrolling()

        gtype = [1, 2]
        sizer = wx.GridBagSizer(-1, -1)
        for i in range(1, 5):
            for j in range(1, 4):

                g = random.choice(gtype)
                if g == 1:
                    myp = myGridLabel(p, 'i_%s , j_%s' % (i, j), (120, 50))
                elif g == 2:
                    myp = myGridBtn(p, 'i_%s , j_%s' % (i, j), (120, 50))
                sizer.Add(myp, (i, j))

        myp = myGridBtn(p, 'i_%s , j_%s' % (5, 10), (120, 50))
        sizer.Add(myp, (7, 10))

        p.SetSizerAndFit(sizer)

        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = main_frame(None, -1, size=(440, 300))
    app.MainLoop()
