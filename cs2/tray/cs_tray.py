import webbrowser

import wx
import wx.adv

ID_ICON_TIMER = wx.NewId()
OPEN_BROWSER = wx.NewId()
SHOW_MAIN_FRAME = wx.NewId()

app = None


class MailTaskBarIcon(wx.adv.TaskBarIcon):

    def __init__(self, parent):
        wx.adv.TaskBarIcon.__init__(self)
        self.parentApp = parent

        self.noMailIcon = wx.Icon("nomail.png", wx.BITMAP_TYPE_PNG)
        self.youHaveMailIcon = wx.Icon("mail-message-new.png", wx.BITMAP_TYPE_PNG)

        self.menu = wx.Menu()
        self.CreateMenu()

        self.SetIconImage()

    def CreateMenu(self):

        self.Bind(wx.EVT_MENU, self.parentApp.openBrowser, id=OPEN_BROWSER)

        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.ShowMenu)
        self.Bind(wx.EVT_MENU, self.parentApp.showMainFrame, id=SHOW_MAIN_FRAME)

        self.menu.Append(OPEN_BROWSER, "Open process in browser", "watsen toolbox")
        self.menu.Append(SHOW_MAIN_FRAME, "Open main window")
        self.menu.AppendSeparator()
        self.menu.Append(wx.ID_EXIT, "Close App")

    def ShowMenu(self, event):
        self.PopupMenu(self.menu)

    def SetIconImage(self, mail=False):
        if mail:
            self.SetIcon(self.youHaveMailIcon, "You have mail")
        else:
            self.SetIcon(self.noMailIcon, "No mail")


class MailFrame(wx.Frame):

    def __init__(self, parent, id, title):
        # wx.Frame.__init__(self, parent, -1, title, size = (1, 1),
        #                   style=wx.FRAME_NO_TASKBAR|wx.NO_FULL_REPAINT_ON_RESIZE)
        wx.Frame.__init__(self, parent, id=id, title=title, size=(640, 480))

        # atdo minimize main window
        self.Bind(wx.EVT_ICONIZE, self.onMinimize)
        self.Bind(wx.EVT_CLOSE, self.onMinimize)

        self.tbicon = MailTaskBarIcon(self)
        self.tbicon.Bind(wx.EVT_MENU, self.exitApp, id=wx.ID_EXIT)

        self.Show(True)

    def onMinimize(self, event):
        """
        When minimizing, hide the frame so it "minimizes to tray"
        """
        # if self.IsIconized():
        #     self.Hide()
        self.Hide()

    def exitApp(self, event):
        self.tbicon.RemoveIcon()
        self.tbicon.Destroy()
        self.Destroy()

        # closeApp()
        # sys.exit(0)
        # atdo use wx.Exit() is right way to close the app, even up two lines is ok.
        wx.Exit()

    def showMainFrame(self, event):
        # pass
        self.Show()

    def openBrowser(self, event):
        self.Show(False)
        webbrowser.open('http://localhost:2018')


# atdo desctroy app when exit form taskBar
def closeApp():
    global app
    app.Destroy()


# ---------------- run the program -----------------------
def main(argv=None):
    global app
    app = wx.App(False)

    # frame = MailFrame(None, -1, ' ')
    # #frame.Center(wx.BOTH)
    # frame.Show(False)

    frame = MailFrame(None, -1, 'process of watsen ..')
    frame.Center(wx.BOTH)

    app.MainLoop()

    # del app
    # app.Destroy()
    # app.Exit()
    # wx.Exit() #atdo this equals to app.Exit(), app.Desctroy(), del app.


if __name__ == '__main__':
    main()
