# coding:utf-8

import wx
import os
import sys
# sys.path.append("/Volumes/py/tool")
import wat
import demjson
print(os.path.join(os.path.dirname(sys.argv[0]), "lib"))
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), "lib"))

def toggleBtnDeal(btn):
    """toggleBtn add open nums and focused"""
    if not hasattr(btn, 'openNums'):
        btn.openNums = 1
    else:
        btn.openNums = btn.openNums + 1
    btn.SetValue(True)

def pageObjClose(event, toggleBtn):
    """when pageobj close, chg togglebutton state"""
    toggleBtn.openNums = toggleBtn.openNums - 1
    if toggleBtn.openNums == 0:
        toggleBtn.SetValue(False)
    event.Skip()

def btnClickNewPage(event, app_page):
    """open a new page"""
    btn = event.GetEventObject()
    toggleBtnDeal(btn)

    pageModule = None

    if app_page == 'paint1':
        import pages.calc as pageModule
    if app_page == 'paint2':
        import pages.calc2 as pageModule

    if pageModule:
        wat.myreload(pageModule)
        pageObj = pageModule.run()
        # appObj.Bind(wx.EVT_CLOSE, appObjClose)
        if pageObj:
            pageObj.Bind(wx.EVT_CLOSE, lambda evt, p=btn: pageObjClose(evt, p))

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY,
                          title='process of watsen', size=(640, 480))
        self.SetBackgroundColour('yellow')
        self.SetBackgroundColour(wx.Colour(0xFA, 0xF9, 0xDE, 256))  # 杏仁黄
        # self.SetBackgroundColour(wx.Colour(199,238,206,256 )) # 豆沙绿
        # self.SetBackgroundColour(wx.Colour(0xFF,0xF2,0xE2,256 )) # 秋叶褐
        # self.SetBackgroundColour(wx.Colour(0xEA,0xEA,0xEF,256 )) # 极光灰
        # self.SetBackgroundColour(wx.Colour(0xdc,0xE2,0xf1,256 )) # 海天蓝

        # atdo minimize main window
        self.Bind(wx.EVT_ICONIZE, self.onMinimize)
        # self.Bind(wx.EVT_CLOSE, self.onMinimize)
        self.Bind(wx.EVT_CLOSE, self.CloseMainWnd)

        sizer = wx.BoxSizer(orient=wx.VERTICAL)

        sizerMain = wx.BoxSizer()
        sizer.Add(sizerMain, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 10)

        # atdo sizerApp 3 ok
        sbox = wx.StaticBoxSizer(wx.HORIZONTAL, self, "app_page")
        sizerApp = wx.WrapSizer()
        # sbox.Add(sizerApp, 0, wx.EXPAND, 0) # proportion 0 make resize to more rows will not to less rows
        sbox.Add(sizerApp, 1, wx.EXPAND, 0)
        # sizer.Add(sbox, 1, wx.EXPAND, 0) # proportion 1 make top bottom full fill
        sizer.Add(sbox, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 10)

        def btnApp(app_page, label):
            # btn2 = wx.Button(self, id=wx.ID_ANY, label=label, style=wx.WANTS_CHARS)
            # btn2.Bind(wx.EVT_BUTTON, lambda evt, p=app_page: btnClickNewApp(evt, p))
            btn2 = wx.ToggleButton(self, id=wx.ID_ANY, label=label, style=wx.WANTS_CHARS | wx.BU_EXACTFIT)
            btn2.Bind(wx.EVT_TOGGLEBUTTON, lambda evt, p=app_page: btnClickNewPage(evt, p))
            sizerApp.Add(btn2, 1, wx.ALIGN_LEFT, 0)  # |wx.EXPAND


        if getattr(sys, 'frozen', False):
            # watDir = chrome.cefpython.GetModuleDirectory() + '/lib/watsen'
            watDir = './'
        else:
            watDir = os.path.split(os.path.realpath(__file__))[0]

        apps = open(watDir + '/apps.js',encoding="utf8").read()
        apps = apps[apps.find('['):]
        wat.d(apps)
        apps = demjson.decode(apps)
        wat.d(apps)
        for i in apps:
            wat.d(i['label'])
            app_page = i['app']
            label = i['label']
            btnApp(app_page, label)

        self.SetSizer(sizer)

    def CloseMainWnd(self, event):
        wat.d('CloseMainWnd()')
        # atdo close event call twice, if not call app.ExitMainLoop()

        self.Hide()

        wat.d('call app.ExitMainLoop()')
        wx.GetApp().ExitMainLoop()

    def onMinimize(self, event):
        """
        When minimizing, hide the frame so it "minimizes to tray"
        """
        # if self.IsIconized():
        #     self.Hide()
        # self.Hide()

    def showMainFrame(self, event):
        # pass
        self.Show()

class MyApp(wx.App):
    def __init__(self, redirect):
        wat.d("dddddddddddddddddd")
        self.chromInited = False
        super(MyApp, self).__init__(redirect=redirect)

    # def OnInit(self):
    #     frame = MainFrame()
    #     self.SetTopWindow(frame)
    #     frame.SetSize(0, 0, 800, 568)
    #     frame.Center(wx.BOTH)
    #     frame.Show()
    #     return True


    def OnExit(self):
        wat.d('app exit')

        return 0


def run():
    # atdo freeze
    # multiprocessing.freeze_support()

    print('[sample1.py] wx.version=%s' % wx.version())

    # watcef.chromInit()

    app = MyApp(False)

    frame = MainFrame()
    frame.SetSize(0, 0, 800, 568)
    frame.Center(wx.BOTH)
    frame.Show()
    app.SetTopWindow(frame)

    app.MainLoop()

    # atdo use app.ExitMainLoop() in close event
    wat.d(' ======================= app.ExitMainLoop() called')

    # atdo way 1
    # # Important: do the wx cleanup before calling Shutdown
    # # del app
    # app.Destroy()
    #
    # # On Mac Shutdown is called in OnClose
    # if platform.system() in ["Linux", "Windows"]:
    #     chrome.Shutdown()

    # del app
    # atdo this wx.Exit() must here..
    wx.Exit()  # atdo chrome.Shutdown() first, then wx.Exit() is ok

    # atdo for cx_freeze need exit
    sys.exit(0)

if __name__ == '__main__':
    run()
