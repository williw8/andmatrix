import wx
from csvdb import csvmemory
from actions import utils

BOX_SPACER = 5

class AndMatrixDialog(wx.Dialog):

  def __init__(self,parent,table):
    wx.Dialog.__init__(self,parent)
    self.horiz_column = None
    self.vert_column = None
    self.zero_char = '0'
    self.one_char = '1'
    self.table = table
    self.path = None

    self.initUI()
    self.SetSize((320,240))
    self.SetTitle("AND Matrix")


  def setPath(self,v):
    '''
    Required
    '''
    self.path = v

  def initUI(self):
    vbox = wx.BoxSizer(wx.VERTICAL)

    hbox = wx.BoxSizer(wx.HORIZONTAL)
    x = wx.StaticText(self,-1,"First Column")
    hbox.Add(x)
    self.horiz_ctrl = wx.ComboBox(self,style=wx.CB_DROPDOWN,choices=self.table.header)
    self.horiz_ctrl.SetEditable(False)
    self.horiz_ctrl.SetStringSelection(self.table.header[0])
    hbox.Add(self.horiz_ctrl)
    vbox.Add(hbox);

    hbox = wx.BoxSizer(wx.HORIZONTAL)
    x = wx.StaticText(self,-1,"Second Column")
    hbox.AddSpacer(BOX_SPACER)
    hbox.Add(x)
    hbox.AddSpacer(BOX_SPACER)
    self.vert_ctrl = wx.ComboBox(self,style=wx.CB_DROPDOWN,choices=self.table.header)
    self.vert_ctrl.SetEditable(False)
    self.vert_ctrl.SetStringSelection(self.table.header[-1])
    hbox.AddSpacer(BOX_SPACER)
    hbox.Add(self.vert_ctrl)
    hbox.AddSpacer(BOX_SPACER)
    vbox.Add(hbox);

    hbox = wx.BoxSizer(wx.HORIZONTAL)
    x = wx.StaticText(self,-1,"AND value")
    hbox.AddSpacer(BOX_SPACER)
    hbox.Add(x)
    hbox.AddSpacer(BOX_SPACER)
    self.one_char_ctrl = wx.TextCtrl(self)
    self.one_char_ctrl.SetEditable(True)
    self.one_char_ctrl.AppendText(self.one_char)
    hbox.AddSpacer(BOX_SPACER)
    hbox.Add(self.one_char_ctrl)
    hbox.AddSpacer(BOX_SPACER)
    vbox.Add(hbox);

    hbox = wx.BoxSizer(wx.HORIZONTAL)
    x = wx.StaticText(self,-1,"NOT value")
    hbox.AddSpacer(BOX_SPACER)
    hbox.Add(x)
    hbox.AddSpacer(BOX_SPACER)
    self.zero_char_ctrl = wx.TextCtrl(self)
    self.zero_char_ctrl.SetEditable(True)
    self.zero_char_ctrl.AppendText(self.zero_char)
    hbox.AddSpacer(BOX_SPACER)
    hbox.Add(self.zero_char_ctrl)
    hbox.AddSpacer(BOX_SPACER)
    vbox.Add(hbox);

    hbox = wx.BoxSizer(wx.HORIZONTAL)
    self.ok_button = wx.Button(self,wx.ID_OK)
    hbox.AddSpacer(BOX_SPACER)
    hbox.Add(self.ok_button)
    hbox.AddSpacer(BOX_SPACER)
    self.cancel_button = wx.Button(self,wx.ID_CANCEL)
    hbox.AddSpacer(BOX_SPACER)
    hbox.Add(self.cancel_button)
    hbox.AddSpacer(BOX_SPACER)
    vbox.Add(hbox)

    self.ok_button.Bind(wx.EVT_BUTTON,self.onOK)
    self.cancel_button.Bind(wx.EVT_BUTTON,self.onCancel)

    self.SetSizer(vbox)

  def getHorizCol(self):
    return self.horiz_column

  def getVertCol(self):
    return self.vert_column

  def getZeroString(self):
    return self.zero_char

  def getOneString(self):
    return self.one_char

  def onOK(self,event):
    idx = self.horiz_ctrl.GetCurrentSelection()
    self.horiz_column = self.table.header[idx]
    idx = self.vert_ctrl.GetCurrentSelection()
    self.vert_column = self.table.header[idx]
    self.zero_char = self.zero_char_ctrl.GetValue()
    self.one_char = self.one_char_ctrl.GetValue()
    self.EndModal(wx.ID_OK)

  def onCancel(self,event):
    self.EndModal(wx.ID_CANCEL)


class AndMatrixPlugin(object):

  def __init__(self,parent_frame):
    self.path = None
    self.parent_frame = parent_frame
 
  def get_label(self):
    '''
    Required
    '''
    return 'AND Matrix'

  def get_description(self):
    '''
    Required
    '''
    return 'Perform a natural join between two .csv files'

  def set_path(self,v):
    self.path = v

  def do_action(self,table):
    '''
    Required
    '''
    if None is table:
      wx.MessageBox('Missing table', 'Info', wx.OK | wx.ICON_INFORMATION)
      return
    dialog = AndMatrixDialog(self.parent_frame,table)
    chk = dialog.ShowModal()
    if wx.ID_OK == chk:
      hcol = dialog.getHorizCol()
      vcol = dialog.getVertCol()
      one_str = dialog.getOneString()
      zero_str = dialog.getZeroString()
      memw = csvmemory.MemoryWriter()
      location_list = table.select(hcol,None,'*')
      labels = table.makeSingleSelectionDistinct(location_list)
      labels.insert(0,vcol)
      memw.setHeader(labels)
      row_list = table.select(vcol,None,'*')
      row_values = table.makeSingleSelectionDistinct(row_list)
      for row in row_values:
        output = list()
        value_list = table.select(hcol,vcol,row)
        value_values = table.makeSingleSelectionDistinct(value_list)
        idx = 0
        for v in labels:
          if 0 == idx:
            output.append(row)
          else:
            if v in value_values:
              output.append(one_str)
            else:
              output.append(zero_str)
          idx += 1
        memw.appendRow(output)
      path = utils.getTempFilename()
      memw.save(path)
      self.parent_frame.addPage(path,delete_on_exit=True)

def get_plugin(parent_frame):
  return AndMatrixPlugin(parent_frame)


