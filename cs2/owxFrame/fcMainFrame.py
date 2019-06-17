#!python

'''
Created on 2011-12-6
@author: curliph@gmail.com
'''

import wx
import gettext

import platebtn as pbtn
from fcTitlePanel import fcTitlePanel

_ = gettext.gettext

MG_POS_TL = 0
MG_POS_TR = 1
MG_POS_BR = 2
MG_POS_BL = 3
MG_POS_TOP = 4
MG_POS_RIGHT = 5
MG_POS_BOTTOM = 6
MG_POS_LEFT = 7
MG_POS_AWAY = -1

class fcMainFrame(wx.Frame):
    
    def __init__(self, parent, title='', size=wx.DefaultSize, pos=wx.DefaultPosition):
        super(fcMainFrame, self).__init__(parent, id=-1, size=size, pos=pos, style = wx.NO_BORDER|wx.SYSTEM_MENU)
        
        self._dragPos = None
        self._sflag = False
        self._cur = MG_POS_AWAY
        
        self._mSizer = wx.BoxSizer(wx.VERTICAL)
        self._titleBar = fcTitlePanel(self)
        self._titleBar.SetLabel(title)
        self.SetTitle(title)
                
        self._tSizer = wx.BoxSizer(wx.HORIZONTAL)
        self._tUserSizer = wx.BoxSizer(wx.VERTICAL)
        
        bstyle = pbtn.PB_STYLE_NOBG | pbtn.PB_STYLE_GRADIENT
        self._sysmenu = pbtn.PlateButton(self._titleBar, wx.ID_ANY, ' ', None, style=bstyle|pbtn.PB_STYLE_DROPARROW)
        self._iconzbox = pbtn.PlateButton(self._titleBar, wx.ID_ANY, '-', None, style=bstyle)
        self._closebox = pbtn.PlateButton(self._titleBar, wx.ID_ANY, '+', None, style=bstyle)
        
        self._tSizer.Add(self._sysmenu, 0, wx.ALL, 2)
        self._tSizer.Add((0, 0), 1, wx.RIGHT|wx.LEFT|wx.EXPAND)
        self._tSizer.Add(self._iconzbox, 0, wx.ALL, 2)
        self._tSizer.Add(self._closebox, 0, wx.ALL, 2)
        
        self._mSizer.Add(self._titleBar, 0, wx.ALL|wx.EXPAND)
        self._mSizer.Add(self._tUserSizer, 1, wx.ALL|wx.EXPAND)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_BUTTON, self.OnClose, self._closebox)
        self.Bind(wx.EVT_BUTTON, self.OnIconize, self._iconzbox)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

        self._titleBar.Bind(wx.EVT_MOTION, self.OnMotion)
        self._titleBar.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)        
        self._titleBar.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self._closebox.Bind(wx.EVT_MOTION, self.OnMotionA)
        self._iconzbox.Bind(wx.EVT_MOTION, self.OnMotionA)
        self._sysmenu.Bind(wx.EVT_MOTION, self.OnMotionA)
        
        self._titleBar.SetSizer(self._tSizer)
        self.SetSizer(self._mSizer)
        self.Layout()
    
    def __GetCursorPos(self, pos):
        w, h = self.GetClientSize()
        #rect_tl = wx.Rect(0, 0, 2, 2)
        #rect_tr = wx.Rect(w-2, 0, 2, 2)
        #rect_bl = wx.Rect(0, h-2, 2, 2)
        rect_br = wx.Rect(w-2, h-2, 2, 2)
        #rect_t = wx.Rect(2, 0, w-4, 2)
        rect_r = wx.Rect(w-2, 2, 2, h-4)
        rect_b = wx.Rect(2, h-2, w-4, 2)
        #rect_l = wx.Rect(0, 2, 2, h-4)
        
        if rect_br.Contains(pos):
            return MG_POS_BR
        elif rect_r.Contains(pos):
            return MG_POS_RIGHT
        elif rect_b.Contains(pos):
            return MG_POS_BOTTOM
        else:
            return MG_POS_AWAY
    
    def OnClose(self, event):
        self.Destroy()
        
    def OnIconize(self, event):
        self.Iconize(True)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        colRef = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
        colBdr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION)
        
        rect = self.GetClientRect()
        gBrush = wx.Brush(colRef)
        gc.SetBrush(gBrush)
        gc.SetPen(gc.CreatePen(wx.Pen(colBdr, 2)))
        gc.DrawRectangle(0, 0, rect.width, rect.height)
        
    def OnErase(self, event):
        pass
    
    def OnSize(self, event):
        self.Refresh()
        event.Skip()

    def OnMotionA(self, event):
        if self._cur in (MG_POS_RIGHT, MG_POS_BR, MG_POS_BOTTOM):
            self._cur = MG_POS_AWAY
            self.SetCursor(wx.NullCursor)
            
    def OnMotion(self, event):  
        pos = event.GetPosition()
        cur = self.__GetCursorPos(pos)
        if cur == MG_POS_RIGHT:
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZEWE))
        elif cur == MG_POS_BOTTOM:
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZENS))
        elif cur == MG_POS_BR:
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZENWSE))
        elif self._cur in (MG_POS_BR, MG_POS_RIGHT, MG_POS_BOTTOM):
            self.SetCursor(wx.NullCursor)        
         
        if not event.Dragging():
            self._dragPos = None
            self._cur = cur
            return
                         
        if not self._dragPos:
            self._dragPos = pos
        elif not self._sflag:
            cur_ofs = self._dragPos - pos
            self.SetPosition(self.GetPosition() - cur_ofs)
        elif self._cur in (2, 5, 6):
            w, h = self.GetClientSize()
            iw, ih = self.GetMinClientSize()
            ew = w if self._cur == 6 else max(iw, pos[0])
            eh = h if self._cur == 5 else max(ih, pos[1])
            self.SetClientSize((ew, eh))
            self.Update()
            
    def OnLeftDown(self, event):
        if not self.HasCapture():
            self.CaptureMouse()
        if self._cur in (2, 5, 6):
            self._sflag = True
        else:
            self._sflag = False
        
    def OnLeftUp(self, event):
        if self.HasCapture():
            self.ReleaseMouse()
            
    def AddItem(self, item):
        self._tUserSizer.Add(item, 1, wx.ALL)
            
if __name__ == '__main__':
    app = wx.App()
    frm = fcMainFrame(None, title="Own-draw Frame", size=(1000, 562))
    frm.SetMinClientSize((800, 450))
    frm.CenterOnScreen()
    frm.Show(True)
    app.MainLoop()
        
