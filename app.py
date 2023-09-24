#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Developed by Paulo Henrique Junqueira Amorim (paulojamorim at gmail.com)

import wx
import extract

class MainFrame(wx.Frame):

    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.CAPTION | wx.CLIP_CHILDREN | wx.CLOSE_BOX | wx.MINIMIZE | wx.MINIMIZE_BOX
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((436, 129))
        self.SetTitle("imageP")

        self.main_painel = wx.Panel(self, wx.ID_ANY)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        label_folder = wx.StaticText(self.main_painel, wx.ID_ANY, "Folder: ?")
        main_sizer.Add(label_folder, 0, wx.ALL | wx.EXPAND, 2)

        self.btn_folder = wx.Button(self.main_painel, wx.ID_ANY, "Select folder")
        main_sizer.Add(self.btn_folder, 0, wx.ALL | wx.EXPAND, 1)

        self.btn_process = wx.Button(self.main_painel, wx.ID_ANY, "Split")
        main_sizer.Add(self.btn_process, 0, wx.ALL | wx.EXPAND, 1)

        self.main_painel.SetSizer(main_sizer)

        self.label_folder = label_folder
        self.selected_folder = ""
        self.__bind()
        
        self.Layout()
        # end wxGlade


    def __bind(self):
        self.Bind(wx.EVT_BUTTON, self.OnSelectFolder, self.btn_folder)
        self.Bind(wx.EVT_BUTTON, self.OnSplit, self.btn_process)

    def OnSelectFolder(self, evt):
        # In this case we include a "New directory" button.
        dlg = wx.DirDialog(self, "Choose a directory:",
                          style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )

        # If the user selects OK, then we process the dialog's data.
        # This is done by getting the path data from the dialog - BEFORE
        # we destroy it.
        if dlg.ShowModal() == wx.ID_OK:
            self.selected_folder = dlg.GetPath()
            self.label_folder.SetLabelText("Folder: " + self.selected_folder)

        # Only destroy a dialog after you're done with it.
        dlg.Destroy()

    def ShowMessageFinished(self):
        dlg = wx.MessageDialog(self, 'All files that were found were splited',
                               'Finished',wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def OnSplit(self, evt):
        tiff_list = extract.find_tiff(self.selected_folder)
        extract.process(tiff_list)
        self.ShowMessageFinished()
        evt.Skip()

# end of class MainFrame

class MyApp(wx.App):
    def OnInit(self):
        self.main_frame = MainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.main_frame)
        self.main_frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
