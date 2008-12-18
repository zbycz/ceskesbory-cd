# -*- coding: utf8 -*-


#         # This time, we let the botton be as big as it can be.
#         # Also, this one is fancier, with custom colors and bezel size.
#         b = buttons.GenButton(self, -1, 'bigger')
#         self.Bind(wx.EVT_BUTTON, self.OnBiggerButton, b)
#         b.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD, False))
#         b.SetBezelWidth(5)
#         b.SetMinSize(wx.DefaultSize)
#         b.SetBackgroundColour("Navy")
#         b.SetForegroundColour(wx.WHITE)
#         b.SetToolTipString("This is a BIG button...")
#         # let the sizer set best size
#         sizer.Add(b, flag=wx.ADJUST_MINSIZE) 



import layout, wx, db



class UcpsSpltr(wx.SplitterWindow):
    PnlActive = False
    PnlFiltr = False
    PnlVysl = False
    PnlDetail = False
    PnlFirst = False
    PnlAbout = False
    userdata = False
    form =  [
             ['druh', u'Druh souboru:', True],
             ['kraje', u'Kraj:', True],
             ['char', u'Zvláštní charakteristika:', True],
             ['zanr', u'Žánrové zaměření:', True],
             ['nazev', u'Název souboru, sídlo, příjmení sbormistra:', False],
            ]
    #self.form[5] = ['order', u'Výsledky řadit podle:', db.arrOrder]

    
    def __init__(self, parent):
        wx.SplitterWindow.__init__(self, parent, -1)

        db.fillLists()
        
        self.CreatePnlFirst()
        self.Initialize(self.PnlFirst)
        self.PnlActive = self.PnlFirst
        
    
    def CreatePnlFirst(self):
        self.PnlFirst = wx.Panel(self)
        self.PnlFirst.Hide()
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        gifLogo = wx.Image('logo_cs.gif', wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        logo = wx.StaticBitmap(self.PnlFirst, -1, gifLogo, None, (gifLogo.GetWidth(), gifLogo.GetHeight())) #(250, 62)
        vbox.Add(logo, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 100)
        

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        butt = wx.Button(self.PnlFirst, -1, u'Vyhledávání')
        hbox.Add(butt, 0, wx.RIGHT, 100)
        self.Bind(wx.EVT_BUTTON, self.OnSwitchFiltr, butt)

        butt = wx.Button(self.PnlFirst, -1, u'O projektu')
        hbox.Add(butt, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.OnSwitchAbout, butt)
        
        vbox.Add(hbox, 0, wx.ALIGN_CENTER)


        gifLogo = wx.Image('loga.gif', wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        logo = wx.StaticBitmap(self.PnlFirst, -1, gifLogo, None, (gifLogo.GetWidth(), gifLogo.GetHeight())) #(250, 62)
        vbox.Add(logo, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 100)



        
        self.PnlFirst.SetSizer(vbox)

    
    def OnSwitchFiltr(self, event):
        layout.btnevt = self.OnSwitchFirst

        if not self.PnlFiltr:
            layout.CreateFiltrPnl(self, db)
        self.PnlActive.Hide()
        self.PnlFiltr.Show()
        self.PnlFiltr.SetFocus()
        self.ReplaceWindow(self.PnlActive, self.PnlFiltr)
        self.PnlActive = self.PnlFiltr

    def OnSwitchFirst(self, event):
        #if not PnlFiltr:
        #    layout.CreateFiltrPnl(self, db)
        self.PnlActive.Hide()
        self.PnlFirst.Show()
        self.PnlFirst.SetFocus()
        self.ReplaceWindow(self.PnlActive, self.PnlFirst)
        self.PnlActive = self.PnlFirst

    def OnSwitchAbout(self, event):
        htmldata = layout.abouttext;
        
        layout.btnevt = self.OnSwitchFirst
        
        if not self.PnlAbout:
            self.PnlAbout = layout.CreateHtmlPnl(self, u"O projektu", \
                htmldata, u'<< Zpět na úvod')
        
        self.PnlActive.Hide()
        self.PnlAbout.Show()
        self.PnlAbout.SetFocus()
        self.ReplaceWindow(self.PnlActive, self.PnlAbout)
        self.PnlActive = self.PnlAbout 
    
    def OnSwitchVysl(self, event):
        olduserdata = self.userdata
        self.userdata = {}
        for item in self.form:
            if not item[2]:
                self.userdata[item[0]] = item[3].GetValue()
            else:
                self.userdata[item[0]] = db.arr[item[0]+'Id'][item[3].GetSelection()]
        
        if not olduserdata: self.userdata['orderby'] = 'nazev collate cesky';
        else: self.userdata['orderby'] = olduserdata['orderby']
        htmldata = db.getVysledky(self.userdata);
        
        layout.btnevt = self.OnSwitchFiltr
        
        if not self.PnlVysl:
            self.PnlVysl = layout.CreateHtmlPnl(self, u"Výsledky vyhledávání", \
                    htmldata, u'<< Změnit filtr')
        elif self.userdata != olduserdata and olduserdata:
            self.PnlVysl.html.SetPage(htmldata)
        
        self.PnlActive.Hide()
        self.PnlVysl.Show()
        self.PnlVysl.SetFocus()
        self.ReplaceWindow(self.PnlActive, self.PnlVysl)
        self.PnlActive = self.PnlVysl

    def OnSwitchDetail(self, id):
        htmldata = db.getDetail(id);
        layout.btnevt = self.OnSwitchVysl
        
        if self.PnlDetail:
            self.PnlDetail.html.SetPage(htmldata)
        else:
            self.PnlDetail = layout.CreateHtmlPnl(self, False, \
                htmldata, u'<< Zpět na výsledky')
        
        self.PnlActive.Hide()
        self.PnlDetail.Show()
        self.PnlDetail.SetFocus()
        self.ReplaceWindow(self.PnlActive, self.PnlDetail)
        self.PnlActive = self.PnlDetail



class UcpsFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, u"České-sbory.cz, verze: %s" % db.getDate(), (10, 10), (600, 550))
        self.SetMaxSize((600,1200));
        self.SetMinSize((600,340));
        #self.CenterOnScreen()
        self.SetBackgroundColour((255,255,255))
        
        ib=wx.IconBundle()
        ib.AddIconFromFile("icon.ico",wx.BITMAP_TYPE_ANY)
        self.SetIcons(ib)
        
        self.Spltr = UcpsSpltr(self)
        self.Refresh()

class UcpsApp(wx.App):
    def OnInit(self):
        self.frame = UcpsFrame()
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = UcpsApp(False) # False => vypisuj chyby při startu aplikace
    app.MainLoop()
