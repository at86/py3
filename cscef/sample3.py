# coding=utf-8

# Slightly more advanced sample illustrating the usage of CEFWindow class.

# On Mac the cefpython library must be imported the very first,
# before any other libraries (Issue 155).

# import sys
# sys.path.append("./watsen")
import os
import platform
import time

import cefpython3wx.chromectrl as chrome
import watsen.tool.wat as wat
import wx
import wx.lib.agw.flatnotebook as fnb

class FnbFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY,
                          title='mychrome', size=(880, 600))
        self._InitComponents()
        self._LayoutComponents()
        self._InitEventHandlers()

    def _InitComponents(self):
        self.fnb = fnb.FlatNotebook(self, wx.ID_ANY, agwStyle=fnb.FNB_X_ON_TAB
                                                              | fnb.FNB_NAV_BUTTONS_WHEN_NEEDED)
        # You also have to set the wx.WANTS_CHARS style for
        # all parent panels/controls, if it's deeply embedded.
        self.fnb.SetWindowStyleFlag(wx.WANTS_CHARS)

        # ctrl1 = chrome.ChromeCtrl(self.fnb, useTimer=True,
        #                           url="http://www.qq.com")
        # ctrl1.GetNavigationBar().GetUrlCtrl().SetEditable(True)
        # ctrl1.GetNavigationBar().GetBackButton().SetBitmapLabel(
        #     wx.Bitmap(os.path.join(os.path.dirname(os.path.abspath(__file__)),
        #                            "back.png"), wx.BITMAP_TYPE_PNG))
        # ctrl1.GetNavigationBar().GetForwardButton().SetBitmapLabel(
        #     wx.Bitmap(os.path.join(os.path.dirname(os.path.abspath(__file__)),
        #                             "forward.png"), wx.BITMAP_TYPE_PNG))
        # ctrl1.GetNavigationBar().GetReloadButton().SetBitmapLabel(
        #     wx.Bitmap(os.path.join(os.path.dirname(os.path.abspath(__file__)),
        #                             "reload_page.png"), wx.BITMAP_TYPE_PNG))
        #
        # self.fnb.AddPage(ctrl1, "qq")

        # ctrl2 = chrome.ChromeCtrl(self.fnb, useTimer=True, url="https://www.google.com", hasNavBar=False)
        # self.fnb.AddPage(ctrl2, "Google")

        # atdo EVT_TAB_DRAW_EVENT this is a customer event
        # self.fnb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,self.OnFnbChanged)
        # self.fnb._pages.Bind(wx.EVT_PAINT,self.OnPaint2)
        # self.fnb._pages.Bind(fnb.EVT_TAB_DRAW_EVENT,self.OnTabSize)

        # self.MakeCefCtrl('', "http://localhost:2018")
        self.MakeCefCtrl('', "https://www.baidu.com")

    def MakeCefCtrl(self, title, url=""):
        cefctrl = chrome.ChromeCtrl(self.fnb, useTimer=True, url=url)
        self.fnb.AddPage(cefctrl, self.caclcTitle(title), select=True)
        # wat.d(self.fnb._pages)
        # wat.d(self.fnb._pages._pagesInfoVec[0].GetSize())
        cefctrl.GetNavigationBar().GetAddButton().Bind(wx.EVT_BUTTON, self.OnAddPage)
        browser = cefctrl.chromeWindow.browser
        # atdo AttributeError: 'cefpython_py27.PyBrowser' object has no attribute '_mTitle'
        # browser._mTitle = title
        # browser._mPage = cefctrl
        # browser._mFnb = self.fnb
        browser.SetClientHandler(LoadHandler(title, cefctrl, self))
        browser.SetClientHandler(DisplayHandler(title, cefctrl, self))

        return cefctrl

    def caclcTitle(self, title):
        titleLen = title.decode('utf-8').encode('gbk').__len__()
        suitLen = 14
        quanJaooBlank = '　'
        if titleLen < suitLen:
            s = (suitLen - titleLen) // 2
            if s > 0:
                title = title + quanJaooBlank * s
            print title.decode('utf-8').encode('gbk').__len__()
        return title + quanJaooBlank

    # def OnPaint2(self, event):
    #     event.Skip()
    #     wat.d('OnPaint last Bind()')
    #
    # def OnTabSize(self, event):
    #     wat.d('OnTabSize')
    #     wat.d(self.fnb._pages._pagesInfoVec[0].GetSize())
    #     wat.d(self.fnb._pages._pagesInfoVec[0].SetSize((222, -1)))
    #
    # def OnFnbChanged(self, event):
    #     event.Skip()
    #     wat.d('fnbChanged 33')

    def OnAddPage(self, event):
        # wat.d(self.fnb._pages._pagesInfoVec[0].GetSize())
        # wat.d(self.fnb._pages._pagesInfoVec[0].SetSize((360, -1)))
        self.MakeCefCtrl('blank')

    def _LayoutComponents(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.fnb, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def _InitEventHandlers(self):
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        # Remember to destroy all CEF browser references before calling
        # Destroy(), so that browser closes cleanly. In this specific
        # example there are no references kept, but keep this in mind
        # for the future.
        self.Destroy()
        # On Mac the code after app.MainLoop() never executes, so
        # need to call CEF shutdown here.
        if platform.system() == "Darwin":
            chrome.Shutdown()
            wx.GetApp().Exit()

class LoadHandler(object):
    def __init__(self, title, page, fnbFrame):
        self.title = title
        self.page = page
        self.fnbFrame = fnbFrame

    def OnLoadingStateChange(self, browser, is_loading, **_):
        """Called when the loading state has changed."""
        if not is_loading:
            # # Loading is complete. DOM is ready.
            # js_print(browser, "Python", "OnLoadingStateChange",
            #          "Loading is complete")
            wat.d('loaded ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            wat.d(browser.GetUrl())
            self.page.GetNavigationBar().GetUrlCtrl().SetValue(browser.GetUrl())
            # # browser.ExecuteJavascript("alert(document.body.scrollWidth)")
            # browser.ExecuteJavascript("external.pycall(document.body.scrollWidth)")
            #
            # # browser.ShowDevTools()
            # fdir = os.path.split(os.path.realpath(__file__))[0]
            # wat.d(3333, fdir)
            # file_object = open(fdir + "/cscef.js")
            # try:
            #     cnt = file_object.read()
            #     #  file_context = open(file).read().splitlines()
            #     browser.ExecuteJavascript(cnt)
            # finally:
            #     file_object.close()

class DisplayHandler(object):
    def __init__(self, title, page, fnbFrame):
        self.title = title
        self.page = page
        self.fnbFrame = fnbFrame

    # def OnConsoleMessage(self, browser, message, **_):
    #     print message

    # # atdo need chrome66, and somtimes tab no text display.
    # def OnLoadingProgressChange(self, browser, progress):
    #     idx = self.fnbFrame.fnb.GetPageIndex(self.page)
    #     wat.d(idx)
    #     progress = str(int(100 * progress))
    #     if self.title == '':
    #         title = '加载中 ' + progress + '%'
    #     else:
    #         if progress != '100':
    #             title = self.title + str(int(100 * progress)) + '%'
    #         else:
    #             title = self.title
    #     # self.fnbFrame.fnb.SetPageText(idx, self.fnbFrame.caclcTitle(title))
    #     wat.d(progress)

    # def OnStatusMessage(self, browser, value):
    #     idx = self.fnbFrame.fnb.GetPageIndex(self.page)
    #     self.fnbFrame.fnb.SetPageText(idx, self.fnbFrame.caclcTitle(value))
    #     wat.d(value)

    def OnTitleChange(self, browser, title):
        idx = self.fnbFrame.fnb.GetPageIndex(self.page)
        self.title = title
        self.fnbFrame.fnb.SetPageText(idx, self.fnbFrame.caclcTitle(title))
        wat.d(title)

class CustomNavigationBar(chrome.NavigationBar):
    def _LayoutComponents(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.url, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 12)

        sizer.Add(self.GetBackButton(), 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                  wx.ALL, 0)
        sizer.Add(self.GetForwardButton(), 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                  wx.ALL, 0)
        # in this example we dont want reload button
        self.GetReloadButton().Hide()
        self.SetSizer(sizer)
        self.Fit()


class MyApp(wx.App):
    def OnInit(self):
        frame = FnbFrame()
        self.SetTopWindow(frame)
        frame.Show()
        return True


if __name__ == '__main__':
    chrome.Initialize()
    print('sample3.py: wx.version=%s' % wx.version())
    app = MyApp()
    app.MainLoop()
    # Important: do the wx cleanup before calling Shutdown
    del app
    # On Mac Shutdown is called in OnClose
    if platform.system() in ["Linux", "Windows"]:
        chrome.Shutdown()
