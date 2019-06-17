
import  random

import  wx
import  wx.grid as  gridlib

#---------------------------------------------------------------------------

class MyCustomRenderer(gridlib.PyGridCellRenderer):
    def __init__(self):
        gridlib.PyGridCellRenderer.__init__(self)
        self.down = False
        self.click_handled = False

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        """This is called when the widget is Refreshed"""
        print 'drawing button'
        dc.Clear()
        if self.down:
            state = wx.CONTROL_PRESSED | wx.CONTROL_SELECTED
        else:
            state = 0

        #if not self.IsEnabled():
        #    state = wx.CONTROL_DISABLED
        #pt = self.ScreenToClient(wx.GetMousePosition())
        #if self.GetClientRect().Contains(pt):
        #    state |= wx.CONTROL_CURRENT

        wx.RendererNative.Get().DrawPushButton(grid, dc, rect, state)
        #extra logic required since a button gets drawn at various times that could be while the mouse button is held down
        if self.down and not self.click_handled:
            self.click_handled = True
            self.HandleClick()

    def HandleClick(self):
        print 'clicked'

    def GetBestSize(self, grid, attr, dc, row, col):
        text = grid.GetCellValue(row, col)
        dc.SetFont(attr.GetFont())
        w, h = dc.GetTextExtent(text)
        return wx.Size(w, h)


    def Clone(self):
        return MyCustomRenderer()


#---------------------------------------------------------------------------

rendererDemoData = [
    ('GridCellStringRenderer\n(the default)', 'this is a text value', gridlib.GridCellStringRenderer, ()),
    ('GridCellNumberRenderer', '12345', gridlib.GridCellNumberRenderer, ()),
    ('GridCellFloatRenderer', '1234.5678', gridlib.GridCellFloatRenderer, (6,2)),
    ('GridCellBoolRenderer', '1', gridlib.GridCellBoolRenderer, ()),
    ('MyCustomRenderer', 'This is my renderer', MyCustomRenderer, ()),
]

editorDemoData = [
    ('GridCellTextEditor\n(the default)', 'Here is some more text', gridlib.GridCellTextEditor, ()),
    ('GridCellNumberEditor\nwith min,max', '101', gridlib.GridCellNumberEditor, (5, 10005)),
    ('GridCellNumberEditor\nwithout bounds', '101', gridlib.GridCellNumberEditor, ()),
    ('GridCellFloatEditor', '1234.5678', gridlib.GridCellFloatEditor, ()),
    ('GridCellBoolEditor', '1', gridlib.GridCellBoolEditor, ()),
    ('GridCellChoiceEditor', 'one', gridlib.GridCellChoiceEditor, (['one', 'two', 'three', 'four',
                                                                    'kick', 'Microsoft', 'out the',
                                                                    'door'], False)),
]

comboDemoData = [
    ('GridCellNumberRenderer\nGridCellNumberEditor', '20792', gridlib.GridCellNumberRenderer, gridlib.GridCellNumberEditor),
    ('GridCellBoolRenderer\nGridCellBoolEditor', '1', gridlib.GridCellBoolRenderer, gridlib.GridCellBoolEditor),
]


class EditorsAndRenderersGrid(gridlib.Grid):
    def __init__(self, parent, log):
        gridlib.Grid.__init__(self, parent, -1)
        self.log = log
        self.down = False
        self.CreateGrid(25, 8)
        renCol = 1
        edCol = 4


        self.SetCellValue(0, renCol, '''\
Cell Renderers are used to draw
the contents of the cell when they
need to be refreshed.  Different
types of Renderers can be plugged in
to different cells in the grid, it can
even be automatically determined based
on the type of data in the cell.
''')

        self.SetCellValue(0, edCol, '''\
Cell Editors are used when the
value of the cell is edited by
the user.  An editor class is
wrapped around a an object
derived from wxControl and it
implements some methods required
to integrate with the grid.
''')

        self.SetCellValue(16, renCol, '''\
Here are some combinations of Editors and
Renderers used together.
''')

        row = 2

        for label, value, renderClass, args in rendererDemoData:
            renderer = renderClass(*args)
            self.SetCellValue(row, renCol, label)
            self.SetCellValue(row, renCol+1, value)
            self.SetCellRenderer(row, renCol+1, renderer)
            row = row + 2

        renderer = MyCustomRenderer()
        self.SetCellValue(row-2, renCol, 'Custom Button Renderer')
        self.SetCellValue(row-2, renCol+1, 'My Custom Cell Button')
        self.SetCellRenderer(row-2, renCol+1, renderer)
        self.SetReadOnly(row-2, renCol+1, True)
        row = 2

        for label, value, editorClass, args in editorDemoData:
            editor = editorClass(*args)
            self.SetCellValue(row, edCol, label)
            self.SetCellValue(row, edCol+1, value)
            self.SetCellEditor(row, edCol+1, editor)
            row = row + 2


        row = 18

        for label, value, renClass, edClass in comboDemoData:
            self.SetCellValue(row, renCol, label)
            self.SetCellValue(row, renCol+1, value)
            editor = edClass()
            renderer = renClass()
            self.SetCellEditor(row, renCol+1, editor)
            self.SetCellRenderer(row, renCol+1, renderer)
            row = row + 2

        font = self.GetFont()
        font.SetWeight(wx.BOLD)
        attr = gridlib.GridCellAttr()
        attr.SetFont(font)
        attr.SetBackgroundColour(wx.LIGHT_GREY)
        attr.SetReadOnly(True)
        attr.SetAlignment(wx.RIGHT, -1)
        self.SetColAttr(renCol, attr)
        attr.IncRef()
        self.SetColAttr(edCol, attr)

        # There is a bug in wxGTK for this method...
        self.AutoSizeColumns(True)
        self.AutoSizeRows(True)

        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnLeftDClick)
        self.GetGridWindow().Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.GetGridWindow().Bind(wx.EVT_LEFT_UP, self.OnLeftUp)


    # I do this because I don't like the default behaviour of not starting the
    # cell editor on double clicks, but only a second click.
    def OnLeftDClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()

    def OnLeftDown(self, evt):
        col, row = self.HitTestCell(evt.GetPosition().x, evt.GetPosition().y)
        if isinstance(self.GetCellRenderer(row, col), MyCustomRenderer):
            self.GetCellRenderer(row, col).down = True
        self.Refresh()
        evt.Skip()

    def OnLeftUp(self, evt):
        col, row = self.HitTestCell(evt.GetPosition().x, evt.GetPosition().y)
        if isinstance(self.GetCellRenderer(row, col), MyCustomRenderer):
            self.GetCellRenderer(row, col).down = False
            self.GetCellRenderer(row, col).click_handled = False

        self.Refresh()
        evt.Skip()

    def HitTestCell(self, x, y):
        x, y = self.CalcUnscrolledPosition(x, y)
        return self.XToCol(x),self.YToRow(y)

#---------------------------------------------------------------------------

class TestFrame(wx.Frame):
    def __init__(self, parent, log):
        wx.Frame.__init__(self, parent, -1, "Editors and Renderers Demo", size=(640,480))
        grid = EditorsAndRenderersGrid(self, log)



#---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    app = wx.App()
    frame = TestFrame(None, sys.stdout)
    frame.Show(True)
    app.MainLoop()


#---------------------------------------------------------------------------