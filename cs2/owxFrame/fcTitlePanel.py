'''
Created on 2011-12-6
@author: curliph
'''

import wx
from platebtn import AdjustColour

class fcTitlePanel(wx.Panel):
    
    def __init__(self, parent):
        super(fcTitlePanel, self).__init__(parent)
        
        self._label = None
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        
        title = self.GetLabel()
        colRef = wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION)
        colStr = AdjustColour(colRef, -1)
        colEnd = AdjustColour(colRef, -60)
        
        rect = self.GetClientRect()
        gBrush = gc.CreateLinearGradientBrush(0, 1, 0, rect.height, colStr, colEnd)
        gc.SetBrush(gBrush)
        gc.SetPen(gc.CreatePen(wx.Pen(colRef, 2)))
        gc.DrawRectangle(0, 0, rect.width, rect.height)
        
        if title is not None:
            font = self.GetFont()
            font.SetFamily(wx.FONTFAMILY_ROMAN)
            font.SetPointSize(10)
            font.SetWeight(wx.FONTWEIGHT_BOLD)
            dc.SetFont(font)
            dc.SetTextForeground(wx.Colour(219, 238, 243))
            dc.DrawLabel(title, rect, wx.ALIGN_CENTER)

    def OnErase(self, event):
        pass
    
    def OnSize(self, event):
        self.Refresh()
        event.Skip()
    
    def SetLabel(self, label):
        self._label = label
        self.Refresh()
        
    def GetLabel(self):
        return self._label
