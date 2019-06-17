import random
import wx

########################################################################
class TabPanel(wx.Panel):
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent)

        colors = ["red", "blue", "gray", "yellow", "green"]
        self.SetBackgroundColour(random.choice(colors))

        btn = wx.Button(self, label="Press Me"+str(random.randint(1,10)))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL, 10)
        self.SetSizer(sizer)

########################################################################
class DemoFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Notebook Tutorial",
                          size=(600,400)
                          )
        panel = wx.Panel(self)
        self.tab_num = 3

        self.notebook = wx.Notebook(panel)
        tabOne = TabPanel(self.notebook)
        self.notebook.AddPage(tabOne, "Tab 1")

        tabTwo = TabPanel(self.notebook)
        self.notebook.AddPage(tabTwo, "Tab 2")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)

        btn = wx.Button(panel, label="Add Page")
        btn.Bind(wx.EVT_BUTTON, self.addPage)
        sizer.Add(btn)

        panel.SetSizer(sizer)
        self.Layout()

        self.Show()

    #----------------------------------------------------------------------
    def addPage(self, event):
        """"""
        new_tab = TabPanel(self.notebook)
        self.notebook.AddPage(new_tab, "Tab %s" % self.tab_num)
        self.tab_num += 1

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = DemoFrame()
    app.MainLoop()